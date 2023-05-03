<template>
    <div class="tb-middle-light m-2 shadow pb-3">
        <ContentHeader :title="title" :icon="'bi-text-left'"/>
        <slot></slot>
    </div>
</template>

<script>
import ContentHeader from './ContentHeader.vue'

export default {
    name: 'content-text',
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