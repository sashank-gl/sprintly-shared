<template>
  <div>
    <div class="mb-4 flex justify-between items-center">
      <div>
        <div class="relative w-96">
          <input
            type="text"
            class="w-full"
            :class="$baseTextInputStyle"
            v-model="searchQuery"
            placeholder="Search"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
          >
            &times;
          </button>
        </div>
      </div>
      <div class="invisible relative column-filter">
        <button
          @click="columnFilterOpen = !columnFilterOpen"
          class="ml-4 rounded bg-gray-200 px-3 py-1.5 text-sm dark:bg-slate-700"
        >
          Columns
        </button>
        <div
          v-if="columnFilterOpen"
          class="absolute right-0 mt-2 w-48 rounded-md border bg-white p-2 shadow-md dark:bg-slate-800 dark:border-slate-700"
        >
          <div class="mb-2">
            <label class="flex items-center">
              <input type="checkbox" @change="(e) => toggleAllColumns(e.target.checked)" />
              <span class="ml-2 text-sm">Select All</span>
            </label>
          </div>
          <div v-for="col in allColumns" :key="col.key">
            <template v-if="col && col.condition">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  :checked="visibleColumns.includes(col.key)"
                  @change="() => toggleColumn(col.key)"
                />
                <span class="ml-2 text-sm">{{ col.label }}</span>
              </label>
            </template>
          </div>
        </div>
      </div>
    </div>
    <div class="overflow-hidden rounded-2xl border border-slate-100 dark:border-slate-800">
      <table v-if="tasks.length" class="min-w-full table-auto border-collapse text-left">
        <thead class="bg-background dark:bg-slate-800">
          <tr>
            <th v-if="visibleColumns.includes('project_name')" class="px-4 py-3">Project</th>
            <th v-if="visibleColumns.includes('task_id')" class="px-4 py-3">Task ID</th>
            <th v-if="visibleColumns.includes('title')" class="px-4 py-3">Title</th>
            <th v-if="visibleColumns.includes('status')" class="px-4 py-3">Status</th>
            <th v-if="visibleColumns.includes('priority')" class="px-4 py-3">Priority</th>
            <th v-if="visibleColumns.includes('type')" class="px-4 py-3">Type</th>
            <th v-if="visibleColumns.includes('due_date')" class="px-4 py-3">Due Date</th>
            <th v-if="visibleColumns.includes('created_date')" class="px-4 py-3">Created Date</th>
            <th v-if="visibleColumns.includes('completed_date')" class="px-4 py-3">
              Completed Date
            </th>
          </tr>
        </thead>

        <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
          <tr
            v-for="task in paginatedTasks"
            :key="task.id"
            class="hover:bg-slate-50 dark:hover:bg-slate-800"
          >
            <td v-if="visibleColumns.includes('project_name')" class="px-4 py-3">
              {{ task.project_name }}
            </td>
            <td
              v-if="visibleColumns.includes('task_id')"
              class="cursor-pointer px-4 py-3"
              @click="handleRowClick(task.id)"
            >
              {{ task.task_id }}
            </td>
            <td
              v-if="visibleColumns.includes('title')"
              class="cursor-pointer px-4 py-3"
              @click="handleRowClick(task.id)"
            >
              {{ task.title }}
            </td>
            <td
              v-if="visibleColumns.includes('status')"
              class="px-4 py-3 text-center text-onDarkBackground"
            >
              <div
                class="rounded-full px-2 py-0.5 w-fit text-sm"
                :class="getStatusClass(task.status)"
              >
                {{ task.status }}
              </div>
            </td>
            <td
              v-if="visibleColumns.includes('priority')"
              class="px-4 py-3 text-center text-onDarkBackground"
            >
              <div
                class="rounded-full px-2 py-0.5 w-fit text-sm"
                :class="getPriorityClass(task.priority)"
              >
                {{ task.priority }}
              </div>
            </td>
            <td v-if="visibleColumns.includes('type')" class="px-4 py-3">{{ task.type }}</td>
            <td v-if="visibleColumns.includes('due_date')" class="px-4 py-3">
              {{ task.due_date ? formatLocalDateOnly(task.due_date) : '-' }}
            </td>
            <td v-if="visibleColumns.includes('created_date')" class="px-4 py-3">
              {{ formatLocalDateOnly(task.created_date) }}
            </td>
            <td v-if="visibleColumns.includes('completed_date')" class="px-4 py-3">
              {{ task.completed_date ? formatLocalDateOnly(task.completed_date) : '-' }}
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="filteredTasks.length === 0" class="p-4 text-center text-slate-500">
        No matching tasks found.
      </div>
    </div>

    <div v-if="!tasks.length" class="p-4 text-center text-slate-500">No tasks available.</div>

    <div class="mt-4 flex items-center justify-between text-sm text-slate-600 dark:text-slate-300">
      <div>
        Showing {{ paginatedTasks.length }} of {{ filteredTasks.length }} task<span
          v-if="filteredTasks.length !== 1"
          >s</span
        >
      </div>
      <div class="flex items-center gap-2">
        <select v-model="rowsPerPage" class="rounded border px-2 py-1 dark:bg-slate-700">
          <option :value="10">10</option>
          <option :value="25">25</option>
          <option :value="50">50</option>
        </select>
        <button @click="prevPage" :disabled="currentPage === 1" class="px-2">&#x276E;</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages" class="px-2">
          &#x276F;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatLocalDateOnly } from '@/utils/dateUtils'
import { defineProps, defineEmits, ref, computed, onMounted } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    required: true,
  },
  showProjectColumn: {
    type: Boolean,
    default: false,
  },
  enableNavigation: {
    type: Boolean,
    default: false,
  },
})

const searchQuery = ref('')
const visibleColumns = ref([
  ...(props.showProjectColumn ? ['project_name'] : []),
  'task_id',
  'title',
  'status',
  'priority',
  'type',
  'due_date',
  'created_date',
  'completed_date',
])
const rowsPerPage = ref(10)
const currentPage = ref(1)
const columnFilterOpen = ref(false)

const allColumns = computed(() => [
  { key: 'project_name', label: 'Project', condition: props.showProjectColumn },
  { key: 'task_id', label: 'Task ID', condition: true },
  { key: 'title', label: 'Title', condition: true },
  { key: 'status', label: 'Status', condition: true },
  { key: 'priority', label: 'Priority', condition: true },
  { key: 'type', label: 'Type', condition: true },
  { key: 'due_date', label: 'Due Date', condition: true },
  { key: 'created_date', label: 'Created Date', condition: true },
  { key: 'completed_date', label: 'Completed Date', condition: true },
])

const filteredTasks = computed(() => {
  if (searchQuery.value.length < 3) return props.tasks
  const lowerQuery = searchQuery.value.toLowerCase()
  return props.tasks.filter((task) =>
    Object.entries(task).some(
      ([key, value]) => typeof value === 'string' && value.toLowerCase().includes(lowerQuery),
    ),
  )
})

const totalPages = computed(() => Math.ceil(filteredTasks.value.length / rowsPerPage.value))
const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value
  return filteredTasks.value.slice(start, start + rowsPerPage.value)
})

function toggleColumn(key) {
  if (visibleColumns.value.includes(key)) {
    visibleColumns.value = visibleColumns.value.filter((c) => c !== key)
  } else {
    visibleColumns.value.push(key)
  }
}

function toggleAllColumns(selectAll) {
  if (selectAll) {
    visibleColumns.value = allColumns.value.filter((col) => col.condition).map((col) => col.key)
  } else {
    visibleColumns.value = []
  }
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}

function handleClickOutside(e) {
  if (!e.target.closest('.column-filter')) {
    columnFilterOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

const emit = defineEmits(['go-to-task'])

function handleRowClick(taskId) {
  if (props.enableNavigation) {
    emit('go-to-task', taskId)
  }
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
</script>
