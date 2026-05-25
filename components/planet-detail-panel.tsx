'use client'

import { useState, useEffect } from 'react'
import { X, ChevronDown, ChevronRight, Check, BookOpen, Clock } from 'lucide-react'
import {
  getChildModules,
  getModuleById,
  modulePercent,
  percentColor,
  formatCredits,
  type ApiModule,
} from '@/lib/progress'
import { fetchRecommendCourses, type ApiCourse } from '@/lib/courses'

interface PlanetDetailPanelProps {
  moduleId: string | null
  focusSubModuleId?: string | null
  allModules: ApiModule[]
  onClose: () => void
}

export default function PlanetDetailPanel({
  moduleId,
  focusSubModuleId = null,
  allModules,
  onClose,
}: PlanetDetailPanelProps) {
  const [expandedSubs, setExpandedSubs] = useState<Record<string, boolean>>({})
  const [recommendCourses, setRecommendCourses] = useState<ApiCourse[]>([])
  const [loadingCourses, setLoadingCourses] = useState(false)

  const module = moduleId ? getModuleById(allModules, moduleId) : undefined
  const children = moduleId ? getChildModules(allModules, moduleId) : []

  useEffect(() => {
    if (!moduleId) return
    const init: Record<string, boolean> = {}
    children.forEach((c) => {
      init[String(c.id)] = focusSubModuleId === String(c.id)
    })
    if (focusSubModuleId) init[focusSubModuleId] = true
    setExpandedSubs(init)
  }, [moduleId, focusSubModuleId, children.length])

  useEffect(() => {
    if (!moduleId || children.length > 0) return
    
    const loadCourses = async () => {
      setLoadingCourses(true)
      try {
        const courses = await fetchRecommendCourses(Number(moduleId))
        setRecommendCourses(courses)
      } catch (error) {
        console.error('加载推荐课程失败:', error)
      } finally {
        setLoadingCourses(false)
      }
    }
    
    loadCourses()
  }, [moduleId, children.length])

  const toggleSub = (subId: string) => {
    setExpandedSubs((prev) => ({ ...prev, [subId]: !prev[subId] }))
  }

  if (!moduleId || !module) return null

  const percent = modulePercent(module)
  const barColor = percentColor(percent)

  return (
    <aside
      className="glass-card fixed right-4 top-1/2 -translate-y-1/2 z-40 w-80 max-h-[min(85vh,680px)] flex flex-col p-4 text-white animate-[slideInPanel_0.28s_ease-out]"
      role="dialog"
      aria-label="模块详情"
    >
      <div className="flex items-start justify-between gap-2 mb-4">
        <div className="min-w-0">
          <p className="text-xs text-white/45 uppercase tracking-wider mb-1">模块详情</p>
          <h2 className="text-lg font-medium leading-snug">{module.name}</h2>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="p-2 rounded-xl hover:bg-white/10 transition-colors shrink-0"
          aria-label="关闭"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="mb-4">
        <p className="text-sm tabular-nums mb-2">
          已修学分:{' '}
          <span className="font-medium">{formatCredits(module.earned)}</span>
          <span className="text-white/50"> / {formatCredits(module.required)}</span>
        </p>
        <div className="h-2 rounded-full bg-white/10 overflow-hidden mb-2">
          <div
            className="h-full rounded-full transition-all duration-300"
            style={{ width: `${Math.min(percent, 100)}%`, backgroundColor: barColor }}
          />
        </div>
        <p className="text-xs text-white/45 tabular-nums">{percent}%</p>
      </div>

      <div className="flex-1 overflow-y-auto scrollbar-none">
        {children.length > 0 ? (
          <>
            <p className="text-xs text-white/45 uppercase tracking-wider mb-2 px-1">
              子模块（只读）
            </p>
            <ul className="space-y-2">
              {children.map((child) => {
                const subId = String(child.id)
                const expanded = expandedSubs[subId]
                const cp = modulePercent(child)

                return (
                  <li
                    key={child.id}
                    className="rounded-xl bg-white/5 border border-white/8 overflow-hidden"
                  >
                    <button
                      type="button"
                      onClick={() => toggleSub(subId)}
                      className="collapse-button"
                    >
                      {expanded ? (
                        <ChevronDown className="w-4 h-4 shrink-0 text-white/50" />
                      ) : (
                        <ChevronRight className="w-4 h-4 shrink-0 text-white/50" />
                      )}
                      <span className="flex-1 text-sm truncate text-left">{child.name}</span>
                      <span className="text-xs tabular-nums" style={{ color: percentColor(cp) }}>
                        {cp}%
                      </span>
                    </button>
                    {expanded && (
                      <div className="px-2 pb-2 pt-0">
                        <div className="flex items-center justify-between text-xs px-2 py-1">
                          <span className="text-white/50">学分</span>
                          <span className="tabular-nums">
                            <span className="text-emerald-400">{formatCredits(child.earned)}</span>
                            <span className="text-white/30"> / </span>
                            <span className="text-white/50">{formatCredits(child.required)}</span>
                          </span>
                        </div>
                        <div className="h-1.5 rounded-full bg-white/10 overflow-hidden mx-2 my-1">
                          <div
                            className="h-full rounded-full"
                            style={{ width: `${Math.min(cp, 100)}%`, backgroundColor: percentColor(cp) }}
                          />
                        </div>
                        {child.earned >= child.required && child.required > 0 && (
                          <div className="flex items-center gap-1 px-2 py-1">
                            <Check className="w-3 h-3 text-emerald-400" />
                            <span className="text-xs text-emerald-400/70">已完成</span>
                          </div>
                        )}
                      </div>
                    )}
                  </li>
                )
              })}
            </ul>
          </>
        ) : (
          <>
            <p className="text-xs text-white/45 uppercase tracking-wider mb-2 px-1 flex items-center gap-1">
              <BookOpen className="w-3 h-3" />
              推荐课程
            </p>
            {loadingCourses ? (
              <div className="flex items-center justify-center py-8">
                <Clock className="w-5 h-5 text-white/40 animate-spin" />
              </div>
            ) : recommendCourses.length === 0 ? (
              <p className="text-sm text-white/45 px-2 py-3 rounded-xl bg-white/5">
                暂无推荐课程
              </p>
            ) : (
              <ul className="space-y-2">
                {recommendCourses.map((course) => (
                  <li
                    key={course.id}
                    className="rounded-xl bg-white/5 border border-white/8 p-3"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <p className="text-sm font-medium truncate">{course.name}</p>
                        <p className="text-xs text-white/45">{course.course_code}</p>
                      </div>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 shrink-0">
                        {course.credit} 学分
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </div>
    </aside>
  )
}
