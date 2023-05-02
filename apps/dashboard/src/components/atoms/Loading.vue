<template>
    <div class="text-center opacity-75">
        <div :class="[color ? 'text-'+color : 'text-light','spinner-grow']" role="status"></div>
        <div class="loading-text">Loading data</div>
    </div>
</template>

<script>
export default {
    name: 'loading-spinner',
    props: {
        color: {
            type: String,
            required: false
        }
    }
}
</script>

<style scoped>
.loading-text {
    font-size: 0.8em;
}
</style>