<template>
  <div class="document-editor">
    <div class="editor-header">
      <el-input
        v-model="title"
        placeholder="文档标题"
        class="title-input"
        @change="handleTitleChange"
      />
      <div class="editor-actions">
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </div>
    </div>
    <div class="editor-container" ref="editorContainer"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as monaco from 'monaco-editor'
import { ElMessage } from 'element-plus'
import { updateDocument } from '@/api/document'

const props = defineProps<{
  documentId: number
  initialContent: string
  initialTitle: string
}>()

const emit = defineEmits<{
  (e: 'save', content: string, title: string): void
  (e: 'cancel'): void
}>()

const editorContainer = ref<HTMLElement | null>(null)
const editor = ref<monaco.editor.IStandaloneCodeEditor | null>(null)
const title = ref(props.initialTitle)
const content = ref(props.initialContent)

// 初始化编辑器
onMounted(() => {
  if (editorContainer.value) {
    editor.value = monaco.editor.create(editorContainer.value, {
      value: content.value,
      language: 'markdown',
      theme: 'vs',
      automaticLayout: true,
      minimap: {
        enabled: true
      },
      scrollBeyondLastLine: false,
      fontSize: 14,
      lineNumbers: 'on',
      roundedSelection: false,
      scrollbar: {
        vertical: 'visible',
        horizontal: 'visible'
      }
    })

    // 监听内容变化
    editor.value.onDidChangeModelContent(() => {
      content.value = editor.value?.getValue() || ''
    })
  }
})

// 清理编辑器
onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.dispose()
  }
})

// 监听初始内容变化
watch(() => props.initialContent, (newContent) => {
  if (editor.value && newContent !== content.value) {
    content.value = newContent
    editor.value.setValue(newContent)
  }
})

// 处理标题变化
const handleTitleChange = async () => {
  try {
    await updateDocument(props.documentId, {
      title: title.value
    })
    ElMessage.success('标题已更新')
  } catch (error) {
    ElMessage.error('更新标题失败')
  }
}

// 处理保存
const handleSave = async () => {
  try {
    await updateDocument(props.documentId, {
      content: content.value,
      title: title.value
    })
    ElMessage.success('保存成功')
    emit('save', content.value, title.value)
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 处理取消
const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.document-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #fff;
}

.editor-header {
  display: flex;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #dcdfe6;
}

.title-input {
  flex: 1;
  margin-right: 16px;
}

.editor-actions {
  display: flex;
  gap: 8px;
}

.editor-container {
  flex: 1;
  min-height: 0;
}
</style> 