<template>
  <div>
    <apexchart
      :key="isDark"
      height="250"
      type="donut"
      :options="projectOverviewChartOptions"
      :series="projectOverviewChartSeries"
    />
  </div>
</template>

<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useGlobalStore } from '@/stores/global'
import { computed } from 'vue'

const props = defineProps({
  projectOverview: {
    type: Object,
    required: true,
  },
})

const globalStore = useGlobalStore()
const isDark = computed(() => globalStore.darkMode)

const projectOverviewChartOptions = computed(() => ({
  labels: Object.keys(props.projectOverview?.task_status_counts || {}),
  colors: ['#f87171', '#fb923c', '#eab308', '#4ade80'],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 2,
    colors: isDark.value ? '#020617' : '#f8fafc',
  },
  legend: {
    position: 'bottom',
    show: true,
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
            label: 'Total Tasks',
            fontSize: '14px',
            color: isDark.value ? '#f8fafc' : '#020617',
            formatter: () => `${props.projectOverview?.total_tasks}`,
          },
          value: {
            show: true,
            color: isDark.value ? '#f8fafc' : '#020617',
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

const projectOverviewChartSeries = computed(() =>
  Object.values(props.projectOverview?.task_status_counts || {}),
)
</script>
