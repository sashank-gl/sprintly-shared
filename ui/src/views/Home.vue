<template>
  <div class="pb-20">
    <div v-if="isProjectsLoaded">
      <div class="flex flex-col gap-6">
        <ProjectsOverview :projects="projects" @open-new-project="() => (isCreateProject = true)" />
        <MyTasks />
      </div>
    </div>

    <div v-else>
      <div
        v-if="userRole === 'Admin'"
        class="flex h-96 flex-col items-center justify-center gap-4 rounded-2xl bg-container dark:bg-containerDark"
      >
        <div
          @click="isCreateProject = true"
          class="group cursor-pointer rounded-full bg-blue-500 p-2 text-white"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="size-12 transition-transform duration-700 ease-in-out group-hover:rotate-180"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
        </div>

        <p class="text-xl">Create a New Project</p>
      </div>

      <div
        v-else
        class="flex h-96 flex-col items-center justify-center rounded-2xl bg-container dark:bg-containerDark"
      >
        <p class="text-2xl">You're not a part of any project at the moment.</p>
      </div>
    </div>

    <Modal
      v-if="isCreateProject"
      submitButtonText="Create"
      @close="isCreateProject = false"
      @submit="submitProject"
    >
      <CreateProject ref="CreateProjectRef" @project-created="onProjectCreated" />
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

import MyTasks from '@/pages/dashboard/MyTasks.vue'
import Projects from '@/pages/dashboard/RecentProjects.vue'
import ProjectsOverview from '@/pages/dashboard/ProjectsOverview.vue'
import Modal from '@/components/base/Modal.vue'
import CreateProject from '@/pages/task//CreateProject.vue'
import { userConfig } from '@/utils/userConfig'

const projects = ref([])

const isCreateProject = ref(false)
const isProjectsLoaded = ref(false)
const username = userConfig.username
const userRole = userConfig.userRole

const route = useRoute()

const CreateProjectRef = ref(null)

function fetchUserProjects() {
  axios
    .get(`http://localhost:5000/projects/user/${username}`)
    .then((response) => {
      projects.value = response.data
      isProjectsLoaded.value = Array.isArray(response.data) && response.data.length > 0
    })
    .catch((error) => {
      console.error('There was an error fetching the projects:', error)
    })
}

function onProjectCreated() {
  fetchUserProjects()
  isCreateProject.value = false
}

function submitProject() {
  if (CreateProjectRef.value) {
    CreateProjectRef.value.createProject()
  }
}

onMounted(() => {
  fetchUserProjects()
})
</script>
