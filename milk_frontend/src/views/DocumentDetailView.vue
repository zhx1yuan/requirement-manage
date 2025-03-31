<template>
  <div class="document-detail-container">
    <div class="page-header">
      <div class="title-section">
        <h2>{{ document?.title }}</h2>
        <p class="meta">
          版本：{{ document?.version }} | 
          更新时间：{{ formatDate(document?.updated_at) }}
        </p>
      </div>
      <div class="actions">
        <el-button-group>
          <el-button type="primary" @click="handleSave" :loading="saving">
            <el-icon><Save /></el-icon>
            保存
          </el-button>
          <el-button @click="showVersionHistory">
            <el-icon><Timer /></el-icon>
            历史版本
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 文档编辑器 -->
    <div class="editor-container">
      <el-input
        v-model="title"
        placeholder="请输入文档标题"
        class="title-input"
      />
      <el-input
        v-model="content"
        type="textarea"
        :rows="20"
        placeholder="请输入文档内容"
        class="content-input"
      />
    </div>

    <!-- 历史版本对话框 -->
    <el-dialog
      v-model="versionDialogVisible"
      title="历史版本"
      width="800px"
    >
      <el-table
        :data="versions"
        style="width: 100%"
        border
      >
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="title" label="标题" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" @click="handleRestore(row)">
              恢复
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 恢复版本确认对话框 -->
    <el-dialog
      v-model="restoreDialogVisible"
      title="恢复版本"
      width="500px"
    >
      <el-form
        ref="restoreFormRef"
        :model="restoreForm"
        :rules="restoreRules"
        label-width="80px"
      >
        <el-form-item label="备注" prop="comment">
          <el-input
            v-model="restoreForm.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入恢复版本的备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="restoreDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRestoreConfirm">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Document, Timer } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { Document as DocumentType, DocumentVersion } from '@/types'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'DocumentDetailView',
  components: {
    Save: Document,
    Timer
  },
  setup() {
    const route = useRoute()
    const documentId = Number(route.params.documentId)
    
    const loading = ref(false)
    const saving = ref(false)
    const document = ref<DocumentType | null>(null)
    const versions = ref<DocumentVersion[]>([])
    const versionDialogVisible = ref(false)
    const restoreDialogVisible = ref(false)
    const restoreFormRef = ref<FormInstance>()
    const selectedVersion = ref<DocumentVersion | null>(null)

    const title = ref('')
    const content = ref('')
    
    const restoreForm = ref({
      comment: ''
    })

    const restoreRules: FormRules = {
      comment: [
        { required: true, message: '请输入恢复版本的备注', trigger: 'blur' },
        { max: 200, message: '长度不能超过 200 个字符', trigger: 'blur' }
      ]
    }

    const formatDate = (date?: string) => {
      if (!date) return ''
      return new Date(date).toLocaleString()
    }

    const fetchDocument = async () => {
      loading.value = true
      try {
        // TODO: 获取文档详情
        document.value = {
          id: documentId,
          title: '',
          content: '',
          list_id: 0,
          creator_id: 0,
          version: 1,
          is_deleted: false,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        title.value = document.value.title
        content.value = document.value.content
      } catch (error) {
        console.error('Failed to fetch document:', error)
        ElMessage.error('获取文档失败')
      } finally {
        loading.value = false
      }
    }

    const handleSave = async () => {
      saving.value = true
      try {
        // TODO: 保存文档
        ElMessage.success('保存成功')
      } catch (error) {
        console.error('Failed to save document:', error)
        ElMessage.error('保存失败')
      } finally {
        saving.value = false
      }
    }

    const showVersionHistory = async () => {
      try {
        // TODO: 获取历史版本列表
        versions.value = []
        versionDialogVisible.value = true
      } catch (error) {
        console.error('Failed to fetch versions:', error)
        ElMessage.error('获取历史版本失败')
      }
    }

    const handleRestore = (version: DocumentVersion) => {
      selectedVersion.value = version
      restoreForm.value.comment = ''
      restoreDialogVisible.value = true
    }

    const handleRestoreConfirm = async () => {
      if (!restoreFormRef.value || !selectedVersion.value) return
      
      await restoreFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            // TODO: 恢复历史版本
            restoreDialogVisible.value = false
            versionDialogVisible.value = false
            fetchDocument()
            ElMessage.success('恢复版本成功')
          } catch (error) {
            console.error('Failed to restore version:', error)
            ElMessage.error('恢复版本失败')
          }
        }
      })
    }

    // 监听标题和内容变化，自动保存
    let saveTimeout: number
    watch([title, content], () => {
      if (saveTimeout) {
        clearTimeout(saveTimeout)
      }
      saveTimeout = window.setTimeout(() => {
        handleSave()
      }, 3000)
    })

    onMounted(() => {
      fetchDocument()
    })

    return {
      document,
      versions,
      loading,
      saving,
      title,
      content,
      versionDialogVisible,
      restoreDialogVisible,
      restoreFormRef,
      restoreForm,
      restoreRules,
      formatDate,
      handleSave,
      showVersionHistory,
      handleRestore,
      handleRestoreConfirm
    }
  }
})
</script>

<style scoped>
.document-detail-container {
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

.meta {
  margin: 0;
  color: #666;
}

.editor-container {
  margin-bottom: 20px;
}

.title-input {
  margin-bottom: 16px;
}

.content-input {
  font-family: monospace;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 