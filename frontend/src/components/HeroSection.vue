<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: Boolean,
  parsed: Boolean,
})

const emit = defineEmits(['parse'])

const url = ref('')

function handleSubmit() {
  if (url.value.trim()) {
    emit('parse', url.value.trim())
  }
}

const platforms = [
  { name: 'YouTube', icon: '▶' },
  { name: 'Bilibili', icon: '▶' },
  { name: '抖音', icon: '♪' },
  { name: 'TikTok', icon: '♪' },
  { name: 'Twitter/X', icon: '𝕏' },
  { name: 'Instagram', icon: '📷' },
]
</script>

<template>
  <section :class="['transition-all duration-700 ease-out relative', parsed ? 'py-8' : 'py-28 sm:py-36']">
    <!-- 装饰光效 -->
    <div v-show="!parsed" class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-1/4 w-72 h-72 bg-cyan-500/20 rounded-full blur-[100px] animate-pulse"></div>
      <div class="absolute bottom-20 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-[120px] animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[150px]"></div>
    </div>

    <div class="max-w-5xl mx-auto px-4 text-center relative">
      <!-- 标题区域 -->
      <div v-show="!parsed" class="mb-12">
        <!-- 标签 -->
        <div class="animate-fade-in-up inline-flex items-center gap-2 px-5 py-2.5 bg-white/10 backdrop-blur-md rounded-full text-sm text-cyan-400 font-medium mb-8 border border-white/10">
          <span class="relative flex h-2.5 w-2.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-400"></span>
          </span>
          支持 1800+ 视频平台
        </div>

        <!-- 主标题 -->
        <h1 class="animate-fade-in-up delay-100 text-6xl sm:text-8xl font-black mb-8 leading-[1.1] tracking-tight">
          <span class="text-white">万能视频</span>
          <br />
          <span class="gradient-text neon">下载神器</span>
        </h1>

        <!-- 副标题 -->
        <p class="animate-fade-in-up delay-200 text-xl sm:text-2xl text-white/60 max-w-2xl mx-auto mb-4 leading-relaxed">
          一键解析 · 多格式选择 · AI 智能总结
        </p>
        <p class="animate-fade-in-up delay-300 text-white/40">
          支持 YouTube、B站、抖音、TikTok 等主流平台
        </p>
      </div>

      <!-- 搜索框 -->
      <form @submit.prevent="handleSubmit" class="animate-fade-in-up delay-300 relative max-w-3xl mx-auto">
        <div class="relative group">
          <!-- 光效 -->
          <div class="absolute -inset-1 bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 rounded-full opacity-30 group-hover:opacity-50 group-focus-within:opacity-60 blur-lg transition-opacity duration-500"></div>

          <div class="relative flex items-center bg-black/50 backdrop-blur-xl rounded-full border border-white/20 shadow-2xl shadow-cyan-500/20">
            <!-- 搜索图标 -->
            <div class="pl-6 text-white/40">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <input
              v-model="url"
              type="url"
              placeholder="粘贴视频链接..."
              class="flex-1 px-5 py-5 text-lg bg-transparent border-none focus:outline-none focus:ring-0 placeholder:text-white/30 text-white"
              :disabled="loading"
            />

            <button
              type="submit"
              :disabled="loading || !url.trim()"
              class="mr-2 btn-primary !px-8 !py-3 text-base"
            >
              <span v-if="loading" class="flex items-center gap-2">
                <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                解析中...
              </span>
              <span v-else class="flex items-center gap-2">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                解析
              </span>
            </button>
          </div>
        </div>
      </form>

      <!-- 快捷链接 -->
      <div v-show="!parsed" class="animate-fade-in-up delay-400 mt-8 flex flex-wrap justify-center gap-3">
        <span class="text-sm text-white/30">热门平台：</span>
        <button
          v-for="p in platforms"
          :key="p.name"
          @click="url = p.name === 'YouTube' ? 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' :
                   p.name === 'Bilibili' ? 'https://www.bilibili.com/video/BV1GJ411x7h7' : ''"
          class="text-sm px-4 py-2 bg-white/5 hover:bg-white/10 rounded-full text-white/60 hover:text-white transition-all duration-300 border border-white/10 hover:border-white/20"
        >
          {{ p.icon }} {{ p.name }}
        </button>
      </div>

      <!-- 信任指标 -->
      <div v-show="!parsed" class="animate-fade-in-up delay-500 mt-12 flex items-center justify-center gap-10 text-sm text-white/40">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <span>免费使用</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span>极速下载</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-purple-500/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <span>安全隐私</span>
        </div>
      </div>
    </div>
  </section>
</template>
