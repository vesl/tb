<template>
    <div class="collapse-button" @click="collapse"><Icon :icon="collapseIcon" />{{ title }}</div>
    <div :class="[{'d-none' : collapsed},'collapse-content']">
        <slot></slot>
    </div>
</template>

<script>

export default {
    name: 'collapse-custom',

    data() {
        return {
          collapsed: true,
          collapseIcon: 'bi-caret-right-fill' 
        }
    },
    props: {
      title: {
          type: String,
          required: true
      }  
    },
    methods: {
        collapse(){
            this.collapsed = !this.collapsed
            this.collapseIcon = this.collapsed ? 'bi-caret-right-fill':'bi-caret-down-fill'
        }
    }
}
</script>

<style scoped>
.collapse-button {
    background: var(--dark);
    color: var(--middle-light);
    padding: 1em;
    margin-top: 0.5em;
}
</style>