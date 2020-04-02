<template>
  <div>
    <p class="icon-header">信息面板</p>
    <div class="columns">
      <div class="column">
        <div class="icon">
          <span>
            <i class="fa fa-file fa-3x has-text-link"></i>
          </span>
        </div>
        <div>
          <p>监控问题数</p>
          <span class="is-size-5">{{questionsNum}}</span>
          <!-- <p>篇文章</p> -->
        </div>
      </div>
      <div class="column">
        <div class="icon">
          <span>
            <i class="fa fa-star fa-3x has-text-primary"></i>
          </span>
        </div>
        <div>
          <p>监控回答数</p>
          <span class="is-size-5">{{answersNum}}</span>
        </div>
      </div>
      <div class="column">
        <div class="icon">
          <span>
            <i class="fa fa-tag fa-3x has-text-info"></i>
          </span>
        </div>
        <div>
          <p>Test</p>
          <span class="is-size-5">0</span>
        </div>
      </div>
      <div class="column">
        <div class="icon">
          <span>
            <i class="fa fa-comment fa-3x has-text-primary"></i>
          </span>
        </div>
        <div>
          <p>Test</p>
          <span class="is-size-5">0</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Request } from "network/request.js";
export default {
  name: "IconCard",
  data() {
    return {
      questionsNum: 0,
      answersNum: 0,
      // tagsNum: 0,
      // likesNum: 0
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.getAnswerQuestionNum();
      // this.getAnswerNum();
  //     this.getTagNum();
  //     this.getLikeNum();
    },
    getAnswerQuestionNum(){
      Request({
        url:"/questions",
        method:'get'
      }).then(res=>{
        // console.log(res)
        this.questionsNum = res['totalNum']
      })
      Request({
        url:"/answers",
        method:'get'
      }).then(res=>{
        this.answersNum = res['totalNum']
      })
    }
  }
  //   getArticleNum() {
  //     adminRequest({
  //       url: "/articles",
  //       method: "get"
  //     })
  //       .then(res => {
  //         this.articlesNum = res["totalNum"];
  //       })
  //       .catch(err => {
  //         // console.log(err);
  //       });
  //   },
  //   getCategoryNum() {
  //     adminRequest({
  //       url: "/categories",
  //       method: "get"
  //     }).then(res => {
  //       this.categoriesNum = res["totalNum"];
  //     });
  //   },
  //   getTagNum() {
  //     adminRequest({
  //       url: "/tags",
  //       method: "get"
  //     }).then(res => {
  //       this.tagsNum = res["totalNum"];
  //     });
  //   },
  //   getLikeNum() {
  //     adminRequest({
  //       url: "/likes",
  //       method: "get"
  //     }).then(res => {
  //       this.likesNum = res["likesNum"];
  //     });
  //   }
  // }
};
</script>

<style lang="less" scoped>
.column {
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-right: 0.5rem;
  margin-left: 0.5rem;
  border-radius: 4px;
  padding-left: 1rem;
  padding-right: 2rem;
  padding-top: 2rem;
  padding-bottom: 2rem;
}
.column div p {
  color: #777;
}
.icon {
  height: 105%;
  width: 30%;
  // background-color: red;
  border-radius: 4px;
}
.is-size-5 {
  font-weight: 700;
  color: #666;
}
.icon-header {
  color:#111;
  font-size: 1.35rem;
  margin-bottom: 1.5rem;
  font-weight: 700
}
</style>
