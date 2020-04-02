<template>
  <el-container style="height: 100vh">
    <app-aside></app-aside>
    <el-container>
      <app-header></app-header>
      <el-main>
        <p class="title is-size-6">问题：{{title}}</p>

        <div class="block">
          <span class="demonstration is-size-6">查询的时间范围</span>
          <el-date-picker
            v-model="value2"
            type="datetimerange"
            :picker-options="pickerOptions"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
          ></el-date-picker>
        </div>
        <ve-line :data="chartData" :settings="chartSettings" :extend="extend"></ve-line>
      </el-main>
      <el-footer></el-footer>
    </el-container>
  </el-container>
</template>

<script>
import Aside from "components/content/Aside";
import Header from "components/content/Header";
import { Request } from "network/request.js";
import { formatDate } from "plugins/utils.js";
export default {
  name: "QuestionView",
  data() {
    // this.chartSettings = {
    // axisSite: { right: ["下单率"] },
    // yAxisType: ["KMB", "percent"],
    // yAxisName: ["数值", "比率"]
    // };
     this.extend = {
        'xAxis.0.axisLabel.rotate': 45
      },
       this.chartSettings = {
        // xAxisType: 'time'
        // min:10000
      }
    return {
      title: "",
      chartData: {
        columns: ["日期", "关注数","浏览数"],
        rows: [
          { 日期: "1/2", 关注数: 100, 浏览数: 10 },
          { 日期: "1/3", 关注数: 200, 浏览数: 20 },
          { 日期: "1/4", 关注数: 300, 浏览数: 100 },
          { 日期: "1/5", 关注数: 400, 浏览数: 200 },
          // { time: "1/3", value: 100 },
          // { time: "1/4", value: 1000 },
          // { time: "1/5", value: 3000 },
          // { time: "1/6", value: 5000 }
        ]
      },
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            }
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            }
          }
        ]
      },
      // value1: [new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)],
      value2: "",
      startTime: 0,
      endTime: parseInt(new Date().getTime())
    };
  },
  watch: {
    value2(newValue) {
      console.log(newValue);
      this.startTime = parseInt(formatDate(newValue[0]).getTime());
      this.endTime = parseInt(formatDate(newValue[1]).getTime());
      this.getData();
    }
  },
  components: {
    "app-aside": Aside,
    "app-header": Header
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      Request({
        url: "/question",
        method: "get",
        params: {
          id: this.$route.query.questionId,
          startTime: this.startTime,
          endTime: this.endTime
        }
      }).then(res => {
        this.title = res.data.title;
        // this.chartData.rows = res.data.followerNums;
        // 处理数据
        let newRows = new Array();
        console.log(new Date().getTime())
        for (let i = 0; i < res.data.followerNums.length; i++) {
          let timeStamp = res.data.followerNums[i].time;
          let value = res.data.followerNums[i].value;
          let dateObj = new Date(timeStamp);
          // console.log(new Date().getDate());
          // console.log(timeStamp);
          newRows.push({
            日期: (dateObj.getMonth()+1) + "/" + dateObj.getDate() + "/" +dateObj.getHours() + "/" + dateObj.getMinutes(),
            关注数:value,
            浏览数:res.data.viewNums[i].value
          })
        }
        this.chartData.rows = newRows;
        console.log(res);
      });
    }
  }
};
</script>

<style scoped>
</style>
