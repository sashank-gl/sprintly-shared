<template>
  <div>
    <h2 class="mb-4">Recent Projects</h2>

    <div
      class="w-88 h-88 flex flex-col rounded-2xl bg-container p-6 dark:bg-containerDark overflow-y-auto"
    >
      <div v-if="projects.length > 0" class="flex flex-col gap-6">
        <div
          v-for="project in sortedProjects"
          :key="project.id"
          class="flex items-center justify-center text-center"
        >
          <RouterLink
            :to="{ name: 'project', query: { id: project.id } }"
            class="grow truncate rounded-xl border border-slate-100 p-6 hover:bg-slate-100 dark:border-slate-800 dark:hover:bg-slate-800"
          >
            {{ project.name }}
          </RouterLink>
        </div>
      </div>

      <div v-else class="flex h-full items-center justify-center">No projects found.</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  projects: {
    type: Array,
    required: true,
  },
})

const sortedProjects = computed(() => {
  return [...props.projects].sort(
    (a, b) => new Date(b.last_user_activity) - new Date(a.last_user_activity),
  )
})
</script>
