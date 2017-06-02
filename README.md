# rtms
基于vuejs+elementUI+django+restframework+celery+uwsgi框架的pythonweb项目                                                                     这个一个前后端完全分离的项目。前端通过axios请求,发送api的数据，后端通过restframework处理api数据返回jsonResponse。    
前端使用vuejs和elementUI,从而摈弃了django中的模板
详细架构，前后端交互及celery使用可参见图片
前端nodejs安装过程：
yum install nodejs
yum install npm
npm install -g vue-cli
npm install vue-router
pip2.7 install django-cors-headers   参见https://zhuanlan.zhihu.com/p/25080236
django环境搭建参见README.rst requirements.txt
