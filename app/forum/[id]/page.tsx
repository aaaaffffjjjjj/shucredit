'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { 
  ArrowLeft, 
  Clock, 
  MessageSquare,
  Send,
  Heart,
  Share2,
  Bookmark,
  AlertCircle,
} from 'lucide-react'
import { MathBackground } from '@/components/math-background'

const mockPostDetail = {
  id: '1',
  title: '关于大三下学期选课的建议',
  author: '李明',
  createdAt: '2024年3月15日',
  category: '选课',
  content: `想请教一下大家，大三下学期选课有什么建议吗？

特别是机器学习和云计算这两门课，听说都挺难的，同时选会不会压力太大？

我的情况是这样的：
1. 目前已经修了 102 学分
2. 专业核心课程还差 10 学分
3. 想在毕业前多学一些实用的技术

希望有经验的学长学姐能给一些建议，非常感谢！`,
  likes: 45,
}

const mockReplies = [
  {
    id: '1',
    author: '王芳',
    createdAt: '3月15日 15:20',
    content: '建议不要同时选这两门课，确实压力会比较大。如果你对机器学习更感兴趣，可以先选机器学习，云计算下学期再选。',
    likes: 23,
  },
  {
    id: '2',
    author: '张伟',
    createdAt: '3月15日 16:45',
    content: '我上学期两门都选了，确实很累，但也学到了很多东西。关键是要提前预习，跟上老师的进度。',
    likes: 15,
  },
  {
    id: '3',
    author: '刘洋',
    createdAt: '3月15日 18:00',
    content: `分享一下我的经验：

1. 机器学习需要一定的数学基础，建议提前复习线性代数和概率论
2. 云计算更偏实践，需要多动手实验
3. 如果时间充裕，两门一起选也是可以的`,
    likes: 31,
  },
]

export default function PostDetailPage() {
  const params = useParams()
  const postId = params.id as string
  const post = postId === 'not-found' ? null : mockPostDetail

  const [replyContent, setReplyContent] = useState('')
  const [isLiked, setIsLiked] = useState(false)
  const [isBookmarked, setIsBookmarked] = useState(false)
  const [likes, setLikes] = useState(post?.likes ?? 0)

  const handleSubmitReply = (e: React.FormEvent) => {
    e.preventDefault()
    if (!replyContent.trim()) return
    setReplyContent('')
  }

  const handleLike = () => {
    setIsLiked(!isLiked)
    setLikes(isLiked ? likes - 1 : likes + 1)
  }

  const handleShare = async () => {
    if (!post) return
    if (navigator.share) {
      await navigator.share({
        title: post.title,
        url: window.location.href,
      })
    } else {
      await navigator.clipboard.writeText(window.location.href)
    }
  }

  return (
    <div className="min-h-screen bg-background relative">
      <MathBackground />
      
      {/* Header */}
      <header className="relative z-10 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center gap-4">
          <Link 
            href="/forum"
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <span className="text-sm text-muted-foreground">返回列表</span>
        </div>
      </header>

      {/* Content */}
      <main className="relative z-10 max-w-3xl mx-auto px-6 py-8">
        {!post ? (
          <div className="py-20 text-center">
            <AlertCircle className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-base text-muted-foreground mb-1">帖子不存在</p>
            <p className="text-xs text-muted-foreground/60 mb-6">该帖子可能已被删除，或链接有误</p>
            <Link
              href="/forum"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm bg-foreground/10 hover:bg-foreground/15 text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              返回论坛
            </Link>
          </div>
        ) : (
          <>
        {/* Post */}
        <article className="mb-12">
          <div className="mb-6">
            <div className="flex items-center gap-2 text-xs text-muted-foreground mb-3">
              <span>{post.category}</span>
              <span>·</span>
              <span>{post.author}</span>
              <span>·</span>
              <span>{post.createdAt}</span>
            </div>
            <h1 className="text-2xl font-medium mb-6">
              {post.title}
            </h1>
          </div>

          <div className="text-sm leading-relaxed whitespace-pre-wrap text-foreground/90 mb-8">
            {post.content}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 pt-6 border-t border-border">
            <button
              onClick={handleLike}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${
                isLiked 
                  ? 'bg-destructive/10 text-destructive' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-card'
              }`}
            >
              <Heart className={`w-4 h-4 ${isLiked ? 'fill-current' : ''}`} />
              <span>{likes}</span>
            </button>
            <button
              onClick={() => setIsBookmarked(!isBookmarked)}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md transition-colors ${
                isBookmarked 
                  ? 'bg-foreground/10 text-foreground' 
                  : 'text-muted-foreground hover:text-foreground hover:bg-card'
              }`}
            >
              <Bookmark className={`w-4 h-4 ${isBookmarked ? 'fill-current' : ''}`} />
              <span>收藏</span>
            </button>
            <button
              onClick={handleShare}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md text-muted-foreground hover:text-foreground hover:bg-card transition-colors"
            >
              <Share2 className="w-4 h-4" />
              <span>分享</span>
            </button>
          </div>
        </article>

        {/* Replies */}
        <section>
          <h2 className="text-sm font-medium mb-6 flex items-center gap-2">
            <MessageSquare className="w-4 h-4" />
            回复 ({mockReplies.length})
          </h2>

          <div className="space-y-6 mb-8">
            {mockReplies.map((reply, index) => (
              <div key={reply.id} className="group">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="font-medium text-foreground">{reply.author}</span>
                    <span>·</span>
                    <Clock className="w-3 h-3" />
                    <span>{reply.createdAt}</span>
                  </div>
                  <span className="text-xs text-muted-foreground">#{index + 1}</span>
                </div>

                <div className="text-sm leading-relaxed whitespace-pre-wrap text-foreground/90 mb-2">
                  {reply.content}
                </div>

                <button className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors">
                  <Heart className="w-3.5 h-3.5" />
                  <span>{reply.likes}</span>
                </button>
              </div>
            ))}
          </div>

          {/* Reply Form */}
          <div className="pt-6 border-t border-border">
            <h3 className="text-sm font-medium mb-4">发表回复</h3>
            <form onSubmit={handleSubmitReply}>
              <textarea
                value={replyContent}
                onChange={(e) => setReplyContent(e.target.value)}
                placeholder="写下你的回复..."
                rows={4}
                className="w-full px-4 py-3 text-sm rounded-lg bg-transparent border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-foreground transition-colors resize-none mb-4"
              />
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={!replyContent.trim()}
                  className="flex items-center gap-1.5 px-4 py-2 text-sm bg-foreground text-background rounded-md hover:bg-foreground/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="w-3.5 h-3.5" />
                  发表
                </button>
              </div>
            </form>
          </div>
        </section>
          </>
        )}
      </main>
    </div>
  )
}
