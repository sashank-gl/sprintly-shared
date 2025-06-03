<template>
  <div v-if="user">
    <div class="flex gap-6">
      <UserDetails :user="user" @update-avatar="fetchUser" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { userConfig } from '@/utils/userConfig'
import axios from 'axios'
import UserDetails from './UserDetails.vue'

const user = ref(null)

async function fetchUser() {
  try {
    const response = await axios.get(`http://localhost:5000/users/${userConfig.userId}`)
    user.value = response.data
  } catch (error) {
    console.error('Failed to fetch user: ', error)
  }
}

onMounted(fetchUser)
</script>
