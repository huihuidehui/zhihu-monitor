<template>
  <el-aside width="auto">
    <el-menu
      :default-active="activeTab"
      class="el-menu-vertical-demo"
      background-color="#2c3b4e"
      text-color="#fff"
      active-text-color="#ffd04b"
      :collapse="isExpansion"
      router
    >
      <el-menu-item index="/admin/index" :route="{path:'/'}">
        <i class="el-icon-location"></i>
        <span>首页</span>
      </el-menu-item>
      <!-- <el-menu-item index="/admin/category"> -->
      <!-- <i class="el-icon-menu"></i> -->
      <!-- <span slot="title">分类</span> -->
      <!-- </el-menu-item> -->
      <!-- <el-submenu index="3"> -->
        <!-- <template v-slot:title> -->
          <!-- <i class="el-icon-document"></i> -->
          <!-- <span slot="title">查看问题</span> -->
        <!-- </template> -->
        <el-menu-item index="/showquestion" :disabled="isInViewQuestionPage">
          <i class="el-icon-document"></i>
          <span slot="title">查看问题</span>
        </el-menu-item>
        <el-menu-item index="/admin/category/create" :disabled="isInViewAnswerPage">
          <i class="el-icon-document"></i>
          <span slot="title">查看回答</span>
        </el-menu-item>
        <!-- <el-menu-item index="/admin/category/manage" :route="{path:'/admin/category/manage'}"> -->
          <!-- <i class="el-icon-document"></i> -->
          <!-- <span slot="title">查看回答</span> -->
        <!-- </el-menu-item> -->
      <!-- </el-submenu> -->
      <el-submenu index="4">
        <template v-slot:title>
          <i class="el-icon-document"></i>
          <span slot="title">关于</span>
        </template>
        <el-menu-item index="/introduce">
          <i class="el-icon-document"></i>
          <span slot="title">网站简介</span>
        </el-menu-item>
        <el-menu-item index="/about">
          <i class="el-icon-document"></i>
          <span slot="title">关于</span>
        </el-menu-item>
      </el-submenu>
      <el-menu-item v-on:click="isCollapse">
        <i class="el-icon-menu"></i>
        <span>收起</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: "Aside",
  data() {
    return {
      isExpansion: false,
      asideWidth: "200px"
    };
  },
  methods: {
    isCollapse() {
      this.isExpansion = !this.isExpansion;
      //   this.
    }
  },
  computed: {
    activeTab() {
      return this.$route.path;
    },
    // 用于在非查看页面禁用该选项卡
    isInViewQuestionPage() {
      return this.$route.path !== "/showquestion";
    },
    isInViewAnswerPage(){
      return this.$route.path !== "/showanswer";
    }
  }
};
</script>

<style scoped>
.el-aside {
  background-color: #2c3b4e;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
span {
  color: #fff;
}
</style>
