<template>
    <span class="content-header">{{ title }}</span>
    <hr>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
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