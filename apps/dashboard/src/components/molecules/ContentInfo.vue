<template>
    <div class="tb-middle-dark rounded m-2 shadow pb-3">
        <ContentHeader :title="title"/>
        <slot></slot>
    </div>
</template>

<script>
import ContentHeader from '../atoms/ContentHeader.vue'

export default {
    name: 'content-info',
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