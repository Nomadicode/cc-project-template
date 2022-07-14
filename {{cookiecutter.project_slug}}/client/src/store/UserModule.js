const UserModule = {
    namespaced: true,
  
    state: {
      token: null,
      user: null
    },
    mutations: {
      LOGIN_USER (state, token) {
        state.token = token
      },
      SET_USER_DATA (state, userData) {
        state.user = userData
      },
      LOGOUT_USER (state) {
        state.user = null
        state.token = null
      }
    },
    getters: {
      email: state => {
        return (state.user) ? state.user.email : null
      },
      isLoggedIn: state => {
        return (state.token) ? true : false
      },
      token: state => {
        return state.token
      },
      userId: state => {
        return (state.user) ? state.user.id : null
      }
    }
  }
  
  export default UserModule
  