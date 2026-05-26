'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, GraduationCap } from 'lucide-react'
import { apiFetch } from '@/lib/api'

interface College {
  id: number
  name: string
  code: string
}

interface CollegeSelectorProps {
  value: number | null
  onChange: (collegeId: number) => void
  onAdminActivated?: () => void
  className?: string
}

const COLLEGES_CACHE_KEY = 'colleges_cache'

const SECRET_SEQUENCE = [
  '理学院',
  '通信与信息工程学院',
  '理学院',
  '通信与信息工程学院',
]

function getCachedColleges(): College[] | null {
  if (typeof window === 'undefined') return null
  try {
    const raw = localStorage.getItem(COLLEGES_CACHE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      if (Array.isArray(data) && data.length > 0) return data
    }
  } catch {
    return null
  }
  return null
}

function setCachedColleges(colleges: College[]) {
  try {
    localStorage.setItem(COLLEGES_CACHE_KEY, JSON.stringify(colleges))
  } catch {
    // ignore
  }
}

export function CollegeSelector({
  value,
  onChange,
  onAdminActivated,
  className = '',
}: CollegeSelectorProps) {
  const [colleges, setColleges] = useState<College[]>(() => getCachedColleges() || [])
  const [isOpen, setIsOpen] = useState(false)
  const [loading, setLoading] = useState(true)
  const [secretStep, setSecretStep] = useState(0)
  const [adminActivated, setAdminActivated] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const selectedCollege = colleges.find((c) => c.id === value)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    apiFetch('/api/colleges')
      .then((res) => res.json())
      .then((data) => {
        if (cancelled) return
        const list = data.colleges || []
        setColleges(list)
        setCachedColleges(list)
      })
      .catch(() => {
        if (cancelled) return
        const cached = getCachedColleges()
        if (cached) setColleges(cached)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleCollegeClick = useCallback(
    (college: College) => {
      onChange(college.id)

      if (adminActivated) {
        setIsOpen(false)
        return
      }

      const expected = SECRET_SEQUENCE[secretStep]
      if (college.name === expected) {
        const next = secretStep + 1
        if (next >= SECRET_SEQUENCE.length) {
          setAdminActivated(true)
          setSecretStep(0)
          onAdminActivated?.()
        } else {
          setSecretStep(next)
        }
      } else {
        setSecretStep(0)
        if (college.name === SECRET_SEQUENCE[0]) {
          setSecretStep(1)
        }
      }

      setIsOpen(false)
    },
    [onChange, secretStep, adminActivated, onAdminActivated],
  )

  return (
    <div ref={ref} className={`relative ${className}`}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-colors text-sm"
      >
        <GraduationCap className="w-4 h-4 text-white/60" />
        <span className="text-white/80 max-w-[140px] truncate">
          {loading ? '加载中...' : selectedCollege ? selectedCollege.name : '选择学院'}
        </span>
        <ChevronDown
          className={`w-3.5 h-3.5 text-white/50 transition-transform ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-64 max-h-80 overflow-y-auto rounded-xl bg-black/80 backdrop-blur-xl border border-white/15 shadow-2xl z-50">
          <div className="py-1">
            {colleges.map((college) => (
              <button
                key={college.id}
                onClick={() => handleCollegeClick(college)}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                  college.id === value
                    ? 'bg-white/15 text-white'
                    : 'text-white/70 hover:bg-white/8 hover:text-white'
                }`}
              >
                <span className="block truncate">{college.name}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}