'use client'

import { useState, type ReactNode } from 'react'
import { ChevronDown, ChevronRight, Menu, X } from 'lucide-react'
import {
  getChildModules,
  modulePercent,
  percentColor,
  formatCredits,
  type ApiModule,
  type SidebarModule,
} from '@/lib/progress'

interface SidebarModulesProps {
  modules: SidebarModule[]
  allModules: ApiModule[]
  selectedModuleId: string | null
  onSelectModule: (id: string) => void
  onSelectSubModule: (moduleId: string, subModuleId: string) => void
  loading?: boolean
  uploadSlot?: ReactNode
}

export default function SidebarModules({
  modules,
  allModules,
  selectedModuleId,
  onSelectModule,
  onSelectSubModule,
  loading,
  uploadSlot,
}: SidebarModulesProps) {
  const [expandedRoots, setExpandedRoots] = useState<Record<string, boolean>>({})
  const [mobileOpen, setMobileOpen] = useState(false)

  const toggleRoot = (id: string) => {
    setExpandedRoots((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  if (loading) {
    return (
      <div className="glass-card fixed left-4 top-1/2 -translate-y-1/2 z-40 w-64 p-4 text-white/50 text-sm">
        加载模块…
      </div>
    )
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setMobileOpen(true)}
        className="sm:hidden fixed left-2 top-1/2 -translate-y-1/2 z-40 p-2.5 rounded-xl glass-card text-white/70 hover:text-white transition-colors"
        aria-label="打开模块列表"
      >
        <Menu className="w-5 h-5" />
      </button>

      {mobileOpen && (
        <div
          className="sm:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside
        className={`glass-card fixed left-4 top-1/2 -translate-y-1/2 z-40 w-72 max-h-[min(85vh,640px)] flex flex-col p-4 text-white transition-transform duration-300 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-[calc(100%+2rem)] sm:translate-x-0'
        }`}
        aria-label="学分模块"
      >
        <div className="flex items-center justify-between mb-3 px-1">
          <p className="text-xs uppercase tracking-wider text-white/50">
            学分模块
          </p>
          <button
            type="button"
            onClick={() => setMobileOpen(false)}
            className="sm:hidden p-1 rounded text-white/40 hover:text-white hover:bg-white/10 transition-colors"
            aria-label="关闭"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto scrollbar-none space-y-1">
        {modules.map((mod) => {
          const children = getChildModules(allModules, mod.id)
          const expanded = expandedRoots[mod.id] ?? false
          const pct = modulePercent(mod)
          const active = selectedModuleId === mod.id

          return (
            <div key={mod.id} className="rounded-xl overflow-hidden">
              <div className="flex items-stretch gap-0.5">
                {children.length > 0 && (
                  <button
                    type="button"
                    onClick={() => toggleRoot(mod.id)}
                    className="collapse-button !w-auto !px-2 shrink-0"
                    aria-label={expanded ? '折叠' : '展开'}
                  >
                    {expanded ? (
                      <ChevronDown className="w-3.5 h-3.5" />
                    ) : (
                      <ChevronRight className="w-3.5 h-3.5" />
                    )}
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => onSelectModule(mod.id)}
                  className={`collapse-button flex-1 ${active ? 'bg-white/15' : ''}`}
                >
                  <span className="flex-1 truncate text-left text-sm">{mod.name}</span>
                  <span
                    className="text-xs tabular-nums shrink-0"
                    style={{ color: percentColor(pct) }}
                  >
                    {pct}%
                  </span>
                </button>
              </div>
              {!expanded && (
                <p className="text-[11px] text-white/40 px-2 pb-1 tabular-nums">
                  {formatCredits(mod.earned)}/{formatCredits(mod.required)} 学分
                </p>
              )}
              {expanded && children.length > 0 && (
                <ul className="ml-2 mt-1 mb-2 space-y-0.5 border-l border-white/10 pl-2">
                  {children.map((child) => (
                    <li key={child.id}>
                      <button
                        type="button"
                        onClick={() => onSelectSubModule(mod.id, String(child.id))}
                        className="collapse-button !py-1.5 !text-xs"
                      >
                        <span className="flex-1 truncate text-left">{child.name}</span>
                        <span className="text-white/45 tabular-nums shrink-0">
                          {formatCredits(child.earned)}/{formatCredits(child.required)}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )
        })}
      </div>
      {uploadSlot && <div className="mt-3 pt-3 border-t border-white/10">{uploadSlot}</div>}
      </aside>
    </>
  )
}
