//登录页
<template>
    <div>
      <h1> 你好！ </h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">Username: </label>
          <input type="text" v-model="username" id="username" required />
        </div>
        <div>
          <label for="password">Password: </label>
          <input type="password" v-model="password" id="password" required />
        </div>
        <button type="submit">登录</button>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  
  const username = ref('')
  const password = ref('')
  const router = useRouter()
  
  const login = async () => {
    try {
        const formData = new URLSearchParams()
            formData.append('username', username.value)
            formData.append('password', password.value)

        const response = await axios.post('http://127.0.0.1:8000/token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
      localStorage.setItem('token', response.data.access_token)
      router.push('/')
    } catch (error) {
      console.error('Login failed:', error)
    }
  }
  </script>
  
  <style scoped>
  </style>