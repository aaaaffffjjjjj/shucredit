'use client'

import { useState, useMemo, useEffect, useCallback } from 'react'
import dynamic from 'next/dynamic'
import Link from 'next/link'
import { LogOut, Settings } from 'lucide-react'
import {
  transformRootModules,
  toPlanetModules,
  type ApiModule,
  type ProgressSun,
  type SidebarModule,
} from '@/lib/progress'
import { MathBackground, SCENE_BG } from '@/components/math-background'
import TopNavbar from '@/components/top-navbar'
import SidebarModules from '@/components/sidebar-modules'
import PlanetDetailPanel from '@/components/planet-detail-panel'
import ToolPanel from '@/components/tool-panel'
import UploadPdf from '@/components/upload-pdf'
import { CollegeSelector } from '@/components/college-selector'
import { MajorSelector } from '@/components/major-selector'
import { AdminPanel } from '@/components/admin-panel'
import { apiFetch } from '@/lib/api'
import { useRouter } from 'next/navigation'

const CreditSolarSystem = dynamic(
  () => import('@/components/credit-solar-system'),
  {
    ssr: false,
    loading: () => (
      <div
        className="w-full h-full flex flex-col items-center justify-center gap-3"
        style={{ background: '#1a1f2e' }}
      >
        <div className="w-8 h-8 border-2 border-white/20 border-t-white/80 rounded-full animate-spin" />
        <p className="text-sm text-white/40">加载太阳系场景…</p>
      </div>
    ),
  },
)

function applyProgressPayload(
  data: { modules?: ApiModule[]; sun?: ProgressSun },
  setAllModules: (m: ApiModule[]) => void,
  setModules: (m: SidebarModule[]) => void,
  setSun: (s: ProgressSun | null) => void,
) {
  const apiModules: ApiModule[] = data.modules || []
  setAllModules(apiModules)
  setModules(transformRootModules(apiModules))
  setSun(data.sun ?? null)
}

export default function DashboardPage() {
  const router = useRouter()
  const [semester] = useState(8)
  const [selectedModule, setSelectedModule] = useState<string | null>(null)
  const [focusSubModuleId, setFocusSubModuleId] = useState<string | null>(null)
  const [modules, setModules] = useState<SidebarModule[]>([])
  const [allModules, setAllModules] = useState<ApiModule[]>([])
  const [sun, setSun] = useState<ProgressSun | null>(null)
  const [progressLoading, setProgressLoading] = useState(true)
  const [progressError, setProgressError] = useState<string | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)
  const [resetViewTrigger, setResetViewTrigger] = useState(0)
  const [authChecked, setAuthChecked] = useState(false)
  const [isToolPanelOpen, setIsToolPanelOpen] = useState(false)
  const [collegeId, setCollegeId] = useState<number | null>(null)
  const [majorId, setMajorId] = useState<number | null>(null)
  const [isAdminMode, setIsAdminMode] = useState(false)
  const [adminPanelOpen, setAdminPanelOpen] = useState(false)

  const planets = useMemo(() => toPlanetModules(modules), [modules])

<<<<<<< HEAD
  const loadProgress = useCallback(async (collegeIdOverride?: number | null, majorIdOverride?: number | null) => {
    setProgressLoading(true)
    setProgressError(null)
    try {
      const cid = collegeIdOverride !== undefined ? collegeIdOverride : collegeId
      const mid = majorIdOverride !== undefined ? majorIdOverride : majorId
      
      const params = new URLSearchParams()
      if (cid) params.set('college_id', String(cid))
      if (mid) params.set('major_id', String(mid))
      
      const url = params.toString()
        ? `/api/progress_data?${params.toString()}`
        : '/api/progress_data'
=======
  const loadProgress = useCallback(async (params?: { collegeId?: number | null; majorId?: number | null }) => {
    setProgressLoading(true)
    setProgressError(null)
    try {
      const cid = params?.collegeId !== undefined ? params.collegeId : collegeId
      const mid = params?.majorId !== undefined ? params.majorId : majorId
      const searchParams = new URLSearchParams()
      if (mid) {
        searchParams.set('major_id', String(mid))
      } else if (cid) {
        searchParams.set('college_id', String(cid))
      }
      const qs = searchParams.toString()
      const url = qs ? `/api/progress_data?${qs}` : '/api/progress_data'
>>>>>>> 362a0993f8aed3fe82b446ba8efe589d3311317e
      const res = await apiFetch(url, { method: 'GET' })
      if (res.status === 401) {
        router.replace('/login')
        return
      }
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.error || body.message || `HTTP ${res.status}`)
      }
      const data = await res.json()
      applyProgressPayload(data, setAllModules, setModules, setSun)
    } catch (err) {
      setProgressError(err instanceof Error ? err.message : '加载失败')
    } finally {
      setProgressLoading(false)
    }
  }, [router, collegeId, majorId])

  const handleCollegeChange = useCallback(
    (newCollegeId: number) => {
      setCollegeId(newCollegeId)
<<<<<<< HEAD
      setMajorId(null) // 切换学院时重置专业
=======
      setMajorId(null)
>>>>>>> 362a0993f8aed3fe82b446ba8efe589d3311317e
      apiFetch('/api/user/college', {
        method: 'POST',
        body: JSON.stringify({ college_id: newCollegeId }),
      }).catch(() => {
        /* ignore persistence error */
      })
<<<<<<< HEAD
      // 清除专业选择
      apiFetch('/api/user/major', {
        method: 'POST',
        body: JSON.stringify({ major_id: '' }),
      }).catch(() => {})
      loadProgress(newCollegeId, null)
=======
      loadProgress({ collegeId: newCollegeId, majorId: null })
>>>>>>> 362a0993f8aed3fe82b446ba8efe589d3311317e
    },
    [loadProgress],
  )

  const handleMajorChange = useCallback(
<<<<<<< HEAD
    (newMajorId: number | null) => {
      setMajorId(newMajorId)
      apiFetch('/api/user/major', {
        method: 'POST',
        body: JSON.stringify({ major_id: newMajorId }),
      }).catch(() => {
        /* ignore persistence error */
      })
      loadProgress(undefined, newMajorId)
=======
    (newMajorId: number) => {
      setMajorId(newMajorId)
      loadProgress({ majorId: newMajorId })
>>>>>>> 362a0993f8aed3fe82b446ba8efe589d3311317e
    },
    [loadProgress],
  )

  useEffect(() => {
    apiFetch('/api/auth/me')
      .then(async (res) => {
        if (!res.ok) {
          router.replace('/login')
          return
        }
        const data = await res.json()
        if (data.college?.id) {
          setCollegeId(data.college.id)
        }
        if (data.major?.id) {
          setMajorId(data.major.id)
        }
      })
      .catch(() => router.replace('/login'))
      .finally(() => setAuthChecked(true))
  }, [router])

  useEffect(() => {
    if (!authChecked) return
    loadProgress()
  }, [authChecked, refreshKey, loadProgress])

  const handleSelectModule = (id: string) => {
    setFocusSubModuleId(null)
    setSelectedModule((prev) => (prev === id ? null : id))
  }

  const handleSelectSubModule = (rootId: string, subId: string) => {
    setSelectedModule(rootId)
    setFocusSubModuleId(subId)
  }

  const handlePlanetClick = (planet: { id: string }) => {
    setFocusSubModuleId(null)
    setSelectedModule((prev) => (prev === planet.id ? null : planet.id))
  }

  const handleResetView = () => {
    setSelectedModule(null)
    setFocusSubModuleId(null)
    setResetViewTrigger((t) => t + 1)
  }

  const handleLogout = async () => {
    try {
      await apiFetch('/api/auth/logout', { method: 'POST' })
    } catch {
      /* ignore */
    }
    router.push('/login')
  }

  if (!authChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: SCENE_BG }}>
        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen relative overflow-hidden" style={{ background: SCENE_BG }}>
      <MathBackground formulaCount={150} />
      <header className="fixed top-2 sm:top-4 left-2 sm:left-4 right-2 sm:right-auto z-50 flex items-center gap-1.5 sm:gap-2 flex-wrap">
        <CollegeSelector
          value={collegeId}
          onChange={handleCollegeChange}
          onAdminActivated={() => setIsAdminMode(true)}
          className="text-xs sm:text-sm"
        />
        <MajorSelector
          collegeId={collegeId}
          value={majorId}
          onChange={handleMajorChange}
          className="text-xs sm:text-sm"
        />
        <MajorSelector
          collegeId={collegeId}
          value={majorId}
          onChange={handleMajorChange}
        />
        {isAdminMode && (
          <button
            type="button"
            onClick={() => setAdminPanelOpen(true)}
            className="flex items-center gap-1 px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/30 text-amber-400 text-xs sm:text-sm transition-colors"
          >
            <Settings className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
            <span className="hidden sm:inline">管理后台</span>
          </button>
        )}
        <Link
          href="/forum"
          className="glass-card !rounded-full px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm text-white/70 hover:text-white transition-colors"
        >
          论坛
        </Link>
        <button
          type="button"
          onClick={handleLogout}
          className="glass-card !rounded-full p-2 sm:p-2.5 text-white/70 hover:text-white transition-colors"
          title="退出"
        >
          <LogOut className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
        </button>
      </header>

      <main className="relative w-full h-screen min-h-[600px]">
        {!progressLoading && modules.length > 0 && (
          <TopNavbar
            modules={modules}
            selectedModuleId={selectedModule}
            onSelectModule={handleSelectModule}
            onResetView={handleResetView}
          />
        )}

        <SidebarModules
          modules={modules}
          allModules={allModules}
          selectedModuleId={selectedModule}
          onSelectModule={handleSelectModule}
          onSelectSubModule={handleSelectSubModule}
          loading={progressLoading}
          uploadSlot={
            <UploadPdf onSuccess={() => setRefreshKey((k) => k + 1)} />
          }
        />

        {progressError && (
          <p className="absolute bottom-4 left-1/2 -translate-x-1/2 z-40 text-red-400 text-sm glass-card px-4 py-2">
            {progressError}
          </p>
        )}

        <CreditSolarSystem
          semester={semester}
          planets={planets}
          loading={progressLoading}
          error={progressError}
          selectedModuleId={selectedModule}
          resetViewTrigger={resetViewTrigger}
          onPlanetClick={handlePlanetClick}
          onSunClick={() => setIsToolPanelOpen(true)}
          collegeId={collegeId}
        />

        <PlanetDetailPanel
          moduleId={selectedModule}
          focusSubModuleId={focusSubModuleId}
          allModules={allModules}
          onClose={() => {
            setSelectedModule(null)
            setFocusSubModuleId(null)
          }}
        />

        <ToolPanel
          isOpen={isToolPanelOpen}
          onClose={() => setIsToolPanelOpen(false)}
          initialTool="feedback"
          onFocusModule={(moduleId) => {
            setSelectedModule(moduleId)
          }}
          progressData={{
            sun: sun ?? undefined,
            modules: allModules.map(m => ({
              id: m.id,
              name: m.name,
              required: m.required,
              earned: m.earned,
              parent_id: m.parent_id,
              percent: m.percent
            }))
          }}
        />

        <AdminPanel
          open={adminPanelOpen}
          onClose={() => setAdminPanelOpen(false)}
          onDataChanged={() => setRefreshKey((k) => k + 1)}
        />
      </main>
    </div>
  )
}
