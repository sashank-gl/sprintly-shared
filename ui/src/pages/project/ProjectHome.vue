<template>
  <div class="space-y-6 pb-40" v-if="projectId !== null">
    <div class="flex gap-6">
      <div class="flex grow flex-col rounded-2xl bg-container p-6 dark:bg-containerDark">
        <div class="flex w-full items-start justify-between">
          <div v-if="project" class="flex grow flex-col">
            <div class="mb-4 flex items-end gap-2">
              <h1>
                {{ project.name }}
              </h1>
              <p class="text-sm italic text-slate-600 dark:text-slate-300">
                last updated {{ formatDate(lastUpdatedTimestamp) }}
              </p>
            </div>

            <p class="text-sm">
              {{ project.team_name }} &nbsp; • &nbsp;
              {{ project.project_manager_name }}
            </p>

            <MyContributionChart :project-id="projectId" />
          </div>

          <div
            @click="isCreateSprint = true"
            class="group w-fit cursor-pointer rounded-full bg-primary p-2 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
          >
            <PlusIcon
              class="size-6 transition-transform duration-300 ease-in-out group-hover:rotate-90"
            />
          </div>
        </div>

        <div
          class="flex items-center gap-6 border-t border-slate-200 pt-4 text-xl dark:border-slate-600"
        >
          <div
            @click="activeSection = 'sprints'"
            :class="[
              'cursor-pointer px-4 py-2',
              activeSection === 'sprints' ? 'rounded-full bg-slate-100  dark:bg-slate-800' : '',
            ]"
          >
            Sprints
          </div>

          <div
            @click="activeSection = 'tasks'"
            :class="[
              'cursor-pointer px-4 py-2',
              activeSection === 'tasks' ? 'rounded-full bg-slate-100  dark:bg-slate-800' : '',
            ]"
          >
            Tasks
          </div>

          <div
            @click="activeSection = 'details'"
            :class="[
              'cursor-pointer px-4 py-2',
              activeSection === 'details' ? 'rounded-full bg-slate-100  dark:bg-slate-800' : '',
            ]"
          >
            Details
          </div>

          <div
            @click="activeSection = 'activity'"
            :class="[
              'cursor-pointer px-4 py-2',
              activeSection === 'activity' ? 'rounded-full bg-slate-100  dark:bg-slate-800' : '',
            ]"
          >
            Activity
          </div>
        </div>
      </div>

      <div class="size-80 rounded-2xl bg-container p-6 dark:bg-containerDark">
        <ProjectOverviewChart v-if="projectOverview" :project-overview="projectOverview" />
      </div>
    </div>
    
    <Modal
      v-if="isCreateSprint === true"
      submitButtonText="Create Sprint"
      @close="isCreateSprint = false"
      @submit="createSprint"
    >
      <CreateSprint
        ref="createSprintRef"
        :project-id="projectId"
        :created-by="userConfig.username"
        @sprint-created="onSprintCreated"
      />
    </Modal>

    <div v-if="activeSection === 'sprints'" class="space-y-6">
      <div v-for="sprint in project?.sprints || []" :key="sprint.id">
        <Sprint
          :sprint="sprint"
          :setSprintForTask="setSprintForTask"
          @edit-sprint="openEditSprint"
          @view-sprint-details="openSprintDetails"
        />
      </div>
    </div>

    <div v-if="activeSection === 'tasks'">
      <ProjectTasks :project-id="projectId" @edit-task="selectedTaskId = $event" />
    </div>

    <div v-if="activeSection === 'details'">
      <ProjectDetails :project="project" />
    </div>

    <div v-if="activeSection === 'activity'">
      <ProjectActivity :activities="activities" />
    </div>

    <Modal
      v-if="isAddTask"
      submitButtonText="Create Task"
      @close="closeCreateTask"
      @submit="createTask"
    >
      <CreateTask
        ref="createTaskRef"
        :project-id="projectId"
        :sprint-id="sprintIdForTask"
        :created-by="userConfig.username"
        @task-created="closeCreateTask"
      />
    </Modal>

    <Modal
      submit-button-text="Update Sprint"
      v-if="sprintIdForEdit"
      @close="sprintIdForEdit = null"
      @submit="updateSprint"
    >
      <EditSprint ref="editSprintRef" :sprint-id="sprintIdForEdit" />
    </Modal>

    <div v-if="sprintIdForDetails">
      <Modal
        @close="sprintIdForDetails = null"
        :showSubmitButton="false"
        cancel-button-text="Go Back"
      >
        <SprintDetails :sprint-id="sprintIdForDetails" />
      </Modal>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRoute } from 'vue-router'
import CreateSprint from './CreateSprint.vue'
import CreateTask from './CreateTask.vue'
import EditProject from './EditProject.vue'
import EditSprint from './EditSprint.vue'
import ProjectActivity from './ProjectActivity.vue'
import ProjectDetails from './ProjectDetails.vue'
import ProjectTasks from './ProjectTasks.vue'
import SprintDetails from './SprintDetails.vue'
import SprintTasks from './SprintTasks.vue'
import Sprint from './Sprint.vue'
import Modal from '@/components/base/Modal.vue'
import ProjectOverviewChart from '@/components/charts/ProjectOverviewChart.vue'
import MyContributionChart from '@/components/charts/MyContributionChart.vue'
import { formatDate } from '@/utils/dateUtils'
import { PlusIcon } from '@heroicons/vue/24/solid'
import { onMounted, ref } from 'vue'
import { userConfig } from '@/utils/userConfig'

const route = useRoute()
const projectId = ref(null)
const selectedTaskId = ref(null)
const activeSection = ref('sprints')
const isProjectDetails = ref(false)
const isProjectActivity = ref(false)
const isSprintTasks = ref(true)
const isProjectTasks = ref(false)
const isCreateSprint = ref(false)
const isAddTask = ref(false)
const project = ref(null)
const loading = ref(true)
const sprintIdForTask = ref(null)
const sprintIdForEdit = ref(null)
const sprintIdForDetails = ref(null)
const activities = ref([])
const lastUpdatedTimestamp = ref(null)
const projectOverview = ref(null)
const createTaskRef = ref(null)
const editSprintRef = ref(null)
const createSprintRef = ref(null)

function fetchProjectDetails() {
  axios
    .get(`http://localhost:5000/projects/${projectId.value}`)
    .then((res) => {
      project.value = res.data
      if (project.value?.sprints?.length) {
        const statusOrder = { Active: 0, Planning: 1, Completed: 2 }

        project.value.sprints.sort((a, b) => {
          const statusDiff = statusOrder[a.status] - statusOrder[b.status]
          if (statusDiff !== 0) return statusDiff

          if (a.status === 'Planning') {
            return new Date(a.start_date) - new Date(b.start_date)
          } else if (a.status === 'Completed') {
            return new Date(b.end_date) - new Date(a.end_date)
          } else {
            return 0
          }
        })
      }
      loading.value = false
    })
    .catch((err) => {
      console.error('Error loading project details', err)
      loading.value = false
    })
}

function fetchProjectOverview() {
  axios
    .get(`http://localhost:5000/projects/${projectId.value}/overview`)
    .then((res) => {
      projectOverview.value = res.data
    })
    .catch((err) => {
      console.error('Error loading project overview', err)
      error.value = err
    })
}

function fetchProjectActivity() {
  axios
    .get(`http://localhost:5000/projects/activity/${projectId.value}`)
    .then((res) => {
      activities.value = res.data
      if (activities.value.length > 0) {
        lastUpdatedTimestamp.value = activities.value[0].timestamp
      }
    })
    .catch((err) => {
      console.error('Failed to load project activity:', err)
    })
}

function setSprintForTask(sprintId) {
  isAddTask.value = true
  sprintIdForTask.value = sprintId
}

function closeCreateTask() {
  isAddTask.value = false
  sprintIdForTask.value = null
}

function createTask() {
  createTaskRef.value.createTask()
}

function openEditSprint(sprintId) {
  sprintIdForEdit.value = sprintId
}

function updateSprint() {
  editSprintRef.value.updateSprint()
  sprintIdForEdit.value = null
}

function openSprintDetails(sprintId) {
  sprintIdForDetails.value = sprintId
}

function handleTimestamp(timestamp) {
  lastUpdatedTimestamp.value = timestamp
}

function createSprint() {
  createSprintRef.value.createSprint()
}

function onSprintCreated() {
  isCreateSprint.value = false
  fetchProjectDetails()
  fetchProjectActivity()
  fetchProjectOverview()
}

onMounted(() => {
  projectId.value = parseInt(route.query.id)

  if (projectId.value !== null) {
    fetchProjectDetails()
    fetchProjectActivity()
    fetchProjectOverview()
  }
})
</script>
