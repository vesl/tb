<template>
  <div class="row">
    <div class="tb-primary col-3">
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
  .tb-primary {
    background-color: var(--primary);
    color: white;
  }
  .tb-light {
    background-color: var(--light);
  }
  .tb-middle-light {
    background-color: var(--middle-light);
  }
  .tb-middle-dark {
    background-color: var(--middle-dark);
  }
  .tb-dark {
    background-color: var(--dark);
  }
  .tb-flash {
    background-color: var(--flash);
  }
  .tb-transition {
    transition: all 0.2s ease-in-out;
  }
  :root {
    --primary: #1c3c5d;
    --light: #e9eff4;
    --middle-light: #9ea8bc;
    --middle-dark: #1a334d;
    --dark: #18303f;
    --flash: #007efb;
  }
</style>