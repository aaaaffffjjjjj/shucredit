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
const FOCUS_DURATION = 0.6 // 动画时长
const INITIAL_FOV = 48
const FOCUSED_FOV = 32 // 聚焦时放大

function easeInOutCubic(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}

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

function Sun({ onClick }: { onClick?: () => void }) {
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
      <mesh
        ref={meshRef}
        onPointerOver={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'pointer'
        }}
        onPointerOut={() => {
          document.body.style.cursor = 'auto'
        }}
        onClick={(e) => {
          e.stopPropagation()
          onClick?.()
        }}
      >
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

function Starfield() {
  const { positions, colors } = useMemo(() => {
    const count = 2000
    const p = new Float32Array(count * 3)
    const c = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      const r = 35 + Math.random() * 80
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      p[i * 3] = r * Math.sin(phi) * Math.cos(theta)
      p[i * 3 + 1] = (Math.random() - 0.5) * 30
      p[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta)
      const brightness = 0.4 + Math.random() * 0.6
      c[i * 3] = brightness
      c[i * 3 + 1] = brightness
      c[i * 3 + 2] = brightness
    }
    return { positions: p, colors: c }
  }, [])

  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions, 3]}
        />
        <bufferAttribute
          attach="attributes-color"
          args={[colors, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.15}
        vertexColors
        transparent
        opacity={0.8}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
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

function PlanetLabel({ 
  text, 
  visible, 
  positionY 
}: { 
  text: string, 
  visible: boolean, 
  positionY: number 
}) {
  const { camera } = useThree()
  const elementRef = useRef<HTMLDivElement | null>(null)
  const [labelVisible, setLabelVisible] = useState(false)

  useEffect(() => {
    if (visible && !elementRef.current) {
      const div = document.createElement('div')
      div.textContent = text
      div.style.position = 'fixed'
      div.style.pointerEvents = 'none'
      div.style.zIndex = '10'
      div.style.color = '#ffffff'
      div.style.fontSize = '14px'
      div.style.fontWeight = '500'
      div.style.fontFamily = 'system-ui, sans-serif'
      div.style.background = 'rgba(0, 0, 0, 0.6)'
      div.style.backdropFilter = 'blur(8px)'
      div.style.padding = '6px 12px'
      div.style.borderRadius = '8px'
      div.style.border = '1px solid rgba(255, 255, 255, 0.15)'
      div.style.textShadow = '0 2px 8px rgba(0, 0, 0, 0.5)'
      div.style.whiteSpace = 'nowrap'
      div.style.transition = 'opacity 0.2s ease, transform 0.2s ease'
      div.style.opacity = '0'
      div.style.transform = 'translate(-50%, -50%) scale(0.9)'
      document.body.appendChild(div)
      elementRef.current = div
    }

    if (elementRef.current) {
      if (visible) {
        elementRef.current.textContent = text
        elementRef.current.style.opacity = '1'
        elementRef.current.style.transform = 'translate(-50%, -50%) scale(1)'
        setLabelVisible(true)
      } else {
        elementRef.current.style.opacity = '0'
        elementRef.current.style.transform = 'translate(-50%, -50%) scale(0.9)'
        setLabelVisible(false)
      }
    }

    return () => {
      if (elementRef.current) {
        elementRef.current.remove()
        elementRef.current = null
      }
    }
  }, [visible, text])

  useFrame((state) => {
    if (elementRef.current && labelVisible) {
      const vector = new THREE.Vector3(0, positionY, 0)
      vector.project(camera)
      
      const x = (vector.x * 0.5 + 0.5) * window.innerWidth
      const y = (-(vector.y * 0.5) + 0.5) * window.innerHeight
      
      elementRef.current.style.left = `${x}px`
      elementRef.current.style.top = `${y}px`
    }
  })

  return null
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
  const isActive = isSelected || isHovered
  const segments = isActive ? 48 : 24
  const glowSegments = isActive ? 32 : 16

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
      <PlanetLabel 
        text={planet.name} 
        visible={isHovered || isSelected} 
        positionY={baseRadius + 0.8}
      />
      {isHovered && (
        <ProgressRing
          percent={percent}
          innerRadius={baseRadius * 1.18}
          outerRadius={baseRadius * 1.32}
          color={ringColor}
        />
      )}
      <mesh scale={1.15} renderOrder={1}>
        <sphereGeometry args={[baseRadius, glowSegments, glowSegments]} />
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
        <sphereGeometry args={[baseRadius, segments, segments]} />
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
  onSunClick,
  controlsRef,
  livePositions,
  planetsRef,
}: {
  semester: number
  planets: PlanetModule[]
  selectedId: string | null
  focusedId: string | null
  onPlanetHover: (p: PlanetModule | null) => void
  onPlanetClick: (p: PlanetModule) => void
  onSunClick?: () => void
  controlsRef: React.RefObject<OrbitControlsImpl | null>
  livePositions: React.MutableRefObject<Map<string, THREE.Vector3>>
  planetsRef: React.MutableRefObject<PlanetModule[]>
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
      <Starfield />
      <Sun onClick={onSunClick} />

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

      <CameraRig
        focusId={focusedId}
        livePositions={livePositions}
        resetToken={0}
        controlsRef={controlsRef}
        planetsRef={planetsRef}
      />
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
  planetsRef,
}: {
  focusId: string | null
  livePositions: React.MutableRefObject<Map<string, THREE.Vector3>>
  resetToken: number
  controlsRef: React.RefObject<OrbitControlsImpl | null>
  planetsRef: React.MutableRefObject<PlanetModule[]>
}) {
  const { camera, invalidate } = useThree()
  const animRef = useRef<{
    startPos: THREE.Vector3
    endPos: THREE.Vector3
    startTarget: THREE.Vector3
    endTarget: THREE.Vector3
    startFov: number
    endFov: number
    elapsed: number
    active: boolean
    isFocusing: boolean
  }>({
    startPos: INITIAL_CAMERA.clone(),
    endPos: INITIAL_CAMERA.clone(),
    startTarget: INITIAL_TARGET.clone(),
    endTarget: INITIAL_TARGET.clone(),
    startFov: INITIAL_FOV,
    endFov: INITIAL_FOV,
    elapsed: FOCUS_DURATION,
    active: false,
    isFocusing: false,
  })

  const prevFocusId = useRef<string | null>(null)

  useEffect(() => {
    const ctrl = controlsRef.current
    if (ctrl) {
      ctrl.target.copy(INITIAL_TARGET)
      ctrl.update()
    }
    prevFocusId.current = null
    animRef.current.endPos.copy(INITIAL_CAMERA)
    animRef.current.endTarget.copy(INITIAL_TARGET)
    animRef.current.elapsed = FOCUS_DURATION
    animRef.current.active = false
    camera.position.copy(INITIAL_CAMERA)
    camera.lookAt(INITIAL_TARGET)
  }, [resetToken, controlsRef, camera])

  useEffect(() => {
    if (focusId === prevFocusId.current) return
    prevFocusId.current = focusId

    const ctrl = controlsRef.current
    const a = animRef.current

    a.startPos.copy(camera.position)
    a.startTarget.copy(ctrl?.target ?? INITIAL_TARGET)
    a.startFov = camera.fov

    if (focusId) {
      let targetPos = livePositions.current.get(focusId)
      // 如果没有 livePosition，就从 planet 数据里算！
      if (!targetPos) {
        const planet = planetsRef.current.find((p) => p.id === focusId)
        if (planet) {
          targetPos = new THREE.Vector3(
            Math.cos(planet.angle) * planet.orbitRadius,
            0,
            Math.sin(planet.angle) * planet.orbitRadius,
          )
        }
      }
      if (targetPos) {
        // 立即开始聚焦动画 - 使用更近的距离 + FOV 缩放
        const offset = new THREE.Vector3(5, 8, 12)
        a.endPos.copy(targetPos).add(offset)
        a.endTarget.copy(targetPos)
        a.endFov = FOCUSED_FOV
        a.elapsed = 0
        a.active = true
        a.isFocusing = true
      }
    } else {
      // 取消聚焦，回到初始位置
      a.endPos.copy(INITIAL_CAMERA)
      a.endTarget.copy(INITIAL_TARGET)
      a.endFov = INITIAL_FOV
      a.elapsed = 0
      a.active = true
      a.isFocusing = false
    }
  }, [focusId, livePositions, controlsRef, camera, planetsRef])

  useFrame((_state, delta) => {
    const a = animRef.current

    // 每帧都检查一下当前 focusId 的位置，确保更新（跟随模式）
    if (focusId && !a.active) {
      const live = livePositions.current.get(focusId)
      if (live) {
        const offset = new THREE.Vector3(5, 8, 12)
        const targetPos = live.clone().add(offset)
        camera.position.lerp(targetPos, 0.15)
        camera.lookAt(live)
        camera.fov = THREE.MathUtils.lerp(camera.fov, FOCUSED_FOV, 0.15)
        camera.updateProjectionMatrix()
        const ctrl = controlsRef.current
        if (ctrl) {
          ctrl.target.lerp(live, 0.15)
          ctrl.update()
        }
        invalidate()
      }
    }

    if (a.active) {
      a.elapsed += delta
      const t = Math.min(a.elapsed / FOCUS_DURATION, 1)
      const e = easeInOutCubic(t)

      camera.position.lerpVectors(a.startPos, a.endPos, e)
      const target = new THREE.Vector3().lerpVectors(a.startTarget, a.endTarget, e)
      camera.lookAt(target)
      camera.fov = THREE.MathUtils.lerp(a.startFov, a.endFov, e)
      camera.updateProjectionMatrix()

      const ctrl = controlsRef.current
      if (ctrl) {
        ctrl.target.copy(target)
        ctrl.update()
      }

      invalidate()

      if (t >= 1) {
        a.active = false
      }
    }
  })

  return null
}

export interface CreditSolarSystemProps {
  semester?: number
  onPlanetClick?: (planet: PlanetModule) => void
  onSunClick?: () => void
  planets?: PlanetModule[]
  loading?: boolean
  error?: string | null
  onModulesLoaded?: (planets: PlanetModule[]) => void
  selectedModuleId?: string | null
  onModuleHover?: (planet: PlanetModule | null) => void
  refreshKey?: number
  resetViewTrigger?: number
  collegeId?: number | null
}

export default function CreditSolarSystem({
  semester = 8,
  onPlanetClick,
  onSunClick,
  planets: planetsProp,
  loading: loadingProp,
  error: errorProp,
  onModulesLoaded,
  selectedModuleId = null,
  onModuleHover,
  refreshKey = 0,
  resetViewTrigger = 0,
  collegeId = null,
}: CreditSolarSystemProps) {
  const [internalPlanets, setInternalPlanets] = useState<PlanetModule[]>([])
  const [internalLoading, setInternalLoading] = useState(!planetsProp)
  const [internalError, setInternalError] = useState<string | null>(null)
  const [focusedId, setFocusedId] = useState<string | null>(null)
  const [resetToken, setResetToken] = useState(0)
  const controlsRef = useRef<OrbitControlsImpl | null>(null)
  const livePositions = useRef(new Map<string, THREE.Vector3>())
  const planetsRef = useRef<PlanetModule[]>([])

  const controlled = planetsProp !== undefined
  const planets = controlled ? planetsProp : internalPlanets
  const loading = controlled ? (loadingProp ?? false) : internalLoading
  const error = controlled ? (errorProp ?? null) : internalError

  useEffect(() => {
    planetsRef.current = planets
  }, [planets])

  useEffect(() => {
    if (controlled) return
    let cancelled = false
    setInternalLoading(true)
    setInternalError(null)
    const url = collegeId
      ? `/api/progress_data?college_id=${collegeId}`
      : '/api/progress_data'
    apiFetch(url, { method: 'GET' })
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
  }, [controlled, onModulesLoaded, refreshKey, collegeId])

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
          onPlanetClick={(p) => {
            setFocusedId(p.id)
            onPlanetClick?.(p)
          }}
          onSunClick={onSunClick}
          controlsRef={controlsRef}
          livePositions={livePositions}
          planetsRef={planetsRef}
        />
      </Canvas>
    </div>
  )
}
