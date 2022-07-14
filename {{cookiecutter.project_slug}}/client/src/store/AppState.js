const AppState = {
    namespaced: true,
  
    state: {
      {%- if cookiecutter.use_i18n == 'y' %}
      locale: null
      {%- endif %}
    },
    mutations: {
      {%- if cookiecutter.use_i18n == 'y' %}
      SET_LOCALE (state, locale) {
        state.locale = locale
      }
      {%- endif %}
    },
    getters: {
      {%- if cookiecutter.use_i18n == 'y' %}
      locale: state => {
        return state.locale
      }
      {%- endif %}
    }
  }
  
  export default AppState
  