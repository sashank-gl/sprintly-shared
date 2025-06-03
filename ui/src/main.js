import './main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import VueApexCharts from 'vue3-apexcharts'

import { baseTextInputStyle, baseTextareaStyle } from '@/utils/baseStyles'

const app = createApp(App)

app.config.globalProperties.$baseTextInputStyle = baseTextInputStyle
app.config.globalProperties.$baseTextareaStyle = baseTextareaStyle

app.use(VueApexCharts)

app.use(createPinia())
app.use(router)
app.mount('#app')
