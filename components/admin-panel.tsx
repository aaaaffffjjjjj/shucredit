'use client'

import { useState, useEffect, useCallback } from 'react'
import { Plus, Pencil, Trash2, X, FolderTree, BookOpen, ChevronRight, ChevronDown } from 'lucide-react'
import { apiFetch } from '@/lib/api'

interface AdminModule {
  id: number
  name: string
  required_credits: number
  parent_id: number | null
  college_id: number
  children_count: number
}

interface AdminCourse {
  id: number
  course_code: string
  name: string
  credit: number
  module_id: number | null
  module_path: string
}

type TabKey = 'modules' | 'courses'

interface AdminPanelProps {
  open: boolean
  onClose: () => void
  onDataChanged?: () => void
}

interface ModuleFormData {
  name: string
  required_credits: number
  parent_id: number | null
}

interface CourseFormData {
  course_code: string
  name: string
  credit: number
  module_id: number | null
}

function buildModuleTree(modules: AdminModule[]) {
  const map = new Map<number, AdminModule & { children: (AdminModule & { children: any[] })[] }>()
  const roots: (AdminModule & { children: any[] })[] = []

  for (const m of modules) {
    map.set(m.id, { ...m, children: [] })
  }

  for (const m of map.values()) {
    if (m.parent_id !== null && map.has(m.parent_id)) {
      map.get(m.parent_id)!.children.push(m)
    } else {
      roots.push(m)
    }
  }

  return roots
}

function TreeNode({
  node,
  depth,
  onEdit,
  onAddChild,
  onDelete,
}: {
  node: AdminModule & { children: any[] }
  depth: number
  onEdit: (m: AdminModule) => void
  onAddChild: (parentId: number) => void
  onDelete: (m: AdminModule) => void
}) {
  const [expanded, setExpanded] = useState(depth < 2)

  return (
    <div>
      <div
        className="flex items-center gap-2 py-2 px-2 rounded-lg hover:bg-white/5 group transition-colors"
        style={{ paddingLeft: `${depth * 20 + 8}px` }}
      >
        {node.children.length > 0 ? (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-white/40 hover:text-white/70 transition-colors"
          >
            {expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
        ) : (
          <span className="w-4" />
        )}
        <span className="flex-1 text-sm text-white/80 truncate">{node.name}</span>
        <span className="text-xs text-white/40 shrink-0">{node.required_credits} 学分</span>

        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
          <button
            onClick={() => onAddChild(node.id)}
            className="p-1 rounded text-white/40 hover:text-white hover:bg-white/10"
            title="添加子模块"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onEdit(node)}
            className="p-1 rounded text-white/40 hover:text-white hover:bg-white/10"
            title="编辑"
          >
            <Pencil className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onDelete(node)}
            className="p-1 rounded text-white/40 hover:text-red-400 hover:bg-white/10"
            title="删除"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {expanded &&
        node.children.map((child: any) => (
          <TreeNode
            key={child.id}
            node={child}
            depth={depth + 1}
            onEdit={onEdit}
            onAddChild={onAddChild}
            onDelete={onDelete}
          />
        ))}
    </div>
  )
}

function ModuleFormModal({
  open,
  onClose,
  onSave,
  initial,
  modules,
}: {
  open: boolean
  onClose: () => void
  onSave: (data: ModuleFormData) => void
  initial?: ModuleFormData & { id?: number }
  modules: AdminModule[]
}) {
  const [name, setName] = useState(initial?.name || '')
  const [credits, setCredits] = useState(initial?.required_credits || 0)
  const [parentId, setParentId] = useState<number | null>(initial?.parent_id ?? null)

  useEffect(() => {
    if (open) {
      setName(initial?.name || '')
      setCredits(initial?.required_credits || 0)
      setParentId(initial?.parent_id ?? null)
    }
  }, [open, initial])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative bg-zinc-900 border border-white/15 rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">
            {initial?.id ? '编辑模块' : '添加模块'}
          </h3>
          <button onClick={onClose} className="text-white/40 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-1">模块名称</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
              placeholder="例：公共基础课"
            />
          </div>

          <div>
            <label className="block text-sm text-white/60 mb-1">要求学分</label>
            <input
              type="number"
              value={credits}
              onChange={(e) => setCredits(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
              min={0}
              step={0.5}
            />
          </div>

          <div>
            <label className="block text-sm text-white/60 mb-1">父模块</label>
            <select
              value={parentId ?? ''}
              onChange={(e) => setParentId(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
            >
              <option value="">无（顶级模块）</option>
              {modules
                .filter((m) => m.id !== initial?.id)
                .map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name}
                  </option>
                ))}
            </select>
          </div>
        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-sm text-white/60 hover:text-white hover:bg-white/5 transition-colors"
          >
            取消
          </button>
          <button
            onClick={() => {
              if (!name.trim()) return
              onSave({ name: name.trim(), required_credits: credits, parent_id: parentId })
              onClose()
            }}
            className="px-4 py-2 rounded-lg text-sm bg-white/10 hover:bg-white/20 text-white transition-colors"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  )
}

function CourseFormModal({
  open,
  onClose,
  onSave,
  initial,
  modules,
}: {
  open: boolean
  onClose: () => void
  onSave: (data: CourseFormData) => void
  initial?: CourseFormData & { id?: number }
  modules: AdminModule[]
}) {
  const [code, setCode] = useState(initial?.course_code || '')
  const [name, setName] = useState(initial?.name || '')
  const [credit, setCredit] = useState(initial?.credit || 0)
  const [moduleId, setModuleId] = useState<number | null>(initial?.module_id ?? null)

  useEffect(() => {
    if (open) {
      setCode(initial?.course_code || '')
      setName(initial?.name || '')
      setCredit(initial?.credit || 0)
      setModuleId(initial?.module_id ?? null)
    }
  }, [open, initial])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      <div className="relative bg-zinc-900 border border-white/15 rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">
            {initial?.id ? '编辑课程' : '添加课程'}
          </h3>
          <button onClick={onClose} className="text-white/40 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm text-white/60 mb-1">课程编号</label>
            <input
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
              placeholder="例：CS101"
            />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">课程名称</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
              placeholder="例：高等数学"
            />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">学分</label>
            <input
              type="number"
              value={credit}
              onChange={(e) => setCredit(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
              min={0}
              step={0.5}
            />
          </div>
          <div>
            <label className="block text-sm text-white/60 mb-1">所属模块</label>
            <select
              value={moduleId ?? ''}
              onChange={(e) => setModuleId(e.target.value ? Number(e.target.value) : null)}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:outline-none focus:border-white/30"
            >
              <option value="">未分配</option>
              {modules.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-sm text-white/60 hover:text-white hover:bg-white/5 transition-colors"
          >
            取消
          </button>
          <button
            onClick={() => {
              if (!code.trim() || !name.trim()) return
              onSave({ course_code: code.trim(), name: name.trim(), credit, module_id: moduleId })
              onClose()
            }}
            className="px-4 py-2 rounded-lg text-sm bg-white/10 hover:bg-white/20 text-white transition-colors"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  )
}

export function AdminPanel({ open, onClose, onDataChanged }: AdminPanelProps) {
  const [activeTab, setActiveTab] = useState<TabKey>('modules')
  const [modules, setModules] = useState<AdminModule[]>([])
  const [courses, setCourses] = useState<AdminCourse[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [moduleFormOpen, setModuleFormOpen] = useState(false)
  const [editingModule, setEditingModule] = useState<(ModuleFormData & { id?: number }) | undefined>()

  const [courseFormOpen, setCourseFormOpen] = useState(false)
  const [editingCourse, setEditingCourse] = useState<(CourseFormData & { id?: number }) | undefined>()

  const loadModules = useCallback(async () => {
    try {
      const res = await apiFetch('/api/admin/modules')
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: '请求失败' }))
        setError(err.error || `HTTP ${res.status}`)
        setModules([])
        return
      }
      const data = await res.json()
      setModules(data.modules || [])
    } catch (e) {
      setError('加载模块失败')
    }
  }, [])

  const loadCourses = useCallback(async () => {
    try {
      const res = await apiFetch('/api/admin/courses')
      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: '请求失败' }))
        setError(err.error || `HTTP ${res.status}`)
        setCourses([])
        return
      }
      const data = await res.json()
      setCourses(data.courses || [])
    } catch (e) {
      setError('加载课程失败')
    }
  }, [])

  useEffect(() => {
    if (!open) return
    setLoading(true)
    setError(null)
    Promise.all([loadModules(), loadCourses()]).finally(() => setLoading(false))
  }, [open, loadModules, loadCourses])

  const handleSaveModule = async (data: ModuleFormData) => {
    try {
      if (editingModule?.id) {
        await apiFetch(`/api/admin/modules/${editingModule.id}`, {
          method: 'PUT',
          body: JSON.stringify(data),
        })
      } else {
        await apiFetch('/api/admin/modules', {
          method: 'POST',
          body: JSON.stringify(data),
        })
      }
      await loadModules()
      onDataChanged?.()
    } catch (e) {
      setError('保存模块失败')
    }
  }

  const handleDeleteModule = async (mod: AdminModule) => {
    if (!confirm(`确定删除模块「${mod.name}」吗？`)) return
    try {
      const res = await apiFetch(`/api/admin/modules/${mod.id}`, { method: 'DELETE' })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        alert(body.error || '删除失败')
        return
      }
      await loadModules()
      onDataChanged?.()
    } catch (e) {
      setError('删除模块失败')
    }
  }

  const handleSaveCourse = async (data: CourseFormData) => {
    try {
      if (editingCourse?.id) {
        await apiFetch(`/api/admin/courses/${editingCourse.id}`, {
          method: 'PUT',
          body: JSON.stringify(data),
        })
      } else {
        await apiFetch('/api/admin/courses', {
          method: 'POST',
          body: JSON.stringify(data),
        })
      }
      await loadCourses()
      onDataChanged?.()
    } catch (e) {
      setError('保存课程失败')
    }
  }

  if (!open) return null

  const moduleTree = buildModuleTree(modules)

  return (
    <>
      <div className="fixed inset-0 z-[55] bg-black/70 backdrop-blur-sm" onClick={onClose} />
      <div className="fixed inset-x-4 top-[5vh] bottom-[5vh] z-[55] mx-auto max-w-4xl bg-zinc-950 border border-white/15 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 shrink-0">
          <div className="flex items-center gap-3">
            <span className="text-lg font-semibold text-white">管理后台</span>
            <span className="text-xs text-white/30 bg-white/5 px-2 py-0.5 rounded">管理员模式</span>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-white/40 hover:text-white hover:bg-white/5 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex border-b border-white/10 shrink-0 px-6">
          <button
            onClick={() => setActiveTab('modules')}
            className={`flex items-center gap-2 px-4 py-3 text-sm border-b-2 transition-colors ${
              activeTab === 'modules'
                ? 'border-white text-white'
                : 'border-transparent text-white/40 hover:text-white/70'
            }`}
          >
            <FolderTree className="w-4 h-4" />
            模块管理
          </button>
          <button
            onClick={() => setActiveTab('courses')}
            className={`flex items-center gap-2 px-4 py-3 text-sm border-b-2 transition-colors ${
              activeTab === 'courses'
                ? 'border-white text-white'
                : 'border-transparent text-white/40 hover:text-white/70'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            课程管理
          </button>
        </div>

        {error && (
          <div className="mx-6 mt-3 px-4 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
            <button onClick={() => setError(null)} className="ml-2 underline">关闭</button>
          </div>
        )}

        <div className="flex-1 overflow-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
            </div>
          ) : activeTab === 'modules' ? (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm text-white/50">共 {modules.length} 个模块</h3>
                <button
                  onClick={() => {
                    setEditingModule(undefined)
                    setModuleFormOpen(true)
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white text-sm transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  添加顶级模块
                </button>
              </div>

              <div className="rounded-xl border border-white/10 overflow-hidden">
                {moduleTree.map((node) => (
                  <TreeNode
                    key={node.id}
                    node={node}
                    depth={0}
                    onEdit={(m) => {
                      setEditingModule({
                        id: m.id,
                        name: m.name,
                        required_credits: m.required_credits,
                        parent_id: m.parent_id,
                      })
                      setModuleFormOpen(true)
                    }}
                    onAddChild={(parentId) => {
                      setEditingModule({ name: '', required_credits: 0, parent_id: parentId })
                      setModuleFormOpen(true)
                    }}
                    onDelete={handleDeleteModule}
                  />
                ))}
                {moduleTree.length === 0 && (
                  <p className="text-center text-white/30 text-sm py-12">暂无模块</p>
                )}
              </div>
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm text-white/50">共 {courses.length} 门课程</h3>
                <button
                  onClick={() => {
                    setEditingCourse(undefined)
                    setCourseFormOpen(true)
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/15 text-white text-sm transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  添加课程
                </button>
              </div>

              <div className="rounded-xl border border-white/10 overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/10">
                      <th className="text-left px-4 py-3 text-white/40 font-medium">课程编号</th>
                      <th className="text-left px-4 py-3 text-white/40 font-medium">课程名称</th>
                      <th className="text-left px-4 py-3 text-white/40 font-medium">学分</th>
                      <th className="text-left px-4 py-3 text-white/40 font-medium">所属模块</th>
                      <th className="text-right px-4 py-3 text-white/40 font-medium">操作</th>
                    </tr>
                  </thead>
                  <tbody>
                    {courses.map((c) => (
                      <tr key={c.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                        <td className="px-4 py-3 text-white/60 font-mono text-xs">{c.course_code}</td>
                        <td className="px-4 py-3 text-white/80">{c.name}</td>
                        <td className="px-4 py-3 text-white/60">{c.credit}</td>
                        <td className="px-4 py-3 text-white/50 text-xs max-w-[200px] truncate">{c.module_path}</td>
                        <td className="px-4 py-3 text-right">
                          <button
                            onClick={() => {
                              setEditingCourse({
                                id: c.id,
                                course_code: c.course_code,
                                name: c.name,
                                credit: c.credit,
                                module_id: c.module_id,
                              })
                              setCourseFormOpen(true)
                            }}
                            className="p-1.5 rounded text-white/40 hover:text-white hover:bg-white/10 transition-colors"
                            title="编辑"
                          >
                            <Pencil className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    ))}
                    {courses.length === 0 && (
                      <tr>
                        <td colSpan={5} className="text-center text-white/30 text-sm py-12">暂无课程</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>

      <ModuleFormModal
        open={moduleFormOpen}
        onClose={() => setModuleFormOpen(false)}
        onSave={handleSaveModule}
        initial={editingModule}
        modules={modules}
      />

      <CourseFormModal
        open={courseFormOpen}
        onClose={() => setCourseFormOpen(false)}
        onSave={handleSaveCourse}
        initial={editingCourse}
        modules={modules}
      />
    </>
  )
}