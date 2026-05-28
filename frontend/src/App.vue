<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import HeroSection from './components/HeroSection.vue'
import VideoResult from './components/VideoResult.vue'
import FeatureSection from './components/FeatureSection.vue'
import PricingSection from './components/PricingSection.vue'
import PlatformSection from './components/PlatformSection.vue'
import AppFooter from './components/AppFooter.vue'
import { parseVideo } from './api/video'

const videoData = ref(null)
const loading = ref(false)
const error = ref('')
const parsedUrl = ref('')

async function handleParse(url) {
  loading.value = true
  error.value = ''
  videoData.value = null
  parsedUrl.value = url

  try {
    const result = await parseVideo(url)
    if (result.success) {
      videoData.value = result.data
      setTimeout(() => {
        document.getElementById('result-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } else {
      error.value = result.error || '解析失败，请检查链接是否正确'
    }
  } catch (e) {
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <!-- 粒子背景 -->
    <div class="particles"></div>

    <!-- 额外的光效 -->
    <div class="fixed top-1/4 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <AppHeader />

    <main class="flex-1 relative z-10">
      <HeroSection
        :loading="loading"
        :parsed="!!videoData"
        @parse="handleParse"
      />

      <!-- 错误提示 -->
      <transition name="slide">
        <div v-if="error" class="max-w-4xl mx-auto px-4 -mt-4">
          <div class="bg-red-500/10 border border-red-500/30 text-red-400 px-5 py-4 rounded-2xl flex items-center gap-3 backdrop-blur-sm">
            <div class="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center flex-shrink-0">
              <svg class="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span class="text-sm">{{ error }}</span>
          </div>
        </div>
      </transition>

      <!-- 视频结果 -->
      <div id="result-section">
        <transition name="slide">
          <VideoResult
            v-if="videoData"
            :video="videoData"
            :url="parsedUrl"
            class="mt-8"
          />
        </transition>
      </div>

      <!-- 首页内容 -->
      <transition name="fade">
        <div v-if="!videoData && !loading">
          <FeatureSection class="mt-8" />
          <PricingSection />
          <PlatformSection />
        </div>
      </transition>
    </main>

    <AppFooter />
  </div>
</template>
