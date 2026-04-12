"""
爱奇艺榜单爬虫

功能：
- 尝试从爱奇艺首页查找榜单/热播榜页面
- 解析电视剧、电影、综艺等板块的榜单，提取：排名、标题、链接
- 支持用户在命令行传入具体榜单 URL（以逗号分隔）作为备选
- 结果保存为 JSON 文件

使用：
python "05爱奇艺榜单.py"
或
python "05爱奇艺榜单.py" --urls "https://example.com/rank_tv,https://example.com/rank_movie"

注意：爱奇艺会使用 JavaScript 渲染或反爬措施；本脚本尽力通过解析静态 HTML 提取信息，若遇到动态渲染页面可考虑用 Selenium 或手动提供榜单 URL。
"""

from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random
import json
import logging
import argparse
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

DEFAULT_BASE = "https://www.iqiyi.com/"


def get(url: str, timeout: int = 15, retries: int = 3) -> Optional[str]:
    """GET 请求，带简单重试和限速"""
    for i in range(retries):
        try:
            logging.debug(f"GET {url} (try {i+1})")
            resp = requests.get(url, headers=HEADERS, timeout=timeout)
            if resp.status_code == 200:
                return resp.text
            else:
                logging.warning(f"非200响应 {resp.status_code} for {url}")
        except requests.RequestException as e:
            logging.warning(f"请求异常 {e} for {url}")
        time.sleep(1 + random.random() * 2)
    return None


def find_rank_pages_from_home(home_html: str, base: str = DEFAULT_BASE) -> List[str]:
    """在首页中查找包含“榜”或“热播”的链接作为榜单入口"""
    soup = BeautifulSoup(home_html, "lxml")
    candidates = []
    for a in soup.find_all("a", href=True):
        txt = (a.get_text() or "").strip()
        if not txt:
            continue
        if any(k in txt for k in ("榜", "热播", "排行榜")):
            href = urljoin(base, a['href'])
            if href not in candidates:
                candidates.append(href)
    logging.info(f"在首页找到 {len(candidates)} 个候选榜单页")
    return candidates


def extract_links_from_section(section_soup, base: str) -> List[Dict]:
    """从一个板块的 BeautifulSoup 节点中抽取可疑条目（标题+链接）"""
    items = []
    # 常见结构：li a, div a 等
    for a in section_soup.find_all("a", href=True):
        title = (a.get_text() or "").strip()
        href = a['href']
        if not title:
            # 有时候标题在img的alt
            img = a.find('img')
            if img and img.get('alt'):
                title = img['alt'].strip()
        if not title:
            continue
        full = urljoin(base, href)
        items.append({"title": title, "link": full})
    # 去重并保持顺序
    seen = set()
    uniq = []
    for it in items:
        key = (it['title'], it['link'])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(it)
    return uniq


def parse_rank_page(html: str, base: str) -> Dict[str, List[Dict]]:
    """尝试解析榜单页面，返回包含多个类别的字典：{ '电视剧': [{rank,title,link}, ...], ... }"""
    soup = BeautifulSoup(html, "lxml")
    result: Dict[str, List[Dict]] = {}

    # 优先根据页面中可能的标题（h1/h2/h3）来分块
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    target_categories = ["电视剧", "电影", "综艺", "影视", "电影榜", "热播"]

    for h in headings:
        txt = (h.get_text() or "").strip()
        for cat in target_categories:
            if cat in txt:
                # 找到后，尝试抽取该节点之后的列表或容器
                section = None
                # 尝试下一个兄弟节点
                sib = h.find_next_sibling()
                if sib:
                    section = sib
                else:
                    # 尝试父节点中寻找列表
                    parent = h.parent
                    if parent:
                        section = parent
                if section:
                    links = extract_links_from_section(section, base)
                    if links:
                        # 为结果增加排名信息
                        result.setdefault(cat, [])
                        for idx, it in enumerate(links, 1):
                            result[cat].append({"rank": idx, "title": it['title'], "link": it['link']})
    # 如果没有通过 headings 抽到内容，作为兜底，尝试在整个页面抓取高频链接
    if not result:
        logging.info("未通过标题分块抽取到榜单，使用全页面候选链接策略")
        # 常见包含榜单的容器类名关键词
        container_keywords = ["rank", "list", "榜", "hot", "rank-list", "site-piclist", "mod-list"]
        for cls_kw in container_keywords:
            containers = soup.find_all(class_=lambda c: c and cls_kw in c)
            for cont in containers:
                links = extract_links_from_section(cont, base)
                if links:
                    cat = f"候选-{cls_kw}"
                    if cat not in result:
                        result[cat] = []
                    for idx, it in enumerate(links, 1):
                        result[cat].append({"rank": idx, "title": it['title'], "link": it['link']})
        # 最后兜底：页面中提取前50个有效链接
        if not result:
            all_links = extract_links_from_section(soup, base)
            if all_links:
                result['候选-全部'] = []
                for idx, it in enumerate(all_links[:50], 1):
                    result['候选-全部'].append({"rank": idx, "title": it['title'], "link": it['link']})
    return result


def normalize_url(url: str, base: str) -> str:
    return urljoin(base, url)


def crawl_iqiyi_rankings(candidate_urls: List[str]) -> Dict[str, List[Dict]]:
    """遍历候选榜单页并聚合解析结果"""
    aggregated: Dict[str, List[Dict]] = {}
    for url in candidate_urls:
        logging.info(f"解析榜单页: {url}")
        html = get(url)
        if not html:
            logging.warning(f"无法获取 {url}")
            continue
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        parsed = parse_rank_page(html, base)
        # 合并 parsed 到 aggregated
        for cat, items in parsed.items():
            if cat not in aggregated:
                aggregated[cat] = []
            # 避免重复 title
            existing_titles = {it['title'] for it in aggregated[cat]}
            for it in items:
                if it['title'] in existing_titles:
                    continue
                aggregated[cat].append(it)
        # 友好等待
        time.sleep(1 + random.random() * 2)
    return aggregated


def main():
    parser = argparse.ArgumentParser(description='爬取爱奇艺排行榜（电视剧/电影/综艺）')
    parser.add_argument('--urls', type=str, help='逗号分隔的榜单页面URL列表，若不提供脚本将尝试从首页发现榜单页')
    parser.add_argument('--save', type=str, default='iqiyi_rankings.csv', help='保存结果的CSV文件名（将存储在脚本目录下的05数据文件夹）')
    args = parser.parse_args()

    candidate_urls: List[str] = []
    if args.urls:
        candidate_urls = [u.strip() for u in args.urls.split(',') if u.strip()]
    else:
        logging.info('未提供 URL，尝试从爱奇艺首页发现榜单页...')
        home = get(DEFAULT_BASE)
        # 若无法从主站获取，尝试移动站点（通常更轻量）
        if not home:
            logging.info('主站请求失败，尝试移动站点 m.iqiyi.com')
            home = get('https://m.iqiyi.com/')
        if home:
            found = find_rank_pages_from_home(home, DEFAULT_BASE)
            candidate_urls = found
        if not candidate_urls:
            logging.warning('未能自动发现榜单页。脚本将尝试从首页抓取前50个链接作为候选，或使用内置候选列表')
            if home:
                # 兜底：从首页抽取前50链接
                soup = BeautifulSoup(home, 'lxml')
                all_links = extract_links_from_section(soup, DEFAULT_BASE)
                candidate_urls = [it['link'] for it in all_links[:50]]

        # 进一步兜底：添加一些常见的榜单/频道 URL（这些是常见路径，若网站调整可能失效）
        if not candidate_urls:
            fallback = [
                'https://www.iqiyi.com/rank/',
                'https://www.iqiyi.com/hot/',
                'https://www.iqiyi.com/dianying/',
                'https://www.iqiyi.com/zongyi/',
                'https://www.iqiyi.com/vipbang/',
                'https://m.iqiyi.com/rank/',
            ]
            logging.info(f'尝试内置候选URL共 {len(fallback)} 个')
            # 只保留能成功请求到的 URL
            good = []
            for u in fallback:
                if get(u):
                    good.append(u)
                else:
                    logging.debug(f'候选不可用: {u}')
            candidate_urls = good

    if not candidate_urls:
        logging.error('没有候选 URL，退出。可尝试手动提供榜单页面 URL，例如 --urls "https://www.iqiyi.com/rank/"')
        return

    aggregated = crawl_iqiyi_rankings(candidate_urls)

    if not aggregated:
        logging.warning('未抓取到任何榜单项，请检查网络、反爬或考虑使用 Selenium（动态渲染）或手动提供榜单 URL（--urls）')
    else:
        # 保存结果为 CSV，按 category/rank/title/link 写入同一个文件
        import os
        import csv
        save_dir = os.path.join(os.path.dirname(__file__), '05数据')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, args.save)
        # 写入 CSV
        with open(save_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['category', 'rank', 'title', 'link'])
            for cat, items in aggregated.items():
                for it in items:
                    rank = it.get('rank', '')
                    title = it.get('title', '')
                    link = it.get('link', '')
                    writer.writerow([cat, rank, title, link])
        logging.info(f'已将抓取结果保存为 CSV: {save_path}')


if __name__ == '__main__':
    main()
