<template>
  <button class="rounded-full text-xs text-white" :class="buttonClasses">
    <slot></slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'info',
  },
  size: {
    type: String,
  },
})

const buttonClasses = computed(() => [
  props.variant === 'success' ? 'bg-green-500 ' : '',
  props.variant === 'info' ? 'bg-blue-500 ' : '',
  props.variant === 'warning' ? 'bg-yellow-500 ' : '',
  props.variant === 'error' ? 'bg-red-500 ' : '',
  props.size === 'sm' ? 'px-2 py-1' : 'px-4 py-2',
])
</script>
