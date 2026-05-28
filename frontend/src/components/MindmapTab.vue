<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  url: String,
})

const svgRef = ref(null)
const loading = ref(true)
const mindmapData = ref('')
const markmapInstance = ref(null)

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
          if (event.type === 'mindmap' && event.data) {
            mindmapData.value = event.data
          } else if (event.type === 'done') {
            loading.value = false
          }
        } catch (e) {}
      }
    }

    if (mindmapData.value) {
      await nextTick()
      await renderMindmap()
    }
  } catch (e) {
    loading.value = false
  }
})

onUnmounted(() => {
  if (markmapInstance.value) {
    markmapInstance.value.destroy()
  }
})

async function renderMindmap() {
  if (!svgRef.value || !mindmapData.value) return

  const { Transformer } = await import('markmap-lib')
  const { Markmap } = await import('markmap-view')

  const transformer = new Transformer()
  const { root } = transformer.transform(mindmapData.value)

  if (markmapInstance.value) {
    markmapInstance.value.destroy()
  }
  markmapInstance.value = Markmap.create(svgRef.value, undefined, root)
}

async function toggleFullscreen() {
  const container = svgRef.value?.parentElement
  if (!container) return

  if (document.fullscreenElement) {
    await document.exitFullscreen()
  } else {
    await container.requestFullscreen()
    await nextTick()
    markmapInstance.value?.fit()
  }
}

function downloadSvg() {
  if (!svgRef.value) return
  const svgData = svgRef.value.outerHTML
  const blob = new Blob([svgData], { type: 'image/svg+xml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'mindmap.svg'
  a.click()
  URL.revokeObjectURL(url)
}

function downloadPng() {
  if (!svgRef.value) return
  const svgData = new XMLSerializer().serializeToString(svgRef.value)
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  const img = new Image()

  img.onload = () => {
    canvas.width = img.width * 2
    canvas.height = img.height * 2
    ctx.scale(2, 2)
    ctx.fillStyle = '#000000'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    ctx.drawImage(img, 0, 0)
    canvas.toBlob(blob => {
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'mindmap.png'
      a.click()
      URL.revokeObjectURL(url)
    })
  }

  img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)))
}
</script>

<template>
  <div>
    <div v-if="loading && !mindmapData" class="flex flex-col items-center gap-3 text-white/40 py-12">
      <svg class="animate-spin h-8 w-8 text-cyan-400" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
      <span class="text-sm">正在生成思维导图...</span>
    </div>

    <div v-else-if="!mindmapData" class="text-center py-12 text-white/30">
      无法生成思维导图
    </div>

    <template v-else>
      <!-- 操作按钮 -->
      <div class="flex gap-2 mb-4">
        <button @click="toggleFullscreen" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          全屏展示
        </button>
        <button @click="downloadPng" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          下载 PNG
        </button>
        <button @click="downloadSvg" class="px-4 py-2 text-xs bg-white/5 hover:bg-white/10 rounded-lg transition-colors border border-white/10 text-white/70">
          下载 SVG
        </button>
      </div>

      <!-- 思维导图容器 -->
      <div class="border border-white/10 rounded-2xl overflow-hidden bg-white/5" style="min-height: 400px;">
        <svg ref="svgRef" style="width: 100%; height: 100%; min-height: 400px;" />
      </div>
    </template>
  </div>
</template>
