'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, BookOpen } from 'lucide-react'
import { apiFetch } from '@/lib/api'

interface Major {
  id: number
  name: string
  code: string | null
  college_id: number
}

interface MajorSelectorProps {
  collegeId: number | null
  value: number | null
  onChange: (majorId: number | null) => void
  className?: string
}

export function MajorSelector({
  collegeId,
  value,
  onChange,
  className = '',
}: MajorSelectorProps) {
  const [majors, setMajors] = useState<Major[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const selectedMajor = majors.find((m) => m.id === value)

  useEffect(() => {
    if (!collegeId) {
      setMajors([])
      return
    }

    let cancelled = false
    setLoading(true)
    apiFetch(`/api/colleges/${collegeId}/majors`)
      .then((res) => res.json())
      .then((data) => {
        if (cancelled) return
        setMajors(data.majors || [])
      })
      .catch(() => {
        if (cancelled) return
        setMajors([])
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => { cancelled = true }
  }, [collegeId])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleMajorClick = useCallback(
    (major: Major | null) => {
      onChange(major?.id || null)
      setIsOpen(false)
    },
    [onChange],
  )

  if (!collegeId) {
    return null
  }

  return (
    <div ref={ref} className={`relative ${className}`}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        disabled={majors.length === 0 && !loading}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <BookOpen className="w-4 h-4 text-white/60" />
        <span className="text-white/80 max-w-[140px] truncate">
          {loading
            ? '加载中...'
            : selectedMajor
              ? selectedMajor.name
              : majors.length > 0
                ? '选择专业'
                : '暂无专业'}
        </span>
        {majors.length > 0 && (
          <ChevronDown
            className={`w-3.5 h-3.5 text-white/50 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          />
        )}
      </button>

      {isOpen && majors.length > 0 && (
        <div className="absolute top-full left-0 mt-2 w-72 max-h-80 overflow-y-auto rounded-xl bg-black/80 backdrop-blur-xl border border-white/15 shadow-2xl z-50">
          <div className="py-1">
            <button
              key="none"
              onClick={() => handleMajorClick(null)}
              className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                !value ? 'bg-white/15 text-white' : 'text-white/70 hover:bg-white/8 hover:text-white'
              }`}
            >
              <span className="block truncate">不选择专业</span>
            </button>
            {majors.map((major) => (
              <button
                key={major.id}
                onClick={() => handleMajorClick(major)}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                  major.id === value
                    ? 'bg-white/15 text-white'
                    : 'text-white/70 hover:bg-white/8 hover:text-white'
                }`}
              >
                <span className="block truncate">{major.name}</span>
                {major.code && (
                  <span className="block text-xs text-white/40 mt-0.5">{major.code}</span>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
