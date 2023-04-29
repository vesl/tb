<template>
    <div class="input-group">
        <label class="input-group-text" for=""><Icon :icon="labelIcon" /></label>
        <select class="form-select" @change="select">
            <option v-for="item in items" :value="item.value">{{ item.name }}</option>
        </select>
    </div>
</template>

<script>
import Icon from '../atoms/Icon.vue'

export default {
    name: 'form-select',
    components: {
        Icon
    },
    data (){
      return {
          icon: "bi-box-arrow-in-left",
          selected: this.items[0].value
      }  
    },
    props: {
        items: {
            type: Array,
            required: true
        },
        action: {
            type: Function,
            required: true
        },
        labelIcon: {
            type: String,
            required: true
        }
    },
    methods: {
        select(event) {
            this.action(event)
            this.selected = event.target.value
        }
    }
}
</script>

<style scoped>
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  -webkit-border-radius: 0px;
  color: white;
  background: var(--primary) url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 512'%3e%3cpath fill='white' d='M137.4 374.6c12.5 12.5 32.8 12.5 45.3 0l128-128c9.2-9.2 11.9-22.9 6.9-34.9s-16.6-19.8-29.6-19.8L32 192c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9l128 128z'/%3e%3c/svg%3e") no-repeat right .75rem center/8px 10px !important;
}
</style>