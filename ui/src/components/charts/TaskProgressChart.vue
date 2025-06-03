<template>
  <div>
    <apexchart
      :key="isDark"
      height="270"
      type="donut"
      :options="taskProgressChartOptions"
      :series="taskProgressChartSeries"
    />
  </div>
</template>

<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useGlobalStore } from '@/stores/global'
import { computed } from 'vue'

const props = defineProps({
  startDate: {
    type: String,
  },
  dueDate: {
    type: String,
    required: true,
  },
  currentDate: {
    type: String,
    default: () => new Date().toISOString().split('T')[0],
  },
  isCompleted: {
    type: Boolean,
    default: false,
  },
})

const globalStore = useGlobalStore()
const isDark = computed(() => globalStore.darkMode)

const isOverdue = computed(() => {
  const current = new Date(props.currentDate)
  const due = new Date(props.dueDate)
  return !props.isCompleted && current > due
})

const overdueDays = computed(() => {
  if (!isOverdue.value) return 0
  const current = new Date(props.currentDate)
  const due = new Date(props.dueDate)
  return Math.ceil((current - due) / (1000 * 60 * 60 * 24))
})

const taskProgressChartOptions = computed(() => ({
  labels: isOverdue.value ? ['Overdue', ''] : ['Elapsed', 'Remaining'],
  colors: isOverdue.value
    ? ['#ef4444', isDark.value ? '#0f172a' : '#ffffff']
    : ['#4ade80', '#f97316'],
  dataLabels: {
    enabled: false,
    formatter: (val) => `${Math.round(val)}%`,
    style: {
      colors: [isDark.value ? '#f8fafc' : '#020617'],
    },
  },
  stroke: {
    show: true,
    width: 2,
    colors: [isDark.value ? '#0f172a' : '#ffffff'],
  },
  legend: {
    position: 'bottom',
    labels: {
      colors: isDark.value ? '#f8fafc' : '#020617',
    },
    markers: {
      strokeWidth: 0,
      offsetX: -2,
    },
  },
  plotOptions: {
    pie: {
      donut: {
        labels: {
          show: true,
          total: {
            show: true,
            label: 'Progress',
            fontSize: '14px',
            color: isDark.value ? '#f8fafc' : '#020617',
            formatter: () => {
              return isOverdue.value
                ? `${overdueDays.value}d Overdue`
                : `${taskProgressChartSeries.value[0]}%`
            },
          },
          value: {
            show: true,
            color: isDark.value ? '#f8fafc' : '#020617',
            formatter: function (val) {
              return `${Math.round(val)}%`
            },
          },
        },
      },
    },
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        chart: { width: 200 },
        legend: { position: 'bottom' },
      },
    },
  ],
}))

const taskProgressChartSeries = computed(() => {
  if (isOverdue.value) {
    return [100, 0]
  }

  const start = new Date(props.startDate)
  const due = new Date(props.dueDate)
  const current = new Date(props.currentDate)
  const total = (due - start) / (1000 * 60 * 60 * 24)
  const elapsed = Math.min(Math.max((current - start) / (1000 * 60 * 60 * 24), 0), total)

  const progress = Math.round((elapsed / total) * 100)
  return [progress, 100 - progress]
})
</script>
