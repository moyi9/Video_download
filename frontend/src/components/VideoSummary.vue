<script setup>
import { ref } from 'vue'
import SummaryTab from './SummaryTab.vue'
import SubtitleTab from './SubtitleTab.vue'
import MindmapTab from './MindmapTab.vue'
import ChatTab from './ChatTab.vue'

const props = defineProps({
  video: Object,
  url: String,
})

const tabs = [
  { id: 'summary', label: '总结摘要', icon: '📊' },
  { id: 'subtitle', label: '字幕文本', icon: '📝' },
  { id: 'mindmap', label: '思维导图', icon: '🧠' },
  { id: 'chat', label: 'AI 问答', icon: '💬' },
]

const activeTab = ref('summary')
</script>

<template>
  <div class="card">
    <!-- 标题 -->
    <div class="flex items-center gap-3 mb-5">
      <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg shadow-purple-500/30">
        <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      </div>
      <h3 class="font-bold text-white text-lg">AI 智能分析</h3>
    </div>

    <!-- Tab 导航 -->
    <div class="flex gap-2 mb-5 overflow-x-auto pb-2 -mx-1 px-1">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all duration-300',
          activeTab === tab.id
            ? 'bg-gradient-to-r from-cyan-400 to-blue-500 text-black shadow-lg shadow-cyan-500/30'
            : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white border border-white/10'
        ]"
      >
        <span>{{ tab.icon }}</span>
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <!-- Tab 内容 -->
    <div class="min-h-[400px] bg-white/5 rounded-2xl p-5 border border-white/5">
      <SummaryTab v-if="activeTab === 'summary'" :url="url" />
      <SubtitleTab v-if="activeTab === 'subtitle'" :url="url" />
      <MindmapTab v-if="activeTab === 'mindmap'" :url="url" />
      <ChatTab v-if="activeTab === 'chat'" :url="url" />
    </div>
  </div>
</template>
