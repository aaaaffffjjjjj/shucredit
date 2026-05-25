'use client'

import { X } from 'lucide-react'
import {
  getChildModules,
  getModuleById,
  modulePercent,
  percentColor,
  type ApiModule,
} from '@/lib/progress'

function formatCredits(value: number): string {
  const n = Number(value) || 0
  return Number.isInteger(n) ? String(n) : n.toFixed(1)
}

interface ModuleDetailPanelProps {
  moduleId: string | null
  allModules: ApiModule[]
  onClose: () => void
}

export default function ModuleDetailPanel({
  moduleId,
  allModules,
  onClose,
}: ModuleDetailPanelProps) {
  if (!moduleId) return null

  const module = getModuleById(allModules, moduleId)
  if (!module) return null

  const children = getChildModules(allModules, moduleId)
  const percent = modulePercent(module)
  const barColor = percentColor(percent)

  return (
    <div
      className="absolute top-0 right-0 bottom-0 z-30 w-full max-w-sm flex flex-col border-l border-border/80 bg-background/75 backdrop-blur-xl shadow-2xl font-sans transition-transform duration-300 ease-out"
      style={{ animation: 'slideInPanel 0.28s ease-out' }}
      role="dialog"
      aria-label="模块详情"
    >
      <div className="flex items-start justify-between gap-3 p-5 border-b border-border/60">
        <div className="min-w-0">
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
            模块详情
          </p>
          <h2 className="text-lg font-medium text-foreground leading-snug">
            {module.name}
          </h2>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="shrink-0 p-2 rounded-xl border border-border/80 bg-card/60 text-muted-foreground hover:text-foreground hover:bg-card transition-colors duration-200"
          aria-label="关闭"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-6">
        <section>
          <div className="flex items-baseline justify-between mb-2">
            <span className="text-sm text-muted-foreground">学分进度</span>
            <span className="text-sm tabular-nums font-medium" style={{ color: barColor }}>
              {percent}%
            </span>
          </div>
          <div className="h-2 rounded-full bg-card overflow-hidden mb-2">
            <div
              className="h-full rounded-full transition-all duration-300"
              style={{
                width: `${Math.min(percent, 100)}%`,
                backgroundColor: barColor,
              }}
            />
          </div>
          <p className="text-sm tabular-nums text-foreground">
            已修{' '}
            <span className="font-medium">{formatCredits(module.earned)}</span>
            <span className="text-muted-foreground">
              {' '}
              / {formatCredits(module.required)} 学分
            </span>
          </p>
          {module.remaining > 0 && (
            <p className="text-xs text-muted-foreground mt-1 tabular-nums">
              还差 {formatCredits(module.remaining)} 学分
            </p>
          )}
        </section>

        <section>
          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-3">
            子模块
            {children.length > 0 && (
              <span className="ml-1 normal-case">（{children.length}）</span>
            )}
          </p>
          {children.length === 0 ? (
            <p className="text-sm text-muted-foreground rounded-xl border border-border/50 bg-card/30 px-4 py-3">
              该模块下暂无子模块
            </p>
          ) : (
            <ul className="space-y-2">
              {children.map((child) => {
                const childPercent = modulePercent(child)
                const childColor = percentColor(childPercent)
                return (
                  <li
                    key={child.id}
                    className="rounded-xl border border-border/60 bg-card/40 px-4 py-3 transition-colors duration-200 hover:bg-card/60"
                  >
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <span className="text-sm text-foreground leading-snug">
                        {child.name}
                      </span>
                      <span
                        className="text-xs tabular-nums shrink-0 font-medium"
                        style={{ color: childColor }}
                      >
                        {childPercent}%
                      </span>
                    </div>
                    <div className="h-1.5 rounded-full bg-background/80 overflow-hidden mb-1.5">
                      <div
                        className="h-full rounded-full transition-all duration-300"
                        style={{
                          width: `${Math.min(childPercent, 100)}%`,
                          backgroundColor: childColor,
                        }}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground tabular-nums">
                      {formatCredits(child.earned)} / {formatCredits(child.required)}{' '}
                      学分
                    </p>
                  </li>
                )
              })}
            </ul>
          )}
        </section>
      </div>
    </div>
  )
}
