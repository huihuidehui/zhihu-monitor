### 知乎运营辅助工具

知乎运营辅助可部署在服务器或个人PC。主要实现的功能如下：

1. 用于监控知乎上某个问题的浏览数、关注数的趋势。

   [<img src="https://z3.ax1x.com/2021/03/21/65S4fg.png" alt="65S4fg.png" style="zoom: 50%;" />](https://imgtu.com/i/65S4fg)

[<img src="https://z3.ax1x.com/2021/03/21/65SXkT.png" alt="65SXkT.png" style="zoom:50%;" />](https://imgtu.com/i/65SXkT)

2. 监控某个回答在其问题下的排名、点赞数、评论数。

[<img src="https://z3.ax1x.com/2021/03/21/65CKTP.png" alt="65CKTP.png" style="zoom: 50%;" />](https://imgtu.com/i/65CKTP)

#### 快速开始

1. 克隆本项目到本地

2. 进入api目录后打开终端

   1. 安装python3依赖(你需要提前安装好python3.7及以上的环境)

      ```
      pip3 install requirements.txt
      ```

      

   2. 使用`flask init`命令初始化项目，依照提示输入用户名和密码即可(更多支持的命令可使用`flask --help`查看)
   3. `flask run`启动后端api

3. 进入front目录后打开终端

   1. 使用`npm install`安装依赖(注意node版本需要低于15，推荐14.15.1)
   2. `npm run serve`
   3. 浏览器输入`127.0.0.1:8080`即可。
   4. 关于使用时的细节
      1. 问题URL是指：像`https://www.zhihu.com/question/60334228`这样的链接，其中的`60334288`作为问题标识不可缺失。
      2. 回答URL是指：像`https://www.zhihu.com/question/60334228/answer/1787732050`这样的链接，其中的`60334288`作为问题标识和`1787732050`作为回答标识均不可缺失。
      3. 特别的，需要先添加`该回答`所属的`问题`后才可添加`该回答`。

#### 技术栈

核心爬取部分使用`Python requests`模块完成，使用`flask_apscheduler`插件完成定时抓取数据更新。后端框架使用`flask-restful`完成`RESTful API`开发，数据存储方面使用`sqlalchemy`框架支持`mysql、sqlite3`数据库，默认使用`sqlite3`可在项目配置文件中更改使用`mysql`。

前端使用`vue.js + bulma`完成，网络请求使用HTTP库`axios`完成。

