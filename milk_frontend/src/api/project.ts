import request from '@/utils/request'
import type { Project } from '@/types'

export function getProjects(): Promise<Project[]> {
  return request.get('/api/projects')
}

export function createProject(data: { name: string; description?: string }): Promise<Project> {
  return request.post('/api/projects', data)
}

export function updateProject(id: number, data: { name?: string; description?: string }): Promise<Project> {
  return request.put(`/api/projects/${id}`, data)
}

export function deleteProject(id: number): Promise<void> {
  return request.delete(`/api/projects/${id}`)
} 