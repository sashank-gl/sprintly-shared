<template>
  <div v-if="task" class="h-auto min-w-96 rounded-2xl bg-container dark:bg-containerDark">
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Edit Task</p>
    </div>

    <form>
      <div class="mb-4">
        <label class="mb-1 block font-medium">Title</label>
        <input
          v-model="task.title"
          type="text"
          class="w-full"
          :class="$baseTextInputStyle"
          required
        />
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Description</label>
        <div
          v-for="(line, index) in task.description"
          :key="index"
          class="flex items-center gap-2 mb-2"
        >
          <input
            v-model="task.description[index]"
            type="text"
            class="w-full"
            :class="$baseTextInputStyle"
            placeholder="Description line"
          />

          <button
            @click="removeDescriptionLine(index)"
            class="group w-fit cursor-pointer rounded-full bg-red-500 p-2 size-8 text-white hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-500"
          >
            <TrashIcon class="size-4" />
          </button>
        </div>

        <button
          @click="addDescriptionLine"
          class="group w-fit cursor-pointer rounded-full bg-primary p-2 size-8 text-white hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark"
        >
          <PlusIcon class="size-4" />
        </button>
      </div>

      <div class="mb-4 flex gap-4">
        <div>
          <label class="mb-1 block font-medium">Priority</label>
          <select v-model="task.priority" class="w-full" :class="$baseTextInputStyle">
            <option>Critical</option>
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="mb-1 block font-medium">Type</label>
          <select v-model="task.type" class="w-full" :class="$baseTextInputStyle">
            <option>Feature</option>
            <option>Bug</option>
            <option>Improvement</option>
          </select>
        </div>

        <div>
          <label class="mb-1 block font-medium">Status</label>
          <select v-model="task.status" class="w-full" :class="$baseTextInputStyle">
            <option>To Do</option>
            <option>In Progress</option>
            <option>Completed</option>
            <option>On Hold</option>
          </select>
        </div>
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Due Date</label>
        <input type="date" v-model="task.due_date" class="w-full" :class="$baseTextInputStyle" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { formatToCalendarDate } from '@/utils/dateUtils'
import { PlusIcon, TrashIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  taskId: Number,
  updatedBy: String,
})

const emit = defineEmits(['task-updated'])

const task = ref(null)

function fetchTask() {
  if (props.taskId) {
    axios.get(`http://localhost:5000/tasks/${props.taskId}`).then((res) => {
      const t = res.data
      t.due_date = formatToCalendarDate(t.due_date)
      if (!Array.isArray(t.description)) t.description = t.description ? [t.description] : []
      task.value = t
    })
  }
}

function updateTask() {
  const payload = {
    title: task.value.title,
    description: task.value.description.filter((line) => line && line.trim() !== ''),
    status: task.value.status,
    priority: task.value.priority,
    type: task.value.type,
    scope: task.value.scope,
    tool: task.value.tool,
    due_date: task.value.due_date,
    updated_by: props.updatedBy,
  }

  axios
    .put(`http://localhost:5000/tasks/${props.taskId}`, payload)
    .then(() => {
      alert('Task updated!')
      emit('task-updated')
    })
    .catch((err) => {
      console.error('Error updating task:', err)
    })
}

function addDescriptionLine() {
  if (!Array.isArray(task.value.description)) task.value.description = []
  task.value.description.push('')
}

function removeDescriptionLine(index) {
  task.value.description.splice(index, 1)
}

onMounted(fetchTask)

watch(
  () => props.taskId,
  (newId, oldId) => {
    if (newId !== oldId) {
      fetchTask()
    }
  },
)

defineExpose({
  updateTask,
})
</script>
