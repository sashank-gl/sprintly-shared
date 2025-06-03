<template>
  <div class="relative" ref="dropdownEl">
    <button
      @click="toggleDropdown"
      class="flex w-full items-center justify-between gap-4 rounded-lg border border-slate-200 bg-container px-2 py-2 placeholder:text-slate-400 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary dark:border-slate-600 dark:bg-containerDark dark:focus:ring-slate-400"
    >
      <span>{{ selectedLabel }}</span>

      <ChevronDownIcon
        class="size-5 transition-transform duration-300 ease-in-out"
        :class="isDropdownOpen ? 'rotate-180' : ''"
      />
    </button>

    <div
      v-if="isDropdownOpen"
      class="absolute z-10 mt-1 w-full overflow-hidden rounded-lg border border-slate-200 bg-container dark:border-slate-600 dark:bg-containerDark"
    >
      <div
        v-for="option in props.options"
        :key="option.value"
        @click="selectOption(option)"
        class="cursor-pointer px-2 py-2 hover:bg-slate-100 dark:hover:bg-slate-700"
      >
        {{ option.label }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ChevronDownIcon } from '@heroicons/vue/24/solid'
import { ref, computed, defineProps, defineEmits, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: null,
  options: {
    type: Array,
    required: true,
  },
  placeholder: {
    type: String,
    default: 'Select An Option',
  },
})

const emit = defineEmits(['update:modelValue'])

const isDropdownOpen = ref(false)
const dropdownEl = ref(null)

const selectedLabel = computed(() => {
  const selected = props.options.find((option) => option.value === props.modelValue)
  return selected ? selected.label : props.placeholder
})

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function closeDropdown() {
  isDropdownOpen.value = false
}

function selectOption(option) {
  emit('update:modelValue', option.value)
  closeDropdown()
}

function handleClickOutside(event) {
  if (dropdownEl.value && !dropdownEl.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.body.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.body.removeEventListener('click', handleClickOutside)
})
</script>
