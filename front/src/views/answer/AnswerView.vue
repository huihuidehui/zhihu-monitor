<template>
  <el-container style="height: 100vh">
    <app-aside></app-aside>
    <el-container>
      <app-header></app-header>
      <el-main>
        <p class="title is-size-6">作者：{{title}}</p>
        <p class="title is-size-6">问题：{{question}}</p>

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
        <ve-line :data="chartData" :extend="extend"></ve-line>
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
  name: "AnswerView",
  data() {
    //  this.extend = {
    // 'xAxis.0.axisLabel.rotate': 45
    // }
    (this.extend = {
      "xAxis.0.axisLabel.rotate": 45,
      series: {
        label: {
          normal: {
            show: true
          }
        }
      }
    }),
      (this.chartSettings = {
        // xAxisType: 'time'
        // min:10000
        min: ["dataMin", "dataMin"],
        max: ["dataMax", "dataMax"]
      });
    return {
      title: "",
      question: "",
      chartData: {
        columns: ["日期", "点赞数", "排名", "评论数"],
        rows: [
          { 日期: "1/2", 点赞数: 100, 排名: 10, 评论数: 1 },
          { 日期: "1/3", 点赞数: 150, 排名: 9, 评论数: 4 },
          { 日期: "1/4", 点赞数: 180, 排名: 3, 评论数: 10 },
          { 日期: "1/5", 点赞数: 200, 排名: 1, 评论数: 19 }
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
        url: "/answer",
        method: "get",
        params: {
          questionZhiHuId: this.$route.query.questionZhiHuId,
          answerZhiHuId: this.$route.query.answerZhiHuId,
          startTime: this.startTime,
          endTime: this.endTime
        }
      }).then(res => {
        this.title = res.data.title;
        this.question = res.data.question;
        // this.chartData.rows = res.data.followerNums;
        // 处理数据
        let newRows = new Array();
        for (let i = 0; i < res.data.voteNum.length; i++) {
          let timeStamp = res.data.voteNum[i].time;
          let value = res.data.voteNum[i].value;
          let dateObj = new Date(timeStamp);
          newRows.push({
            日期:
              dateObj.getMonth() +
              1 +
              "/" +
              dateObj.getDate() +
              "/" +
              dateObj.getHours() +
              "/" +
              dateObj.getMinutes(),
            点赞数: value,
            排名: res.data.rank[i].value,
            评论数: res.data.commentNum[i].value
          });
        }
        this.chartData.rows = newRows;
      });
    }
  }
};
</script>

<style scoped>
</style>

