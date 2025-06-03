<template>
  <div class="">
    <div v-if="loading">Loading tasks...</div>

    <TasksTable
      v-else
      :tasks="tasks"
      :showProjectColumn="false"
      :enableEdit="true"
      :enableNavigation="true"
      @go-to-task="goToTask"
      @edit-task="selectedTaskId = $event"
    />

    <div v-if="!loading && tasks.length === 0">No tasks in this sprint.</div>

    <EditTask
      v-if="selectedTaskId"
      :task-id="selectedTaskId"
      :updated-by="userConfig.username"
      @task-updated="onTaskUpdated"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TasksTable from '@/components/TasksTable.vue'
import EditTask from '../project/EditTask.vue'

const props = defineProps({
  sprintId: {
    type: Number,
    required: true,
  },
})

const tasks = ref([])
const loading = ref(true)
const selectedTaskId = ref(null)

const router = useRouter()

function fetchSprintTasks() {
  axios
    .get(`http://localhost:5000/tasks/sprint/${props.sprintId}`)
    .then((res) => {
      tasks.value = res.data
      loading.value = false
    })
    .catch((err) => {
      console.error('Error loading sprint tasks', err)
      loading.value = false
    })
}

function goToTask(taskId) {
  router.push({ name: 'task-home', query: { id: taskId } })
}

function onTaskUpdated() {
  fetchSprintTasks()
  selectedTaskId.value = null
}

onMounted(() => {
  fetchSprintTasks()
})
</script>
