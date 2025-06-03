<template>
  <div>
    <div v-if="project" class="flex flex-col gap-6">
      <div class="flex grow flex-col gap-2 rounded-2xl bg-container p-6 dark:bg-containerDark">
        <div class="flex w-full items-center justify-between">
          <h2>{{ project.name }}</h2>
          <div
            @click="isEditProject = true"
            class="w-fit cursor-pointer rounded-full bg-primary p-2 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
          >
            <PencilIcon class="size-6" />
          </div>
        </div>
        <p>{{ project.description }}</p>
        <p>
          <span class="text-sm font-semibold">Team:</span>
          {{ project.team_name }}
        </p>
        <p>
          <span class="text-sm font-semibold">Owner:</span>
          {{ project.project_manager_name }}
        </p>
        <p>
          <span class="text-sm font-semibold">Created by:</span>
          {{ project.created_by_name }}
        </p>
      </div>

      <MyTeam :project="project" />
    </div>
    <div v-else>
      <p>No project details available.</p>
    </div>

    <Modal v-if="isEditProject === true" @close="isEditProject = false" @submit="updateProject">
      <EditProject
        ref="editProjectRef"
        :project-id="project.id"
        @project-updated="onProjectUpdated"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '@/components/base/Modal.vue'
import EditProject from './EditProject.vue'
import MyTeam from './MyTeam.vue'
import { PencilIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
})

const isEditProject = ref(false)
const editProjectRef = ref(null)

function onProjectUpdated() {
  isEditProject.value = false
}

function updateProject() {
  editProjectRef.value.updateProject()
}
</script>
