import Vue from "vue";
import VueRouter from "vue-router";
import store from "store/index.js";

const Home = () => import("../views/home/Home.vue");
const Login = () => import("../views/login/Login.vue");
const QuestionView = () => import("../views/question/QuestionView");
const AnswerView = () => import("../views/answer/AnswerView");
Vue.use(VueRouter);
let routes = [
  {
    path: "/",
    redirect: "/home"
  },
  {
    // name: '404',
    path: "/home",
    component: Home
  },
  {
    path: "/login",
    component: Login
  },
  {
    path: "/showquestion",
    component: QuestionView
  },
  {
    path: "/showanswer",
    component: AnswerView
  }
  // {
  // path: "*", // 此处需特别注意至于最底部
  // redirect: "/404"
  // }
];
const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes: routes,
  // 切换路由后页面返回顶部
  scrollBehavior(to, from, savedPosition) {
    // return 期望滚动到哪个的位置
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});

router.beforeEach((to, from, next) => {
  // if (to.meta.hasOwnProperty("requireAuth")) {
  // if(from)
  // console.log(to);
  if (to.path == "/login") {
    next();
  } else {
    //   请求要求权限的路由，判断是否有权限
    if (store.state.token !== "") {
      //     // token值不为空时
      //     // console.log(store.state.token);
      next();
    } else {
      // console.log("没有权限")
      router.push({ path: "/login" });
    }
  }
  // }
  next();
});
export default router;
