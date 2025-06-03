<template>
  <div
    class="fixed inset-0 z-40 flex h-screen w-full items-center justify-center overflow-y-auto bg-slate-900/50 pt-6 dark:bg-slate-800/80"
  >
    <div class="rounded-2xl bg-container p-6 dark:bg-containerDark">
      <slot></slot>

      <div class="mt-6 flex justify-end gap-4">
        <Button @click="$emit('close')" variant="neutral">
          {{ cancelButtonText }}
        </Button>

        <Button v-if="showSubmitButton" @click="$emit('submit')" variant="primary">
          {{ submitButtonText }}
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  cancelButtonText: {
    type: String,
    default: 'Cancel',
  },
  submitButtonText: {
    type: String,
    default: 'Submit',
  },
  showSubmitButton: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['close', 'submit'])

function handleEsc(e) {
  if (e.key === 'Escape') {
    emit('close')
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEsc)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEsc)
})
</script>
