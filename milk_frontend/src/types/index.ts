export interface User {
  id: number
  username: string
  created_at: string
}

export interface Project {
  id: number
  name: string
  description: string
  owner_id: number
  created_at: string
  updated_at: string
}

export interface List {
  id: number
  name: string
  project_id: number
  parent_id: number | null
  level_id: number
  order_index: number
  is_ordered: boolean
  created_at: string
  updated_at: string
  children?: List[]
}

export interface Document {
  id: number
  title: string
  content: string
  list_id: number
  creator_id: number
  version: number
  is_deleted: boolean
  created_at: string
  updated_at: string
}

export interface DocumentVersion {
  id: number
  document_id: number
  title: string
  content: string
  version: number
  created_by_id: number
  comment: string | null
  created_at: string
}

export interface DocumentPermission {
  id: number
  document_id: number
  user_id: number
  permission_level: 'READ' | 'WRITE' | 'ADMIN'
  created_at: string
}

export interface DocumentLock {
  id: number
  document_id: number
  user_id: number
  locked_at: string
  expires_at: string
  is_active: boolean
} 