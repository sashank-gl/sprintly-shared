<template>
  <div class="flex justify-center p-6 w-full">
    <div
      class="relative flex flex-col rounded-2xl w-1/2 bg-container p-12 dark:bg-containerDark gap-4 items-center"
    >
      <img
        v-if="user.avatar_url"
        :src="`http://localhost:5000${user.avatar_url}`"
        alt="User Avatar"
        class="size-36 object-cover rounded-full"
      />

      <div v-else>
        <div
          @click="setAvatar = true"
          class="size-36 cursor-pointer flex justify-center items-center bg-slate-100 rounded-full"
        >
          <CameraIcon class="size-10 text-primary dark:text-primaryDark" />
        </div>
      </div>

      <div class="flex text-center flex-col gap-2">
        <h1 class="mb-2">{{ user.first_name }} {{ user.last_name }}</h1>
        <h4 class="text-slate-600">{{ user.job_title }}</h4>
        <h4 class="text-slate-600">{{ user.email }}</h4>
        <h4 class="text-slate-600">{{ user.team }} Team</h4>
      </div>

      <div
        @click="setAvatar = !setAvatar"
        class="absolute right-6 top-6 w-fit cursor-pointer rounded-full bg-slate-100 p-2 hover:bg-buttonHover dark:bg-primaryDark dark:hover:bg-buttonHoverDark hover:text-onDarkBackground"
      >
        <PencilIcon v-if="setAvatar === false" class="size-5" />
        <XMarkIcon v-else class="size-5" />
      </div>
      <div v-if="setAvatar" class="flex flex-col items-center gap-6">
        <FileUploadButton ref="fileInputRef" @change="onFileChange" />
        <Button v-if="selectedFile" @click="uploadAvatar">Upload Avatar</Button>
        <Button v-if="user.avatar_url" variant="error" @click="removeAvatar">Remove Avatar</Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import Avatar from '@/components/base/Avatar.vue'
import Button from '@/components/base/Button.vue'
import FileUploadButton from '@/components/base/FileUploadButton.vue'
import { CameraIcon, PencilIcon, XMarkIcon } from '@heroicons/vue/24/solid'

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update-avatar'])

const selectedFile = ref(null)
const fileInputRef = ref(null)
const setAvatar = ref(false)
function onFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function uploadAvatar() {
  if (!selectedFile.value) return
  const formData = new FormData()
  formData.append('avatar', selectedFile.value)
  try {
    await axios.put(`http://localhost:5000/users/${props.user.id}/avatar`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    selectedFile.value = null
    if (fileInputRef.value) {
      fileInputRef.value.$el.value = ''
    }
    emit('update-avatar')
    setAvatar.value = false
  } catch (err) {
    console.error('Upload error:', err)
    console.log('Axios error response:', err.response)
    alert(err.response?.data?.message || 'Upload failed')
  }
}

async function removeAvatar() {
  try {
    await axios.delete(`http://localhost:5000/users/${props.user.id}/avatar`)
    selectedFile.value = null
    emit('update-avatar')
  } catch (err) {
    console.error('Remove error:', err)
    alert(err.response?.data?.message || 'Failed to remove avatar')
  }
}
</script>
