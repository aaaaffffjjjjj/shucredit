'use client'

import { useState, useEffect } from 'react'
import { Plus, Edit2, Trash2, Eye, EyeOff, Save, X } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { useToast } from '@/hooks/use-toast'
import type { Announcement } from './announcement-panel'

export function AdminAnnouncementManager() {
  const { toast } = useToast()
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [loading, setLoading] = useState(true)
  const [isCreating, setIsCreating] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    is_active: true
  })

  useEffect(() => {
    loadAnnouncements()
  }, [])

  const loadAnnouncements = () => {
    setLoading(true)
    fetch('/api/admin/announcements')
      .then(res => res.json())
      .then(data => {
        setAnnouncements(data.announcements || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('获取公告失败:', err)
        toast({
          title: '获取公告失败',
          description: '无法加载公告列表',
          variant: 'destructive'
        })
        setLoading(false)
      })
  }

  const formatDate = (dateStr: string) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleCreate = () => {
    setIsCreating(true)
    setFormData({ title: '', content: '', is_active: true })
  }

  const handleEdit = (ann: Announcement) => {
    setEditingId(ann.id)
    setFormData({
      title: ann.title,
      content: ann.content,
      is_active: ann.is_active
    })
  }

  const handleSave = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      toast({
        title: '输入错误',
        description: '标题和内容不能为空',
        variant: 'destructive'
      })
      return
    }

    try {
      if (editingId) {
        // 更新公告
        const res = await fetch(`/api/admin/announcements/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        })
        const data = await res.json()
        if (data.ok) {
          toast({
            title: '更新成功',
            description: '公告已更新',
            variant: 'default'
          })
        } else {
          throw new Error(data.error || '更新失败')
        }
      } else {
        // 创建公告
        const res = await fetch('/api/admin/announcements', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        })
        const data = await res.json()
        if (data.ok) {
          toast({
            title: '创建成功',
            description: '公告已发布',
            variant: 'default'
          })
        } else {
          throw new Error(data.error || '创建失败')
        }
      }
      setIsCreating(false)
      setEditingId(null)
      loadAnnouncements()
    } catch (err) {
      toast({
        title: '操作失败',
        description: err instanceof Error ? err.message : '未知错误',
        variant: 'destructive'
      })
    }
  }

  const handleCancel = () => {
    setIsCreating(false)
    setEditingId(null)
    setFormData({ title: '', content: '', is_active: true })
  }

  const handleDelete = async (id: number) => {
    if (!confirm('确定要删除此公告吗？')) return

    try {
      const res = await fetch(`/api/admin/announcements/${id}`, {
        method: 'DELETE'
      })
      const data = await res.json()
      if (data.ok) {
        toast({
          title: '删除成功',
          description: '公告已删除',
          variant: 'default'
        })
        loadAnnouncements()
      } else {
        throw new Error(data.error || '删除失败')
      }
    } catch (err) {
      toast({
        title: '删除失败',
        description: err instanceof Error ? err.message : '未知错误',
        variant: 'destructive'
      })
    }
  }

  const handleToggleActive = async (ann: Announcement) => {
    try {
      const res = await fetch(`/api/admin/announcements/${ann.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !ann.is_active })
      })
      const data = await res.json()
      if (data.ok) {
        toast({
          title: '状态已更新',
          description: ann.is_active ? '公告已隐藏' : '公告已发布',
          variant: 'default'
        })
        loadAnnouncements()
      } else {
        throw new Error(data.error || '更新失败')
      }
    } catch (err) {
      toast({
        title: '操作失败',
        description: err instanceof Error ? err.message : '未知错误',
        variant: 'destructive'
      })
    }
  }

  if (loading) {
    return (
      <Card className="w-full">
        <CardContent className="py-8">
          <div className="flex justify-center items-center">
            <div className="w-6 h-6 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg">📢 公告管理</CardTitle>
        <Button onClick={handleCreate} className="gap-2">
          <Plus className="w-4 h-4" />
          发布公告
        </Button>
      </CardHeader>
      <CardContent>
        {(isCreating || editingId !== null) && (
          <div className="mb-6 p-4 border rounded-lg bg-muted/50">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-medium">
                {editingId ? '编辑公告' : '发布新公告'}
              </h3>
              <Button variant="ghost" size="sm" onClick={handleCancel}>
                <X className="w-4 h-4" />
              </Button>
            </div>
            <div className="space-y-4">
              <div>
                <Label htmlFor="title">公告标题</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="请输入公告标题"
                />
              </div>
              <div>
                <Label htmlFor="content">公告内容</Label>
                <Textarea
                  id="content"
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  placeholder="请输入公告内容"
                  className="min-h-[100px]"
                />
              </div>
              <div className="flex items-center justify-between">
                <Label htmlFor="is_active">是否发布</Label>
                <Switch
                  id="is_active"
                  checked={formData.is_active}
                  onCheckedChange={(checked) => setFormData({ ...formData, is_active: checked })}
                />
              </div>
              <div className="flex gap-2">
                <Button onClick={handleSave} className="gap-2">
                  <Save className="w-4 h-4" />
                  保存
                </Button>
                <Button variant="outline" onClick={handleCancel}>
                  取消
                </Button>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-3">
          {announcements.length === 0 ? (
            <div className="text-center py-8 text-muted">
              暂无公告，点击上方按钮发布第一条公告
            </div>
          ) : (
            announcements.map((ann) => (
              <div
                key={ann.id}
                className={`p-4 border rounded-lg ${
                  ann.is_active ? 'bg-green-50/50 border-green-200' : 'bg-gray-50/50 border-gray-200'
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium truncate">{ann.title}</h3>
                      {!ann.is_active && (
                        <span className="px-2 py-0.5 text-xs bg-gray-200 text-gray-600 rounded">已隐藏</span>
                      )}
                    </div>
                    <p className="text-sm text-muted mt-1 line-clamp-2">{ann.content}</p>
                    <div className="flex items-center gap-4 mt-2 text-xs text-muted">
                      <span>{formatDate(ann.created_at)}</span>
                      <span>发布者: {ann.username}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleToggleActive(ann)}
                      className="h-8 w-8 p-0"
                      title={ann.is_active ? '隐藏公告' : '发布公告'}
                    >
                      {ann.is_active ? (
                        <Eye className="w-4 h-4 text-green-600" />
                      ) : (
                        <EyeOff className="w-4 h-4 text-gray-400" />
                      )}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleEdit(ann)}
                      className="h-8 w-8 p-0"
                      title="编辑公告"
                    >
                      <Edit2 className="w-4 h-4 text-blue-600" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(ann.id)}
                      className="h-8 w-8 p-0"
                      title="删除公告"
                    >
                      <Trash2 className="w-4 h-4 text-red-600" />
                    </Button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  )
}