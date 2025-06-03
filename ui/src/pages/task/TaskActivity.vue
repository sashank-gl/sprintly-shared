<template>
  <div>
    <h2 class="mb-4">Task Activity</h2>
    <div class="rounded-2xl bg-container p-6 dark:bg-containerDark">
      <div v-if="activities.length > 0" class="">
        <div
          v-for="activity in activities"
          :key="activity.id"
          class="grid h-16 grid-cols-12 items-center gap-2 border-b p-3 text-center last:border-b-0"
        >
          <div class="col-span-2">
            {{ formatDate(activity.timestamp) }}
          </div>
          <div class="col-span-2">{{ activity.actor_name }}</div>
          <div class="">{{ activity.action }}</div>
          <div class="col-span-2 capitalize">
            {{ formatFieldChanged(activity.field_changed) || 'task' }}
          </div>
          
          <div class="col-span-5 flex items-center gap-2">
            <div
              class="w-56 truncate flex justify-center items-center"
              :class="activity.field_changed?.startsWith('description') ? 'justify-start' : ''"
            >
              <div
                :class="
                  activity.field_changed === 'status'
                    ? getStatusClass(activity.old_value)
                    : activity.field_changed === 'priority'
                      ? getPriorityClass(activity.old_value)
                      : ''
                "
              >
                {{ activity.old_value }}
              </div>
            </div>
            <div v-if="activity.action !== 'created'" class="flex justify-center">
              <ChevronRightIcon class="size-6" />
            </div>
            <div
              class="w-56 truncate flex justify-center items-center"
              :class="activity.field_changed?.startsWith('description') ? 'justify-start' : ''"
            >
              <div
                :class="
                  activity.field_changed === 'status'
                    ? getStatusClass(activity.new_value)
                    : activity.field_changed === 'priority'
                      ? getPriorityClass(activity.new_value)
                      : ''
                "
              >
                {{ activity.new_value }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <p v-else>No activity yet.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { formatDate } from '@/utils/dateUtils'
import { ChevronRightIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  taskId: {
    type: Number,
    required: true,
  },
})

const activities = ref([])

function getStatusClass(status) {
  switch (status) {
    case 'To Do':
      return 'bg-blue-500 px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'In Progress':
      return 'bg-orange-500 px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'Completed':
      return 'bg-green-500 px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'On Hold':
      return 'bg-yellow-500 px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    default:
      return ''
  }
}

function getPriorityClass(priority) {
  if (!priority) return ''
  switch (priority.toLowerCase()) {
    case 'critical':
      return 'bg-[#f87171] px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'high':
      return 'bg-[#fb923c] px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'medium':
      return 'bg-[#facc15] px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    case 'low':
      return 'bg-[#22c55e] px-4 py-2 text-sm w-fit text-onDarkBackground text-center rounded-full'
    default:
      return ''
  }
}

function fetchActivity() {
  axios
    .get(`http://localhost:5000/task/activity/${props.taskId}`)
    .then((res) => {
      activities.value = res.data
    })
    .catch((err) => {
      console.error('Failed to load task activity', err)
    })
}

function formatFieldChanged(field) {
  if (!field) return ''
  const descMatch = field.match(/^description\[(\d+)\]$/)
  if (descMatch) {
    const idx = parseInt(descMatch[1], 10)
    let suffix = 'th'
    if (idx === 0) suffix = 'st'
    else if (idx === 1) suffix = 'nd'
    else if (idx === 2) suffix = 'rd'
    return `Description ${idx + 1}${suffix} line`
  }
  return field
    .split('_')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

onMounted(() => {
  fetchActivity()
})
</script>
