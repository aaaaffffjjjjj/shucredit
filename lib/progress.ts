/** Flask /api/progress_data 模块项 */
export interface ApiModule {
  id: number
  name: string
  parent_id: number | null
  required: number
  earned: number
  remaining: number
  percent: number
  status: string
}

export interface ProgressSun {
  required: number
  earned: number
}

export interface ProgressData {
  modules: ApiModule[]
  sun?: ProgressSun
  all_met?: boolean
}

export interface SidebarModule {
  id: string
  name: string
  required: number
  earned: number
}

export interface PlanetColorPair {
  primary: string
  highlight: string
}

export const MODULE_COLOR_PAIRS: Array<{ key: string } & PlanetColorPair> = [
  { key: '公共基础', primary: '#a1a1aa', highlight: '#d4d4d8' },
  { key: '专业基础', primary: '#71717a', highlight: '#a1a1aa' },
  { key: '专业必修', primary: '#52525b', highlight: '#71717a' },
  { key: '专业选修', primary: '#3f3f46', highlight: '#52525b' },
  { key: '个性化', primary: '#27272a', highlight: '#3f3f46' },
  { key: '专业方向', primary: '#18181b', highlight: '#27272a' },
]

const COLOR_FALLBACK: PlanetColorPair[] = MODULE_COLOR_PAIRS.map(
  ({ primary, highlight }) => ({ primary, highlight }),
)

export function getPlanetColors(name: string, index = 0): PlanetColorPair {
  for (const item of MODULE_COLOR_PAIRS) {
    if (name.includes(item.key)) {
      return { primary: item.primary, highlight: item.highlight }
    }
  }
  return COLOR_FALLBACK[index % COLOR_FALLBACK.length]
}

/** 行星半径：最大 1.1，最小 0.65（避免过小不可见） */
export function mapRequiredToPlanetRadius(required: number): number {
  const r = Math.max(required, 2)
  return Math.max(0.65, Math.min(1.1, Math.log2(r) * 0.15 + 0.35))
}

/** 顶级模块 → 侧栏 / 太阳系行星 */
export function transformRootModules(apiModules: ApiModule[]): SidebarModule[] {
  const roots = apiModules.filter((m) => m.parent_id == null)
  return roots.map((p) => ({
    id: String(p.id),
    name: p.name,
    required: Number(p.required) || 0,
    earned: Number(p.earned) || 0,
  }))
}

/** 侧栏数据 + 太阳系轨道布局（轨道圆心为太阳 0,0,0） */
export function toPlanetModules(sidebar: SidebarModule[]) {
  const count = sidebar.length || 1
  return sidebar.map((p, idx) => {
    const colors = getPlanetColors(p.name, idx)
    return {
      ...p,
      ...colors,
      color: colors.primary,
      orbitRadius: 8 + idx * 2.4,
      angle: (idx / count) * Math.PI * 2,
      size: mapRequiredToPlanetRadius(p.required),
      breathSpeed: (Math.PI * 2) / (3 + Math.random() * 3),
      breathPhase: Math.random() * Math.PI * 2,
      /** 公转角速度（弧度/秒），外圈略慢 */
      orbitSpeed: 0.052 - idx * 0.0045,
    }
  })
}

export type PlanetModule = ReturnType<typeof toPlanetModules>[number]

export function getModuleById(
  all: ApiModule[],
  id: string,
): ApiModule | undefined {
  return all.find((m) => String(m.id) === id)
}

export function getChildModules(
  all: ApiModule[],
  parentId: string,
): ApiModule[] {
  const pid = Number(parentId)
  return all.filter((m) => m.parent_id === pid)
}

export function getDescendantModuleIds(
  all: ApiModule[],
  rootId: number,
): number[] {
  const ids = new Set<number>([rootId])
  let changed = true
  while (changed) {
    changed = false
    for (const m of all) {
      if (m.parent_id != null && ids.has(m.parent_id) && !ids.has(m.id)) {
        ids.add(m.id)
        changed = true
      }
    }
  }
  return [...ids]
}

export function modulePercent(m: { earned: number; required: number }): number {
  if (!m.required) return 0
  return Math.min(100, Math.round((m.earned / m.required) * 1000) / 10)
}

export function percentColor(percent: number): string {
  if (percent >= 100) return '#10b981'
  if (percent < 60) return '#ef4444'
  return '#f59e0b'
}

export function formatCredits(value: number): string {
  const n = Number(value) || 0
  return Number.isInteger(n) ? String(n) : n.toFixed(1)
}
