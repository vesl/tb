<template>
  <div @click="$emit('select-category',category.id)" class="category row tb-transition p-3">
    <div class="d-flex align-items-center">
    <BootstrapIcon :icon="'bi bi-clipboard-data'" />
    <span class="category-name">
      {{ category.name }}
    </span>
    </div>
  </div>
</template>

<script>
import BootstrapIcon from '../atoms/BootstrapIcon.vue'

export default {
  name: 'NavCategories',
  components: {
    BootstrapIcon
  },
  props: {
    category: {
      type: Object,
      required: true
    },
    active: {
      type: Number,
    },
  }
}
</script>

<style scoped>
.active {
  background-color: #123150;
}
.category:hover {
  background-color: #123150;
}
.category-name {
  display: float;
  font-size: 1.4rem;
}
</style>