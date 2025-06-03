<template>
  <div class="flex flex-col gap-6 rounded-2xl bg-container p-6 dark:bg-containerDark">
    <div class="grid grid-cols-4 gap-4">
      <div>
        <p class="mb-1 text-sm font-semibold">Type</p>
        <p>
          {{ task.type }}
        </p>
      </div>

      <div>
        <p class="mb-1 text-sm font-semibold">Scope</p>
        <p>
          {{ task.scope }}
        </p>
      </div>

      <div>
        <p class="mb-1 text-sm font-semibold">Tool</p>
        <p>
          {{ task.tool }}
        </p>
      </div>
    </div>

    <div class="grid grid-cols-4 gap-4">
      <div>
        <p class="mb-1 text-sm font-semibold">Task ID</p>
        <p>
          {{ task.task_id }}
        </p>
      </div>

      <div>
        <p class="mb-1 text-sm font-semibold">Sprint</p>
        <p>
          {{ task.sprint_name }}
        </p>
      </div>

      <div>
        <p class="mb-1 text-sm font-semibold">Project</p>
        <p>
          {{ task.project_name }}
        </p>
      </div>

      <div>
        <p class="mb-1 text-sm font-semibold">Created By</p>
        <p>
          {{ task.created_by_name }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
})

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
