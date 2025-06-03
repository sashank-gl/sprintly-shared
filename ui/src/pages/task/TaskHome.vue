<template>
  <div class="pb-40">
    <div v-if="task" class="space-y-6">
      <h2 class="">{{ task.title }}</h2>
      <div class="flex h-80 gap-6">
        <div class="size-80 rounded-2xl bg-container p-6 dark:bg-containerDark">
          <TaskProgressChart
            :start-date="task.created_date"
            :due-date="task.due_date"
            :is-completed="!!task.completed_date"
          />
        </div>

        <div
          class="flex items-start justify-between gap-12 rounded-2xl bg-container p-6 dark:bg-containerDark"
        >
          <div class="flex flex-col gap-6">
            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">Status</p>
              <div
                class="flex w-fit items-center gap-2 rounded-full px-3 py-1 text-xs text-onDarkBackground"
                :class="getStatusClass(task.status)"
              >
                {{ task.status }}
              </div>
            </div>

            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">Priority</p>
              <div
                class="flex w-fit items-center gap-2 rounded-full px-3 py-1 text-xs text-onDarkBackground"
                :class="getPriorityClass(task.priority)"
              >
                {{ task.priority }}
              </div>
            </div>

            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">Owner</p>
              <p>
                {{ task.owner_name }}
              </p>
            </div>

            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">Created On</p>
              <p>
                {{ formatLocalDateOnly(task.created_date) }}
              </p>
            </div>

            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">Due On</p>
              <p>
                {{ formatLocalDateOnly(task.due_date) }}
              </p>
            </div>

            <div class="flex items-center gap-8">
              <p class="mb-1 w-32 text-sm font-semibold">
                {{ task.completed_date ? 'Completed On' : 'Due In' }}
              </p>
              <p>
                {{
                  task.completed_date
                    ? formatLocalDateOnly(task.completed_date)
                    : getDueDateStatus(task.due_date)
                }}
              </p>
            </div>
          </div>

          <div
            @click="selectedTaskId = task.id"
            class="group w-fit cursor-pointer rounded-full bg-primary p-2 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
          >
            <PencilIcon class="size-6" />
          </div>
        </div>

        <div
          class="flex grow flex-col rounded-2xl justify-between bg-container p-6 dark:bg-containerDark"
        >
          <div class="overflow-y-auto">
            <div v-for="(line, index) in editableDescription" :key="index">
              <div v-if="editIndex === index" class="flex gap-4">
                <input
                  v-model="editLine"
                  class="w-full mr-2"
                  :class="$baseTextInputStyle"
                  @keyup.enter="saveEdit(index)"
                />
                <button
                  @click="saveEdit(index)"
                  class="group w-fit cursor-pointer rounded-full bg-primary p-2 size-8 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
                >
                  <PlusIcon class="size-4" />
                </button>
                <button
                  @click="cancelEdit"
                  class="group w-fit cursor-pointer rounded-full bg-red-500 p-2 size-8 text-white hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-500"
                >
                  <XMarkIcon class="size-4" />
                </button>
              </div>
              <div v-else class="flex w-full flex-col gap-2">
                <div class="flex gap-4 group">
                  <span class="p-2 rounded-2xl grow">{{ line }}</span>

                  <div
                    @click="startEdit(index, line)"
                    class="group-hover:visible invisible size-8 cursor-pointer rounded-full bg-primary p-2 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
                  >
                    <PencilIcon class="size-4" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex gap-4 items-center mt-2">
            <input
              v-model="newLine"
              class="w-full mr-2"
              :class="$baseTextInputStyle"
              placeholder="Update Task Progress"
              @keyup.enter="addLine"
            />
            <button
              @click="addLine"
              :disabled="!newLine"
              class="group w-fit cursor-pointer rounded-full bg-primary p-2 size-8 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark disabled:cursor-not-allowed disabled:opacity-50"
            >
              <PlusIcon class="size-4" />
            </button>
            <button
              v-if="newLine"
              @click="cancelAdd"
              class="group w-fit cursor-pointer rounded-full bg-red-500 p-2 size-8 text-white hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-500"
            >
              <XMarkIcon class="size-4" />
            </button>
          </div>
        </div>
      </div>

      <TaskDetails v-if="task" :task="task" />

      <TaskActivity v-if="taskId" :task-id="taskId" />
    </div>

    <Modal
      v-if="selectedTaskId"
      submitButtonText="Update"
      @close="selectedTaskId = null"
      @submit="editTask"
    >
      <EditTask
        ref="editTaskRef"
        :task-id="selectedTaskId"
        :updated-by="task?.created_by"
        @task-updated="onTaskUpdated"
      />
    </Modal>
  </div>
</template>

<script setup>
import axios from 'axios'
import TaskDetails from './TaskDetails.vue'
import TaskActivity from '../task/TaskActivity.vue'
import EditTask from '../project/EditTask.vue'
import Modal from '@/components/base/Modal.vue'
import TaskProgressChart from '@/components/charts/TaskProgressChart.vue'
import { formatLocalDateOnly } from '@/utils/dateUtils'
import { PencilIcon, PlusIcon, XMarkIcon } from '@heroicons/vue/24/solid'
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
const taskId = ref(null)
const task = ref(null)
const selectedTaskId = ref(null)
const activeSection = ref('details')
const editTaskRef = ref(null)
const route = useRoute()

const editableDescription = ref([])
const editIndex = ref(null)
const editLine = ref('')
const newLine = ref('')
const addingLine = ref(false)

function fetchTaskDetails() {
  axios
    .get(`http://localhost:5000/tasks/${taskId.value}`)
    .then((res) => {
      task.value = res.data
      editableDescription.value = Array.isArray(res.data.description)
        ? [...res.data.description]
        : []
    })
    .catch((err) => {
      console.error('Error fetching task details', err)
    })
}

function onTaskUpdated() {
  fetchTaskDetails()
  selectedTaskId.value = null
}

function getStatusClass(status) {
  switch (status) {
    case 'To Do':
      return 'bg-blue-500'
    case 'In Progress':
      return 'bg-orange-500'
    case 'Completed':
      return 'bg-green-500'
    case 'On Hold':
      return 'bg-yellow-500'
    default:
      return ''
  }
}

function getPriorityClass(priority) {
  switch (priority.toLowerCase()) {
    case 'critical':
      return 'bg-[#f87171]'
    case 'high':
      return 'bg-[#fb923c]'
    case 'medium':
      return 'bg-[#facc15]'
    case 'low':
      return 'bg-[#22c55e]'
    default:
      return ''
  }
}

function getDueDateStatus(dueDateStr) {
  const today = new Date()
  const dueDate = new Date(dueDateStr)

  today.setHours(0, 0, 0, 0)
  dueDate.setHours(0, 0, 0, 0)

  const diffTime = dueDate.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays > 0) {
    return `${diffDays} Day${diffDays > 1 ? 's' : ''}`
  } else {
    return `Late by ${Math.abs(diffDays)} Day${Math.abs(diffDays) > 1 ? 's' : ''}`
  }
}

function editTask() {
  editTaskRef.value.updateTask()
}

onMounted(() => {
  taskId.value = parseInt(route.query.id)
  fetchTaskDetails()
})

function startEdit(index, line) {
  editIndex.value = index
  editLine.value = line
}

function saveEdit(index) {
  if (editLine.value.trim() !== '' && editLine.value !== editableDescription.value[index]) {
    editableDescription.value[index] = editLine.value
    updateDescription()
  }
  editIndex.value = null
  editLine.value = ''
}

function cancelEdit() {
  editIndex.value = null
  editLine.value = ''
}

function addLine() {
  if (newLine.value.trim() !== '') {
    editableDescription.value.push(newLine.value)
    updateDescription()
  }
  newLine.value = ''
  addingLine.value = false
}

function cancelAdd() {
  newLine.value = ''
  addingLine.value = false
}

function updateDescription() {
  const filtered = editableDescription.value.filter((line) => line && line.trim() !== '')
  axios
    .put(`http://localhost:5000/tasks/${task.value.id}`, {
      description: filtered,
      updated_by: task.value.created_by,
    })
    .then(() => {
      fetchTaskDetails()
    })
}
</script>
