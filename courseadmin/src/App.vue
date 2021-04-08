<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
<style>
path {
  fill: inherit !important;
}
.el-input__inner:focus,.el-textarea__inner:focus {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>
