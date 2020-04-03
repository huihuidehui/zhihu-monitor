# FROM node:8-slim
# RUN apt-get update  && apt-get install -y nginx
# WORKDIR /usr/src/app
# COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
# RUN npm install
# COPY . .
# RUN npm run build
# RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	# && ln -sf /dev/stderr /var/log/nginx/error.log
# EXPOSE 80
# RUN cp -r dist/* /var/www/html \
    # && rm -rf /user/src/app
 FROM node:12.11.1
 WORKDIR /app
 COPY package.json /app/
 RUN npm config set registry "https://registry.npm.taobao.org/" && npm install
 COPY ./ /app
 RUN npm run build
 #指定nginx配置项目，--from=builder 指的是从上一次 build 的结果中提取了编译结果(FROM node:alpine as builder)，即是把刚刚打>    包生成的dist放进nginx中
 FROM nginx
 COPY --from=0 /app/dist /app
 COPY nginx.conf /etc/nginx/nginx.conf
 EXPOSE 80

CMD ["nginx","-g","daemon off;"]