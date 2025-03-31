<template>
    <div class="login-container">
        <el-card class="login-card">
            <h2 class="login-title">Login</h2>
            <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="80px">
                <el-form-item label="Username" prop="username">
                    <el-input v-model="loginForm.username" placeholder="Enter your username"></el-input>
                </el-form-item>
                <el-form-item label="Password" prop="password">
                    <el-input
                        v-model="loginForm.password"
                        placeholder="Enter your password"
                        show-password
                        type="password"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleLogin">Login</el-button>
                    <el-button @click="resetForm">Reset</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script>
export default {
    name: "LoginView",
    data() {
        return {
            loginForm: {
                username: "",
                password: "",
            },
            rules: {
                username: [{ required: true, message: "Please input username", trigger: "blur" }],
                password: [{ required: true, message: "Please input password", trigger: "blur" }],
            },
        };
    },
    methods: {
        handleLogin() {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    console.log("Login successful with:", this.loginForm);
                    // Add your login logic here
                } else {
                    console.log("Validation failed");
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.loginForm.resetFields();
        },
    },
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
}

.login-card {
    width: 400px;
    padding: 20px;
}

.login-title {
    text-align: center;
    margin-bottom: 20px;
}
</style>
  