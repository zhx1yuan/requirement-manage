import request from '@/utils/request'
import type { User } from '@/types'

interface LoginResponse {
  access_token: string
  token_type: string
}

export function login(username: string, password: string) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)
  
  return request.post<LoginResponse>('/token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

export function register(username: string, password: string) {
  return request.post<User>('/users/', {
    username,
    password
  })
} 