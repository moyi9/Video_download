import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from summarizer import extract_subtitles, stream_summary, generate_mindmap, stream_chat

router = APIRouter(prefix="/api")


class SummarizeRequest(BaseModel):
    url: str
    language: str = "zh"


class ChatRequest(BaseModel):
    url: str
    question: str
    history: Optional[List[dict]] = None


@router.post("/summarize")
async def api_summarize(req: SummarizeRequest):
    """AI 视频总结（SSE 流式）"""
    async def event_generator():
        try:
            # 提取字幕
            subtitle_data = extract_subtitles(req.url)
            yield f"data: {json.dumps({'type': 'subtitle', 'data': subtitle_data}, ensure_ascii=False)}\n\n"

            # 流式生成总结
            full_text = subtitle_data.get('full_text', '')
            for token in stream_summary(full_text):
                yield f"data: {json.dumps({'type': 'summary', 'data': token}, ensure_ascii=False)}\n\n"

            # 生成思维导图
            mindmap = generate_mindmap(full_text)
            yield f"data: {json.dumps({'type': 'mindmap', 'data': mindmap}, ensure_ascii=False)}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/chat")
async def api_chat(req: ChatRequest):
    """AI 视频问答（SSE 流式）"""
    async def event_generator():
        try:
            # 提取字幕
            subtitle_data = extract_subtitles(req.url)
            full_text = subtitle_data.get('full_text', '')

            # 流式问答
            for token in stream_chat(full_text, req.question, req.history or []):
                yield f"data: {json.dumps({'type': 'answer', 'data': token}, ensure_ascii=False)}\n\n"

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
