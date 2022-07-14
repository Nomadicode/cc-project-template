import { createApp } from 'vue'
import App from './App.vue'
import VueAxios from 'vue-axios'
import mitt from 'mitt'

{%- if cookiecutter.use_i18n == 'y' %}
import i18n from "./locales"
{%- endif %}
import router from './router'
import store from './store'
import api from './api'

import './assets/scss/app.scss'

const emitter = mitt()
app.config.globalProperties.emitter = emitter

const app = createApp(App)

{%- if cookiecutter.use_i18n == 'y' %}
app.use(i18n)
{%- endif %}
app.use(store)
app.use(router)
app.use(VueAxios, api)
app.provide('http', app.config.globalProperties.axios)

app.mount('#app')
