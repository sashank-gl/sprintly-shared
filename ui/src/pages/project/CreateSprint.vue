<template>
  <div class="h-auto min-w-96 rounded-2xl bg-container dark:bg-containerDark">
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Create Sprint</p>
    </div>

    <form @submit.prevent="createSprint">
      <div class="mb-4">
        <label class="mb-1 block font-medium">Sprint Name</label>
        <input v-model="sprint.name" required class="w-full" :class="$baseTextInputStyle" />
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Goal</label>
        <textarea v-model="sprint.goal" class="h-40 w-full" :class="$baseTextareaStyle" />
      </div>

      <div class="mb-4 flex gap-4">
        <div>
          <label class="mb-1 block font-medium">Start Date</label>
          <input
            type="date"
            v-model="sprint.start_date"
            class="w-full"
            :class="$baseTextInputStyle"
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">End Date</label>
          <input
            type="date"
            v-model="sprint.end_date"
            class="w-full"
            :class="$baseTextInputStyle"
          />
        </div>
        <div>
          <label class="mb-1 block font-medium">Planned Release Date</label>
          <input type="date" v-model="sprint.planned_release_date" :class="$baseTextInputStyle" />
        </div>
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Status</label>
        <select v-model="sprint.status" :class="$baseTextInputStyle">
          <option>Planning</option>
          <option>Active</option>
          <option>Completed</option>
        </select>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  projectId: Number,
  createdBy: String,
})

const emit = defineEmits(['sprint-created'])

const sprint = ref({
  name: '',
  goal: '',
  start_date: '',
  end_date: '',
  planned_release_date: '',
  status: 'Planning',
})

function createSprint() {
  axios
    .post('http://localhost:5000/sprints', {
      ...sprint.value,
      project_id: props.projectId,
      created_by: props.createdBy,
    })
    .then(() => {
      alert('Sprint created!')
      emit('sprint-created')
    })
    .catch((err) => {
      console.error('Error creating sprint:', err)
    })
}

defineExpose({ createSprint })
</script>
