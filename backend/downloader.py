import yt_dlp
import re
from typing import Optional


# 通用浏览器User-Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'


def _get_base_opts() -> dict:
    """获取基础yt-dlp选项"""
    return {
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': USER_AGENT,
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.bilibili.com/',
        },
        'geo_bypass': True,
        'geo_bypass_country': 'US',
    }


def parse_video(url: str) -> dict:
    """解析视频信息，返回格式化的视频数据"""
    ydl_opts = {
        **_get_base_opts(),
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if info is None:
        raise ValueError("无法解析该链接")

    formats = _process_formats(info.get('formats', []))

    return {
        'id': info.get('id', ''),
        'title': info.get('title', '未知标题'),
        'thumbnail': (info.get('thumbnail', '') or '').replace('http://', 'https://'),
        'duration': info.get('duration', 0),
        'duration_string': _format_duration(info.get('duration', 0)),
        'uploader': info.get('uploader', info.get('channel', '未知')),
        'platform': _detect_platform(url, info),
        'view_count': info.get('view_count', 0),
        'upload_date': info.get('upload_date', ''),
        'description': (info.get('description', '') or '')[:500],
        'formats': formats,
        'subtitles': list(info.get('subtitles', {}).keys()),
        'automatic_captions': list(info.get('automatic_captions', {}).keys()),
    }


def get_direct_url(url: str, format_id: str) -> dict:
    """获取视频直链"""
    ydl_opts = {
        **_get_base_opts(),
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if info is None:
        raise ValueError("无法解析该链接")

    # 查找指定格式
    target_format = None
    for f in info.get('formats', []):
        if f['format_id'] == format_id:
            target_format = f
            break

    if target_format is None:
        # 尝试组合格式（如 137+140）
        parts = format_id.split('+')
        video_fmt = None
        audio_fmt = None
        for f in info.get('formats', []):
            if f['format_id'] == parts[0]:
                video_fmt = f
            if len(parts) > 1 and f['format_id'] == parts[1]:
                audio_fmt = f

        if video_fmt:
            direct_url = video_fmt.get('url', '')
            if audio_fmt and audio_fmt.get('url'):
                # 对于音视频分离的情况，返回视频直链
                # 实际合并需要服务端处理
                pass
            return {
                'direct_url': direct_url,
                'ext': video_fmt.get('ext', 'mp4'),
                'filesize': video_fmt.get('filesize') or video_fmt.get('filesize_approx', 0),
            }
        raise ValueError(f"未找到格式: {format_id}")

    return {
        'direct_url': target_format.get('url', ''),
        'ext': target_format.get('ext', 'mp4'),
        'filesize': target_format.get('filesize') or target_format.get('filesize_approx', 0),
    }


def is_youtube_url(url: str) -> bool:
    """判断是否为YouTube链接"""
    return 'youtube.com' in url.lower() or 'youtu.be' in url.lower()


def _process_formats(formats: list) -> list:
    """处理格式列表，合并音视频，按分辨率排序"""
    result = []
    seen_heights = set()

    # 按高度降序排列
    sorted_formats = sorted(formats, key=lambda x: x.get('height', 0) or 0, reverse=True)

    for f in sorted_formats:
        height = f.get('height')
        vcodec = f.get('vcodec', 'none')
        acodec = f.get('acodec', 'none')
        filesize = f.get('filesize') or f.get('filesize_approx', 0)

        # 跳过没有视频流的格式（纯音频）
        if vcodec == 'none' or vcodec is None:
            continue

        # 跳过重复分辨率
        if height and height in seen_heights:
            continue
        if height:
            seen_heights.add(height)

        # 生成可读标签
        label = _make_format_label(f, filesize)

        result.append({
            'format_id': f.get('format_id', ''),
            'ext': f.get('ext', 'mp4'),
            'resolution': f.get('resolution', '未知'),
            'height': height or 0,
            'filesize': filesize,
            'filesize_approx': f.get('filesize_approx', 0),
            'vcodec': vcodec,
            'acodec': acodec,
            'fps': f.get('fps'),
            'label': label,
            'has_audio': acodec != 'none' and acodec is not None,
        })

    # 如果没有找到有高度信息的格式，取前几个
    if not result and formats:
        for f in formats[:6]:
            if f.get('vcodec', 'none') != 'none':
                filesize = f.get('filesize') or f.get('filesize_approx', 0)
                result.append({
                    'format_id': f.get('format_id', ''),
                    'ext': f.get('ext', 'mp4'),
                    'resolution': f.get('resolution', '未知'),
                    'height': f.get('height', 0) or 0,
                    'filesize': filesize,
                    'filesize_approx': f.get('filesize_approx', 0),
                    'vcodec': f.get('vcodec', 'none'),
                    'acodec': f.get('acodec', 'none'),
                    'fps': f.get('fps'),
                    'label': _make_format_label(f, filesize),
                    'has_audio': f.get('acodec', 'none') != 'none',
                })

    return result


def _make_format_label(f: dict, filesize: int) -> str:
    """生成格式的可读标签"""
    height = f.get('height', 0)
    ext = f.get('ext', 'mp4')
    fps = f.get('fps', '')

    if height:
        label = f"{height}p {ext.upper()}"
    elif f.get('resolution'):
        label = f"{f['resolution']} {ext.upper()}"
    else:
        label = ext.upper()

    if fps and fps > 30:
        label += f" {fps}fps"

    if filesize:
        size_mb = filesize / (1024 * 1024)
        if size_mb >= 1:
            label += f" ({size_mb:.1f}MB)"
        else:
            label += f" ({filesize / 1024:.0f}KB)"

    return label


def _format_duration(seconds) -> str:
    """格式化时长"""
    if not seconds:
        return "0:00"
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _detect_platform(url: str, info: dict) -> str:
    """检测视频平台"""
    url_lower = url.lower()
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'YouTube'
    elif 'bilibili.com' in url_lower or 'b23.tv' in url_lower:
        return 'Bilibili'
    elif 'douyin.com' in url_lower:
        return '抖音'
    elif 'tiktok.com' in url_lower:
        return 'TikTok'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'Twitter/X'
    elif 'instagram.com' in url_lower:
        return 'Instagram'
    elif 'vimeo.com' in url_lower:
        return 'Vimeo'

    # 从 extractor 推断
    extractor = info.get('extractor', '')
    if 'youtube' in extractor.lower():
        return 'YouTube'
    elif 'bilibili' in extractor.lower():
        return 'Bilibili'

    return '其他平台'


def download_video(url: str, format_id: str, output_dir: str) -> str:
    """下载视频到本地，返回文件绝对路径"""
    import os
    import time
    # 转为绝对路径
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 使用时间戳作为临时文件名，避免中文编码问题
    temp_name = f'video_{int(time.time())}'
    ydl_opts = {
        **_get_base_opts(),
        'outtmpl': os.path.join(output_dir, f'{temp_name}.%(ext)s'),
        'merge_output_format': 'mp4',
        'writethumbnail': False,
    }

    # YouTube：强制使用自动选择，忽略format_id（SABR限制导致很多格式不可用）
    if is_youtube_url(url):
        ydl_opts['format'] = 'best'
        ydl_opts['extractor_args'] = {'youtube': {'player_client': ['web', 'android']}}
    elif format_id:
        # 其他平台使用指定格式
        ydl_opts['format'] = format_id
    else:
        ydl_opts['format'] = 'best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is None:
            raise ValueError("下载失败")

        # 获取下载后的文件名（绝对路径）
        filename = ydl.prepare_filename(info)
        # 确保是mp4
        if not filename.endswith('.mp4'):
            base = os.path.splitext(filename)[0]
            filename = base + '.mp4'

        # 确保返回绝对路径
        if not os.path.isabs(filename):
            filename = os.path.join(output_dir, os.path.basename(filename))

        # 重命名为最终文件名（使用视频标题）
        title = info.get('title', 'video')
        # 清理文件名中的非法字符
        import re
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
        final_path = os.path.join(output_dir, f'{safe_title}.mp4')

        # 如果临时文件存在，重命名
        if os.path.exists(filename) and filename != final_path:
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(filename, final_path)
            filename = final_path

        return filename
