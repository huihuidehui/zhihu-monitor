import axios from "axios";
import store from "store/index.js"
import router from "router/index.js"
export function Request(config) {
  // 1.创建axios的实例
  const instance = axios.create({
    baseURL: "http://120.55.45.233:5000",
    timeout: 50000
  });
  //   axios的拦截器
  // 请求拦截的作用
  instance.interceptors.request.use(
    config => {
    //   startLoading();
    //   给每个请求添加token
      if (store.state.token !== "") {
        config.headers.Authorization = "Bearer " + store.state.token
      }
      return config;
    },
    err => {
      console.log(err);
    }
  );
  //   响应拦截
  instance.interceptors.response.use(
    res => {
    //   endLoading();
      return res.data;
    },
    err => {
    //   endLoading();
      if (err.response.status == 401) {
        // 跳转到登陆页面
        router.push({ path: "/login" });
        return Promise.reject(err.response.data)
      }
      return Promise.reject(err.response.data) // 返回接口返回的错误信息
    }
    // }
  );
  //   发送真正的请求
  return instance(config);
}
