<template>
  {{ app }} {{ view }} {{ symbol }}   
</template>

<script>
export default {
    props: {
        app: {
            type: String,
            required: true
        },
        view: {
            type: String,
            required: true
        },
        symbol: {
            type: String,
            required: true
        }
    }
}
</script>