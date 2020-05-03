
<template>
  <div>
    <div>
      <p class="is-size-6">添加监控的回答</p>
      <el-input v-model="questionZhiHuId" placeholder="输入回答所在问题id"></el-input>
      <el-input v-model="answerZhiHuId" placeholder="输入回答id"></el-input>
      <el-button type="primary" size="mini" round v-on:click="addNewAnswer">提交</el-button>
    </div>
    <div class="question-table">
      <p class="title is-size-5">监控回答</p>
      <el-table v-loading="loading" :border="true" :data="answersData" style="width: 100%"
      v-on:sort-change="newSort">
        <el-table-column type="index" :index="indexMethod"></el-table-column>
        <el-table-column prop="title" sortable="custom" label="答主" ></el-table-column>
        <!-- <el-table-column prop="questionId" label="问题id"></el-table-column> -->
        <el-table-column prop="question" label="问题"></el-table-column>
        <el-table-column prop="questionZhiHuId" label="问题Id"></el-table-column>

        <el-table-column prop="rank" sortable="custom" label="排名"></el-table-column>
        <el-table-column prop="voteNums" sortable="custom" label="点赞数"></el-table-column>
        <el-table-column prop="commentNums" sortable="custom" label="评论数"></el-table-column>
        <el-table-column prop="answerZhiHuId" label="回答Id"></el-table-column>

        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
            <el-button type="text" size="small" @click="deleteAnswer(scope.row)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination">
      <el-pagination
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalNum"
        :page-count="totalPage"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { Request } from "network/request.js";
// import { formatDate } from "plugins/utils.js";
export default {
  name: "AnswerTable",
  data() {
    return {
      questionZhiHuId: "",
      answerZhiHuId: "",
      answersData: [],
      page: 1,
      currentPage: 1,
      totalPage: 0,
      totalNum: 0,
      loading: true,
      pageSize: 10,
      sortord:1
    };
  },
  watch: {
    page(newPage) {
      console.log(newPage);
      this.getData();
    }
  },
  created() {
    this.getData();
  },
  methods: {
    newSort(a) {
      switch (a.column.property) {
        case "title":
          this.sortord = 1;
          break;
        case "voteNums":
          this.sortord = 2;
          break;
        case "commentNums":
          this.sortord = 3;
          break;
        case "rank":
          this.sortord = 4;
          break;
        // case "currentFollowerNums":
          // this.sortord = 5;
          // break;
        default:
          this.sortord = 1;
      }
      if (a.column.order != "ascending") {
        this.sortord = -this.sortord;
      }

      this.getData();
    },
    addNewAnswer() {
      Request({
        url: "/answer",
        method: "put",
        data: {
          questionZhiHuId: this.questionZhiHuId,
          answerZhiHuId: this.answerZhiHuId
        }
      })
        .then(res => {
          if (res.res == 1) {
            this.getData();
            this.questionZhiHuId = "";
            this.answerZhiHuId = "";
            this.$message({
              message: "恭喜你，提交成功",
              type: "success"
            });
          } else {
            this.$message.error("提交失败，请核对回答id、问题id");
          }
        })
        .catch(err => {
          console.log(err);
          this.$message.error("提交失败，请核对回答id、问题id");
        });
      //   console.log("tijai");
    },
    handleClick(data) {
      // this.$router.push({
      // path: "showanswer",
      // query: {
      // questionZhiHuId: data.questionZhiHuId,
      // answerZhiHuId: data.answerZhiHuId
      // }
      // });
      const { href } = this.$router.resolve({
        path: "showanswer",
        query: {
          questionZhiHuId: data.questionZhiHuId,
          answerZhiHuId: data.answerZhiHuId
        }
      });
      window.open(href, "_blank");

      // console.log(data.questionId);
    },
    deleteAnswer(data) {
      Request({
        url: "/answer",
        method: "delete",
        data: {
          questionZhiHuId: data.questionZhiHuId,
          answerZhiHuId: data.answerZhiHuId
        }
      })
        .then(res => {
          if (res.res == 1) {
            this.$message({
              message: "恭喜你，提交成功",
              type: "success"
            });
            this.getData();
          } else {
            this.$message.error("提交失败，请核对回答id、问题id");
          }
        })
        .catch(err => {
          this.$message.error("提交失败，请核对回答id、问题id");
        });
    },
    indexMethod(index) {
      return index + 1;
    },
    handleSizeChange(value) {
      //   console.log(value);
      this.pageSize = value;
      this.getData();
    },
    getData() {
      Request({
        url: "/answers",
        params: {
          page: this.page,
          size: this.pageSize,
          sortord: this.sortord
        },
        method: "get"
      })
        .then(res => {
          //   格式化数据
          // this.articlesData = this.formatPostTime(res["data"]);
          this.answersData = res["data"];
          this.totalPage = res["totalPage"];
          this.totalNum = res["totalNum"];
          this.loading = false;
        })
        .catch(err => {
          console.log(err);
        });
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
      this.page = currentPage;
    }
  }
};
</script>

<style scoped>
.question-table {
  margin-top: 2rem;
}
.pagination {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>

