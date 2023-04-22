<template>
  <div 
    :class="['sub-category','row','tb-transition','p-2',{ 'tb-middle-dark': (subActive == subCategory.id) || isHover }]"
    @click="$emit('selectSubCategory',subCategory.id)"
    @mouseover="isHover = true" 
    @mouseleave="isHover = false"
  >
    <div class="d-flex align-items-center shadow">
      <BootstrapIcon :icon="'bi-caret-right-square-fill'" />
      <span>
       {{ subCategory.name }}
      </span>
    </div>
  </div>
</template>

<script>
import BootstrapIcon from '../atoms/BootstrapIcon.vue'

export default {
  name: 'NavSubCategories',
  components: {
      BootstrapIcon
  },
  emits: ['selectSubCategory'],
  props: {
    subCategory: {
      type: Object,
      required: true
    },
    subActive: {
      type: Number,
    }
  },
  data (){
    return {
      isHover: false,
    }
  }
}
</script>

<style scoped>
sub-category {
  border-bottom: 2px solid var(--light);
}
</style>