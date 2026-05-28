'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, ArrowRight, ChevronDown, GraduationCap, BookOpen } from 'lucide-react'
import Link from 'next/link'
import { MathBackground } from '@/components/math-background'
import { apiFetch } from '@/lib/api'

type AuthMode = 'login' | 'register'

export default function LoginPage() {
  const router = useRouter()
  const [mode, setMode] = useState<AuthMode>('login')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [collegesOpen, setCollegesOpen] = useState(false)
  const [colleges, setColleges] = useState<Array<{ id: number; name: string; code: string }>>([])
  const [selectedCollegeId, setSelectedCollegeId] = useState<number | null>(null)
  const [majors, setMajors] = useState<Array<{ id: number; name: string; college_id: number }>>([])
  const [majorsOpen, setMajorsOpen] = useState(false)
  const [selectedMajorId, setSelectedMajorId] = useState<number | null>(null)
  const collegesRef = useRef<HTMLDivElement>(null)
  const majorsRef = useRef<HTMLDivElement>(null)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [apiError, setApiError] = useState('')

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.username.trim()) {
      newErrors.username = '请输入用户名'
    }

    if (!formData.password) {
      newErrors.password = '请输入密码'
    } else if (formData.password.length < 6) {
      newErrors.password = '密码至少 6 位'
    }

    if (mode === 'register') {
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = '请确认密码'
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = '密码不一致'
      }
      if (!formData.name.trim()) {
        newErrors.name = '请输入姓名'
      }
      if (!selectedCollegeId) {
        newErrors.college = '请选择学院'
      }
      if (!selectedMajorId) {
        newErrors.major = '请选择专业'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  useEffect(() => {
    apiFetch('/api/colleges')
      .then((res) => res.json())
      .then((data) => setColleges(data.colleges || []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (collegesRef.current && !collegesRef.current.contains(e.target as Node)) {
        setCollegesOpen(false)
      }
      if (majorsRef.current && !majorsRef.current.contains(e.target as Node)) {
        setMajorsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    if (!selectedCollegeId) {
      setMajors([])
      setSelectedMajorId(null)
      return
    }
    let cancelled = false
    apiFetch(`/api/majors?college_id=${selectedCollegeId}`)
      .then((res) => res.json())
      .then((data) => {
        if (cancelled) return
        setMajors(data.majors || [])
      })
      .catch(() => {})
    return () => { cancelled = true }
  }, [selectedCollegeId])

  const selectedCollege = colleges.find((c) => c.id === selectedCollegeId)
  const selectedMajor = majors.find((m) => m.id === selectedMajorId)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validateForm()) return

    setIsLoading(true)
    setApiError('')

    try {
      const endpoint =
        mode === 'login' ? '/api/auth/login' : '/api/auth/register'
      const body =
        mode === 'login'
          ? {
              username: formData.username.trim(),
              password: formData.password,
            }
          : {
              username: formData.username.trim(),
              password: formData.password,
              name: formData.name.trim(),
              college_id: selectedCollegeId,
              major_id: selectedMajorId,
            }

      const res = await apiFetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(body),
      })
      const data = await res.json()

      if (!res.ok || !data.success) {
        setApiError(data.message || '认证失败')
        return
      }

      router.push('/')
      router.refresh()
    } catch (err) {
      setApiError(err instanceof Error ? err.message : '网络错误')
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }))
    }
    setApiError('')
  }

  return (
    <div className="min-h-screen flex relative">
      <MathBackground />

      <div className="hidden lg:flex lg:w-1/2 flex-col justify-between p-12 bg-background/60 backdrop-blur-sm border-r border-border relative z-10">
        <div>
          <h1 className="text-xl font-medium tracking-tight">Credit</h1>
        </div>
        <div className="max-w-md">
          <h2 className="text-4xl font-serif italic leading-tight text-balance">
            Crafting your academic journey.
          </h2>
          <p className="mt-6 text-muted-foreground leading-relaxed">
            可视化学分管理，清晰规划每一个学期。
          </p>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-8 relative z-10">
        <div className="w-full max-w-sm">
          <div className="lg:hidden mb-12">
            <h1 className="text-xl font-medium tracking-tight">Credit</h1>
          </div>

          <div className="mb-8">
            <h2 className="text-2xl font-medium tracking-tight">
              {mode === 'login' ? '欢迎回来' : '创建账户'}
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              使用 Flask 账号登录（与旧版学分系统相同用户名）
            </p>
          </div>

          {apiError && (
            <div className="mb-4 px-3 py-2 text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20">
              {apiError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {mode === 'register' && (
              <div>
                <label className="block text-sm font-medium mb-2">姓名</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="您的姓名"
                  className="w-full px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border"
                />
                {errors.name && (
                  <p className="mt-1.5 text-sm text-destructive">{errors.name}</p>
                )}
              </div>
            )}

            {mode === 'register' && (
              <div ref={collegesRef} className="relative">
                <label className="block text-sm font-medium mb-2">所属学院</label>
                <button
                  type="button"
                  onClick={() => setCollegesOpen(!collegesOpen)}
                  className="w-full flex items-center gap-2 px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border text-left"
                >
                  <GraduationCap className="w-4 h-4 text-muted-foreground" />
                  <span className={selectedCollege ? 'text-foreground' : 'text-muted-foreground'}>
                    {selectedCollege ? selectedCollege.name : '请选择学院'}
                  </span>
                  <ChevronDown className={`w-4 h-4 text-muted-foreground ml-auto transition-transform ${collegesOpen ? 'rotate-180' : ''}`} />
                </button>
                {errors.college && (
                  <p className="mt-1.5 text-sm text-destructive">{errors.college}</p>
                )}
                {collegesOpen && (
                  <div className="absolute top-full left-0 right-0 mt-1 max-h-48 overflow-y-auto rounded-lg bg-background/95 backdrop-blur-xl border border-border z-50">
                    {colleges.map((college) => (
                      <button
                        key={college.id}
                        type="button"
                        onClick={() => {
                          setSelectedCollegeId(college.id)
                          setCollegesOpen(false)
                          setErrors((prev) => ({ ...prev, college: '' }))
                        }}
                        className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                          college.id === selectedCollegeId
                            ? 'bg-foreground/10 text-foreground'
                            : 'text-muted-foreground hover:bg-foreground/5 hover:text-foreground'
                        }`}
                      >
                        {college.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {mode === 'register' && (
              <div ref={majorsRef} className="relative">
                <label className="block text-sm font-medium mb-2">所属专业</label>
                <button
                  type="button"
                  onClick={() => selectedCollegeId && setMajorsOpen(!majorsOpen)}
                  disabled={!selectedCollegeId}
                  className="w-full flex items-center gap-2 px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border text-left disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <BookOpen className="w-4 h-4 text-muted-foreground" />
                  <span className={selectedMajor ? 'text-foreground' : 'text-muted-foreground'}>
                    {selectedCollegeId
                      ? (selectedMajor ? selectedMajor.name : '请选择专业')
                      : '请先选学院'}
                  </span>
                  <ChevronDown className={`w-4 h-4 text-muted-foreground ml-auto transition-transform ${majorsOpen ? 'rotate-180' : ''}`} />
                </button>
                {errors.major && (
                  <p className="mt-1.5 text-sm text-destructive">{errors.major}</p>
                )}
                {majorsOpen && majors.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 max-h-48 overflow-y-auto rounded-lg bg-background/95 backdrop-blur-xl border border-border z-50">
                    {majors.map((major) => (
                      <button
                        key={major.id}
                        type="button"
                        onClick={() => {
                          setSelectedMajorId(major.id)
                          setMajorsOpen(false)
                          setErrors((prev) => ({ ...prev, major: '' }))
                        }}
                        className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                          major.id === selectedMajorId
                            ? 'bg-foreground/10 text-foreground'
                            : 'text-muted-foreground hover:bg-foreground/5 hover:text-foreground'
                        }`}
                      >
                        {major.name}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium mb-2">用户名</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                placeholder="与 Flask 系统一致的用户名"
                autoComplete="username"
                className="w-full px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border"
              />
              {errors.username && (
                <p className="mt-1.5 text-sm text-destructive">{errors.username}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">密码</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="••••••••"
                  autoComplete={
                    mode === 'login' ? 'current-password' : 'new-password'
                  }
                  className="w-full px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1.5 text-sm text-destructive">{errors.password}</p>
              )}
            </div>

            {mode === 'register' && (
              <div>
                <label className="block text-sm font-medium mb-2">确认密码</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2.5 rounded-lg bg-background/80 backdrop-blur-sm border border-border"
                />
                {errors.confirmPassword && (
                  <p className="mt-1.5 text-sm text-destructive">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-foreground text-background font-medium text-sm disabled:opacity-50"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-background/30 border-t-background rounded-full animate-spin" />
              ) : (
                <>
                  {mode === 'login' ? '登录' : '注册'}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <p className="mt-8 text-center text-sm text-muted-foreground">
            {mode === 'login' ? '还没有账户?' : '已有账户?'}
            <button
              type="button"
              onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
              className="ml-1 text-foreground hover:underline"
            >
              {mode === 'login' ? '注册' : '登录'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
