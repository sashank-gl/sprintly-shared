<template>
  <div>
    <div class="flex items-center justify-center">
      <apexchart
        :key="isDark"
        height="138"
        type="pie"
        :options="priorityChartOptions"
        :series="priorityChartSeries"
      />
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useGlobalStore } from '@/stores/global'
import { computed } from 'vue'

const props = defineProps({
  projectsOverview: {
    type: Object,
    required: true,
  },
})

const globalStore = useGlobalStore()
const isDark = computed(() => globalStore.darkMode)

const priorityChartOptions = computed(() => ({
  labels: Object.keys(props.projectsOverview?.task_priority_counts || {}),
  colors: ['#f87171', '#fb923c', '#facc15', '#22c55e'],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: isDark.value ? '#020617' : '#f8fafc',
  },
  chart: {
    offsetX: -20,
  },
  legend: {
    position: 'right',
    offsetY: 5,
    offsetX: -10,
    show: true,
    labels: {
      colors: isDark.value ? '#f8fafc' : '#020617',
    },
    markers: {
      strokeWidth: 0,
      offsetX: -2,
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

const priorityChartSeries = computed(() =>
  Object.values(props.projectsOverview?.task_priority_counts || {}),
)
</script>
