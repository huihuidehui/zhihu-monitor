<template>
  <el-header>
    <a v-on:click="logout">
      <i class="fa fa-sign-out"></i>
      注销
    </a>
    <!-- <el-button>退出</el-button> -->
    <span>欢迎{{username}}使用知乎监控系统</span>
  </el-header>
</template>

<script>
import store from "store/index.js";
export default {
  name: "Header",
  data() {
    return {
      username: ""
    };
  },
  // computed:{
    // username(){
      // return store.state.username;
    // }
  // },
  created(){
    this.username = store.state.username;
    // console.log(this.username)
  },
  methods: {
    logout() {
      // 清空localStorage中的token
      window.localStorage.setItem("token", "");
      // 清空vuex中的token
      this.$store.commit("changeToken", "");
      // 退回登陆页面
      this.$router.push({ path: "/login" });
    }
  }
};
</script>

<style lang="less" scoped>
.el-header {
  background: #fff;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  > span {
    margin-right: 10px;
    font-size: 0.85rem;
    color: #777;
  }
  > a {
    font-size: 0.85rem;
    color: #777;
  }
  > a:hover {
    color: blue;
  }
  border-bottom: 1px solid #ddd;
}
</style>
