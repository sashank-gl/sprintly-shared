<script setup>
import Navbar from '@/components/layout/Navbar.vue'
import { computed } from 'vue'
import { useGlobalStore } from '@/stores/global'

const globalStore = useGlobalStore()

const isDark = computed(() => globalStore.darkMode)

function toggleDarkMode() {
  globalStore.toggleDarkMode()
}
</script>

<template>
  <div
    :class="{ dark: isDark }"
    class="bg-background font-inter min-h-screen dark:bg-darkBackground text-onBackground dark:text-onDarkBackground"
  >
    <Navbar :is-dark="isDark" @toggle-theme="toggleDarkMode" />
    <RouterView class="p-6" />
  </div>
</template>
