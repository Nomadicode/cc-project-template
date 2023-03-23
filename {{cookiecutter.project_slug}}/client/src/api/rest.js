import axios from "axios"
import store from "../store"

import { camelCaseKeys, snakeCaseKeys } from "../utils/api"

const token = store.getters['UserModule/token']

const headers = {}

if (token) {
    headers['Authorization'] = `token ${token}`
}

const api = axios.create({
    baseURL: process.env.VUE_APP_API_ROOT,
    headers: headers,
    transformRequest: [(data) => {
        data = (data instanceof FormData) ? data : snakeCaseKeys(data)
        return data
    }, ...axios.defaults.transformRequest],
    transformResponse: [(data) => {
        data = JSON.parse(data)
        data = camelCaseKeys(data)
        return data
    }, ...axios.defaults.transformResponse],
    responseType: "json"
})

export default api
