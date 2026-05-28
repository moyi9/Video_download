<script setup>
import VideoInfo from './VideoInfo.vue'
import VideoSummary from './VideoSummary.vue'

const props = defineProps({
  video: Object,
  url: String,
})
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6">
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- 左栏：视频信息 -->
      <div class="lg:col-span-2">
        <VideoInfo :video="video" :url="url" />
      </div>

      <!-- 右栏：AI 总结 -->
      <div class="lg:col-span-3">
        <VideoSummary :video="video" :url="url" />
      </div>
    </div>
  </section>
</template>
