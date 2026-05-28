<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  url: String,
})

const content = ref('')
const loading = ref(true)

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
          if (event.type === 'summary') {
            content.value += event.data
          } else if (event.type === 'done') {
            loading.value = false
          }
        } catch (e) {}
      }
    }
  } catch (e) {
    content.value = '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <div v-if="loading && !content" class="flex flex-col items-center gap-3 text-white/40 py-12">
      <div class="relative">
        <svg class="animate-spin h-8 w-8 text-cyan-400" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      </div>
      <span class="text-sm">AI 正在分析视频内容...</span>
    </div>
    <div
      v-if="content"
      class="prose prose-sm max-w-none"
      v-html="marked(content)"
    />
    <span v-if="loading && content" class="inline-block w-0.5 h-4 bg-cyan-400 animate-pulse ml-0.5" />
  </div>
</template>
