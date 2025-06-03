<template>
  <input
    type="file"
    :accept="accept"
    :multiple="multiple"
    @change="$emit('change', $event)"
    class="file:rounded-full file:text-onDarkBackground"
    :class="fileClasses"
  />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  accept: {
    type: String,
    default: '*/*',
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  variant: {
    type: String,
    default: 'primary',
  },
  size: {
    type: String,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const fileClasses = computed(() => [
  props.size === 'sm' ? 'file:px-2 file:py-1 file:text-sm' : 'file:px-4 file:py-2 file:mr-6',
  props.variant === 'primary'
    ? 'file:bg-button file:hover:bg-buttonHover dark:file:bg-buttonDark dark:file:hover:bg-buttonHoverDark'
    : '',
  props.disabled ? 'file:opacity-50 file:cursor-not-allowed' : 'file:cursor-pointer',
])
</script>

<!-- Sample Usage

<FileUploadButton
  multiple
  color="primary"
  size="md"
  accept="image/png, image/jpeg"
  accept=".zip,.rar"
  accept=".pdf"
  accept="text/csv"
  accept="image/png, image/jpeg, .zip, .rar, .pdf, text/csv"
  @change="handleImageUpload"
/> -->
