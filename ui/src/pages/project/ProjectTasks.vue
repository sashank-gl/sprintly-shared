<template>
  <div class="rounded-2xl bg-container p-4 dark:bg-containerDark">
    <div v-if="loading">Loading tasks...</div>

    <div v-else-if="tasks.length > 0">
      <TasksTable
        :tasks="tasks"
        :showProjectColumn="false"
        :enableEdit="true"
        :enableNavigation="true"
        @go-to-task="goToTask"
        @edit-task="selectedTaskId = $event"
      />
    </div>

    <div v-else>No tasks found for this project.</div>

    <EditTask
      v-if="selectedTaskId"
      :task-id="selectedTaskId"
      :updated-by="userConfig.username"
      @task-updated="onTaskUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import EditTask from './EditTask.vue'
import TasksTable from '@/components/TasksTable.vue'
import { userConfig } from '@/utils/userConfig'

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
})

const tasks = ref([])
const loading = ref(true)
const selectedTaskId = ref(null)
const router = useRouter()

function fetchTasks() {
  axios
    .get(`http://localhost:5000/tasks/project/${props.projectId}`)
    .then((response) => {
      tasks.value = response.data
      loading.value = false
    })
    .catch((error) => {
      console.error('Failed to load tasks:', error)
      loading.value = false
    })
}

function goToTask(taskId) {
  router.push({ name: 'task-home', query: { id: taskId } })
}

function onTaskUpdated() {
  fetchTasks()
  selectedTaskId.value = null
}

onMounted(() => {
  fetchTasks()
})
</script>
