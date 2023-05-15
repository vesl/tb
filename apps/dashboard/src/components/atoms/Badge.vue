<template>
    <span :class="'badge rounded-pill bg-'+type">{{ text }}</span>
</template>

<script>
export default {
    name: 'bootstrap-badge',
    props: {
        text: {
            type: String,
            required: true
        },
        type: {
            type: String,
            required: true
        }
    }
}
</script>