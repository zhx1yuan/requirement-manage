import request from '@/utils/request'
import type { Project } from '@/types'

export function getProjects() {
  return request.get<Project[]>('/projects/')
}

export function createProject(data: Partial<Project>) {
  return request.post<Project>('/projects/', data)
}

export function updateProject(id: number, data: Partial<Project>) {
  return request.put<Project>(`/projects/${id}`, data)
}

export function deleteProject(id: number) {
  return request.delete(`/projects/${id}`)
}

export function getProjectById(id: number) {
  return request.get<Project>(`/projects/${id}`)
} 