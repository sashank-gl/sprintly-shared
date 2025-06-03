<template>
  <div>
    <apexchart
      height="120"
      width="100%"
      type="area"
      :options="splineAreaChartOptions"
      :series="splineAreaChartSeries"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import TasksTable from '@/components/TasksTable.vue'
import VueApexCharts from 'vue3-apexcharts'
import { computed, onMounted, ref } from 'vue'
import { useGlobalStore } from '@/stores/global'
import { useRouter } from 'vue-router'
const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
})
const router = useRouter()
const tasks = ref([])
const loading = ref(true)
const selectedTaskId = ref(null)

const globalStore = useGlobalStore()
const isDark = computed(() => globalStore.darkMode)

const recentCompletedTasks = computed(() => {
  const sevenDaysAgo = new Date()
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)

  return tasks.value.filter((task) => {
    if (task.status === 'Completed' && task.completed_date) {
      const completedDate = new Date(task.completed_date)
      return completedDate >= sevenDaysAgo
    }
    return false
  })
})

const splineAreaChartOptions = computed(() => ({
  chart: {
    type: 'area',
    zoom: {
      enabled: false,
    },
    toolbar: {
      show: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
  },
  tooltip: {
    theme: isDark.value ? 'dark' : 'light',
  },
  xaxis: {
    categories: getLast7Days(),
    labels: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  yaxis: {
    labels: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  grid: {
    show: false,
  },
  colors: ['#22c55e'],
}))

const splineAreaChartSeries = computed(() => [
  {
    name: 'Completed Tasks',
    data: getCompletedTasksByDay(),
  },
])

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

function getLast7Days() {
  const days = []
  let date = new Date()
  let addedDays = 0
  while (addedDays < 5) {
    const day = date.getDay()
    if (day !== 0 && day !== 6) {
      days.unshift(formatDay(new Date(date)))
      addedDays++
    }
    date.setDate(date.getDate() - 1)
  }
  return days
}

function formatDay(date) {
  const options = { weekday: 'short' }
  return new Intl.DateTimeFormat('en-US', options).format(date)
}

function getCompletedTasksByDay() {
  const completedCounts = Array(5).fill(0)

  const last5Weekdays = []
  let date = new Date()
  while (last5Weekdays.length < 5) {
    const day = date.getDay()
    if (day !== 0 && day !== 6) {
      last5Weekdays.unshift(formatDateYYYYMMDD(new Date(date)))
    }
    date.setDate(date.getDate() - 1)
  }

  tasks.value.forEach((task) => {
    if (task.completed_date) {
      const completedDate = formatDateYYYYMMDD(new Date(task.completed_date))
      const dayIndex = last5Weekdays.indexOf(completedDate)
      if (dayIndex !== -1) {
        completedCounts[dayIndex]++
      }
    }
  })

  return completedCounts
}

function formatDateYYYYMMDD(date) {
  return date.toISOString().split('T')[0]
}

onMounted(() => {
  fetchTasks()
})
</script>
