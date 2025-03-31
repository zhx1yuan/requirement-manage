<template>
  <div class="project-detail-container">
    <div class="page-header">
      <div class="title-section">
        <h2>{{ project?.name }}</h2>
        <p class="description">{{ project?.description }}</p>
      </div>
      <el-button type="primary" @click="showCreateDocumentDialog">
        <el-icon><Plus /></el-icon>
        创建文档
      </el-button>
    </div>

    <!-- 文档列表 -->
    <el-table
      v-loading="loading"
      :data="documents"
      style="width: 100%"
      border
    >
      <el-table-column prop="title" label="文档标题">
        <template #default="{ row }">
          <el-link type="primary" @click="$router.push(`/documents/${row.id}`)">
            {{ row.title }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="version" label="版本" width="80" />
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
            <el-button type="primary" @click="$router.push(`/documents/${row.id}`)">
              查看
            </el-button>
            <el-button type="danger" @click="handleDeleteDocument(row)">
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建文档对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建文档"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="文档标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="5"
            placeholder="请输入文档内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateDocument">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { Project, Document } from '@/types'
import { getProjects } from '@/api/project'
import { ElMessage, ElMessageBox } from 'element-plus'

export default defineComponent({
  name: 'ProjectDetailView',
  components: {
    Plus
  },
  setup() {
    const route = useRoute()
    const projectId = Number(route.params.projectId)
    
    const loading = ref(false)
    const project = ref<Project | null>(null)
    const documents = ref<Document[]>([])
    const dialogVisible = ref(false)
    const formRef = ref<FormInstance>()

    const form = ref({
      title: '',
      content: ''
    })

    const rules: FormRules = {
      title: [
        { required: true, message: '请输入文档标题', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入文档内容', trigger: 'blur' }
      ]
    }

    const formatDate = (date: string) => {
      return new Date(date).toLocaleString()
    }

    const fetchProjectData = async () => {
      loading.value = true
      try {
        // TODO: 获取项目详情和文档列表
        const projects = await getProjects()
        project.value = projects.find(p => p.id === projectId) || null
        
        // TODO: 获取项目下的文档列表
        documents.value = []
      } catch (error) {
        console.error('Failed to fetch project data:', error)
        ElMessage.error('获取项目数据失败')
      } finally {
        loading.value = false
      }
    }

    const showCreateDocumentDialog = () => {
      form.value = {
        title: '',
        content: ''
      }
      dialogVisible.value = true
    }

    const handleCreateDocument = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            // TODO: 创建文档
            dialogVisible.value = false
            fetchProjectData()
            ElMessage.success('创建文档成功')
          } catch (error) {
            console.error('Failed to create document:', error)
            ElMessage.error('创建文档失败')
          }
        }
      })
    }

    const handleDeleteDocument = async (document: Document) => {
      try {
        await ElMessageBox.confirm(
          '确定要删除该文档吗？此操作不可恢复。',
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        // TODO: 删除文档
        fetchProjectData()
        ElMessage.success('删除文档成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('Failed to delete document:', error)
          ElMessage.error('删除文档失败')
        }
      }
    }

    onMounted(() => {
      fetchProjectData()
    })

    return {
      project,
      documents,
      loading,
      dialogVisible,
      formRef,
      form,
      rules,
      formatDate,
      showCreateDocumentDialog,
      handleCreateDocument,
      handleDeleteDocument
    }
  }
})
</script>

<style scoped>
.project-detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.title-section {
  flex: 1;
}

.title-section h2 {
  margin: 0 0 8px 0;
}

.description {
  margin: 0;
  color: #666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 