<template>
  <div>
    <h2 class="mb-4">My Tasks</h2>

    <div class="rounded-2xl bg-container p-6 dark:bg-containerDark">
      <div
        v-if="isTasksLoading"
        class="flex h-96 w-full animate-pulse gap-6 rounded-2xl bg-slate-200 dark:bg-slate-800"
      />

      <div v-else-if="tasks.length > 0">
        <TasksTable
          :tasks="tasks"
          :showProjectColumn="isMultipleProjects"
          :enableNavigation="true"
          @go-to-task="goToTask"
        />
      </div>

      <div v-else class="flex h-full items-center justify-center">No tasks assigned to you.</div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import TasksTable from '@/components/TasksTable.vue'
import { userConfig } from '@/utils/userConfig'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const tasks = ref([])
const isTasksLoading = ref(true)
const username = userConfig.username
const selectedTaskId = ref(null)

const isMultipleProjects = computed(() => {
  const uniqueProjects = new Set(tasks.value.map((task) => task.project_name))
  return uniqueProjects.size > 1
})

function fetchMyTasks() {
  axios
    .get(`http://localhost:5000/users/${username}/tasks`)
    .then((res) => {
      tasks.value = res.data
      isTasksLoading.value = false
    })
    .catch((err) => {
      console.error('Failed to fetch tasks', err)
      isTasksLoading.value = false
    })
}

function goToTask(taskId) {
  router.push({ name: 'task-home', query: { id: taskId } })
}

onMounted(() => {
  fetchMyTasks()
})
</script>
