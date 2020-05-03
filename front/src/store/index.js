import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    // token: window.localStorage.getItem("token"),
    token:
      window.localStorage.getItem("token") == null
        ? ""
        : window.localStorage.getItem("token"),
    // 发布文章后的提示信息
    postInfo: "",
    username: window.localStorage.getItem("username") == null
    ? ""
    : window.localStorage.getItem("username"),
    // 用于全局loading
    // loadingNum: 0
  },
  mutations: {
    changeUsername(state, newName) {
      state.username = newName;
    },
    changeToken(state, newToken) {
      state.token = newToken;
    },
    changePostInfo(state, newMessage) {
      state.postInfo = newMessage;
    },
    addLoadingNum(state) {
      state.loading += 1;
    },
    subLoadingNum(state) {
      state.loadingNum -= 1;
    },
  },
});

export default store;
