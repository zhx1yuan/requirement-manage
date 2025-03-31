<template>
  <div class="projects-container">
    <div class="page-header">
      <h2>项目列表</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        创建项目
      </el-button>
    </div>

    <!-- 项目列表 -->
    <el-table
      v-loading="loading"
      :data="projects"
      style="width: 100%"
      border
    >
      <el-table-column prop="name" label="项目名称">
        <template #default="{ row }">
          <el-link type="primary" @click="$router.push(`/projects/${row.id}`)">
            {{ row.name }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="$router.push(`/projects/${row.id}`)">
              查看
            </el-button>
            <el-button type="warning" @click="showEditDialog(row)">
              编辑
            </el-button>
            <el-button type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑项目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建项目' : '编辑项目'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入项目描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { Project } from '@/types'
import { getProjects, createProject, updateProject, deleteProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute } from 'vue-router'

const loading = ref(false)
const projects = ref<Project[]>([])
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const formRef = ref<FormInstance>()
const form = ref<Partial<Project>>({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '长度不能超过 200 个字符', trigger: 'blur' }
  ]
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

const fetchProjects = async () => {
  loading.value = true
  try {
    console.log('开始获取项目列表...')
    const response = await getProjects()
    console.log('获取到的项目数据:', response.data)
    projects.value = response.data.map(project => ({
      ...project,
      description: project.description || ''
    }))
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  dialogType.value = 'create'
  form.value = {
    name: '',
    description: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (row: Project) => {
  dialogType.value = 'edit'
  form.value = {
    name: row.name,
    description: row.description || ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        console.log('提交的表单数据:', form.value)
        if (dialogType.value === 'create') {
          const response = await createProject(form.value)
          console.log('创建项目响应:', response.data)
          ElMessage.success('创建成功')
        } else {
          const response = await updateProject(form.value.id!, form.value)
          console.log('更新项目响应:', response.data)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await fetchProjects()
      } catch (error) {
        console.error('提交表单失败:', error)
        ElMessage.error(dialogType.value === 'create' ? '创建失败' : '更新失败')
      }
    }
  })
}

const handleDelete = async (row: Project) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await deleteProject(row.id)
    ElMessage.success('删除成功')
    fetchProjects()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete project:', error)
      ElMessage.error('删除失败')
    }
  }
}

const route = useRoute()
watch(() => route.path, () => {
  console.log('路由变化，重新获取项目列表')
  fetchProjects()
})

onMounted(() => {
  console.log('组件挂载，获取项目列表')
  fetchProjects()
})
</script>

<style scoped>
.projects-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 