<template>
  <div v-loading="loading">
    <iframe
      id="show-iframe"
      :width="ratioWidth"
      :height="height"
      frameborder="0"
      name="showHere"
      scrolling="auto"
      :src="webAddress.link"
    />
  </div>
</template>
<script>
export default {
  props: {
    webAddress: {
      type: Object,
      default: () => {}
    },
    width: {
      type: Number,
      default: 500
    },
    height: {
      type: Number,
      default: 600
    },
    loading: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    ratioWidth() {
      return this.width * 0.96
    }
  }
}
</script>
<style scoped>

</style>
