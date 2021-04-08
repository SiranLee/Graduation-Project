<template>
  <div>
    <div id="wangeditor">
      <div :id="id" :ref="editorElem" style="text-align:left" />
    </div>
  </div>
</template>
<script>
import editor from 'wangeditor'
import config from './editor.config'
export default {
  name: 'EditorElem',
  props: {
    catchData: {
      type: Function,
      default: () => {}
    },
    content: {
      type: String,
      default: ''
    },
    editorElem: {
      type: String,
      default: 'editor'
    },
    id: {
      type: String,
      default: 'editor'
    },
    barsAll: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      editor: null,
      editorContent: ''
    }
  }, // 接收父组件的方法
  watch: {
    content() {
      this.editor.txt.html(this.content)
    }
  },
  mounted() {
    this.editor = new editor(this.$refs[this.editorElem])
    this.editor.customConfig.zIndex = 100
    this.editor.customConfig.onchange = (html) => {
      this.editorContent = html
      this.catchData(this.editorContent) // 把这个html通过catchData的方法传入父组件
    }
    this.editor.customConfig.menus = this.barsAll ? config.all : config.basic

    this.editor.create() // 创建富文本实例
    if (!this.content) {
      this.editor.txt.html('')
    } else {
      this.editor.txt.html(this.content)
    }
  }
}
</script>
<style scoped>

</style>
