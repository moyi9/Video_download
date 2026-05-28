import re
import requests
from urllib.parse import urlparse, parse_qs


def resolve_douyin_url(url: str) -> str:
    """
    解析抖音分享链接，获取真实视频URL
    支持: v.douyin.com短链、search页面的modal_id参数
    """
    # 处理搜索页modal_id参数: /search/dy?modal_id=xxx
    if 'modal_id=' in url:
        match = re.search(r'modal_id=(\d+)', url)
        if match:
            return f'https://www.douyin.com/video/{match.group(1)}'

    # 处理 v.douyin.com 短链
    if 'v.douyin.com' not in url:
        return url

    # 跟踪重定向获取真实URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Version/16.0 Mobile/15E148 Safari/604.1',
    }

    try:
        resp = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
        final_url = resp.url

        # 提取视频ID
        match = re.search(r'/(?:video|note)/(\d+)', final_url)
        if match:
            video_id = match.group(1)
            return f'https://www.douyin.com/video/{video_id}'

        return final_url
    except requests.RequestException:
        return url
