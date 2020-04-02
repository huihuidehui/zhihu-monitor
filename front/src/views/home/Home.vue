<template>
  <!-- <el-container class="home-container"> -->
  <!-- <app-aside></app-aside> -->
  <!-- <el-container> -->
  <!-- <app-header></app-header> -->
  <!-- <el-main> -->
  <!-- </el-main> -->
  <el-container style="height: 100vh">
    <app-aside></app-aside>
    <el-container>
      <app-header></app-header>
      <el-main>
        <icon-card></icon-card>
        <question-table></question-table>
        <answer-table></answer-table>
        <!-- <router-view> </router-view> -->
      </el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </el-container>
</template>

<script>
import Aside from "components/content/Aside";
import Header from "components/content/Header";
import IconCard from "./childcpn/IconCard";
import QuestionTable from "./childcpn/QuestionTable";
import AnswerTable from "./childcpn/AnswerTable";
export default {
  name: "Home",
  data() {
    return {};
  },
  components: {
    "app-aside": Aside,
    "app-header": Header,
    IconCard,
    QuestionTable,
    AnswerTable
  }
};
</script>
<style lang="stylus" scoped>
.el-main {
  background-color: #f3f3f4;
}

.el-footer {
  background-color: #f3f3f4;
}
</style>