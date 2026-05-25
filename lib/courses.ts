import { apiFetch } from '@/lib/api'

export interface ApiCourse {
  id: number
  course_code: string
  name: string
  credit: number
  module_id: number
  module_name?: string
}

export async function fetchMyCourses(): Promise<ApiCourse[]> {
  const res = await apiFetch('/api/my_courses')
  if (!res.ok) throw new Error('加载已修课程失败')
  const data = await res.json()
  return data.courses || []
}

export async function fetchRecommendCourses(
  moduleId: number,
): Promise<ApiCourse[]> {
  const res = await apiFetch(`/api/recommend_courses/${moduleId}`)
  if (!res.ok) throw new Error('加载可选课程失败')
  const data = await res.json()
  return data.courses || []
}

export async function enrollCourse(courseId: number): Promise<{
  ok: boolean
  message: string
  progress?: unknown
}> {
  const res = await apiFetch(`/api/enroll/${courseId}`, { method: 'POST' })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.error || '选修失败')
  return data
}
