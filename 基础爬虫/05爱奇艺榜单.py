"""
爱奇艺榜单爬虫

功能：
- 爬取爱奇艺电视剧、电影、综艺等热门榜单
- 提取排名、标题、链接等信息
- 支持用户在命令行传入具体榜单 URL（以逗号分隔）作为备选
- 结果保存为 CSV 文件

使用：
python "05爱奇艺榜单.py"
或
python "05爱奇艺榜单.py" --urls "https://example.com/rank_tv,https://example.com/rank_movie"

注意：爱奇艺可能使用 JavaScript 渲染或反爬措施；本脚本通过多种策略尝试提取数据。
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
import re
from typing import List, Dict, Optional

# 设置日志级别
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 增强的请求头，使用随机User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
]

DEFAULT_BASE = "https://www.iqiyi.com/"

# 已知的榜单URL和API
KNOWN_RANK_URLS = [
    "https://www.iqiyi.com/hot",
    "https://www.iqiyi.com/dianying",
    "https://www.iqiyi.com/zongyi",
    "https://www.iqiyi.com/vip",
    "https://www.iqiyi.com/",  # 首页
]

# 可能的API端点
API_ENDPOINTS = [
    "https://pcw-api.iqiyi.com/search/recommend/list",
    "https://pcw-api.iqiyi.com/hot/rank",
    "https://pcw-api.iqiyi.com/albums/album/info",
]


def get_random_headers() -> Dict[str, str]:
    """生成随机请求头"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Referer": "https://www.google.com/",
    }


def get_api_headers() -> Dict[str, str]:
    """生成API请求头"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://www.iqiyi.com",
        "Referer": "https://www.iqiyi.com/",
        "Connection": "keep-alive",
    }


def get(url: str, timeout: int = 15, retries: int = 3) -> Optional[str]:
    """GET 请求，带简单重试和限速"""
    for i in range(retries):
        try:
            headers = get_random_headers()
            logging.debug(f"GET {url} (try {i+1}) with User-Agent: {headers['User-Agent'][:50]}...")
            # 允许重定向
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            if resp.status_code == 200:
                logging.debug(f"成功获取 {url}，响应长度: {len(resp.text)}")
                return resp.text
            else:
                logging.warning(f"非200响应 {resp.status_code} for {url}")
        except requests.RequestException as e:
            logging.warning(f"请求异常 {e} for {url}")
        time.sleep(2 + random.random() * 3)
    return None


def get_api_data(url: str, params: Dict[str, any] = None) -> Optional[Dict]:
    """获取API数据"""
    for i in range(3):
        try:
            headers = get_api_headers()
            logging.debug(f"GET API {url} (try {i+1}) with params: {params}")
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            if resp.status_code == 200:
                logging.debug(f"成功获取 API 数据，响应长度: {len(resp.text)}")
                return resp.json()
            else:
                logging.warning(f"API 非200响应 {resp.status_code} for {url}")
        except requests.RequestException as e:
            logging.warning(f"API 请求异常 {e} for {url}")
        time.sleep(2 + random.random() * 3)
    return None


def extract_api_endpoints(html: str) -> List[str]:
    """从页面中提取API端点"""
    endpoints = []
    # 查找可能的API调用
    patterns = [
        r'https?://[^"\']+api[^"\']+',
        r'https?://[^"\']+rank[^"\']+',
        r'https?://[^"\']+hot[^"\']+',
        r'https?://[^"\']+list[^"\']+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html)
        endpoints.extend(matches)
    
    # 去重
    return list(set(endpoints))


def extract_rank_items_from_api(data: Dict) -> List[Dict]:
    """从API数据中提取榜单项"""
    items = []
    rank = 1
    
    # 尝试不同的数据结构
    if 'data' in data:
        data = data['data']
    
    if isinstance(data, dict):
        # 尝试常见的字段名
        for key in ['list', 'items', 'data', 'rank', 'hot', 'videos']:
            if key in data:
                if isinstance(data[key], list):
                    for item in data[key]:
                        if isinstance(item, dict):
                            # 尝试提取标题和链接
                            title = item.get('title', item.get('name', ''))
                            link = item.get('url', item.get('link', ''))
                            if title and link:
                                items.append({"rank": rank, "title": title, "link": link})
                                rank += 1
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                title = item.get('title', item.get('name', ''))
                link = item.get('url', item.get('link', ''))
                if title and link:
                    items.append({"rank": rank, "title": title, "link": link})
                    rank += 1
    
    return items


def extract_rank_items_from_html(html: str, base: str) -> Dict[str, List[Dict]]:
    """从HTML中提取榜单项"""
    soup = BeautifulSoup(html, "lxml")
    result: Dict[str, List[Dict]] = {}
    
    # 1. 尝试提取所有可能的链接
    logging.info("尝试提取页面中的所有链接")
    all_links = []
    rank = 1
    
    # 查找所有a标签
    a_tags = soup.find_all('a', href=True)
    logging.debug(f"找到 {len(a_tags)} 个a标签")
    
    for a in a_tags:
        # 提取标题
        title = a.get_text().strip()
        if not title:
            # 尝试从img的alt获取标题
            img = a.find('img')
            if img and img.get('alt'):
                title = img['alt'].strip()
            # 尝试从其他属性获取标题
            if not title and a.get('title'):
                title = a['title'].strip()
        
        # 过滤条件 - 只过滤明显无效的链接
        if title and len(title) > 2:
            link = urljoin(base, a['href'])
            # 只过滤javascript和空链接
            if 'javascript:' not in link and link != base and link != base + '/':
                all_links.append({"rank": rank, "title": title, "link": link})
                rank += 1
                if rank > 50:  # 限制数量
                    break
    
    if all_links:
        logging.info(f"成功提取到 {len(all_links)} 个链接")
        result["热门视频"] = all_links
    else:
        logging.info("未提取到任何链接")
    
    # 2. 尝试提取API端点
    logging.info("尝试提取API端点")
    api_endpoints = extract_api_endpoints(html)
    if api_endpoints:
        logging.info(f"找到 {len(api_endpoints)} 个API端点")
        for endpoint in api_endpoints[:5]:  # 只尝试前5个
            logging.info(f"尝试API端点: {endpoint}")
            data = get_api_data(endpoint)
            if data:
                api_items = extract_rank_items_from_api(data)
                if api_items:
                    logging.info(f"从API提取到 {len(api_items)} 个项")
                    result["API数据"] = api_items
                    break
    
    return result


def crawl_iqiyi_rankings(candidate_urls: List[str]) -> Dict[str, List[Dict]]:
    """遍历候选榜单页并聚合解析结果"""
    aggregated: Dict[str, List[Dict]] = {}
    
    # 首先尝试API端点
    logging.info("尝试直接访问API端点")
    for endpoint in API_ENDPOINTS:
        logging.info(f"访问API端点: {endpoint}")
        # 尝试不同的参数
        params_list = [
            {},
            {"category": "movie"},
            {"category": "tv"},
            {"category": "zongyi"},
        ]
        
        for params in params_list:
            data = get_api_data(endpoint, params)
            if data:
                api_items = extract_rank_items_from_api(data)
                if api_items:
                    logging.info(f"从API提取到 {len(api_items)} 个项")
                    aggregated["API数据"] = api_items
                    break
        if aggregated:
            break
    
    # 然后尝试页面
    for url in candidate_urls:
        logging.info(f"解析榜单页: {url}")
        html = get(url)
        if not html:
            logging.warning(f"无法获取 {url}")
            continue
        base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        parsed = extract_rank_items_from_html(html, base)
        
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
        time.sleep(2 + random.random() * 3)
    return aggregated


def main():
    parser = argparse.ArgumentParser(description='爬取爱奇艺排行榜（电视剧/电影/综艺）')
    parser.add_argument('--urls', type=str, help='逗号分隔的榜单页面URL列表，若不提供脚本将使用内置榜单URL')
    parser.add_argument('--save', type=str, default='iqiyi_rankings.csv', help='保存结果的CSV文件名（将存储在脚本目录下的05数据文件夹）')
    args = parser.parse_args()

    candidate_urls: List[str] = []
    if args.urls:
        candidate_urls = [u.strip() for u in args.urls.split(',') if u.strip()]
    else:
        logging.info('未提供 URL，使用内置榜单URL...')
        candidate_urls = KNOWN_RANK_URLS

    if not candidate_urls:
        logging.error('没有候选 URL，退出。可尝试手动提供榜单页面 URL，例如 --urls "https://www.iqiyi.com/hot"')
        return

    aggregated = crawl_iqiyi_rankings(candidate_urls)

    if not aggregated:
        logging.warning('未抓取到任何榜单项，请检查网络、反爬或考虑使用 Selenium（动态渲染）或手动提供榜单 URL（--urls）')
        logging.info('提示：爱奇艺网站可能使用了JavaScript动态渲染，建议使用Selenium等工具进行爬取')
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