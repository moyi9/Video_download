import os
import json
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from downloader import parse_video, get_direct_url, download_video, is_youtube_url
from douyin import resolve_douyin_url

router = APIRouter(prefix="/api")


class ParseRequest(BaseModel):
    url: str


class DirectUrlRequest(BaseModel):
    url: str
    format_id: str


class DownloadRequest(BaseModel):
    url: str
    format_id: str


@router.post("/parse")
async def api_parse(req: ParseRequest):
    """解析视频信息"""
    try:
        url = req.url.strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL不能为空")

        # 抖音特殊处理
        if 'douyin.com' in url:
            url = resolve_douyin_url(url)
            return {"success": False, "error": "抖音解析需要浏览器cookies，请使用YouTube、B站或其他平台"}

        data = parse_video(url)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/direct-url")
async def api_direct_url(req: DirectUrlRequest):
    """获取视频直链（YouTube不支持，会自动返回错误）"""
    try:
        url = req.url.strip()
        if 'douyin.com' in url:
            url = resolve_douyin_url(url)

        # YouTube直链下载容易403，建议使用代理下载
        if is_youtube_url(url):
            return {"success": False, "error": "YouTube请使用代理下载模式"}

        data = get_direct_url(url, req.format_id)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/download")
async def api_download(req: DownloadRequest):
    """服务端代理下载"""
    try:
        url = req.url.strip()
        if 'douyin.com' in url:
            url = resolve_douyin_url(url)

        output_dir = os.path.join(os.path.dirname(__file__), 'downloads')
        filepath = download_video(url, req.format_id, output_dir)

        # 获取文件名
        filename = os.path.basename(filepath)

        def iter_file():
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    yield chunk
            # 下载完成后删除文件
            try:
                os.remove(filepath)
            except OSError:
                pass

        # RFC 5987 编码文件名，支持中文
        encoded_filename = urllib.parse.quote(filename, safe='')
        content_disp = f"attachment; filename*=UTF-8''{encoded_filename}"

        return StreamingResponse(
            iter_file(),
            media_type='video/mp4',
            headers={
                'Content-Disposition': content_disp
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/thumbnail")
async def api_thumbnail(url: str):
    """代理图片，解决跨域Referer限制"""
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.bilibili.com/',
            })
            if resp.status_code == 200:
                content_type = resp.headers.get('content-type', 'image/jpeg')
                return Response(content=resp.content, media_type=content_type)
            raise HTTPException(status_code=resp.status_code)
    except httpx.HTTPError:
        raise HTTPException(status_code=502)
