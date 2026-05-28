<script setup>
</script>

<template>
  <header class="sticky top-0 z-50 bg-black/50 backdrop-blur-xl border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <span class="text-xl font-black text-white tracking-tight">VideoDL</span>
      </div>

      <!-- 导航 -->
      <nav class="hidden sm:flex items-center gap-1">
        <a href="#features" class="px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200">
          功能
        </a>
        <a href="#pricing" class="px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200">
          定价
        </a>
        <a href="#platforms" class="px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200">
          支持平台
        </a>
        <div class="w-px h-4 bg-white/20 mx-2"></div>
        <button class="btn-primary !px-5 !py-2 !text-sm">
          升级 VIP
        </button>
      </nav>

      <!-- 移动端菜单按钮 -->
      <button class="sm:hidden p-2 text-white/60 hover:text-white hover:bg-white/10 rounded-lg transition-all">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
  </header>
</template>
