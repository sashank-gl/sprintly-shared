import { defineStore } from 'pinia'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    darkMode: false,
  }),
  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
    },
  },
})
