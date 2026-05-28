const API_BASE = '/api'

/**
 * 解析视频信息
 */
export async function parseVideo(url) {
  const resp = await fetch(`${API_BASE}/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  })
  return resp.json()
}

/**
 * 获取视频直链
 */
export async function getDirectUrl(url, formatId) {
  const resp = await fetch(`${API_BASE}/direct-url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, format_id: formatId }),
  })
  return resp.json()
}

/**
 * 服务端代理下载
 */
export async function downloadVideo(url, formatId) {
  const resp = await fetch(`${API_BASE}/download`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, format_id: formatId }),
  })

  if (!resp.ok) {
    const err = await resp.json()
    throw new Error(err.detail || '下载失败')
  }

  // 获取文件名
  const disposition = resp.headers.get('Content-Disposition')
  let filename = 'video.mp4'
  if (disposition) {
    const match = disposition.match(/filename="?([^"]+)"?/)
    if (match) filename = match[1]
  }

  // 流式下载
  const blob = await resp.blob()
  const url2 = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url2
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url2)
}
