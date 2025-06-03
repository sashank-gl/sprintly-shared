<template>
  <div class="relative group inline-flex items-center justify-center">
    <div
      :class="[
        'inline-flex h-10 w-10 items-center justify-center rounded-full text-sm font-medium text-white',
        backgroundColor,
      ]"
    >
      {{ initials }}
    </div>
    <p
      v-if="showTooltip"
      class="text-xs absolute whitespace-nowrap left-1/2 -translate-x-1/2 -top-5 z-10 bg-container dark:bg-containerDark border border-slate-200 dark:border-slate-800 rounded-full py-1 px-2 opacity-0 scale-95 group-hover:opacity-100 group-hover:scale-100 transition-all duration-200 shadow-sm"
    >
      {{ name }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  fullName: {
    type: String,
    default: '',
  },
  firstName: {
    type: String,
    default: '',
  },
  lastName: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: null,
  },
  showTooltip: {
    type: Boolean,
    default: true,
  },
})

const name = computed(() => {
  if (props.fullName) return props.fullName.trim()
  return `${props.firstName} ${props.lastName}`.trim()
})

function hashString(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  return Math.abs(hash)
}

const initials = computed(() => {
  const words = name.value.split(' ')
  const chars = words.slice(0, 2).map((word) => word[0]?.toUpperCase() || '')
  return chars.join('')
})

const backgroundColor = computed(() => {
  if (props.color) {
    return `bg-${props.color}-500`
  }

  const colorPalette = [
    'bg-red-500',
    'bg-orange-500',
    'bg-amber-500',
    'bg-green-500',
    'bg-teal-500',
    'bg-cyan-500',
    'bg-blue-500',
    'bg-indigo-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-rose-500',
  ]

  const index = hashString(name.value) % colorPalette.length
  return colorPalette[index]
})
</script>
