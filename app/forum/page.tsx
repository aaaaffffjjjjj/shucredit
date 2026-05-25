'use client'

import { useState } from 'react'
import Link from 'next/link'
import { 
  ArrowLeft, 
  Search, 
  Plus, 
  MessageSquare, 
  Clock,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { MathBackground } from '@/components/math-background'

const mockPosts = [
  {
    id: '1',
    title: '关于大三下学期选课的建议',
    author: '李明',
    createdAt: '3月15日',
    replyCount: 23,
    category: '选课',
    preview: '想请教一下大家，大三下学期选课有什么建议吗？'
  },
  {
    id: '2',
    title: '软件工程专业培养方案解读',
    author: '王芳',
    createdAt: '3月14日',
    replyCount: 45,
    category: '方案',
    preview: '分享一下我对软件工程专业培养方案的理解。'
  },
  {
    id: '3',
    title: '创新创业学分怎么修？',
    author: '张伟',
    createdAt: '3月13日',
    replyCount: 18,
    category: '咨询',
    preview: '请问创新创业学分有哪些获取途径？'
  },
  {
    id: '4',
    title: '实践教学环节经验分享',
    author: '刘洋',
    createdAt: '3月12日',
    replyCount: 32,
    category: '分享',
    preview: '刚完成毕业实习，分享一下我的实践教学环节经验。'
  },
  {
    id: '5',
    title: '通识选修课推荐清单',
    author: '陈静',
    createdAt: '3月11日',
    replyCount: 67,
    category: '选课',
    preview: '整理了一份通识选修课推荐清单，欢迎补充。'
  },
]

const categories = ['全部', '选课', '方案', '咨询', '分享']

export default function ForumPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('全部')
  const [currentPage, setCurrentPage] = useState(1)

  const filteredPosts = mockPosts.filter(post => {
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === '全部' || post.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <div className="min-h-screen bg-background relative">
      <MathBackground />
      
      {/* Header */}
      <header className="relative z-10 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link 
              href="/"
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <h1 className="text-sm font-medium">论坛</h1>
          </div>
          <Link
            href="/forum/new"
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-foreground text-background rounded-md hover:bg-foreground/90 transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            发帖
          </Link>
        </div>
      </header>

      {/* Main */}
      <main className="relative z-10 max-w-3xl mx-auto px-6 py-8">
        {/* Search & Filter */}
        <div className="flex gap-3 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="搜索帖子..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm rounded-lg bg-transparent border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-foreground transition-colors"
            />
          </div>
        </div>

        {/* Categories */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-3 py-1.5 text-sm rounded-md whitespace-nowrap transition-colors ${
                selectedCategory === category
                  ? 'bg-foreground text-background'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Posts */}
        <div className="space-y-1">
          {filteredPosts.map((post) => (
            <Link
              key={post.id}
              href={`/forum/${post.id}`}
              className="block px-4 py-4 -mx-4 rounded-lg hover:bg-card transition-colors group"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-muted-foreground">{post.category}</span>
                    <span className="text-xs text-muted-foreground">·</span>
                    <span className="text-xs text-muted-foreground">{post.author}</span>
                  </div>
                  <h2 className="text-sm font-medium mb-1 group-hover:text-foreground transition-colors">
                    {post.title}
                  </h2>
                  <p className="text-sm text-muted-foreground line-clamp-1">
                    {post.preview}
                  </p>
                </div>

                <div className="flex items-center gap-4 text-xs text-muted-foreground shrink-0">
                  <div className="flex items-center gap-1">
                    <MessageSquare className="w-3.5 h-3.5" />
                    <span>{post.replyCount}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{post.createdAt}</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}

          {filteredPosts.length === 0 && (
            <div className="py-16 text-center">
              <p className="text-sm text-muted-foreground">暂无相关帖子</p>
            </div>
          )}
        </div>

        {/* Pagination */}
        {filteredPosts.length > 0 && (
          <div className="flex items-center justify-center gap-1 mt-8">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="p-2 text-muted-foreground hover:text-foreground disabled:opacity-30 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            
            {[1, 2, 3].map((page) => (
              <button
                key={page}
                onClick={() => setCurrentPage(page)}
                className={`w-8 h-8 text-sm rounded transition-colors ${
                  currentPage === page
                    ? 'bg-foreground text-background'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={currentPage === 3}
              className="p-2 text-muted-foreground hover:text-foreground disabled:opacity-30 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
