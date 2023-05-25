<template>
    <button class="btn btn-dark shadow" @click="action"><Icon :icon="'bi-play-circle-fill'" />{{ title }}</button>   
</template>

<script>
export default {
    name: 'button-action',

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
