<script setup>
import { ref } from 'vue'
import { getDirectUrl, downloadVideo } from '../api/video'
import { formatFileSize, formatDuration, formatViewCount, formatDate } from '../utils/format'

const props = defineProps({
  video: Object,
  url: String,
})

const selectedFormat = ref(props.video?.formats?.[0]?.format_id || '')
const downloading = ref(false)
const downloadStatus = ref('')

function isYouTube() {
  const u = props.url?.toLowerCase() || ''
  return u.includes('youtube.com') || u.includes('youtu.be')
}

function isBilibili() {
  const u = props.url?.toLowerCase() || ''
  return u.includes('bilibili.com') || u.includes('b23.tv')
}

async function handleDownload() {
  if (!selectedFormat.value) return
  downloading.value = true

  // YouTube/B站强制使用代理下载（直链需要特殊头，浏览器无法设置）
  if (isYouTube() || isBilibili()) {
    try {
      downloadStatus.value = '正在通过服务器下载...'
      await downloadVideo(props.url, selectedFormat.value)
      downloadStatus.value = '下载完成'
      setTimeout(() => { downloadStatus.value = '' }, 3000)
    } catch (e) {
      alert('下载失败：' + e.message)
    } finally {
      downloading.value = false
    }
    return
  }

  // 其他平台先尝试直链
  downloadStatus.value = '正在获取下载链接...'
  try {
    const directResult = await getDirectUrl(props.url, selectedFormat.value)
    if (directResult.success && directResult.data.direct_url) {
      downloadStatus.value = '正在下载...'
      const a = document.createElement('a')
      a.href = directResult.data.direct_url
      a.target = '_blank'
      a.rel = 'noopener noreferrer'
      a.download = `video.${directResult.data.ext || 'mp4'}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      downloadStatus.value = '下载已开始'
      setTimeout(() => { downloadStatus.value = '' }, 3000)
      return
    }
  } catch (e) {
    console.log('直链获取失败，尝试代理下载:', e.message)
  }

  // 直链失败，回退代理下载
  try {
    downloadStatus.value = '正在通过服务器下载...'
    await downloadVideo(props.url, selectedFormat.value)
    downloadStatus.value = '下载完成'
    setTimeout(() => { downloadStatus.value = '' }, 3000)
  } catch (e) {
    alert('下载失败：' + e.message)
  } finally {
    downloading.value = false
  }
}
</script>

<template>
  <div class="card">
    <!-- 缩略图 -->
    <div class="relative aspect-video rounded-2xl overflow-hidden mb-4 bg-white/5 group">
      <img
        v-if="video.thumbnail"
        :src="`/api/thumbnail?url=${encodeURIComponent(video.thumbnail)}`"
        :alt="video.title"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        loading="lazy"
      />
      <div v-else class="w-full h-full flex items-center justify-center text-white/20">
        <svg class="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
        </svg>
      </div>

      <!-- 播放按钮 -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center">
        <div class="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-75 group-hover:scale-100 border border-white/30">
          <svg class="w-7 h-7 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </div>

      <!-- 时长 -->
      <div v-if="video.duration" class="absolute bottom-3 right-3 bg-black/70 text-white text-xs px-2.5 py-1 rounded-lg font-medium backdrop-blur-sm">
        {{ video.duration_string }}
      </div>

      <!-- 平台 -->
      <div class="absolute top-3 left-3 bg-black/50 text-white/80 text-xs px-2.5 py-1 rounded-lg font-medium backdrop-blur-sm">
        {{ video.platform }}
      </div>
    </div>

    <!-- 视频信息 -->
    <h2 class="text-lg font-bold text-white line-clamp-2 mb-3">{{ video.title }}</h2>

    <div class="flex flex-wrap items-center gap-3 text-sm text-white/50 mb-4">
      <div class="flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span>{{ video.uploader }}</span>
      </div>
      <span class="text-white/20">·</span>
      <span v-if="video.view_count" class="flex items-center gap-1">
        {{ formatViewCount(video.view_count) }}
      </span>
      <span v-if="video.upload_date" class="flex items-center gap-1">
        {{ formatDate(video.upload_date) }}
      </span>
    </div>

    <!-- 格式选择 -->
    <div class="mb-4">
      <label class="block text-sm font-medium text-white/70 mb-2">选择格式</label>
      <div class="relative">
        <select
          v-model="selectedFormat"
          class="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-sm text-white focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 focus:outline-none appearance-none cursor-pointer"
        >
          <option v-for="fmt in video.formats" :key="fmt.format_id" :value="fmt.format_id" class="bg-gray-900">
            {{ fmt.label }}
          </option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg class="w-5 h-5 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 下载按钮 -->
    <button
      @click="handleDownload"
      :disabled="downloading || !selectedFormat"
      class="w-full btn-primary flex items-center justify-center gap-2 !py-4"
    >
      <svg v-if="!downloading" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      <svg v-else class="animate-spin w-5 h-5" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      {{ downloading ? downloadStatus || '下载中...' : '下载视频' }}
    </button>

    <p v-if="downloadStatus && !downloading" class="text-center text-sm text-green-400 mt-2">
      {{ downloadStatus }}
    </p>
  </div>
</template>
