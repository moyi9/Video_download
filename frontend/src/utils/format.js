/**
 * 格式化文件大小
 */
export function formatFileSize(bytes) {
  if (!bytes) return '未知'
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  return `${size.toFixed(1)} ${units[unitIndex]}`
}

/**
 * 格式化时长
 */
export function formatDuration(seconds) {
  if (!seconds) return '0:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`
}

/**
 * 格式化播放次数
 */
export function formatViewCount(count) {
  if (!count) return '未知'
  if (count >= 100000000) {
    return `${(count / 100000000).toFixed(1)}亿次播放`
  }
  if (count >= 10000) {
    return `${(count / 10000).toFixed(1)}万次播放`
  }
  return `${count}次播放`
}

/**
 * 格式化上传日期
 */
export function formatDate(dateStr) {
  if (!dateStr || dateStr.length !== 8) return ''
  const year = dateStr.slice(0, 4)
  const month = dateStr.slice(4, 6)
  const day = dateStr.slice(6, 8)
  return `${year}-${month}-${day}`
}
