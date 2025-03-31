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

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { Project } from '@/types'
import { getProjects, createProject, updateProject, deleteProject } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

export default defineComponent({
  name: 'ProjectsView',
  components: {
    Plus
  },
  setup() {
    const loading = ref(false)
    const projects = ref<Project[]>([])
    const dialogVisible = ref(false)
    const dialogType = ref<'create' | 'edit'>('create')
    const formRef = ref<FormInstance>()
    const currentProject = ref<Project | null>(null)

    const form = ref({
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
        projects.value = await getProjects()
      } catch (error) {
        console.error('Failed to fetch projects:', error)
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

    const showEditDialog = (project: Project) => {
      dialogType.value = 'edit'
      currentProject.value = project
      form.value = {
        name: project.name,
        description: project.description
      }
      dialogVisible.value = true
    }

    const handleSubmit = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            if (dialogType.value === 'create') {
              await createProject(form.value)
              ElMessage.success('创建项目成功')
            } else {
              if (currentProject.value) {
                await updateProject(currentProject.value.id, form.value)
                ElMessage.success('更新项目成功')
              }
            }
            dialogVisible.value = false
            fetchProjects()
          } catch (error) {
            console.error('Failed to submit form:', error)
            ElMessage.error(dialogType.value === 'create' ? '创建项目失败' : '更新项目失败')
          }
        }
      })
    }

    const handleDelete = async (project: Project) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除该项目吗？此操作不可恢复。',
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await deleteProject(project.id)
        ElMessage.success('删除项目成功')
        fetchProjects()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Failed to delete project:', error)
          ElMessage.error('删除项目失败')
        }
      }
    }

    onMounted(() => {
      fetchProjects()
    })

    return {
      loading,
      projects,
      dialogVisible,
      dialogType,
      formRef,
      form,
      rules,
      formatDate,
      showCreateDialog,
      showEditDialog,
      handleSubmit,
      handleDelete
    }
  }
})
</script>

<style scoped>
.projects-container {
  max-width: 1200px;
  margin: 0 auto;
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