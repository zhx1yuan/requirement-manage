import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { login as loginApi, register as registerApi } from '@/api/auth'
import request from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  // 获取用户信息
  async function fetchUserInfo() {
    try {
      const response = await request.get<User>('/users/me/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      user.value = null
    }
  }

  async function login(username: string, password: string) {
    try {
      const response = await loginApi(username, password)
      token.value = response.data.access_token
      localStorage.setItem('token', response.data.access_token)
      // 登录成功后获取用户信息
      await fetchUserInfo()
      return true
    } catch (error) {
      return false
    }
  }

  async function register(username: string, password: string) {
    try {
      const response = await registerApi(username, password)
      // 注册成功后自动登录
      await login(username, password)
      return true
    } catch (error) {
      return false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  // 初始化时如果有token，获取用户信息
  if (token.value) {
    fetchUserInfo()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserInfo
  }
}) 