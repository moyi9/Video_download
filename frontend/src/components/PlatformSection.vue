<script setup>
const platforms = [
  { name: 'YouTube', icon: '▶', color: 'text-red-400', bg: 'bg-red-500/20', shadow: 'hover:shadow-red-500/20' },
  { name: 'Bilibili', icon: '▶', color: 'text-cyan-400', bg: 'bg-cyan-500/20', shadow: 'hover:shadow-cyan-500/20' },
  { name: '抖音', icon: '♪', color: 'text-white', bg: 'bg-white/10', shadow: 'hover:shadow-white/10' },
  { name: 'TikTok', icon: '♪', color: 'text-pink-400', bg: 'bg-pink-500/20', shadow: 'hover:shadow-pink-500/20' },
  { name: 'Twitter/X', icon: '𝕏', color: 'text-blue-400', bg: 'bg-blue-500/20', shadow: 'hover:shadow-blue-500/20' },
  { name: 'Instagram', icon: '📷', color: 'text-pink-400', bg: 'bg-pink-500/20', shadow: 'hover:shadow-pink-500/20' },
  { name: 'Vimeo', icon: '▶', color: 'text-cyan-400', bg: 'bg-cyan-500/20', shadow: 'hover:shadow-cyan-500/20' },
  { name: 'Facebook', icon: 'f', color: 'text-blue-400', bg: 'bg-blue-500/20', shadow: 'hover:shadow-blue-500/20' },
  { name: 'Twitch', icon: '⚡', color: 'text-purple-400', bg: 'bg-purple-500/20', shadow: 'hover:shadow-purple-500/20' },
  { name: 'Dailymotion', icon: '▶', color: 'text-blue-400', bg: 'bg-blue-500/20', shadow: 'hover:shadow-blue-500/20' },
  { name: 'SoundCloud', icon: '☁', color: 'text-orange-400', bg: 'bg-orange-500/20', shadow: 'hover:shadow-orange-500/20' },
  { name: '1800+', icon: '+', color: 'text-cyan-400', bg: 'bg-cyan-500/20', shadow: 'hover:shadow-cyan-500/20' },
]
</script>

<template>
  <section id="platforms" class="max-w-6xl mx-auto px-4 sm:px-6 py-20">
    <!-- 标题 -->
    <div class="text-center mb-14">
      <div class="animate-fade-in-up inline-flex items-center gap-2 px-4 py-2 bg-green-500/10 text-green-400 rounded-full text-sm font-medium mb-6 border border-green-500/20">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
        </svg>
        平台支持
      </div>
      <h2 class="animate-fade-in-up delay-100 text-4xl sm:text-5xl font-black text-white mb-5">
        支持
        <span class="gradient-text">1800+</span>
        平台
      </h2>
      <p class="animate-fade-in-up delay-200 text-white/50 text-lg">主流视频平台全覆盖，持续更新中</p>
    </div>

    <!-- 平台网格 -->
    <div class="grid grid-cols-3 sm:grid-cols-4 lg:grid-cols-6 gap-4">
      <div
        v-for="(platform, index) in platforms"
        :key="platform.name"
        class="card group text-center py-6 cursor-default"
        :class="`animate-scale-in delay-${(index % 6 + 2) * 100} ${platform.shadow} hover:shadow-xl`"
      >
        <!-- 图标 -->
        <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 transition-all duration-300 group-hover:scale-110', platform.bg]">
          <span :class="['text-2xl font-bold', platform.color]">{{ platform.icon }}</span>
        </div>

        <!-- 名称 -->
        <span class="text-sm font-medium text-white/70">{{ platform.name }}</span>
      </div>
    </div>
  </section>
</template>
