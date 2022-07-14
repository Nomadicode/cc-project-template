import { createStore } from 'vuex'
import createPersistedState from "vuex-persistedstate"

import AppState from './AppState'
import UserModule from './UserModule'

export default createStore({
  modules: {
    'AppState': AppState,
    'UserModule': UserModule
  },
  plugins: [createPersistedState()]
})
