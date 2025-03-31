import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { login as apiLogin, register as apiRegister } from '@/api/auth'
import request from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string) {
    try {
      const response = await apiLogin(username, password)
      console.log('Login response:', response)
      
      if (!response || !response.data || !response.data.access_token) {
        throw new Error('登录响应数据格式错误')
      }
      
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      
      // 获取用户信息
      const userResponse = await request.get<User>('/users/me/')
      console.log('User info response:', userResponse)
      
      if (!userResponse || !userResponse.data) {
        throw new Error('获取用户信息失败')
      }
      
      user.value = userResponse.data
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function register(username: string, password: string) {
    try {
      await apiRegister(username, password)
      // 注册成功后自动登录
      await login(username, password)
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout
  }
}) 