<template>
  <div class="h-auto min-w-96 rounded-2xl bg-container dark:bg-containerDark">
    <div class="flex items-center justify-between">
      <p class="mb-4 font-red-hat text-2xl font-semibold capitalize">Create Project</p>
    </div>

    <div class="flex gap-12">
      <form @submit.prevent="createProject" class="space-y-4 w-[28rem]">
        <div class="flex flex-col space-y-1">
          <label for="name">Name</label>
          <input
            v-model="newProject.name"
            id="name"
            type="text"
            :class="$baseTextInputStyle"
            required
          />
        </div>

        <div class="flex flex-col space-y-1">
          <label>Description</label>
          <textarea
            v-model="newProject.description"
            placeholder="Enter a description or goal of your project"
            :class="$baseTextareaStyle"
            class="h-72"
            required
          ></textarea>
        </div>
      </form>

      <div class="flex flex-col w-80 gap-4">
        <p>Our Team</p>

        <div class="flex gap-4 flex-col">
          <div
            v-for="member in teamMembers"
            :key="member.username"
            class="flex items-center justify-between gap-6"
          >
            <div class="flex gap-4 items-start">
              <Avatar
                :first-name="member.first_name"
                :last-name="member.last_name"
                :show-tooltip="false"
              />

              <div>
                <p>{{ member.first_name }} {{ member.last_name }}</p>
                <p class="text-xs text-slate-800">{{ member.job_title }}</p>
              </div>
            </div>

            <div>
              <button
                v-if="selectedTeamMembers.find((m) => m.username === member.username)"
                @click="removeMember(member.username)"
                class="cursor-pointer rounded-full bg-slate-100 flex justify-center items-center p-2 hover:text-white hover:bg-red-600 dark:bg-red-600 dark:hover:bg-red-500"
              >
                <MinusIcon class="size-4" />
              </button>

              <button
                v-else
                @click="addMember(member.username)"
                class="cursor-pointer rounded-full bg-slate-100 p-2 hover:text-white hover:bg-primary dark:hover:bg-primaryDark"
              >
                <PlusIcon class="size-4" />
              </button>
            </div>
          </div>
        </div>

        <p class="mt-2">Assign a new member</p>

        <div class="flex gap-4 flex-col relative">
          <input
            v-model="externalMember"
            type="text"
            placeholder="Enter username"
            :class="$baseTextInputStyle"
            @input="onExternalInput"
          />
          <div
            v-if="showUserDropdown && filteredUsers?.length"
            class="z-10 absolute bottom-12 bg-container rounded-2xl border-slate-200 border dark:border-slate-800 py-2 w-full"
          >
            <div
              v-for="user in filteredUsers"
              :key="user.username"
              class="px-4 py-2 hover:bg-slate-100 cursor-pointer flex items-center"
              @click="selectExternalUser(user.username)"
            >
              <div class="flex gap-4 items-start">
                <Avatar
                  :first-name="user.first_name"
                  :last-name="user.last_name"
                  :show-tooltip="false"
                />

                <div>
                  <p>{{ user.first_name }} {{ user.last_name }} ({{ user.username }})</p>
                  <p class="text-xs text-slate-800">{{ user.job_title }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <p v-if="selectedExternalMembers?.length" class="mt-2">Other Team Members</p>
        <div v-if="selectedExternalMembers?.length" class="flex gap-4 flex-col">
          <div
            v-for="member in selectedExternalMembers"
            :key="member.username"
            class="flex items-center justify-between gap-6"
          >
            <div class="flex gap-4 items-start">
              <Avatar
                :first-name="member.first_name"
                :last-name="member.last_name"
                :show-tooltip="false"
              />
              
              <div>
                <p>{{ member.first_name }} {{ member.last_name }}</p>
                <p class="text-xs text-slate-800">{{ member.job_title }}</p>
              </div>
            </div>
            <div>
              <button
                v-if="selectedExternalMembers.find((m) => m.username === member.username)"
                @click="removeMember(member.username)"
                class="cursor-pointer bg-slate-100 rounded-full flex justify-center items-center p-2 hover:text-white hover:bg-red-500 dark:hover:bg-red-600"
              >
                <MinusIcon class="size-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { userConfig } from '@/utils/userConfig'
import Avatar from '@/components/base/Avatar.vue'
import { MinusIcon, PlusIcon } from '@heroicons/vue/24/solid'

const emit = defineEmits(['project-created', 'close'])

const newProject = ref({
  name: '',
  description: '',
  created_by: userConfig.username,
  members: [],
})

const teamMembers = ref([])
const allUsers = ref([])
const selectedTeamMembers = ref([])
const selectedExternalMembers = ref([])
const externalMember = ref('')
const showUserDropdown = ref(false)

onMounted(async () => {
  try {
    const [teamRes, allUsersRes] = await Promise.all([
      axios.get(`http://localhost:5000/teams/${userConfig.userTeam}/members`),
      axios.get('http://localhost:5000/users'),
    ])
    teamMembers.value = teamRes.data
    allUsers.value = allUsersRes.data
    selectedTeamMembers.value = [...teamRes.data]
  } catch (error) {
    console.error('Error loading user data:', error)
  }
})

function removeMember(username) {
  selectedTeamMembers.value = selectedTeamMembers.value.filter((u) => u.username !== username)
  selectedExternalMembers.value = selectedExternalMembers.value.filter(
    (u) => u.username !== username,
  )
}

function addMember(username) {
  if (username && allUsers.value.some((u) => u.username === username)) {
    const user = allUsers.value.find((u) => u.username === username)

    if (
      user &&
      !selectedTeamMembers.value.find((u) => u.username === username) &&
      !selectedExternalMembers.value.find((u) => u.username === username)
    ) {
      if (teamMembers.value.find((tm) => tm.username === username)) {
        selectedTeamMembers.value.push(user)
      } else {
        selectedExternalMembers.value.push(user)
      }
    }
  }
}

function onExternalInput() {
  showUserDropdown.value = externalMember.value.length >= 3 && filteredUsers.value.length > 0
}

function selectExternalUser(username) {
  addMember(username)
  externalMember.value = ''
  showUserDropdown.value = false
}

const filteredUsers = computed(() => {
  if (externalMember.value.length < 3) return []
  const search = externalMember.value.toLowerCase()
  return allUsers.value.filter(
    (u) =>
      (u.username.toLowerCase().includes(search) ||
        (u.first_name && u.first_name.toLowerCase().includes(search)) ||
        (u.last_name && u.last_name.toLowerCase().includes(search))) &&
      !selectedTeamMembers.value.find((m) => m.username === u.username) &&
      !selectedExternalMembers.value.find((m) => m.username === u.username),
  )
})

async function createProject() {
  newProject.value.members = [...selectedTeamMembers.value, ...selectedExternalMembers.value].map(
    (m) => m.username,
  )

  try {
    await axios.post('http://localhost:5000/projects', newProject.value)
    emit('project-created')
    emit('close')
  } catch (error) {
    console.error('Failed to create project:', error)
    alert('Error creating project.')
  }
}

defineExpose({ createProject })
</script>
