<template>
  <div class="sidebar-logo-container" :class="{'collapse':collapse}">
    <transition name="sidebarLogoFade">
      <router-link v-if="collapse" key="collapse" class="sidebar-logo-link" to="/profile/self">
        <div>
          <img v-if="logo" :src="logo" class="sidebar-logo">
          <h1 v-if="!collapse" class="sidebar-title">{{ title }} </h1>
        </div>
      </router-link>
      <router-link v-else key="expand" class="sidebar-logo-link" to="/profile/self">
        <img v-if="logo" :src="logo" class="sidebar-logo" :style="{width:reacticeWidth+'px',height:reactiveHeight+'px'}">
        <h1 v-if="!collapse" class="sidebar-title">{{ title }} </h1>
      </router-link>
    </transition>
  </div>
</template>

<script>
import logo from '@/assets/logo.png'
export default {
  name: 'SidebarLogo',
  props: {
    collapse: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      title: '课程资源管理系统',
      logo: logo,
      reacticeWidth: this.collapse ? 40 : 60,
      reactiveHeight: this.collapse ? 40 : 60
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  position: relative;
  width: 100%;
  background: #2b2f3a;
  text-align: center;
  overflow: hidden;
  padding-top:20px;

  & .sidebar-logo-link {
    height: 100%;
    width: 100%;

    & .sidebar-logo {
      width: 40px;
      height: 40px;
      vertical-align: middle;
      margin-right: 12px;
    }

    & .sidebar-title {
      display: block;
      margin: 0 auto;
      color: #fff;
      font-weight: 100;
      font-size: 14px;
      padding:10px 0;
    }
  }

  &.collapse {
    .sidebar-logo {
      margin-right: 0px;
    }
  }
}
</style>
