<template>
  <div class="h-auto min-w-96 rounded-2xl bg-container dark:bg-containerDark">
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Edit Sprint</p>
    </div>

    <form @submit.prevent="updateSprint">
      <div class="mb-4">
        <label class="block font-medium">Name</label>
        <input v-model="sprint.name" class="w-full" :class="$baseTextInputStyle" />
      </div>

      <div class="mb-4">
        <label class="block font-medium">Goal</label>
        <textarea v-model="sprint.goal" class="w-full" :class="$baseTextInputStyle" />
      </div>

      <div class="mb-4">
        <label class="block font-medium">Status</label>
        <select v-model="sprint.status" class="w-full" :class="$baseTextInputStyle">
          <option>Planning</option>
          <option>Active</option>
          <option>Completed</option>
        </select>
      </div>

      <div class="mb-4 flex gap-4">
        <div>
          <label class="block font-medium">Start Date</label>
          <input
            type="date"
            v-model="sprint.start_date"
            class="w-full"
            :class="$baseTextInputStyle"
          />
        </div>
        <div>
          <label class="block font-medium">End Date</label>
          <input
            type="date"
            v-model="sprint.end_date"
            class="w-full"
            :class="$baseTextInputStyle"
          />
        </div>
        <div>
          <label class="block font-medium">Planned Release Date</label>
          <input
            type="date"
            v-model="sprint.planned_release_date"
            class="w-full"
            :class="$baseTextInputStyle"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { formatToCalendarDate } from '@/utils/dateUtils'
import { userConfig } from '@/utils/userConfig'

const props = defineProps({
  sprintId: Number,
})

const sprint = ref({})

function fetchSprint() {
  axios
    .get(`http://localhost:5000/sprints/${props.sprintId}`)
    .then((res) => {
      const data = res.data
      data.start_date = formatToCalendarDate(data.start_date)
      data.end_date = formatToCalendarDate(data.end_date)
      data.planned_release_date = formatToCalendarDate(data.planned_release_date)
      sprint.value = data
    })
    .catch((err) => {
      console.error('Error loading sprint', err)
    })
}

function updateSprint() {
  axios
    .put(`http://localhost:5000/sprints/${props.sprintId}`, {
      ...sprint.value,
      updated_by: userConfig.username,
    })
    .then(() => alert('Sprint updated!'))
    .catch((err) => {
      console.error('Error updating sprint', err)
    })
}

onMounted(fetchSprint)

defineExpose({ updateSprint })
</script>
