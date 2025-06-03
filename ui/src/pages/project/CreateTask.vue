<template>
  <div class="h-auto w-[36rem] rounded-2xl bg-container dark:bg-containerDark">
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Create Task</p>
    </div>

    <form @submit.prevent="createTask">
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
        <textarea v-model="task.description" class="w-full" :class="$baseTextInputStyle" rows="3" />
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Assign To</label>
        <select v-model="task.owner_id" class="w-full" :class="$baseTextInputStyle">
          <option v-for="member in projectMembers" :key="member.id" :value="member.id">
            {{ member.first_name }} {{ member.last_name }} ({{ member.username }})
          </option>
        </select>
      </div>

      <div class="mb-4 grid grid-cols-3 gap-4">
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
          <select v-model="task.type" class="w-full" required :class="$baseTextInputStyle">
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
        <label class="mb-1 block font-medium">Scope</label>
        <input v-model="task.scope" class="w-full" :class="$baseTextInputStyle" />
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Tool</label>
        <input v-model="task.tool" class="w-full" :class="$baseTextInputStyle" />
      </div>

      <div class="mb-4">
        <label class="mb-1 block font-medium">Due Date</label>
        <input type="date" v-model="task.due_date" class="w-full" :class="$baseTextInputStyle" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  projectId: Number,
  sprintId: Number,
  createdBy: String,
})

const emit = defineEmits(['task-created'])

const task = reactive({
  title: '',
  description: '',
  status: 'To Do',
  priority: 'Medium',
  type: 'Feature',
  scope: '',
  tool: '',
  due_date: '',
  owner_id: null,
})

const projectMembers = ref([])

function fetchProjectMembers() {
  axios
    .get(`http://localhost:5000/projects/${props.projectId}`)
    .then((res) => {
      projectMembers.value = res.data.members || []
    })
    .catch((err) => {
      console.error('Failed to load project members', err)
    })
}

function createTask() {
  const payload = {
    ...task,
    project_id: props.projectId,
    sprint_id: props.sprintId,
    created_by: props.createdBy,
  }

  axios
    .post('http://localhost:5000/tasks', payload)
    .then(() => {
      alert('Task created!')
      emit('task-created')
    })
    .catch((err) => {
      console.error('Failed to create task', err)
    })

  console.log(payload)
}

onMounted(() => {
  fetchProjectMembers()
})

defineExpose({ createTask })
</script>
