<template>
  <div>
    这是首页
    <h1>你好! {{ name }}</h1>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  data() {
    return {

    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>
