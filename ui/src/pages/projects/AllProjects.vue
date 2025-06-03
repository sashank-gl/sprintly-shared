<template>
  <div class="p-4 mt-6">
    <h2 class="mb-4">All Projects</h2>

    <div
      v-if="isProjectsLoading"
      class="flex h-96 w-full animate-pulse gap-6 rounded-2xl bg-slate-200 dark:bg-slate-800"
    />

    <div
      v-else-if="allProjects.length > 0"
      class="grid grid-cols-1 gap-12 lg:grid-cols-2 xl:grid-cols-4 py-6"
    >
      <div v-for="project in allProjects" :key="project.id">
        <RouterLink :to="{ name: 'project', query: { id: project.id } }">
          <div
            class="rounded-2xl size-64 bg-container p-6 dark:bg-containerDark flex gap-2 flex-col justify-center items-center text-center"
          >
            <h4 class="mb-2">{{ project.name }}</h4>
            <p class="text-xs text-slate-600 dark:text-slate-300">
              {{ project.team_name }}
            </p>
            <p class="text-xs text-slate-600 dark:text-slate-300">
              {{ project.project_manager_name }}
            </p>
            <p class="text-xs text-slate-600 dark:text-slate-300">
              {{ formatDate(project.created_date) }}
            </p>
          </div>
        </RouterLink>
      </div>
    </div>

    <div
      v-else
      class="flex h-full items-center justify-center rounded-2xl bg-container p-6 dark:bg-containerDark"
    >
      No projects found.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { formatDate } from '@/utils/dateUtils'
import { RouterLink } from 'vue-router'

const allProjects = ref([])
const isProjectsLoading = ref(true)

const fetchAllProjects = () => {
  axios
    .get('http://localhost:5000/projects')
    .then((res) => {
      allProjects.value = res.data
      isProjectsLoading.value = false
    })
    .catch((err) => {
      console.error('Error fetching all projects:', err)
      isProjectsLoading.value = false
    })
}

onMounted(() => {
  fetchAllProjects()
})
</script>
