<template>
  <div class="row">
    <div class="tb-dark col-3">
      <NavPanel />
    </div>
    <div class="tb-light col-9">
    </div>
  </div>
</template>

<script>
import NavPanel from './components/organisms/NavPanel.vue'

export default {
  name: 'App',
  components: {
    NavPanel,
  },
}
</script>

<style>
  body {
    font-family: 'SF Pro Display', sans-serif;
  }
  .tb-dark {
    background-color: #1c3c5d;
    color: #fff;
  }
  .tb-light {
    background-color: #e9eff4;
  }
  .tb-transition {
    transition: all 0.2s ease-in-out;
  }
</style>