'use client'

import { useState, useEffect, useRef } from 'react'
import { X, MessageSquare, Settings, HelpCircle, Bell, Loader2 } from 'lucide-react'

type ToolType = 'feedback' | 'settings' | 'help' | 'notifications'

interface ToolPanelProps {
  isOpen: boolean
  onClose: () => void
  initialTool?: ToolType
}

const tools = [
  { id: 'feedback' as ToolType, icon: MessageSquare, label: '意见箱' },
  { id: 'settings' as ToolType, icon: Settings, label: '设置', disabled: true },
  { id: 'help' as ToolType, icon: HelpCircle, label: '帮助', disabled: true },
  { id: 'notifications' as ToolType, icon: Bell, label: '通知', disabled: true },
]

export default function ToolPanel({ isOpen, onClose, initialTool = 'feedback' }: ToolPanelProps) {
  const [activeTool, setActiveTool] = useState<ToolType>(initialTool)
  const [content, setContent] = useState('')
  const [contact, setContact] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)
  const panelRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      setActiveTool(initialTool)
      setContent('')
      setContact('')
      setSubmitSuccess(false)
    }
  }, [isOpen, initialTool])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose()
    }
    const handleClickOutside = (e: MouseEvent) => {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        onClose()
      }
    }
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown)
      document.addEventListener('mousedown', handleClickOutside)
      document.body.style.overflow = 'hidden'
    }
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('mousedown', handleClickOutside)
      document.body.style.overflow = ''
    }
  }, [isOpen, onClose])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim()) return

    setIsSubmitting(true)
    try {
      // 模拟 API 调用
      console.log('提交意见:', { content, contact })
      await new Promise(resolve => setTimeout(resolve, 800))
      setSubmitSuccess(true)
      setContent('')
      setContact('')
      setTimeout(() => {
        onClose()
      }, 2000)
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      {/* 蒙层 */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
      
      {/* 面板 */}
      <div
        ref={panelRef}
        className="relative w-[400px] max-w-[90vw] bg-black/40 backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl animate-[fade-in-scale_0.3s_ease-out]"
      >
        {/* 头部 */}
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <h2 className="text-lg font-semibold text-white">工具箱</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/70 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 工具切换栏 */}
        <div className="flex items-center gap-2 p-4 border-b border-white/10">
          {tools.map((tool) => {
            const Icon = tool.icon
            const isActive = activeTool === tool.id
            return (
              <button
                key={tool.id}
                onClick={() => !tool.disabled && setActiveTool(tool.id)}
                disabled={tool.disabled}
                className={`flex flex-col items-center gap-1 p-3 rounded-xl transition-all ${
                  isActive
                    ? 'bg-white/15 text-white'
                    : tool.disabled
                    ? 'text-white/20 cursor-not-allowed'
                    : 'text-white/50 hover:text-white hover:bg-white/10'
                }`}
                title={tool.label}
              >
                <Icon className="w-6 h-6" />
                <span className="text-xs">{tool.label}</span>
              </button>
            )
          })}
        </div>

        {/* 内容区域 */}
        <div className="p-4">
          {activeTool === 'feedback' && (
            <div>
              {submitSuccess ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">✨</div>
                  <p className="text-white/90 text-lg">感谢反馈！</p>
                  <p className="text-white/50 text-sm mt-1">面板即将关闭...</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-white/70 text-sm mb-2">意见内容 *</label>
                    <textarea
                      value={content}
                      onChange={(e) => setContent(e.target.value)}
                      placeholder="请输入您的意见或建议..."
                      className="w-full h-32 bg-white/5 border border-white/15 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:border-white/30 resize-none"
                      disabled={isSubmitting}
                      required
                    />
                    {!content.trim() && content.length > 0 && (
                      <p className="text-red-400 text-xs mt-1">请输入有效的意见内容</p>
                    )}
                  </div>
                  <div>
                    <label className="block text-white/70 text-sm mb-2">联系方式（选填）</label>
                    <input
                      type="text"
                      value={contact}
                      onChange={(e) => setContact(e.target.value)}
                      placeholder="邮箱/手机/QQ"
                      className="w-full bg-white/5 border border-white/15 rounded-xl p-3 text-white placeholder-white/30 focus:outline-none focus:border-white/30"
                      disabled={isSubmitting}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isSubmitting || !content.trim()}
                    className="w-full py-3 bg-white/10 hover:bg-white/15 disabled:bg-white/5 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
                  >
                    {isSubmitting ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        提交中...
                      </>
                    ) : (
                      '提交意见'
                    )}
                  </button>
                </form>
              )}
            </div>
          )}
          {(activeTool === 'settings' || activeTool === 'help' || activeTool === 'notifications') && (
            <div className="text-center py-8 text-white/50">
              此功能即将上线，敬请期待！
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
