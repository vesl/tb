<template>
    <div :class="'spinner-border text-center p-6 text-'+ color ? color : 'light'" role="status">
        <span class="sr-only">Loading...</span>
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