import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/stores/user'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 5000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    // 添加调试信息
    console.log('Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data,
      baseURL: config.baseURL
    })
    // 确保GET请求不会被缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 添加调试信息
    console.log('Response:', {
      status: response.status,
      headers: response.headers,
      data: response.data,
      config: response.config
    })
    return response
  },
  error => {
    console.error('Response Error:', {
      message: error.message,
      config: error.config,
      response: error.response,
      request: error.request
    })
    
    if (error.response) {
      switch (error.response.status) {
        case 401:
          const userStore = useUserStore()
          userStore.logout()
          router.push({
            name: 'login',
            query: { redirect: router.currentRoute.value.fullPath }
          })
          ElMessage.error('登录已过期，请重新登录')
          break
        case 403:
          ElMessage.error('没有权限执行此操作')
          break
        case 404:
          ElMessage.error(`请求的资源不存在: ${error.config.url}`)
          break
        case 409:
          ElMessage.error('资源冲突')
          break
        case 422:
          ElMessage.error('数据验证失败')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(error.response.data.detail || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('服务器无响应，请检查服务器是否正常运行')
    } else {
      ElMessage.error('请求配置错误：' + error.message)
    }
    return Promise.reject(error)
  }
)

export default request 