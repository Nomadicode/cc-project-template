export const snakeCaseKeys = (object) => {
    if (!object) return null
 
    return Object
                .entries(object)
                .reduce((prevValue, [key, value]) => {
                    const newKey = key.replace(/[A-Z0-9]/g, (m) => '_' + m.toLowerCase())
                    prevValue[newKey] = value
                    return prevValue
                }, {})
}

export const camelCaseKeys = (object) => {
    if (!object) return null
    
    return Object
            .entries(object)
            .reduce((prevValue, [key, value]) => {
                const newKey = key.replace(/_([a-z0-9])/g, (m, p1) => p1.toUpperCase())
                prevValue[newKey] = (typeof value === 'object') ? camelCaseKeys(value) : value
                return prevValue
            }, {})
}
