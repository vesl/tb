<template>
  <div class="row shadow">
    <h3 class="m-3 pt-3 pb-3 display-4">{{ title }}</h3>
  </div>
  <div class="row p-1"></div>
  <NavCategory
    @selectCategory="(id) => this.active = id"
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
          name: 'Models',
          icon: 'bi-steam',
          subCategories: [
            {
              id: 0,
              name: 'Train',
            },
            {
              id: 1,
              name: 'Results'
            }
          ]
        },
        {
          id: 1,
          name: 'Traders',
          icon: 'bi-currency-exchange',
          subCategories: [
            {
              id: 0,
              name: 'Results'
            },
            {
              id: 1,
              name: 'Test'
            }
          ]
        },
        {
          id: 3,
          name: 'Other',
          icon: 'bi-card-checklist',
          subCategories: [
            {
              id: 0,
              name: 'Tata'
            }
          ]
        }
      ]
    }
  }
}
</script>

<style scoped>
  hr {
    color: var(--flash);
  }
</style>