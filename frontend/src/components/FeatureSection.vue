<script setup>
const features = [
  {
    icon: `<svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>`,
    title: '万能平台',
    desc: '1800+ 平台一键解析',
    color: 'from-cyan-400 to-cyan-600',
    glow: 'shadow-cyan-500/30',
    iconBg: 'bg-cyan-500/20',
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>`,
    title: '极速下载',
    desc: '智能选择最优通道',
    color: 'from-amber-400 to-orange-500',
    glow: 'shadow-amber-500/30',
    iconBg: 'bg-amber-500/20',
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>`,
    title: 'AI 智能',
    desc: '摘要、导图、问答',
    color: 'from-purple-400 to-violet-500',
    glow: 'shadow-purple-500/30',
    iconBg: 'bg-purple-500/20',
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>`,
    title: '多格式',
    desc: 'MP4、WebM 多清晰度',
    color: 'from-emerald-400 to-teal-500',
    glow: 'shadow-emerald-500/30',
    iconBg: 'bg-emerald-500/20',
  },
  {
    icon: `<svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>`,
    title: '安全隐私',
    desc: '不存储数据，自动清理',
    color: 'from-rose-400 to-pink-500',
    glow: 'shadow-rose-500/30',
    iconBg: 'bg-rose-500/20',
  },
]
</script>

<template>
  <section id="features" class="max-w-7xl mx-auto px-4 sm:px-6 py-20">
    <!-- 标题 -->
    <div class="text-center mb-14">
      <div class="animate-fade-in-up inline-flex items-center gap-2 px-4 py-2 bg-cyan-500/10 text-cyan-400 rounded-full text-sm font-medium mb-6 border border-cyan-500/20">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
        核心功能
      </div>
      <h2 class="animate-fade-in-up delay-100 text-4xl sm:text-5xl font-black text-white mb-5">
        为什么选择
        <span class="gradient-text">VideoDL</span>
      </h2>
      <p class="animate-fade-in-up delay-200 text-white/50 text-lg max-w-2xl mx-auto">简单、快速、智能的视频下载体验</p>
    </div>

    <!-- 功能卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
      <div
        v-for="(feature, index) in features"
        :key="feature.title"
        class="card group cursor-default text-center"
        :class="`animate-fade-in-up delay-${(index + 2) * 100}`"
      >
        <!-- 图标 -->
        <div :class="['w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 transition-all duration-500 group-hover:scale-110 group-hover:shadow-xl', feature.iconBg, feature.glow]">
          <div :class="['bg-gradient-to-br rounded-xl p-3 text-white', feature.color]" v-html="feature.icon"></div>
        </div>

        <!-- 内容 -->
        <h3 class="font-bold text-white text-lg mb-2">{{ feature.title }}</h3>
        <p class="text-sm text-white/50">{{ feature.desc }}</p>
      </div>
    </div>
  </section>
</template>
