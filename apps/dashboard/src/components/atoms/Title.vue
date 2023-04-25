<template>
  <div class="shadow p-3 text-center">
    <h3>{{ title }}</h3>
  </div>
</template>

<script>
export default {
  name: 'title-main',
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
h3 {
  font-weight: 200;
}
</style>