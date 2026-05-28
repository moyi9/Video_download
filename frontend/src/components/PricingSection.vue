<script setup>
const plans = [
  {
    name: '免费版',
    price: '¥0',
    period: '永久',
    description: '适合轻度使用',
    features: [
      { text: '每日 3 次下载', included: true },
      { text: '最高 720p 清晰度', included: true },
      { text: '基础 AI 总结', included: true },
      { text: '标准下载速度', included: true },
      { text: '4K 超高清', included: false },
      { text: '批量下载', included: false },
    ],
    highlighted: false,
    buttonText: '开始使用',
    buttonClass: 'btn-outline',
  },
  {
    name: '高级版',
    price: '¥9.9',
    period: '/月',
    description: '解锁全部能力',
    badge: '最受欢迎',
    features: [
      { text: '无限次下载', included: true },
      { text: '最高 4K 清晰度', included: true },
      { text: '完整 AI 功能', included: true },
      { text: '极速下载通道', included: true },
      { text: '批量下载', included: true },
      { text: '字幕翻译', included: true },
    ],
    highlighted: true,
    buttonText: '立即升级',
    buttonClass: 'btn-primary',
  },
]
</script>

<template>
  <section id="pricing" class="max-w-5xl mx-auto px-4 sm:px-6 py-20">
    <!-- 标题 -->
    <div class="text-center mb-14">
      <div class="animate-fade-in-up inline-flex items-center gap-2 px-4 py-2 bg-amber-500/10 text-amber-400 rounded-full text-sm font-medium mb-6 border border-amber-500/20">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        定价方案
      </div>
      <h2 class="animate-fade-in-up delay-100 text-4xl sm:text-5xl font-black text-white mb-5">
        选择适合你的
        <span class="gradient-text">方案</span>
      </h2>
      <p class="animate-fade-in-up delay-200 text-white/50 text-lg">免费版满足日常需求，高级版解锁全部能力</p>
    </div>

    <!-- 定价卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-4xl mx-auto">
      <div
        v-for="(plan, index) in plans"
        :key="plan.name"
        :class="[
          'relative rounded-3xl p-8 transition-all duration-500',
          plan.highlighted
            ? 'bg-gradient-to-br from-cyan-500/20 via-blue-500/20 to-purple-500/20 border-2 border-cyan-400/50 shadow-2xl shadow-cyan-500/20 scale-[1.02]'
            : 'bg-white/5 border border-white/10 hover:border-white/20 hover:bg-white/10'
        ]"
        :style="`animation-delay: ${index * 200}ms`"
      >
        <!-- 推荐标签 -->
        <div v-if="plan.badge" class="absolute -top-4 left-1/2 -translate-x-1/2">
          <span class="bg-gradient-to-r from-cyan-400 to-blue-400 text-black text-xs font-bold px-5 py-1.5 rounded-full shadow-lg shadow-cyan-500/30">
            {{ plan.badge }}
          </span>
        </div>

        <!-- 套餐名 -->
        <div class="mb-6">
          <h3 class="text-xl font-bold text-white mb-2">{{ plan.name }}</h3>
          <p class="text-sm text-white/40">{{ plan.description }}</p>
        </div>

        <!-- 价格 -->
        <div class="mb-8">
          <div class="flex items-baseline gap-1">
            <span class="text-5xl font-black text-white">{{ plan.price }}</span>
            <span class="text-lg text-white/40">{{ plan.period }}</span>
          </div>
        </div>

        <!-- 功能列表 -->
        <ul class="space-y-4 mb-8">
          <li v-for="feature in plan.features" :key="feature.text" class="flex items-center gap-3">
            <div v-if="feature.included" class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 bg-green-500/20">
              <svg class="w-3 h-3 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div v-else class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 bg-white/5">
              <svg class="w-3 h-3 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <span :class="['text-sm', feature.included ? 'text-white/80' : 'text-white/30']">
              {{ feature.text }}
            </span>
          </li>
        </ul>

        <!-- 按钮 -->
        <button :class="[plan.buttonClass, 'w-full']">
          {{ plan.buttonText }}
        </button>
      </div>
    </div>
  </section>
</template>
