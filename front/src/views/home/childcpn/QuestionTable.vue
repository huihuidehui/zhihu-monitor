<template>
  <!-- <div>table</div> -->
  <!-- <el-table></el-table> -->
  <div>
    <div style="margin-top:2rem">
      <p class="is-size-6">添加监控的问题</p>
      <el-input v-model="questionId" placeholder="输入问题id"></el-input>
      <!-- <el-input v-model="answerName" placeholder="输入作者的知乎昵称"></el-input> -->
      <el-button type="primary" size="mini" round v-on:click="addNewQuestion">提交</el-button>
    </div>
    <div class="question-table">
      <p class="title is-size-5">监控问题</p>
      <el-table v-loading="loading" :border="true" :data="questionsData" style="width: 100%">
        <el-table-column type="index" :index="indexMethod"></el-table-column>
        <el-table-column prop="title" label="标题"></el-table-column>
        <el-table-column prop="questionId" label="问题id"></el-table-column>

        <el-table-column label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
            <el-button type="text" size="small" @click="deleteQuestion(scope.row)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- <div class="block"> -->
      <!-- <span class="demonstration">页数较少时的效果</span> -->
      <!-- </div> -->
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
  name: "QuestionTable",
  data() {
    return {
      questionId: "",
      questionsData: [],
      page: 1,
      currentPage: 1,
      totalPage: 0,
      totalNum: 0,
      loading: true,
      pageSize: 10
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
    handleClick(data) {
      this.$router.push({
        path: "showquestion",
        query: {
          questionId: data.questionId
        }
      });
    },
     deleteQuestion(data) {
      Request({
        url: "/question",
        method: "delete",
        data: {
          id: data.questionId,
        }
      }).then(res => {
        if (res.res == 1) {
          this.$message({
            message: "恭喜你，提交成功",
            type: "success"
          });
          this.getData();
        } else {
          this.$message.error("提交失败，请核对问题id");
        }
      }).catch(err=>{
          this.$message.error("提交失败，请核对问题id");
      })
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
        url: "/questions",
        params: {
          page: this.page,
          size: this.pageSize
        },
        method: "get"
      })
        .then(res => {
          //   格式化数据
          // this.articlesData = this.formatPostTime(res["data"]);
          this.questionsData = res["data"];
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
    },
    addNewQuestion() {
      Request({
        url: "/question",
        method: "put",
        data: {
          id: this.questionId
          // answerName: this.answerName
        }
      })
        .then(res => {
          if (res.res == 1) {
            this.getData();
            this.questionId = "";
            this.$message({
              message: "恭喜你，提交成功",
              type: "success"
            });
          } else {
            this.$message.error("提交失败，请核对问题id");
          }
        })
        .catch(err => {
          console.log(err);
          this.$message.error("提交失败，请核对问题id");
        });
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

