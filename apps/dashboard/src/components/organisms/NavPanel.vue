<template>
  <div class="row shadow">
    <h3 class="m-3 pt-3 pb-3 display-4">{{ title }}</h3>
  </div>
  <NavCategory
    :class = "{ active: this.active == category.id }"
    @select-category="(id) => this.active = id"
    v-for="category in categories"
    :category="category" 
    :key="category.id"
    :active="active"
  />
</template>

<script>
import NavCategory from '../molecules/NavCategory.vue'

export default {
  name: 'NavPanel',
  components: {
    NavCategory,  
  },
  data() {
    return {
      title: 'TB Dashboard',
      openSubCategories: [],
      active: null,
      categories: [
        {
          id: 0,
          name: 'Models'
        },
        {
          id: 1,
          name: 'Traders'
        }
      ]
    }
  }
}
</script>