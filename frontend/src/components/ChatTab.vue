<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  url: String,
})

const messages = ref([])
const input = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

async function sendMessage() {
  const question = input.value.trim()
  if (!question || loading.value) return

  messages.value.push({ role: 'user', content: question })
  input.value = ''
  loading.value = true

  const assistantMessage = { role: 'assistant', content: '' }
  messages.value.push(assistantMessage)

  await nextTick()
  scrollToBottom()

  try {
    const history = messages.value.slice(0, -1).map(m => ({
      role: m.role,
      content: m.content,
    }))

    const resp = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: props.url,
        question,
        history,
      }),
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
          if (event.type === 'answer') {
            assistantMessage.content += event.data
            await nextTick()
            scrollToBottom()
          } else if (event.type === 'error') {
            assistantMessage.content = '抱歉，出现错误：' + event.data
          }
        } catch (e) {}
      }
    }
  } catch (e) {
    assistantMessage.content = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<template>
  <div class="flex flex-col h-[500px]">
    <!-- 消息列表 -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
      <div v-if="!messages.length" class="flex flex-col items-center justify-center h-full text-white/30 text-sm">
        <div class="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        针对视频内容提问，AI 将基于字幕回答
      </div>

      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <div
          :class="[
            'max-w-[80%] rounded-2xl px-4 py-3 text-sm',
            msg.role === 'user'
              ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-br-md shadow-lg shadow-cyan-500/20'
              : 'bg-white/10 text-white/80 rounded-bl-md border border-white/10'
          ]"
        >
          <div v-if="msg.role === 'assistant'" class="prose prose-sm max-w-none" v-html="marked(msg.content || '')" />
          <div v-else>{{ msg.content }}</div>
          <span v-if="msg.role === 'assistant' && loading && i === messages.length - 1 && !msg.content" class="inline-block w-0.5 h-4 bg-cyan-400 animate-pulse ml-0.5" />
        </div>
      </div>
    </div>

    <!-- 输入框 -->
    <form @submit.prevent="sendMessage" class="flex gap-3">
      <input
        v-model="input"
        type="text"
        placeholder="输入你的问题..."
        :disabled="loading"
        class="flex-1 px-5 py-3.5 bg-white/5 border border-white/20 rounded-full text-sm text-white placeholder:text-white/30 focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20 focus:outline-none disabled:bg-white/5 transition-all"
      />
      <button
        type="submit"
        :disabled="loading || !input.trim()"
        class="btn-primary !px-6 !py-3.5 !rounded-full"
      >
        <svg v-if="!loading" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
        <svg v-else class="animate-spin h-5 w-5" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      </button>
    </form>
  </div>
</template>
