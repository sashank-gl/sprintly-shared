<template>
  <div
    class="h-auto min-w-96 rounded-2xl bg-container dark:border dark:border-slate-600 dark:bg-containerDark"
  >
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Sprint Details</p>
    </div>

    <div v-if="loading">Loading sprint details...</div>

    <div v-else class="space-y-2">
      <p><strong>Name:</strong> {{ sprint.name }}</p>
      <p><strong>Status:</strong> {{ sprint.status }}</p>
      <p><strong>Goal:</strong> {{ sprint.goal }}</p>
      <p>
        <strong>Created On:</strong>
        {{ formatLocalDateOnly(sprint.created_date) }}
      </p>
      <p><strong>Created by:</strong> {{ sprint.created_by }}</p>
      <p><strong>Start:</strong> {{ formatLocalDateOnly(sprint.start_date) }}</p>
      <p><strong>End:</strong> {{ formatLocalDateOnly(sprint.end_date) }}</p>
      <p>
        <strong>Planned Release:</strong>
        {{ formatLocalDateOnly(sprint.planned_release_date) }}
      </p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { formatLocalDateOnly } from '@/utils/dateUtils'
import { onMounted, ref } from 'vue'

const props = defineProps({
  sprintId: {
    type: Number,
    required: true,
  },
})

const sprint = ref({})
const loading = ref(true)

function fetchSprint() {
  axios
    .get(`http://localhost:5000/sprints/${props.sprintId}`)
    .then((res) => {
      sprint.value = res.data
      loading.value = false
    })
    .catch((err) => {
      console.error('Error fetching sprint:', err)
    })
}

onMounted(() => {
  fetchSprint()
})
</script>
