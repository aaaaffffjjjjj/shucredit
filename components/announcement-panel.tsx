'use client'

import { useState, useEffect } from 'react'
import { AlertCircle, Clock, ChevronDown, ChevronUp } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export interface Announcement {
  id: number
  title: string
  content: string
  is_active: boolean
  created_at: string
  updated_at: string
  username: string
}

export function AnnouncementPanel() {
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [loading, setLoading] = useState(true)
  const [expandedId, setExpandedId] = useState<number | null>(null)

  useEffect(() => {
    fetch('/api/announcements')
      .then(res => res.json())
      .then(data => {
        setAnnouncements(data.announcements || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('获取公告失败:', err)
        setLoading(false)
      })
  }, [])

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

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id)
  }

  if (loading) {
    return (
      <Card className="w-full">
        <CardContent className="py-4">
          <div className="flex justify-center items-center py-4">
            <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (announcements.length === 0) {
    return null
  }

  return (
    <Card className="w-full bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200">
      <CardHeader className="bg-amber-100/50 border-b border-amber-200">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-amber-600" />
          <CardTitle className="text-amber-800 font-semibold">📢 公告通知</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="space-y-1">
          {announcements.map((ann) => (
            <div
              key={ann.id}
              className="border-b border-amber-100 last:border-b-0 hover:bg-amber-50/50 transition-colors"
            >
              <button
                onClick={() => toggleExpand(ann.id)}
                className="w-full p-3 text-left flex items-center justify-between gap-3"
              >
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-amber-900 truncate">{ann.title}</h3>
                  <div className="flex items-center gap-3 mt-1 text-xs text-amber-600">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDate(ann.created_at)}
                    </span>
                    <span>发布者: {ann.username}</span>
                  </div>
                </div>
                {expandedId === ann.id ? (
                  <ChevronUp className="w-4 h-4 text-amber-500 flex-shrink-0" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-amber-500 flex-shrink-0" />
                )}
              </button>
              {expandedId === ann.id && (
                <div className="px-3 pb-3">
                  <div className="p-3 bg-white/70 rounded-lg border border-amber-100 text-amber-800 whitespace-pre-wrap">
                    {ann.content}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}