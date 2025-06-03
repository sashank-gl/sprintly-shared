<template>
  <div class="flex items-center justify-between pt-4 px-6">
    <RouterLink to="/">
      <div class="flex items-center gap-1 text-indigo-500">
        <BoltIcon class="size-6" />
        <h4 class="font-normal">Sprintly</h4>
      </div>
    </RouterLink>

    <div class="flex gap-2 items-center">
      <SunIcon
        v-if="!isDark"
        @click="toggleTheme"
        class="h-6 w-6 cursor-pointer text-primary hover:text-orange-500 hover:animate-spin-slow"
      />

      <MoonIcon v-else @click="toggleTheme" class="size-6 cursor-pointer text-primary" />

      <RouterLink to="/profile">
        <div class="hover:bg-primary rounded-full cursor-pointer hover:text-white text-primary p-2">
          <UserIcon class="size-5" />
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { BoltIcon, ChartBarIcon, MoonIcon, SunIcon, UserIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  isDark: Boolean,
})

const emit = defineEmits(['toggle-theme'])

function toggleTheme() {
  emit('toggle-theme')
}
</script>
