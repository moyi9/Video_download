<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  url: String,
})

const subtitles = ref([])
const fullText = ref('')
const loading = ref(true)
const expanded = ref(false)
const INITIAL_COUNT = 20

onMounted(async () => {
  try {
    const resp = await fetch('/api/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: props.url, language: 'zh' }),
    })

    const reader = resp.body.getReader()
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
          const event = JSON.parse(line.slice(6))
          if (event.type === 'subtitle') {
            subtitles.value = event.data.segments || []
            fullText.value = event.data.full_text || ''
          } else if (event.type === 'done') {
            loading.value = false
          }
        } catch (e) {}
      }
    }
  } catch (e) {
    loading.value = false
  }
})

const visibleSubtitles = computed(() => {
  return expanded.value ? subtitles.value : subtitles.value.slice(0, INITIAL_COUNT)
})

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

function downloadSubtitle(format) {
  let content = ''
  let filename = ''
  let mimeType = 'text/plain'

  if (format === 'srt') {
    content = subtitles.value.map((s, i) =>
      `${i + 1}\n${formatSrtTime(s.start)} --> ${formatSrtTime(s.end)}\n${s.text}\n`
    ).join('\n')
    filename = 'subtitle.srt'
  } else if (format === 'vtt') {
    content = 'WEBVTT\n\n' + subtitles.value.map(s =>
      `${formatVttTime(s.start)} --> ${formatVttTime(s.end)}\n${s.text}`
    ).join('\n\n')
    filename = 'subtitle.vtt'
    mimeType = 'text/vtt'
  } else {
    content = subtitles.value.map(s => s.text).join('\n')
    filename = 'subtitle.txt'
  }

  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

function formatSrtTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  const ms = Math.floor((seconds % 1) * 1000)
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`
}

function formatVttTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  const ms = Math.floor((seconds % 1) * 1000)
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(ms).padStart(3, '0')}`
}
</script>

<template>
  <div>
    <div v-if="loading && !subtitles.length" class="flex flex-col items-center gap-3 text-white/40 py-12">
      <svg class="animate-spin h-8 w-8 text-cyan-400" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      <span class="text-sm">正在提取字幕...</span>
    </div>

    <div v-else-if="!subtitles.length" class="text-center py-12 text-white/30">
      该视频暂无可用字幕
    </div>

    <template v-else>
      <!-- 下载按钮组 -->
      <div class="flex gap-2 mb-4">
        <button @click="downloadSubtitle('srt')" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          下载 SRT
        </button>
        <button @click="downloadSubtitle('vtt')" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          下载 VTT
        </button>
        <button @click="downloadSubtitle('txt')" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          下载 TXT
        </button>
      </div>

      <!-- 字幕列表 -->
      <div class="space-y-2 max-h-[500px] overflow-y-auto pr-2">
        <div
          v-for="(sub, i) in visibleSubtitles"
          :key="i"
          class="flex gap-3 text-sm py-3 border-b border-white/5 last:border-0"
        >
          <span class="text-cyan-400 font-mono text-xs whitespace-nowrap mt-0.5 bg-cyan-500/10 px-2 py-0.5 rounded">
            {{ formatTime(sub.start) }}
          </span>
          <span class="text-white/70">{{ sub.text }}</span>
        </div>
      </div>

      <!-- 展开/收起 -->
      <button
        v-if="subtitles.length > INITIAL_COUNT"
        @click="expanded = !expanded"
        class="mt-4 text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
      >
        {{ expanded ? '收起' : `展开全部 (${subtitles.length} 条)` }}
      </button>
    </template>
  </div>
</template>
