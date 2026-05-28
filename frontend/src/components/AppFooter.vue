<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="bg-black/80 backdrop-blur-xl border-t border-white/10 mt-auto relative z-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-12">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
        <!-- 品牌 -->
        <div class="lg:col-span-2">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-9 h-9 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="text-xl font-black text-white">VideoDL</span>
          </div>
          <p class="text-sm text-white/40 leading-relaxed max-w-md">
            万能视频下载工具，支持 1800+ 平台，一键解析、多格式选择、AI 智能总结。
          </p>
        </div>

        <!-- 产品 -->
        <div>
          <h4 class="text-white font-bold mb-4">产品</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#features" class="text-white/40 hover:text-white transition-colors">功能介绍</a></li>
            <li><a href="#pricing" class="text-white/40 hover:text-white transition-colors">定价方案</a></li>
            <li><a href="#platforms" class="text-white/40 hover:text-white transition-colors">支持平台</a></li>
            <li><a href="#" class="text-white/40 hover:text-white transition-colors">更新日志</a></li>
          </ul>
        </div>

        <!-- 支持 -->
        <div>
          <h4 class="text-white font-bold mb-4">支持</h4>
          <ul class="space-y-2 text-sm">
            <li><a href="#" class="text-white/40 hover:text-white transition-colors">帮助中心</a></li>
            <li><a href="#" class="text-white/40 hover:text-white transition-colors">联系我们</a></li>
            <li><a href="#" class="text-white/40 hover:text-white transition-colors">反馈建议</a></li>
            <li><a href="#" class="text-white/40 hover:text-white transition-colors">API 文档</a></li>
          </ul>
        </div>
      </div>

      <!-- 分割线 -->
      <div class="border-t border-white/10 pt-8">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p class="text-sm text-white/40">
            &copy; {{ currentYear }} VideoDL. All rights reserved.
          </p>
          <p class="text-xs text-white/30 text-center sm:text-right">
            本工具仅供学习交流使用，请勿用于商业用途。
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>
