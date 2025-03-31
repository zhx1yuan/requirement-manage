<template>
  <div class="document-detail">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="10" animated />
    </div>
    <template v-else>
      <div v-if="isEditing" class="editor-container">
        <DocumentEditor
          :document-id="documentId"
          :initial-content="document.content"
          :initial-title="document.title"
          @save="handleSave"
          @cancel="handleCancel"
        />
      </div>
      <div v-else class="view-container">
        <div class="document-header">
          <h1>{{ document.title }}</h1>
          <div class="document-actions">
            <el-button type="primary" @click="startEditing">编辑</el-button>
            <el-button @click="handleBack">返回</el-button>
          </div>
        </div>
        <div class="document-meta">
          <span>创建者：{{ document.creator.username }}</span>
          <span>创建时间：{{ formatDate(document.created_at) }}</span>
          <span>最后更新：{{ formatDate(document.updated_at) }}</span>
        </div>
        <div class="document-content markdown-body" v-html="renderedContent"></div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getDocument } from '@/api/document'
import DocumentEditor from '@/components/DocumentEditor.vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import type { Document } from '@/types'

const route = useRoute()
const router = useRouter()
const documentId = Number(route.params.id)

const loading = ref(true)
const document = ref<Document>({
  id: 0,
  title: '',
  content: '',
  project_id: 0,
  creator_id: 0,
  creator: { id: 0, username: '' },
  created_at: '',
  updated_at: '',
  versions: [],
  permissions: [],
  locks: []
})
const isEditing = ref(false)

// 配置 marked 选项
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持 GitHub 风格的 Markdown
  sanitize: false // 我们使用 DOMPurify 来处理安全性
})

// 渲染 Markdown 内容
const renderedContent = computed(() => {
  const rawHtml = marked(document.value.content)
  return DOMPurify.sanitize(rawHtml, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'p', 'br', 'strong', 'em', 'code', 'pre',
      'blockquote', 'ul', 'ol', 'li',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'a', 'img'
    ],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'target']
  })
})

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

// 获取文档详情
const fetchDocument = async () => {
  try {
    loading.value = true
    const response = await getDocument(documentId)
    document.value = response.data
  } catch (error) {
    ElMessage.error('获取文档失败')
  } finally {
    loading.value = false
  }
}

// 开始编辑
const startEditing = () => {
  isEditing.value = true
}

// 处理保存
const handleSave = (content: string, title: string) => {
  document.value.content = content
  document.value.title = title
  isEditing.value = false
  ElMessage.success('保存成功')
}

// 处理取消
const handleCancel = () => {
  isEditing.value = false
  ElMessage.warning('已取消编辑')
}

// 返回上一页
const handleBack = () => {
  router.back()
}

onMounted(() => {
  fetchDocument()
})
</script>

<style scoped>
.document-detail {
  height: 100%;
  padding: 20px;
  background-color: #fff;
}

.loading-container {
  padding: 20px;
}

.document-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.document-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.document-actions {
  display: flex;
  gap: 8px;
}

.document-meta {
  margin-bottom: 20px;
  color: #909399;
  font-size: 14px;
}

.document-meta span {
  margin-right: 20px;
}

.document-content {
  line-height: 1.6;
  color: #303133;
}

.editor-container {
  height: 100%;
}

.view-container {
  height: 100%;
  overflow-y: auto;
}

:deep(.markdown-body) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  word-wrap: break-word;
}

:deep(.markdown-body h1) {
  font-size: 2em;
  margin: 0.67em 0;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

:deep(.markdown-body h2) {
  font-size: 1.5em;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

:deep(.markdown-body p) {
  margin-top: 0;
  margin-bottom: 16px;
}

:deep(.markdown-body code) {
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
}

:deep(.markdown-body pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: #f6f8fa;
  border-radius: 3px;
}

:deep(.markdown-body pre code) {
  padding: 0;
  margin: 0;
  font-size: 100%;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border: 0;
}
</style> 