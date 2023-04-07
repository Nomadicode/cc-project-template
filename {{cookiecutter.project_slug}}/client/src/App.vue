<template>
	<nav>
		<router-link to="/">Home</router-link> |
		<router-link to="/about">About</router-link>
	</nav>
	<router-view/>
	<Toast />
</template>

<script>
import Toast from 'primevue/toast'

export default {
	components: {
		Toast
	}
}
</script>
