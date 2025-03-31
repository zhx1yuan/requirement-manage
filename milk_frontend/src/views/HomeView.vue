<template>
  <div class="home-container">
    <el-row :gutter="20">
      <!-- 最近访问的项目 -->
      <el-col :span="12">
        <el-card class="recent-projects">
          <template #header>
            <div class="card-header">
              <span>最近访问的项目</span>
              <el-button type="primary" @click="$router.push('/projects')">
                查看全部
              </el-button>
            </div>
          </template>
          <el-empty v-if="!recentProjects.length" description="暂无最近访问的项目" />
          <el-table v-else :data="recentProjects" style="width: 100%">
            <el-table-column prop="name" label="项目名称">
              <template #default="{ row }">
                <el-link type="primary" @click="$router.push(`/projects/${row.id}`)">
                  {{ row.name }}
                </el-link>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column prop="updated_at" label="更新时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.updated_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 最近访问的文档 -->
      <el-col :span="12">
        <el-card class="recent-documents">
          <template #header>
            <div class="card-header">
              <span>最近访问的文档</span>
            </div>
          </template>
          <el-empty v-if="!recentDocuments.length" description="暂无最近访问的文档" />
          <el-table v-else :data="recentDocuments" style="width: 100%">
            <el-table-column prop="title" label="文档标题">
              <template #default="{ row }">
                <el-link type="primary" @click="$router.push(`/documents/${row.id}`)">
                  {{ row.title }}
                </el-link>
              </template>
            </el-table-column>
            <el-table-column prop="version" label="版本" width="80" />
            <el-table-column prop="updated_at" label="更新时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.updated_at) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速操作 -->
    <el-card class="quick-actions">
      <template #header>
        <div class="card-header">
          <span>快速操作</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-button type="primary" @click="$router.push('/projects')">
            <el-icon><Folder /></el-icon>
            创建项目
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button type="success" @click="$router.push('/projects')">
            <el-icon><Document /></el-icon>
            创建文档
          </el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Folder, Document } from '@element-plus/icons-vue'
import type { Project, Document as DocumentType } from '@/types'
import { getProjects } from '@/api/project'
import { getDocument } from '@/api/document'

const recentProjects = ref<Project[]>([])
const recentDocuments = ref<DocumentType[]>([])

const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

const fetchData = async () => {
  try {
    // 获取最近的项目
    const projectsResponse = await getProjects()
    recentProjects.value = projectsResponse.data.slice(0, 5) // 只显示最近5个

    // 获取最近的文档
    // TODO: 需要后端提供获取最近文档列表的API
    // 暂时使用空数组
    recentDocuments.value = []
  } catch (error) {
    console.error('Failed to fetch data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recent-projects,
.recent-documents,
.quick-actions {
  margin-bottom: 20px;
}

.quick-actions .el-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
