import { createI18n } from 'vue-i18n'

import en from "./languages/en"
import es from "./languages/es"

const i18n = createI18n({
    legacy: true,
    locale: 'en',
    fallbackLocal: 'en',
    messages: {
        en,
        es
    }
})

export default i18n
