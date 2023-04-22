<template>
  <div 
    @click="$emit('selectCategory',category.id)" 
    :class="['category','row','tb-transition','p-3',{ 'tb-dark left-border': (active == category.id) || isHover }]"
    @mouseover="isHover = true" 
    @mouseleave="isHover = false"
  >
    <div class="d-flex align-items-center">
      <BootstrapIcon :icon="category.icon" />
      <span class="category-name">{{ category.name }}</span>
    </div>
  </div>
  <div class="row tb-dark tb-transition" v-if="active == category.id">
    <div class="pt-2">
      <NavSubCategory
        @selectSubCategory="(id) => this.subActive = id"
        v-for="subCategory in category.subCategories"
        :subCategory="subCategory"
        :key="subCategory.id"
        :subActive="subActive"
      />
    </div>
  </div>
</template>

<script>
import BootstrapIcon from '../atoms/BootstrapIcon.vue'
import NavSubCategory from '../molecules/NavSubCategory.vue'

export default {
  name: 'NavCategories',
  emits: ['selectCategory'],
  components: {
    BootstrapIcon,
    NavSubCategory
  },
  props: {
    category: {
      type: Object,
      required: true
    },
    active: {
      type: Number,
    }
  },
  data (){
    return {
      isHover: false,
      subActive: null
    }
  },
  watch: {
    active(){
      this.subActive = null
    }
  }
}
</script>

<style scoped>
.category-name {
  font-size: 1.2rem;
}
.left-border {
  border-left: 20px solid var(--flash);
}
.left-light-border {
  border-left: 15px solid var(--flash);
}
</style>