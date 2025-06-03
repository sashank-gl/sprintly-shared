<template>
  <button
    class="rounded-full text-onDarkBackground"
    :class="buttonClasses"
    @click.stop="emit('click')"
    :disabled="disabled"
  >
    <slot>Click</slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: String,
  variant: {
    type: String,
    default: 'primary',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

function handleClick(event) {
  event.stopPropagation()
  emit('click')
}

const buttonClasses = computed(() => [
  props.size === 'sm' ? 'px-2 py-1 text-sm' : 'px-4 py-2',
  props.variant === 'primary'
    ? 'bg-button hover:bg-buttonHover dark:bg-buttonDark dark:hover:bg-buttonHoverDark'
    : '',
  props.variant === 'neutral'
    ? 'bg-slate-200 hover:bg-slate-300 text-slate-500 hover:text-slate-800 dark:bg-slate-800 dark:text-slate-300 dark:hover:text-slate-200 dark:hover:bg-slate-700'
    : '',
  props.variant === 'error' ? 'bg-red-500 hover:bg-red-600' : '',
  props.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
])
</script>
