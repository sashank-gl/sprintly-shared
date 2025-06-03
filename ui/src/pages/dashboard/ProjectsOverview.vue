<template>
  <div>
    <div
      v-if="isProjectOverviewLoading"
      style="height: 368px"
      class="flex w-full animate-pulse gap-6"
    >
      <div class="grow rounded-2xl bg-slate-200 dark:bg-slate-800"></div>
      <div class="w-96 rounded-2xl bg-slate-200 dark:bg-slate-800"></div>
    </div>

    <div v-else-if="projectsOverview" class="flex w-full gap-6">

      <div class="grow">
        <h2 class="mb-4">
          Project<span v-if="projects.length > 1 && !selectedProjectId">s</span>
          Overview
        </h2>

        <div class="h-88 flex flex-col gap-6">
          <div
            class="flex items-center justify-between rounded-2xl shadow-xs bg-container p-6 dark:bg-containerDark"
          >
            <div class="flex divide-x-2 divide-slate-100 dark:divide-slate-800">
              <p v-if="projectsOverview.total_projects" class="flex items-center gap-1 pr-6">
                <span class="text-xl font-semibold">
                  {{ projectsOverview.total_projects }}
                </span>
                Projects
              </p>

              <p class="flex items-center gap-1 px-6">
                <span class="text-xl font-semibold">
                  {{ projectsOverview.total_sprints }}
                </span>
                Sprints
              </p>

              <p class="flex items-center gap-1 pl-6">
                <span class="text-xl font-semibold">
                  {{ projectsOverview.total_tasks }}
                </span>
                Tasks
              </p>
            </div>

            <div class="flex items-center gap-6">
              <BaseSelect
                :options="projectOptions"
                v-model="selectedProjectId"
                placeholder="All Projects"
                @update:modelValue="fetchOverview"
                class="w-48 text-nowrap"
              />

              <div
                v-if="userRole === 'Admin'"
                @click="$emit('open-new-project')"
                class="group w-fit cursor-pointer rounded-full bg-primary p-2 text-onDarkBackground hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
              >
                <PlusIcon
                  class="size-6 transition-transform duration-300 ease-in-out group-hover:rotate-90"
                />
              </div>

              <router-link to="/projects">
                <div
                  class="group w-fit cursor-pointer rounded-full bg-primary p-2 text-onDarkBackground hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
                >
                  <ArrowUpRightIcon
                    class="size-6 transition-transform duration-300 ease-in-out group-hover:rotate-45"
                  />
                </div>
              </router-link>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-6">
            <div
              class="col-span-2 flex flex-col rounded-2xl shadow-xs bg-container p-6 dark:bg-containerDark"
            >
              <h3 class="mb-4 text-center">Tasks Status</h3>

              <div
                class="flex items-center justify-center divide-x-2 divide-slate-100 dark:divide-slate-800"
              >
                <div class="flex w-36 flex-col items-center justify-center p-6">
                  <h1 class="text-4xl">
                    {{ projectsOverview.task_status_counts['To Do'] || 0 }}
                  </h1>
                  <div class="flex items-center gap-1">
                    <p>To Do</p>
                  </div>
                </div>

                <div class="flex w-36 flex-col items-center justify-center p-6">
                  <h1 class="text-4xl">
                    {{ projectsOverview.task_status_counts['In Progress'] || 0 }}
                  </h1>
                  <div class="flex items-center gap-1">
                    <p>In Progress</p>
                  </div>
                </div>

                <div class="flex w-36 flex-col items-center justify-center p-6">
                  <h1 class="text-4xl">
                    {{ projectsOverview.task_status_counts['Completed'] || 0 }}
                  </h1>
                  <div class="flex items-center gap-1">
                    <p>Completed</p>
                  </div>
                </div>

                <div class="flex w-36 flex-col items-center justify-center p-6">
                  <h1 class="text-4xl">
                    {{ projectsOverview.task_status_counts['On Hold'] || 0 }}
                  </h1>
                  <div class="flex items-center gap-1">
                    <p>On Hold</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="rounded-2xl shadow-xs bg-container p-6 dark:bg-containerDark">
              <h3 class="mb-4 text-center">Task Priority</h3>
              <TaskPriorityChart :projectsOverview="projectsOverview" />
            </div>
          </div>
        </div>
      </div>

      <RecentProjects :projects="projects" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import TaskPriorityChart from '@/components/charts/TaskPriorityChart.vue'
import RecentProjects from './RecentProjects.vue'
import { userConfig } from '@/utils/userConfig'
import BaseSelect from '@/components/base/BaseSelect.vue'
import { ArrowUpRightIcon, PlusIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  projects: {
    type: Array,
    required: true,
  },
})

const projectsOverview = ref(null)
const isProjectOverviewLoading = ref(true)
const error = ref(null)
const selectedProjectId = ref(null)
const userRole = userConfig.userRole

const projectOptions = computed(() => {
  const options = [{ value: null, label: 'All Projects' }]

  props.projects.forEach((project) => {
    options.push({
      value: project.id,
      label: project.name,
    })
  })

  return options
})

function fetchOverview() {
  console.log('fetching')
  isProjectOverviewLoading.value = true

  if (!selectedProjectId.value) {
    const promises = props.projects.map((project) =>
      axios.get(`http://localhost:5000/projects/${project.id}/overview`),
    )
    Promise.all(promises)
      .then((results) => {
        const merged = {
          total_sprints: 0,
          total_tasks: 0,
          total_projects: 0,
          task_status_counts: {},
          task_priority_counts: {},
        }

        results.forEach((res) => {
          const overview = res.data

          merged.total_sprints += overview.total_sprints
          merged.total_tasks += overview.total_tasks

          for (const [status, count] of Object.entries(overview.task_status_counts)) {
            merged.task_status_counts[status] = (merged.task_status_counts[status] || 0) + count
          }

          for (const [priority, count] of Object.entries(overview.task_priority_counts)) {
            merged.task_priority_counts[priority] =
              (merged.task_priority_counts[priority] || 0) + count
          }
        })

        merged.total_projects = results.length

        projectsOverview.value = merged
        isProjectOverviewLoading.value = false
      })
      .catch((err) => {
        console.error('Error loading all project overviews', err)
        error.value = err
        isProjectOverviewLoading.value = false
      })
  } else {
    axios
      .get(`http://localhost:5000/projects/${selectedProjectId.value}/overview`)
      .then((res) => {
        projectsOverview.value = res.data
        isProjectOverviewLoading.value = false
      })
      .catch((err) => {
        console.error('Error loading project overview', err)
        error.value = err
        isProjectOverviewLoading.value = false
      })
  }
}

onMounted(() => {
  if (props.projects.length > 0) {
    selectedProjectId.value = null
    fetchOverview()
  }
})
</script>
