/**
 * AI 视频总结 API（SSE 流式）
 */
export function summarizeVideo(url, language = 'zh') {
  return fetch('/api/summarize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, language }),
  })
}

/**
 * AI 视频问答 API（SSE 流式）
 */
export function chatWithAI(url, question, history = []) {
  return fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, question, history }),
  })
}

/**
 * 解析 SSE 流
 */
export async function* parseSSE(response) {
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n\n')
    buffer = lines.pop()

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      try {
        yield JSON.parse(line.slice(6))
      } catch (e) {}
    }
  }
}
