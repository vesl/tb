<template>
    <div class="tb-middle-dark rounded m-2 shadow pb-3">
        <ContentHeader :title="title" :icon="'bi-bar-chart-fill'" />
        <slot></slot>
    </div>
</template>

<script>
import ContentHeader from './ContentHeader.vue'

export default {
    name: 'content-chart',
    components: {
        ContentHeader
    },
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>