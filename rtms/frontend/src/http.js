import axios from 'axios'

// axios 配置
axios.defaults.timeout = 5000;
axios.defaults.baseURL = 'http://172.17.160.36:8000';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        if (localStorage.token) {
            config.headers.Authorization = `token ${localStorage.token}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    });

export default axios;
