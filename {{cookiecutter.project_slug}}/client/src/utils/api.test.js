import { snakeCaseKeys, camelCaseKeys } from "./api"

describe('snakeCaseKeys', () => {
  it('converts object keys to snake case from camel case', () => {
    const original = {
        "testKey0": []
    }
    const changed = snakeCaseKeys(original)
    expect(Object.keys(changed)[0]).toBe("test_key_0")
  })
})

describe('camelCaseKeys', () => {
    it('converts object keys to snake case from camel case', () => {
      const original = {
          "test_key_0": []
      }
      const changed = camelCaseKeys(original)
      expect(Object.keys(changed)[0]).toBe("testKey0")
    })
  })
