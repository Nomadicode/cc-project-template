import { ApolloClient, InMemoryCache } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option'

// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
const apolloClient = new ApolloClient({
  cache,
  uri: `${process.env.VUE_APP_API_DOMAIN}/graphql`
})

const apolloProvider = createApolloProvider({
  defaultClient: apolloClient
})

export default apolloProvider
