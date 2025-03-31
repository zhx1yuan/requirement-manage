import request from '@/utils/request'
import type { Document, DocumentVersion, DocumentPermission } from '@/types'

export function getDocument(id: number) {
  return request.get<Document>(`/api/documents/${id}`)
}

export function createDocument(data: {
  title: string
  content: string
  list_id: number
}) {
  return request.post<Document>('/api/documents', data)
}

export function updateDocument(
  id: number,
  data: {
    title?: string
    content?: string
    comment?: string
  }
) {
  return request.put<Document>(`/api/documents/${id}`, data)
}

export function deleteDocument(id: number) {
  return request.delete(`/api/documents/${id}`)
}

export function getDocumentVersions(id: number) {
  return request.get<DocumentVersion[]>(`/api/documents/${id}/versions`)
}

export function restoreDocumentVersion(documentId: number, version: number) {
  return request.post<Document>(`/api/documents/${documentId}/versions/${version}`)
}

export function getDocumentPermissions(id: number) {
  return request.get<DocumentPermission[]>(`/api/documents/${id}/permissions`)
}

export function setDocumentPermission(
  id: number,
  data: {
    user_id: number
    permission_level: 'READ' | 'WRITE' | 'ADMIN'
  }
) {
  return request.post<DocumentPermission>(`/api/documents/${id}/permissions`, data)
}

export function acquireDocumentLock(id: number) {
  return request.post(`/api/documents/${id}/lock`)
}

export function releaseDocumentLock(id: number) {
  return request.delete(`/api/documents/${id}/lock`)
} 