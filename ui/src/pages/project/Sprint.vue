<template>
  <div :key="sprint.id" class="gap-6 rounded-2xl bg-container p-6 dark:bg-containerDark">
    <div class="flex items-center justify-between gap-6">
      <div class="flex items-center gap-2">
        <div
          @click="isCollapsed = !isCollapsed"
          class="hover:bg-slate-100 cursor-pointer dark:hover:bg-slate-800 p-2 rounded-full"
        >
          <ChevronDownIcon
            class="size-6 transition-transform duration-300"
            :class="{ '-rotate-90': isCollapsed }"
          />
        </div>
        <div class="flex items-start gap-4">
          <div>
            <h3>{{ sprint.name }}</h3>
            <p class="text-sm text-slate-600 dark:text-slate-300">
              {{ formatSprintDateRange(sprint.start_date, sprint.end_date) }}
            </p>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <ButtonPill size="sm" :variant="getStatusVariant(sprint.status)">
          {{ sprint.status }}
        </ButtonPill>
        <div
          @click="editSprint"
          class="group w-fit cursor-pointer rounded-full bg-slate-100 p-2 hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark hover:text-onDarkBackground"
        >
          <PencilIcon class="size-5" />
        </div>
        <div
          @click="viewSprintDetails"
          class="group w-fit cursor-pointer rounded-full bg-slate-100 p-2 hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark hover:text-onDarkBackground"
        >
          <EyeIcon class="size-5" />
        </div>
        <div
          @click="addTask"
          class="group w-fit cursor-pointer rounded-full bg-slate-100 p-2 hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark hover:text-onDarkBackground"
        >
          <PlusIcon class="size-5" />
        </div>
      </div>
    </div>

    <SprintTasks v-if="!isCollapsed" :sprint-id="sprint.id" class="mt-6" />
  </div>
</template>

<script setup>
import { ChevronDownIcon, EyeIcon, PencilIcon, PlusIcon } from '@heroicons/vue/24/solid'
import SprintTasks from './SprintTasks.vue'
import ButtonPill from '@/components/base/ButtonPill.vue'
import { ref } from 'vue'

const props = defineProps({
  sprint: { type: Object, required: true },
  setSprintForTask: { type: Function, required: true },
})

const isCollapsed = ref(false)
const emit = defineEmits(['edit-sprint', 'view-sprint-details'])

function addTask() {
  props.setSprintForTask(props.sprint.id)
}

function editSprint() {
  emit('edit-sprint', props.sprint.id)
}

function viewSprintDetails() {
  emit('view-sprint-details', props.sprint.id)
}

function formatDate(dateStr) {
  const currentYear = new Date().getFullYear()
  const date = new Date(dateStr)
  const month = date.toLocaleString(undefined, { month: 'short' })
  const day = date.getDate()
  let formatted = `${month} ${day}`
  if (date.getFullYear() !== currentYear) {
    const shortYear = `'${String(date.getFullYear()).slice(-2)}`
    formatted += `, ${shortYear}`
  }
  return formatted
}

function getStatusVariant(status) {
  switch (status) {
    case 'Active':
      return 'error'
    case 'Planning':
      return 'info'
    case 'Completed':
      return 'success'
    default:
      return 'info'
  }
}

function formatSprintDateRange(start, end) {
  return `${formatDate(start)} - ${formatDate(end)}`
}
</script>
