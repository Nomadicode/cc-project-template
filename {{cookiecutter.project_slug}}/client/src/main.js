import { createApp } from 'vue'
import App from './App.vue'
import VueAxios from 'vue-axios'
import mitt from 'mitt'

{%- if cookiecutter.use_i18n == 'y' %}
import i18n from "./locales"
{%- endif %}
import router from './router'
import store from './store'
{%- if cookiecutter.use_rest == 'y' %}
import rest from './api/rest'
{%- elif cookiecutter.use_graphql == 'y' %}
import apolloProvider from './api/apollo'
{%- endif %}

import './assets/scss/app.scss'

const app = createApp(App)
const emitter = mitt()
app.config.globalProperties.emitter = emitter

{%- if cookiecutter.use_i18n == 'y' %}
app.use(i18n)
{%- endif %}
app.use(store)
app.use(router)
{%- if cookiecutter.use_rest == 'y' %}
app.use(VueAxios, api)
{%- elif cookiecutter.use_graphql == 'y' %}
app.use(apolloProvider)
{%- endif %}
app.provide('http', app.config.globalProperties.axios)

app.mount('#app')
