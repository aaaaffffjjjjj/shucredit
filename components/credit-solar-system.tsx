'use client'

import { apiFetch } from '@/lib/api'
import {
  transformRootModules,
  toPlanetModules,
  modulePercent,
  percentColor,
  type ApiModule,
  type PlanetModule,
} from '@/lib/progress'
import { MathFormulaCSS2D, SCENE_BG } from '@/components/math-background'
import { useRef, useMemo, useEffect, useState, useCallback } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib'
import * as THREE from 'three'

export type { PlanetModule } from '@/lib/progress'

const INITIAL_CAMERA = new THREE.Vector3(0, 6, 22)
const INITIAL_TARGET = new THREE.Vector3(0, 0, 0)
const FOCUS_LERP = 0.06

function createPlanetTexture(primary: string, highlight: string): THREE.CanvasTexture {
  const canvas = document.createElement('canvas')
  canvas.width = 256
  canvas.height = 256
  const ctx = canvas.getContext('2d')!
  const p = new THREE.Color(primary)
  const h = new THREE.Color(highlight)
  const grad = ctx.createRadialGradient(96, 72, 8, 128, 128, 150)
  grad.addColorStop(0, `rgb(${h.r * 255},${h.g * 255},${h.b * 255})`)
  grad.addColorStop(0.55, `rgb(${p.r * 255},${p.g * 255},${p.b * 255})`)
  grad.addColorStop(1, `rgb(${p.r * 160},${p.g * 160},${p.b * 160})`)
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, 256, 256)
  for (let i = 0; i < 600; i++) {
    ctx.fillStyle = `rgba(255,255,255,${Math.random() * 0.05})`
    ctx.fillRect(Math.random() * 256, Math.random() * 256, 1, 1)
  }
  return new THREE.CanvasTexture(canvas)
}

function Sun() {
  const meshRef = useRef<THREE.Mesh>(null)
  useFrame(() => {
    if (meshRef.current) meshRef.current.rotation.y += 0.001
  })
  return (
    <group>
      <mesh>
        <sphereGeometry args={[4.9, 48, 48]} />
        <meshBasicMaterial color="#ffe4a8" transparent opacity={0.12} depthWrite={false} />
      </mesh>
      <mesh>
        <sphereGeometry args={[4.7, 48, 48]} />
        <meshBasicMaterial color="#ffd080" transparent opacity={0.1} depthWrite={false} />
      </mesh>
      <mesh ref={meshRef}>
        <sphereGeometry args={[4.5, 64, 64]} />
        <meshStandardMaterial
          color="#fff4dc"
          emissive="#ffcc66"
          emissiveIntensity={0.4}
          roughness={0.35}
          metalness={0.08}
        />
        <pointLight color="#ffe4b8" intensity={2.2} distance={90} decay={1.6} />
      </mesh>
    </group>
  )
}

function OrbitRing({
  radius,
  highlighted,
  dimmed,
}: {
  radius: number
  highlighted?: boolean
  dimmed?: boolean
}) {
  const geometry = useMemo(() => {
    const points: THREE.Vector3[] = []
    for (let i = 0; i <= 64; i++) {
      const a = (i / 64) * Math.PI * 2
      points.push(new THREE.Vector3(Math.cos(a) * radius, 0, Math.sin(a) * radius))
    }
    return new THREE.BufferGeometry().setFromPoints(points)
  }, [radius])

  return (
    <line geometry={geometry}>
      <lineBasicMaterial
        color="#ffffff"
        transparent
        opacity={highlighted ? 0.3 : dimmed ? 0.06 : 0.15}
      />
    </line>
  )
}

function ProgressRing({
  percent,
  innerRadius,
  outerRadius,
  color,
}: {
  percent: number
  innerRadius: number
  outerRadius: number
  color: string
}) {
  const arc = (Math.min(percent, 100) / 100) * Math.PI * 2
  return (
    <group rotation={[Math.PI / 2, 0, 0]}>
      <mesh>
        <ringGeometry args={[innerRadius, outerRadius, 64, 1, 0, Math.PI * 2]} />
        <meshBasicMaterial color="#ffffff" transparent opacity={0.1} side={THREE.DoubleSide} depthWrite={false} />
      </mesh>
      {arc > 0.02 && (
        <mesh>
          <ringGeometry args={[innerRadius, outerRadius, 64, 1, -Math.PI / 2, arc]} />
          <meshBasicMaterial color={color} transparent opacity={0.88} side={THREE.DoubleSide} depthWrite={false} />
        </mesh>
      )}
    </group>
  )
}

function Planet({
  planet,
  semester,
  isSelected,
  isHovered,
  dimmed,
  onHover,
  onSelect,
  onPositionUpdate,
}: {
  planet: PlanetModule
  semester: number
  isSelected: boolean
  isHovered: boolean
  dimmed: boolean
  onHover: (p: PlanetModule | null) => void
  onSelect: (p: PlanetModule) => void
  onPositionUpdate: (id: string, pos: THREE.Vector3) => void
}) {
  const groupRef = useRef<THREE.Group>(null)
  const meshRef = useRef<THREE.Mesh>(null)
  const angleRef = useRef(planet.angle)
  const hoverScale = useRef(1)

  const primary = planet.primary ?? planet.color
  const highlight = planet.highlight ?? planet.color
  const surfaceMap = useMemo(
    () => createPlanetTexture(primary, highlight),
    [primary, highlight],
  )
  const baseRadius = Math.max(0.65, planet.size || 0.65)
  const visualEarned = planet.earned * (semester / 8)
  const percent = modulePercent({ earned: visualEarned, required: planet.required })
  const ringColor = percentColor(percent)

  useFrame((state, delta) => {
    angleRef.current += planet.orbitSpeed * delta
    const x = Math.cos(angleRef.current) * planet.orbitRadius
    const z = Math.sin(angleRef.current) * planet.orbitRadius
    if (groupRef.current) {
      groupRef.current.position.set(x, 0, z)
      onPositionUpdate(planet.id, groupRef.current.position)
    }
    const breath =
      1 + Math.sin(state.clock.elapsedTime * planet.breathSpeed + planet.breathPhase) * 0.05
    const targetHover = isHovered ? 1.06 : 1
    hoverScale.current = THREE.MathUtils.lerp(hoverScale.current, targetHover, 0.1)
    groupRef.current?.scale.setScalar(breath * hoverScale.current)
    if (meshRef.current) meshRef.current.rotation.y += delta * 0.4
  })

  const bodyOpacity = dimmed ? 0.5 : 1

  return (
    <group ref={groupRef}>
      {isHovered && (
        <ProgressRing
          percent={percent}
          innerRadius={baseRadius * 1.18}
          outerRadius={baseRadius * 1.32}
          color={ringColor}
        />
      )}
      <mesh scale={1.15} renderOrder={1}>
        <sphereGeometry args={[baseRadius, 48, 48]} />
        <meshBasicMaterial
          color={primary}
          transparent
          opacity={0.12}
          side={THREE.BackSide}
          depthWrite={false}
        />
      </mesh>
      <mesh
        ref={meshRef}
        renderOrder={2}
        onPointerOver={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'pointer'
          onHover(planet)
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'auto'
          onHover(null)
        }}
        onClick={(e) => {
          e.stopPropagation()
          onSelect(planet)
        }}
      >
        <sphereGeometry args={[baseRadius, 48, 48]} />
        <meshStandardMaterial
          map={surfaceMap}
          color={primary}
          emissive={highlight}
          emissiveIntensity={isSelected || isHovered ? 0.32 : 0.18}
          metalness={0.4}
          roughness={0.32}
          opacity={bodyOpacity}
          transparent={bodyOpacity < 1}
        />
      </mesh>
    </group>
  )
}

function Scene({
  semester,
  planets,
  selectedId,
  focusedId,
  onPlanetHover,
  onPlanetClick,
  controlsRef,
  livePositions,
}: {
  semester: number
  planets: PlanetModule[]
  selectedId: string | null
  focusedId: string | null
  onPlanetHover: (p: PlanetModule | null) => void
  onPlanetClick: (p: PlanetModule) => void
  controlsRef: React.RefObject<OrbitControlsImpl | null>
  livePositions: React.MutableRefObject<Map<string, THREE.Vector3>>
}) {
  const [hoveredId, setHoveredId] = useState<string | null>(null)

  const handleHover = useCallback(
    (p: PlanetModule | null) => {
      setHoveredId(p?.id ?? null)
      onPlanetHover(p)
    },
    [onPlanetHover],
  )

  const handlePosition = useCallback(
    (id: string, pos: THREE.Vector3) => {
      livePositions.current.set(id, pos.clone())
    },
    [livePositions],
  )

  const maxOrbit = useMemo(
    () => Math.max(...planets.map((p) => p.orbitRadius), 10),
    [planets],
  )

  return (
    <>
      <ambientLight intensity={0.78} />
      <hemisphereLight args={['#dce8ff', SCENE_BG, 0.52]} position={[0, 28, 0]} />
      <directionalLight position={[12, 16, 10]} intensity={1.1} color="#fff8ee" />
      <directionalLight position={[-8, 10, -6]} intensity={0.35} color="#8aa0cc" />

      <MathFormulaCSS2D count={180} />
      <Sun />

      {planets.map((planet) => (
        <OrbitRing
          key={`orbit-${planet.id}`}
          radius={planet.orbitRadius}
          highlighted={
            selectedId === planet.id ||
            focusedId === planet.id ||
            hoveredId === planet.id
          }
          dimmed={focusedId != null && focusedId !== planet.id}
        />
      ))}

      {planets.map((planet) => (
        <Planet
          key={planet.id}
          planet={planet}
          semester={semester}
          isSelected={selectedId === planet.id || focusedId === planet.id}
          isHovered={hoveredId === planet.id}
          dimmed={focusedId != null && focusedId !== planet.id}
          onHover={handleHover}
          onSelect={onPlanetClick}
          onPositionUpdate={handlePosition}
        />
      ))}

      <OrbitControls
        ref={controlsRef}
        enablePan
        minDistance={10}
        maxDistance={maxOrbit + 24}
        autoRotate={!focusedId}
        autoRotateSpeed={0.12}
        enableDamping
        dampingFactor={0.06}
      />
    </>
  )
}

function CameraRig({
  focusId,
  livePositions,
  resetToken,
  controlsRef,
}: {
  focusId: string | null
  livePositions: React.MutableRefObject<Map<string, THREE.Vector3>>
  resetToken: number
  controlsRef: React.RefObject<OrbitControlsImpl | null>
}) {
  const { camera } = useThree()
  const desired = useRef(INITIAL_CAMERA.clone())
  const lookAt = useRef(INITIAL_TARGET.clone())

  useEffect(() => {
    desired.current.copy(INITIAL_CAMERA)
    lookAt.current.copy(INITIAL_TARGET)
    camera.position.copy(INITIAL_CAMERA)
    camera.lookAt(INITIAL_TARGET)
    const ctrl = controlsRef.current
    if (ctrl) {
      ctrl.target.copy(INITIAL_TARGET)
      ctrl.update()
    }
  }, [resetToken, controlsRef, camera])

  useFrame(() => {
    if (!focusId) return
    const live = livePositions.current.get(focusId)
    if (live) {
      desired.current.set(live.x + 3, live.y + 5, live.z + 7)
      lookAt.current.copy(live)
    }
    camera.position.lerp(desired.current, FOCUS_LERP)
    camera.lookAt(lookAt.current)
  })

  return null
}

export interface CreditSolarSystemProps {
  semester?: number
  onPlanetClick?: (planet: PlanetModule) => void
  planets?: PlanetModule[]
  loading?: boolean
  error?: string | null
  onModulesLoaded?: (planets: PlanetModule[]) => void
  selectedModuleId?: string | null
  onModuleHover?: (planet: PlanetModule | null) => void
  refreshKey?: number
  resetViewTrigger?: number
}

export default function CreditSolarSystem({
  semester = 8,
  onPlanetClick,
  planets: planetsProp,
  loading: loadingProp,
  error: errorProp,
  onModulesLoaded,
  selectedModuleId = null,
  onModuleHover,
  refreshKey = 0,
  resetViewTrigger = 0,
}: CreditSolarSystemProps) {
  const [internalPlanets, setInternalPlanets] = useState<PlanetModule[]>([])
  const [internalLoading, setInternalLoading] = useState(!planetsProp)
  const [internalError, setInternalError] = useState<string | null>(null)
  const [focusedId, setFocusedId] = useState<string | null>(null)
  const [resetToken, setResetToken] = useState(0)
  const controlsRef = useRef<OrbitControlsImpl | null>(null)
  const livePositions = useRef(new Map<string, THREE.Vector3>())

  const controlled = planetsProp !== undefined
  const planets = controlled ? planetsProp : internalPlanets
  const loading = controlled ? (loadingProp ?? false) : internalLoading
  const error = controlled ? (errorProp ?? null) : internalError

  useEffect(() => {
    if (controlled) return
    let cancelled = false
    setInternalLoading(true)
    setInternalError(null)
    apiFetch('/api/progress_data', { method: 'GET' })
      .then(async (res) => {
        if (res.status === 401) throw new Error('未登录，请先登录')
        if (!res.ok) {
          const body = await res.json().catch(() => ({}))
          throw new Error(body.error || body.message || `HTTP ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        if (cancelled) return
        const transformed = toPlanetModules(
          transformRootModules(data.modules || []),
        )
        setInternalPlanets(transformed)
        onModulesLoaded?.(transformed)
      })
      .catch((err) => {
        if (cancelled) return
        setInternalError(err instanceof Error ? err.message : String(err))
      })
      .finally(() => {
        if (!cancelled) setInternalLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [controlled, onModulesLoaded, refreshKey])

  useEffect(() => {
    if (resetViewTrigger <= 0) return
    setFocusedId(null)
    setResetToken((t) => t + 1)
  }, [resetViewTrigger])

  useEffect(() => {
    if (!selectedModuleId) {
      setFocusedId(null)
      return
    }
    setFocusedId(selectedModuleId)
  }, [selectedModuleId])

  if (loading) {
    return (
      <div
        className="w-full h-full flex flex-col items-center justify-center gap-3"
        style={{ background: SCENE_BG }}
      >
        <div className="w-6 h-6 border-2 border-white/20 border-t-white/80 rounded-full animate-spin" />
        <p className="text-sm text-white/50">正在加载学分数据…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div
        className="w-full h-full flex items-center justify-center p-6"
        style={{ background: SCENE_BG }}
      >
        <p className="text-sm text-red-400">加载失败：{error}</p>
      </div>
    )
  }

  if (!planets.length) {
    return (
      <p className="w-full h-full flex items-center justify-center text-white/50 text-sm" style={{ background: SCENE_BG }}>
        暂无顶级模块数据
      </p>
    )
  }

  return (
    <div className="w-full h-full overflow-hidden relative" style={{ background: 'transparent', position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, zIndex: 1 }}>
      <Canvas camera={{ position: [0, 6, 22], fov: 48 }} gl={{ antialias: true, alpha: true }}>
        <Scene
          semester={semester}
          planets={planets}
          selectedId={selectedModuleId}
          focusedId={focusedId}
          onPlanetHover={onModuleHover ?? (() => {})}
          onPlanetClick={(p) => onPlanetClick?.(p)}
          controlsRef={controlsRef}
          livePositions={livePositions}
        />
      </Canvas>
    </div>
  )
}
