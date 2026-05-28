'use client'

import { useState, useEffect, useRef } from 'react'
import { X, MessageSquare, Calculator, AlertTriangle, TrendingUp, HelpCircle, Loader2, GraduationCap, Calendar, Target, ChevronRight } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts'

type ToolType = 'feedback' | 'planner' | 'warning' | 'trend' | 'help'

interface ToolPanelProps {
  isOpen: boolean
  onClose: () => void
  initialTool?: ToolType
  onFocusModule?: (moduleId: string) => void
  progressData?: {
    sun?: { required: number; earned: number }
    modules?: Array<{ id: number; name: string; required: number; earned: number; parent_id: number | null; percent: number }>
  } | null
}

const tools = [
  { id: 'feedback' as ToolType, icon: MessageSquare, label: '意见箱' },
  { id: 'planner' as ToolType, icon: Calculator, label: '规划助手' },
  { id: 'warning' as ToolType, icon: AlertTriangle, label: '预警通知' },
  { id: 'trend' as ToolType, icon: TrendingUp, label: '学分趋势' },
  { id: 'help' as ToolType, icon: HelpCircle, label: '帮助' },
]

const MOCK_TREND_DATA = [
  { semester: '第1学期', credits: 22 },
  { semester: '第2学期', credits: 24 },
  { semester: '第3学期', credits: 20 },
  { semester: '第4学期', credits: 26 },
  { semester: '第5学期', credits: 18 },
  { semester: '第6学期', credits: 22 },
  { semester: '第7学期', credits: 16 },
  { semester: '第8学期', credits: 12 },
]

const HELP_ITEMS = [
  { icon: '🖱️', title: '点击行星', desc: '聚焦到对应模块，显示进度环' },
  { icon: '🔍', title: '拖拽旋转', desc: '按住鼠标拖拽可旋转视角' },
  { icon: '🔎', title: '缩放视图', desc: '滚轮可放大或缩小' },
  { icon: '🌟', title: '点击太阳', desc: '打开工具箱，获取更多功能' },
  { icon: '📊', title: '侧边栏', desc: '查看模块层级和课程详情' },
  { icon: '⌨️', title: 'ESC键', desc: '关闭弹窗或取消聚焦' },
  { icon: '🔄', title: '重置视角', desc: '点击右上角按钮恢复全景' },
  { icon: '📚', title: '模块选择', desc: '从下拉菜单快速切换专业' },
]

export default function ToolPanel({ isOpen, onClose, initialTool = 'feedback', onFocusModule, progressData }: ToolPanelProps) {
  const [activeTool, setActiveTool] = useState<ToolType>(initialTool)
  const [content, setContent] = useState('')
  const [contact, setContact] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)
  const panelRef = useRef<HTMLDivElement>(null)

  const [targetYear, setTargetYear] = useState('2028')
  const [targetSeason, setTargetSeason] = useState<'春' | '秋'>('春')
  const [customSemesters, setCustomSemesters] = useState(4)

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

  const currentEarned = progressData?.sun?.earned ?? 0
  const totalRequired = progressData?.sun?.required ?? 160
  const remainingCredits = Math.max(0, totalRequired - currentEarned)
  const currentYear = new Date().getFullYear()
  const currentMonth = new Date().getMonth()
  const isSpring = currentMonth < 7
  const currentSemester = (currentYear - 2024) * 2 + (isSpring ? 1 : 2)
  const targetSemesterNum = (parseInt(targetYear) - 2024) * 2 + (targetSeason === '春' ? 1 : 2)
  const remainingSemesters = Math.max(1, targetSemesterNum - currentSemester)
  const avgCreditsPerSemester = (remainingCredits / remainingSemesters).toFixed(1)

  const warningModules = progressData?.modules?.filter(m => {
    if (!m.required || m.required === 0) return false
    const percent = (m.earned / m.required) * 100
    return percent < 50
  }) ?? []

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

      <div
        ref={panelRef}
        className="relative w-[480px] max-w-[90vw] max-h-[80vh] bg-black/40 backdrop-blur-xl border border-white/20 rounded-2xl shadow-2xl animate-[fade-in-scale_0.3s_ease-out] flex flex-col"
      >
        <div className="flex items-center justify-between p-4 border-b border-white/10 shrink-0">
          <h2 className="text-lg font-semibold text-white">工具箱</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/70 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex items-center gap-2 p-4 border-b border-white/10 shrink-0 overflow-x-auto">
          {tools.map((tool) => {
            const Icon = tool.icon
            const isActive = activeTool === tool.id
            return (
              <button
                key={tool.id}
                onClick={() => setActiveTool(tool.id)}
                className={`flex flex-col items-center gap-1 p-3 rounded-xl transition-all shrink-0 ${
                  isActive
                    ? 'bg-white/15 text-white'
                    : 'text-white/50 hover:text-white hover:bg-white/10'
                }`}
                title={tool.label}
              >
                <Icon className="w-5 h-5" />
                <span className="text-xs whitespace-nowrap">{tool.label}</span>
              </button>
            )
          })}
        </div>

        <div className="p-4 overflow-y-auto flex-1">
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

          {activeTool === 'planner' && (
            <div className="space-y-4">
              <div className="text-center mb-6">
                <GraduationCap className="w-12 h-12 mx-auto mb-2 text-blue-400" />
                <h3 className="text-lg font-semibold text-white">学期规划助手</h3>
                <p className="text-white/50 text-sm">帮你规划每学期应修学分</p>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="bg-white/5 rounded-xl p-3 text-center">
                  <div className="text-white/50 text-xs mb-1">已修学分</div>
                  <div className="text-2xl font-bold text-green-400">{currentEarned}</div>
                </div>
                <div className="bg-white/5 rounded-xl p-3 text-center">
                  <div className="text-white/50 text-xs mb-1">毕业要求</div>
                  <div className="text-2xl font-bold text-white">{totalRequired}</div>
                </div>
                <div className="bg-white/5 rounded-xl p-3 text-center">
                  <div className="text-white/50 text-xs mb-1">剩余学分</div>
                  <div className="text-2xl font-bold text-orange-400">{remainingCredits}</div>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-4 space-y-3">
                <div className="flex items-center gap-2 text-white/70 text-sm">
                  <Calendar className="w-4 h-4" />
                  <span>目标毕业时间</span>
                </div>
                <div className="flex gap-2">
                  <select
                    value={targetYear}
                    onChange={(e) => setTargetYear(e.target.value)}
                    className="flex-1 bg-white/10 border border-white/15 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-white/30"
                  >
                    {[2026, 2027, 2028, 2029, 2030].map(y => (
                      <option key={y} value={y} className="bg-gray-900">{y}</option>
                    ))}
                  </select>
                  <select
                    value={targetSeason}
                    onChange={(e) => setTargetSeason(e.target.value as '春' | '秋')}
                    className="w-20 bg-white/10 border border-white/15 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-white/30"
                  >
                    <option value="春" className="bg-gray-900">春季</option>
                    <option value="秋" className="bg-gray-900">秋季</option>
                  </select>
                </div>
              </div>

              <div className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-xl p-4 border border-blue-500/30">
                <div className="flex items-center gap-2 mb-2">
                  <Target className="w-5 h-5 text-blue-400" />
                  <span className="text-white font-medium">规划结果</span>
                </div>
                <div className="text-center py-3">
                  <div className="text-4xl font-bold text-white mb-1">{avgCreditsPerSemester}</div>
                  <div className="text-white/60 text-sm">平均每学期需修读学分</div>
                </div>
                <div className="flex justify-between text-xs text-white/50 mt-3 pt-3 border-t border-white/10">
                  <span>剩余学期: {remainingSemesters}个</span>
                  <span>目标: {targetYear}{targetSeason === '春' ? '年春' : '年秋'}毕业</span>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-3">
                <div className="text-white/50 text-xs mb-2">💡 建议每学期修读</div>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-lg text-sm">10-15 学分</span>
                  <span className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded-lg text-sm">15-20 学分</span>
                  <span className="px-3 py-1 bg-orange-500/20 text-orange-400 rounded-lg text-sm">20+ 学分</span>
                </div>
              </div>
            </div>
          )}

          {activeTool === 'warning' && (
            <div className="space-y-4">
              <div className="text-center mb-6">
                <AlertTriangle className="w-12 h-12 mx-auto mb-2 text-yellow-400" />
                <h3 className="text-lg font-semibold text-white">学分预警通知</h3>
                <p className="text-white/50 text-sm">以下模块完成度低于50%</p>
              </div>

              {warningModules.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-3">🎉</div>
                  <p className="text-white/90">太棒了！暂无预警模块</p>
                  <p className="text-white/50 text-sm mt-1">所有模块进度均已过半</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {warningModules.map((module) => {
                    const percent = Math.round((module.earned / module.required) * 100)
                    return (
                      <button
                        key={module.id}
                        onClick={() => {
                          if (onFocusModule) {
                            onFocusModule(String(module.id))
                            onClose()
                          }
                        }}
                        className="w-full bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/30 rounded-xl p-3 text-left transition-colors group"
                      >
                        <div className="flex items-start gap-3">
                          <span className="text-2xl">⚠️</span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between">
                              <span className="text-white font-medium truncate">{module.name}</span>
                              <ChevronRight className="w-4 h-4 text-yellow-400 opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                            </div>
                            <div className="flex items-center gap-3 mt-1 text-xs">
                              <span className="text-yellow-400 font-semibold">{percent}%</span>
                              <span className="text-white/50">{module.earned} / {module.required} 学分</span>
                            </div>
                            <div className="mt-2 h-1.5 bg-white/10 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full transition-all"
                                style={{ width: `${percent}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      </button>
                    )
                  })}
                </div>
              )}

              {warningModules.length > 0 && (
                <div className="text-center text-white/40 text-xs">
                  点击模块可聚焦到太阳系中查看
                </div>
              )}
            </div>
          )}

          {activeTool === 'trend' && (
            <div className="space-y-4">
              <div className="text-center mb-6">
                <TrendingUp className="w-12 h-12 mx-auto mb-2 text-emerald-400" />
                <h3 className="text-lg font-semibold text-white">学分趋势图</h3>
                <p className="text-white/50 text-sm">展示每学期获得学分变化</p>
              </div>

              <div className="bg-white/5 rounded-xl p-4">
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={MOCK_TREND_DATA}>
                    <defs>
                      <linearGradient id="colorCredits" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis
                      dataKey="semester"
                      stroke="rgba(255,255,255,0.5)"
                      fontSize={10}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="rgba(255,255,255,0.5)"
                      fontSize={10}
                      tickLine={false}
                      axisLine={false}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(0,0,0,0.8)',
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: '8px',
                        color: 'white'
                      }}
                      formatter={(value: number) => [`${value} 学分`, '获得学分']}
                    />
                    <Area
                      type="monotone"
                      dataKey="credits"
                      stroke="#10b981"
                      strokeWidth={2}
                      fill="url(#colorCredits)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white/5 rounded-xl p-3 text-center">
                  <div className="text-white/50 text-xs mb-1">平均每学期</div>
                  <div className="text-xl font-bold text-emerald-400">
                    {(MOCK_TREND_DATA.reduce((s, d) => s + d.credits, 0) / MOCK_TREND_DATA.length).toFixed(1)}
                  </div>
                </div>
                <div className="bg-white/5 rounded-xl p-3 text-center">
                  <div className="text-white/50 text-xs mb-1">最高学期</div>
                  <div className="text-xl font-bold text-white">
                    {Math.max(...MOCK_TREND_DATA.map(d => d.credits))} 学分
                  </div>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-3 text-xs text-white/50">
                <p>📌 数据说明：当前显示为演示数据，实际数据需从后端 enrollment 表按学期聚合获取。</p>
              </div>
            </div>
          )}

          {activeTool === 'help' && (
            <div className="space-y-4">
              <div className="text-center mb-6">
                <HelpCircle className="w-12 h-12 mx-auto mb-2 text-blue-400" />
                <h3 className="text-lg font-semibold text-white">帮助与引导</h3>
                <p className="text-white/50 text-sm">快捷键说明与操作演示</p>
              </div>

              <div className="space-y-2">
                {HELP_ITEMS.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-3 bg-white/5 hover:bg-white/10 rounded-xl p-3 transition-colors"
                  >
                    <span className="text-2xl">{item.icon}</span>
                    <div>
                      <div className="text-white font-medium text-sm">{item.title}</div>
                      <div className="text-white/50 text-xs">{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-xl p-4 border border-blue-500/20 mt-4">
                <div className="text-blue-400 text-sm font-medium mb-2">💡 提示</div>
                <p className="text-white/60 text-xs">
                  点击太阳可打开工具箱，使用规划助手计算学期学分，或查看预警通知了解哪些模块需要加强学习。
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
