export interface User {
  id: number
  username: string
  email?: string
  is_active?: boolean
  is_superuser?: boolean
  created_at?: string
  updated_at?: string
}

export interface Project {
  id: number
  name: string
  description?: string
  creator_id: number
  creator?: User
  created_at: string
  updated_at: string
}

export interface List {
  id: number
  name: string
  description?: string
  project_id: number
  project?: Project
  creator_id: number
  creator?: User
  created_at: string
  updated_at: string
}

export interface Document {
  id: number
  title: string
  content: string
  project_id: number
  project?: Project
  creator_id: number
  creator: User
  created_at: string
  updated_at: string
  versions: DocumentVersion[]
  permissions: DocumentPermission[]
  locks: DocumentLock[]
}

export interface DocumentVersion {
  id: number
  document_id: number
  document?: Document
  version: number
  title: string
  content: string
  comment?: string
  creator_id: number
  creator?: User
  created_at: string
}

export interface DocumentPermission {
  id: number
  document_id: number
  document?: Document
  user_id: number
  user?: User
  can_read: boolean
  can_write: boolean
  can_delete: boolean
  created_at: string
  updated_at: string
}

export interface DocumentLock {
  id: number
  document_id: number
  document?: Document
  user_id: number
  user?: User
  locked_at: string
  expires_at: string
} 