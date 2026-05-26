'use client'

import { useEffect, useRef, useMemo, useCallback } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

export const MATH_SYMBOLS = [
  '∫', '∑', '∏', 'π', 'θ', 'λ', '∂', '∇', '∞', 'e', 'i',
  'α', 'β', 'γ', 'φ', 'ψ', 'ω', 'Δ', 'μ', 'σ', '√', 'ℏ',
]

export const MATH_FORMULAS = [
  '∫ f(x)dx', '∂u/∂t', '∇²φ = ρ/ε₀', 'det(A) ≠ 0', 'Av = λv',
  'E=mc²', 'F=ma', 'e^{iπ}+1=0', 'a²+b²=c²', 'x²+y²=r²',
  'P(A|B)', 'E[X]=∫xf(x)dx', '∇×E=-∂B/∂t', 'F=q(E+v×B)',
  'H(X)=-∑p log p', '∫₀^∞ e^{-x²}dx', 'Σ 1/n²', '∇·B=0',
  'sin²θ+cos²θ=1', 'lim_{n→∞}', '∂f/∂x', 'd/dx sin x',
  '∫ e^{-x²}dx', '∇·E=ρ/ε₀', '∇×B=μ₀J', 'S=∫L dt',
  'V=IR', 'P=IV', 'ω=2πf', 'λ=c/f', 'n₁sinθ₁=n₂sinθ₂',
  'Δx·Δp≥ℏ/2', 'iℏ∂ψ/∂t=Ĥψ', '∫|ψ|²dV=1', 'E=-∇V',
  'C=εA/d', 'Q=CV', 'B=μ₀I/2πr', 'F=kq₁q₂/r²',
  '∮E·dA=Q/ε₀', '∮B·dl=μ₀I', '∇²u=0', '∇²u=∂²u/∂t²',
  'Re(z)=a', 'Im(z)=b', 'z=re^{iθ}', 'log(ab)=log a+log b',
  '∑_{k=1}^n k', '∏_{i=1}^n a_i', '∫_a^b f', '∂²u/∂x²',
  '∇·(∇×A)=0', '∇×(∇φ)=0', 'div grad φ', 'curl curl A',
  'FFT', 'DFT', 'H(f)', 'G(s)', 'Z(z)', 's=jω',
  'SNR', 'BER', 'Eb/N₀', 'C=B log₂(1+S/N)',
]

const SCENE_BG = '#1a1f2e'

type Layer = 'deep' | 'far' | 'mid' | 'near'

interface FormulaItem {
  key: number
  text: string
  opacity: number
  fontSize: number
  position: THREE.Vector3
  baseY: number
  phase: number
  rotSpeed: number
  floatAmp: number
  layer: Layer
}

function buildFormulaPool(count: number): string[] {
  const base = [...MATH_SYMBOLS, ...MATH_FORMULAS]
  const pool: string[] = []
  for (let i = 0; i < count; i++) {
    pool.push(base[i % base.length])
  }
  return pool
}

function generateLayeredFormulas(count: number): FormulaItem[] {
  const pool = buildFormulaPool(count)
  const layerWeights: Layer[] = ['deep', 'deep', 'far', 'far', 'mid', 'mid', 'near']

  return pool.map((text, i) => {
    const layer = layerWeights[i % layerWeights.length]
    const spread =
      layer === 'deep' ? 78 : layer === 'far' ? 62 : layer === 'mid' ? 48 : 34
    const ySpread =
      layer === 'deep' ? 42 : layer === 'far' ? 36 : layer === 'mid' ? 26 : 18

    return {
      key: i,
      text: text.replace(/\d+$/, ''),
      layer,
      opacity:
        layer === 'deep'
          ? 0.02 + Math.random() * 0.015
          : layer === 'far'
            ? 0.03 + Math.random() * 0.02
            : layer === 'mid'
              ? 0.045 + Math.random() * 0.025
              : 0.06 + Math.random() * 0.02,
      fontSize:
        layer === 'deep'
          ? 12 + Math.random() * 14
          : layer === 'far'
            ? 14 + Math.random() * 18
            : layer === 'mid'
              ? 18 + Math.random() * 22
              : 22 + Math.random() * 26,
      position: new THREE.Vector3(
        (Math.random() - 0.5) * spread,
        (Math.random() - 0.5) * ySpread,
        (Math.random() - 0.5) * spread,
      ),
      baseY: (Math.random() - 0.5) * ySpread,
      phase: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 0.0025,
      floatAmp: layer === 'deep' ? 0.35 : layer === 'far' ? 0.5 : layer === 'mid' ? 0.75 : 1.0,
    }
  })
}

/** Three.js 场景内 CSS2D 分层数学公式 - 使用手动投影 */
export function MathFormulaCSS2D({ count = 180 }: { count?: number }) {
  const { camera, size } = useThree()
  const containerRef = useRef<HTMLDivElement | null>(null)
  const items = useMemo(() => generateLayeredFormulas(count), [count])
  const labelRefs = useRef<Array<{ el: HTMLDivElement; item: FormulaItem; baseX: number; baseY: number; baseZ: number }>>([])

  useEffect(() => {
    // 创建容器直接添加到 body，绝对定位，pointer-events: none
    const container = document.createElement('div')
    container.style.position = 'fixed'
    container.style.inset = '0'
    container.style.pointerEvents = 'none'
    container.style.zIndex = '0'
    container.style.overflow = 'hidden'
    document.body.appendChild(container)
    containerRef.current = container

    // 创建所有标签
    const labels = items.map((item) => {
      const el = document.createElement('div')
      el.textContent = item.text
      el.style.color = '#eef2ff'
      el.style.opacity = String(item.opacity)
      el.style.fontSize = `${item.fontSize}px`
      el.style.fontFamily = '"Times New Roman", Georgia, serif'
      el.style.fontStyle = 'italic'
      el.style.fontWeight = item.layer === 'near' ? '400' : '300'
      el.style.userSelect = 'none'
      el.style.whiteSpace = 'nowrap'
      el.style.position = 'absolute'
      el.style.textShadow =
        item.layer === 'near'
          ? '0 0 12px rgba(200,220,255,0.15)'
          : 'none'
      el.style.transformOrigin = 'center center'
      container.appendChild(el)
      
      return {
        el,
        item,
        baseX: item.position.x,
        baseY: item.position.y,
        baseZ: item.position.z,
      }
    })
    labelRefs.current = labels

    return () => {
      labels.forEach(({ el }) => el.remove())
      container.remove()
      containerRef.current = null
      labelRefs.current = []
    }
  }, [items])

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.style.width = `${size.width}px`
      containerRef.current.style.height = `${size.height}px`
    }
  }, [size.width, size.height])

  useFrame((state) => {
    labelRefs.current.forEach(({ el, item, baseX, baseY, baseZ }) => {
      const t = state.clock.elapsedTime * 0.07 + item.phase
      
      // 3D 位置动画
      const x = baseX + Math.sin(t * 0.6 + item.phase) * 0.15
      const y = baseY + Math.sin(t) * item.floatAmp
      const z = baseZ
      const rotation = state.clock.elapsedTime * item.rotSpeed * 35
      
      // 手动投影 3D 位置到 2D 屏幕坐标
      const vector = new THREE.Vector3(x, y, z)
      vector.project(camera)
      
      // 转换为屏幕像素
      const screenX = (vector.x * 0.5 + 0.5) * size.width
      const screenY = (-(vector.y * 0.5) + 0.5) * size.height
      
      // 更新元素位置和旋转
      el.style.transform = `translate(-50%, -50%) translate(${screenX}px, ${screenY}px) rotate(${rotation}deg)`
    })
  })

  return null
}

interface CanvasFormula {
  x: number
  y: number
  text: string
  fontSize: number
  opacity: number
  speed: number
  drift: number
  layer: Layer
}

function initCanvasFormulas(
  w: number,
  h: number,
  count: number,
  layer: Layer,
): CanvasFormula[] {
  const pool = buildFormulaPool(count)
  return pool.map((text, i) => ({
    x: Math.random() * w,
    y: Math.random() * h,
    text,
    layer,
    fontSize:
      layer === 'deep'
        ? 9 + Math.random() * 8
        : layer === 'far'
          ? 11 + Math.random() * 10
          : layer === 'mid'
            ? 14 + Math.random() * 12
            : 16 + Math.random() * 14,
    opacity:
      layer === 'deep'
        ? 0.08 + Math.random() * 0.06
        : layer === 'far'
          ? 0.1 + Math.random() * 0.08
          : layer === 'mid'
            ? 0.12 + Math.random() * 0.1
            : 0.15 + Math.random() * 0.12,
    speed: 0.015 + Math.random() * 0.025,
    drift: (Math.random() - 0.5) * 0.02,
  }))
}

/** 页面级 2D 分层数学背景（与 3D 场景色调一致） */
export function MathBackground({ formulaCount = 100 }: { formulaCount?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const layersRef = useRef<CanvasFormula[][]>([])
  const animRef = useRef<number>(0)

  const init = useCallback((w: number, h: number) => {
    const q = Math.floor(formulaCount / 4)
    layersRef.current = [
      initCanvasFormulas(w, h, q, 'deep' as Layer),
      initCanvasFormulas(w, h, q, 'far'),
      initCanvasFormulas(w, h, q, 'mid'),
      initCanvasFormulas(w, h, formulaCount - q * 3, 'near'),
    ]
  }, [formulaCount])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
      init(canvas.width, canvas.height)
    }

    const animate = () => {
      if (!ctx || !canvas) return
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      for (const layer of layersRef.current) {
        for (const f of layer) {
          f.y -= f.speed
          f.x += f.drift
          if (f.y < -40) {
            f.y = canvas.height + 40
            f.x = Math.random() * canvas.width
          }
          if (f.x < -40) f.x = canvas.width + 40
          if (f.x > canvas.width + 40) f.x = -40

          ctx.save()
          ctx.font = `${f.fontSize}px "Times New Roman", Georgia, serif`
          ctx.fillStyle = `rgba(220, 230, 255, ${f.opacity})`
          ctx.textAlign = 'center'
          ctx.textBaseline = 'middle'
          ctx.fillText(f.text, f.x, f.y)
          ctx.restore()
        }
      }
      animRef.current = requestAnimationFrame(animate)
    }

    resize()
    window.addEventListener('resize', resize)
    animate()
    return () => {
      window.removeEventListener('resize', resize)
      cancelAnimationFrame(animRef.current)
    }
  }, [init])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: -1 }}
      aria-hidden
    />
  )
}

export { SCENE_BG }
