<template>
    <Icon v-if="icon" :icon="icon"/>
    <span class="content-header">{{ title }}</span>
    <hr>
</template>

<script>
import Icon from '../atoms/Icon.vue'

export default {
    name: 'content-header',
    components: {
        Icon
    },
    props: {
        title: {
            type: String,
            required: true
        },
        icon: {
            type: String,
            required: false
        }
    }
}
</script>

<style scoped>
.content-header {
    font-size: 0.8em;
}
hr {
    margin-top: -0.1em;
}
</style>