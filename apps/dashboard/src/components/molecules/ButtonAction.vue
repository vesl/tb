<template>
    <button class="btn btn-dark shadow" @click="action"><Icon :icon="'bi-play-circle-fill'" />{{ title }}</button>   
</template>

<script>
import Icon from '../atoms/Icon.vue'
export default {
    name: 'button-action',
    components: {
        Icon
    },
    props: {
        title: {
            type: String,
            required: true
        },
        action: {
            type: Function,
            required: true
        }
    }
}
</script>
