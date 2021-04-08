<template>
  <div>
    <router-link :to="item.course_name+'/'+item.course_id">
      <el-card :body-style="{ padding: '0px' }">
        <div class="imgContain">
          <!-- <img src="https://picsum.photos/seed/picsum/300/200" class="image"> -->
          <img :src="cover" class="image">
        </div>
        <div style="padding: 14px;">
          <h3>{{ item.course_name }}</h3>
          <div class="bottom clearfix">
            <time class="time">资源管理人:<span style="font-size:18px;"> {{ item.course_teacher }} </span></time>
            <span style="float: right">已上传的资源数:<span style="font-size:18px;"> {{ item.upload_count }} </span> </span>
          </div>
        </div>
      </el-card>
    </router-link>
  </div>
</template>
<style scoped>
.el-card {
  border-radius: 8px;
  margin-bottom: 20px;
  cursor: pointer;
  overflow: hidden;
}
.el-card img {
  transition: all 0.3s ease;
}
.el-card:hover {
  box-shadow: 0 13px 27px -5px hsla(240, 30.1%, 28%, 0.25),
    0 8px 16px -8px hsla(0, 0%, 0%, 0.3), 0 -6px 16px -6px hsla(0, 0%, 0%, 0.03);
}
.el-card:hover img {
  transform: scale(1.1);
}
.el-card .bottom{
  font-size: 15px;
}
.imgContain {
  overflow: hidden;
}
h3 {
  font-size: 20px;
}
h4 {
  font-weight: 600;
}
img {
  width: 100%;
  height: 250px;
  vertical-align: top;
}
</style>
<script>
export default {
  props: {
    item: {
      type: Object,
      default: () => {}
    }
  },
  computed: {
    cover() {
      return process.env.VUE_APP_BASE_API + this.item.course_cover
    }
  }
}
</script>
