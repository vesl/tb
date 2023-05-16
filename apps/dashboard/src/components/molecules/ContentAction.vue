<template>
    <div class="m-2 shadow pb-3">
        <ContentHeader :title="title" :icon="'bi-gear-wide-connected'"/>
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