'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ArrowLeft, Send } from 'lucide-react'
import { MathBackground } from '@/components/math-background'

const categories = ['选课', '方案', '咨询', '分享', '其他']

export default function NewPostPage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [category, setCategory] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validateForm = () => {
    const newErrors: Record<string, string> = {}
    
    if (!title.trim()) {
      newErrors.title = '请输入标题'
    } else if (title.length < 5) {
      newErrors.title = '标题至少 5 个字符'
    }

    if (!content.trim()) {
      newErrors.content = '请输入内容'
    } else if (content.length < 10) {
      newErrors.content = '内容至少 10 个字符'
    }

    if (!category) {
      newErrors.category = '请选择分类'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!validateForm()) return
    router.push('/forum')
  }

  return (
    <div className="min-h-screen bg-background relative">
      <MathBackground />
      
      {/* Header */}
      <header className="relative z-10 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="max-w-2xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link 
              href="/forum"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <h1 className="text-sm font-medium">发布新帖子</h1>
          </div>
        </div>
      </header>

      {/* Form */}
      <main className="relative z-10 max-w-2xl mx-auto px-6 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Category */}
          <div>
            <label className="block text-sm font-medium mb-3">
              分类
            </label>
            <div className="flex flex-wrap gap-2">
              {categories.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  onClick={() => {
                    setCategory(cat)
                    if (errors.category) setErrors(prev => ({ ...prev, category: '' }))
                  }}
                  className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                    category === cat
                      ? 'bg-foreground text-background'
                      : 'border border-border text-muted-foreground hover:text-foreground'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
            {errors.category && (
              <p className="mt-2 text-sm text-destructive">{errors.category}</p>
            )}
          </div>

          {/* Title */}
          <div>
            <label htmlFor="title" className="block text-sm font-medium mb-2">
              标题
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => {
                setTitle(e.target.value)
                if (errors.title) setErrors(prev => ({ ...prev, title: '' }))
              }}
              placeholder="输入帖子标题"
              maxLength={100}
              className="w-full px-4 py-2.5 text-sm rounded-lg bg-transparent border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-foreground transition-colors"
            />
            <div className="flex justify-between mt-1.5">
              {errors.title ? (
                <p className="text-sm text-destructive">{errors.title}</p>
              ) : <span />}
              <p className="text-xs text-muted-foreground">{title.length}/100</p>
            </div>
          </div>

          {/* Content */}
          <div>
            <label htmlFor="content" className="block text-sm font-medium mb-2">
              内容
            </label>
            <textarea
              id="content"
              value={content}
              onChange={(e) => {
                setContent(e.target.value)
                if (errors.content) setErrors(prev => ({ ...prev, content: '' }))
              }}
              placeholder="输入帖子内容"
              rows={12}
              className="w-full px-4 py-3 text-sm rounded-lg bg-transparent border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-foreground transition-colors resize-none"
            />
            <div className="flex justify-between mt-1.5">
              {errors.content ? (
                <p className="text-sm text-destructive">{errors.content}</p>
              ) : <span />}
              <p className="text-xs text-muted-foreground">{content.length} 字符</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4">
            <Link
              href="/forum"
              className="px-4 py-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              取消
            </Link>
            <button
              type="submit"
              className="flex items-center gap-1.5 px-4 py-2 text-sm bg-foreground text-background rounded-md hover:bg-foreground/90 transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
              发布
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}
