'use client'

import { RotateCcw } from 'lucide-react'

export interface NavModule {
  id: string
  name: string
}

interface TopNavbarProps {
  modules: NavModule[]
  selectedModuleId: string | null
  onSelectModule: (id: string) => void
  onResetView: () => void
}

function shortenName(name: string, max = 10): string {
  return name.length <= max ? name : `${name.slice(0, max)}…`
}

export default function TopNavbar({
  modules,
  selectedModuleId,
  onSelectModule,
  onResetView,
}: TopNavbarProps) {
  if (!modules.length) return null

  return (
    <nav
      className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-1.5 max-w-[min(94vw,980px)] px-3 py-2 bg-black/40 backdrop-blur-lg rounded-full border border-white/10 shadow-lg"
      aria-label="模块导航"
    >
      <div className="flex items-center gap-1 overflow-x-auto scrollbar-none">
        {modules.map((module) => {
          const active = selectedModuleId === module.id
          return (
            <button
              key={module.id}
              type="button"
              title={module.name}
              onClick={() => onSelectModule(module.id)}
              className={`shrink-0 px-4 py-2 rounded-full text-sm transition-all duration-200 whitespace-nowrap ${
                active
                  ? 'bg-white/20 text-white'
                  : 'text-white/60 hover:text-white hover:bg-white/10'
              }`}
            >
              {shortenName(module.name)}
            </button>
          )
        })}
      </div>
      <div className="w-px h-5 bg-white/15 shrink-0" aria-hidden />
      <button
        type="button"
        onClick={onResetView}
        title="重置视角"
        className="shrink-0 p-2 rounded-full text-white/60 hover:text-white hover:bg-white/10 transition-all duration-200"
      >
        <RotateCcw className="w-4 h-4" />
      </button>
    </nav>
  )
}
