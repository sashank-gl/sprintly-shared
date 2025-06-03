<template>
  <div>
    <h2 class="mb-4">Members in this Project</h2>
    <div v-for="(members, title) in groupedMembers" :key="title" class="mb-6">
      <div class="grid grid-cols-3 gap-6">
        <div
          v-for="member in members"
          :key="member.id"
          class="flex items-start justify-between rounded-2xl bg-container p-6 dark:bg-containerDark"
        >
          <div>
            <h5>{{ member.first_name }} {{ member.last_name }}</h5>
            <p class="text-sm text-slate-500">{{ member.job_title }}</p>
          </div>

          <div v-if="member.role === 'Admin'">
            <p class="rounded-full bg-slate-800 px-2 py-1 text-xs capitalize text-white">
              {{ member.role }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    default: null,
  },
})

const groupedMembers = computed(() => {
  const groups = {}
  if (props.project?.members) {
    props.project.members.forEach((member) => {
      if (!groups[member.job_title]) {
        groups[member.job_title] = []
      }
      groups[member.job_title].push(member)
    })
  }

  const orderedTitles = []
  // const orderedTitles = ['Manager', 'Frontend Developer', 'Backend Developer']
  const sortedGroups = {}

  orderedTitles.forEach((title) => {
    if (groups[title]) {
      sortedGroups[title] = groups[title]
      delete groups[title]
    }
  })

  const remainingTitles = Object.keys(groups).sort()
  remainingTitles.forEach((title) => {
    sortedGroups[title] = groups[title]
  })

  return sortedGroups
})
</script>
