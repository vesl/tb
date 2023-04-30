<template>
  <div class="container-fluid">
    <div class="row">
      <div class="tb-primary col-2 p-0">
        <Nav :appName="appName" />
      </div>
      <div class="tb-light col-10 p-0">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import Nav from './components/organisms/Nav.vue'

export default {
  name: 'App',
  components: {
    Nav
  },
  data(){
    return {
      appName: 'TB Dashboard'
    }
  }
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
    color: var(--grey);
  }
  .tb-middle-light {
    background-color: var(--middle-light);
    color: var(--grey);
  }
  .tb-middle-dark {
    background-color: var(--middle-dark);
    color: white;
  }
  .tb-dark {
    background-color: var(--dark);
    color: white;
  }
  .tb-flash {
    background-color: var(--flash);
  }
  .tb-fade {
    transition: all 0.2s ease-in-out;
  }
  :root {
    --primary: #1c3c5d;
    --light: #e9eff4;
    --middle-light: #9ea8bc;
    --middle-dark: #1a334d;
    --dark: #18303f;
    --flash: #007efb;
    --grey: #505050;
  }
</style>