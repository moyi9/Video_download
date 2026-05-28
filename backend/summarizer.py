import os
import re
import json
import tempfile
import requests
from openai import OpenAI

# DeepSeek 客户端
_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv('DEEPSEEK_API_KEY', '')
        if not api_key:
            raise ValueError("未配置 DEEPSEEK_API_KEY")
        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    return _client


def extract_subtitles(url: str) -> dict:
    """提取视频字幕，返回 {segments, full_text, language}"""
    # 尝试 B 站专用 API
    if 'bilibili.com' in url or 'b23.tv' in url:
        try:
            return _extract_bilibili_subtitles(url)
        except Exception:
            pass

    # 通用路径：yt-dlp
    return _extract_ytdlp_subtitles(url)


def _extract_bilibili_subtitles(url: str) -> dict:
    """B站字幕提取"""
    import yt_dlp

    # 先获取视频信息
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if not info:
        raise ValueError("无法获取B站视频信息")

    # 尝试从 subtitles 获取
    subtitles = info.get('subtitles', {})
    auto_captions = info.get('automatic_captions', {})

    # 优先级：人工字幕 > 自动字幕
    subtitle_data = None
    lang = None

    for l in ['zh', 'zh-Hans', 'zh-CN', 'en', 'ja', 'ko']:
        if l in subtitles:
            subtitle_data = subtitles[l]
            lang = l
            break
        if l in auto_captions:
            subtitle_data = auto_captions[l]
            lang = l
            break

    if not subtitle_data:
        # 尝试第一个可用的
        for l, data in subtitles.items():
            subtitle_data = data
            lang = l
            break
        if not subtitle_data:
            for l, data in auto_captions.items():
                subtitle_data = data
                lang = l
                break

    if not subtitle_data:
        raise ValueError("无可用字幕")

    # 下载字幕内容
    for sub in subtitle_data:
        sub_url = sub.get('url', '')
        if sub_url:
            resp = requests.get(sub_url, timeout=10)
            if resp.status_code == 200:
                return _parse_vtt(resp.text, lang or 'zh')

    raise ValueError("字幕下载失败")


def _extract_ytdlp_subtitles(url: str) -> dict:
    """通过 yt-dlp 提取字幕"""
    import yt_dlp

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['zh', 'zh-Hans', 'zh-CN', 'en', 'ja', 'ko'],
            'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(tmpdir, '%(id)s.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                raise ValueError("无法获取视频信息")

            # 尝试下载字幕
            ydl.download([url])

            # 查找字幕文件
            video_id = info.get('id', '')
            for f in os.listdir(tmpdir):
                if f.endswith('.vtt'):
                    filepath = os.path.join(tmpdir, f)
                    with open(filepath, 'r', encoding='utf-8') as fp:
                        vtt_content = fp.read()

                    # 检测语言
                    lang = 'zh'
                    if '.en.' in f or '.en-' in f:
                        lang = 'en'
                    elif '.ja.' in f:
                        lang = 'ja'
                    elif '.ko.' in f:
                        lang = 'ko'

                    return _parse_vtt(vtt_content, lang)

    raise ValueError("该视频暂无可用字幕")


def _parse_vtt(vtt_text: str, language: str = 'zh') -> dict:
    """解析 VTT 格式字幕"""
    segments = []
    lines = vtt_text.split('\n')

    i = 0
    # 跳过 WEBVTT 头
    while i < len(lines) and not '-->' in lines[i]:
        i += 1

    while i < len(lines):
        line = lines[i].strip()

        # 查找时间戳行
        if '-->' in line:
            match = re.match(
                r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})',
                line
            )
            if match:
                start = _parse_vtt_time(match.group(1))
                end = _parse_vtt_time(match.group(2))

                # 读取文本
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip():
                    text = re.sub(r'<[^>]+>', '', lines[i].strip())  # 去除 HTML 标签
                    if text:
                        text_lines.append(text)
                    i += 1

                if text_lines:
                    segments.append({
                        'start': start,
                        'end': end,
                        'text': ' '.join(text_lines),
                    })
        i += 1

    # 合并连续的短片段
    merged = []
    for seg in segments:
        if merged and seg['start'] - merged[-1]['end'] < 0.5:
            merged[-1]['end'] = seg['end']
            merged[-1]['text'] += seg['text']
        else:
            merged.append(seg.copy())

    full_text = ' '.join(s['text'] for s in merged)

    return {
        'segments': merged,
        'full_text': full_text,
        'language': language,
    }


def _parse_vtt_time(time_str: str) -> float:
    """解析 VTT 时间格式为秒"""
    parts = time_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def _truncate_text(text: str, max_chars: int = 15000) -> str:
    """截断文本，保留首尾各 50%"""
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + "\n...(中间省略)...\n" + text[-half:]


def stream_summary(subtitle_text: str):
    """流式生成视频总结"""
    client = get_client()
    truncated = _truncate_text(subtitle_text)

    prompt = f"""请根据以下视频字幕内容，生成一份结构化的视频总结。

要求：
1. 使用 Markdown 格式
2. 包含以下部分：
   - ## 概述（一句话总结视频核心内容）
   - ## 内容大纲（分点列出视频的主要内容）
   - ## 核心要点（3-5个关键知识点）
   - ## 一句话总结

字幕内容：
{truncated}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个专业的视频内容分析助手，擅长从字幕中提取关键信息并生成结构化总结。"},
            {"role": "user", "content": prompt}
        ],
        stream=True,
        max_tokens=2000,
        temperature=0.7,
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def generate_mindmap(subtitle_text: str) -> str:
    """生成思维导图 Markdown"""
    client = get_client()
    truncated = _truncate_text(subtitle_text)

    prompt = f"""请根据以下视频字幕内容，生成一个思维导图的 Markdown 结构。

要求：
1. 使用 Markdown 标题层级表示思维导图结构
2. 第一行必须是 # 根节点（视频标题）
3. 用 ## 表示一级分支（主要内容）
4. 用 ### 表示二级分支（详细内容）
5. 每个分支下的叶子节点用简短的描述
6. 控制在 3-5 个一级分支，每个分支下 2-4 个叶子节点

字幕内容：
{truncated}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个擅长将内容结构化为思维导图的助手。只输出 Markdown 格式的思维导图结构，不要有其他解释。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.5,
    )

    return response.choices[0].message.content


def stream_chat(subtitle_text: str, question: str, history: list = None):
    """流式 AI 问答"""
    client = get_client()
    truncated = _truncate_text(subtitle_text)

    messages = [
        {"role": "system", "content": f"你是一个视频内容分析助手。根据以下视频字幕内容回答用户问题。\n\n字幕内容：\n{truncated}"}
    ]

    # 添加历史对话
    if history:
        for msg in history[-10:]:  # 最多保留 10 条历史
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True,
        max_tokens=2000,
        temperature=0.7,
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
