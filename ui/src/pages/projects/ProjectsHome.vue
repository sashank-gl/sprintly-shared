<template>
  <div>
    <TeamProjects :team-name="userTeam" />
    <AllProjects v-if="userRole === 'Admin'" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AllProjects from './AllProjects.vue'
import TeamProjects from './TeamProjects.vue'
import { userConfig } from '@/utils/userConfig'

const userRole = ref(userConfig.userRole)
const userTeam = ref(userConfig.userTeam)
</script>
