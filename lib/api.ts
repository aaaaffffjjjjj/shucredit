/**
 * Flask API 客户端：跨域请求须 credentials: 'include'，且 API 主机名与页面一致
 *（localhost 与 127.0.0.1 的 Cookie 不互通）。
 */

function resolveApiBase(): string {
  const fromEnv = process.env.NEXT_PUBLIC_API_BASE
  if (fromEnv !== undefined && fromEnv !== '') {
    return fromEnv.replace(/\/$/, '')
  }
  if (typeof window !== 'undefined') {
    return `http://${window.location.hostname}:5000`
  }
  return 'http://127.0.0.1:5000'
}

export const API_BASE = resolveApiBase()

export function apiUrl(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  const base = resolveApiBase()
  return base ? `${base}${normalized}` : normalized
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const headers = new Headers(options.headers)
  const isFormData =
    typeof FormData !== 'undefined' && options.body instanceof FormData

  if (!isFormData && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  if (isFormData) {
    headers.delete('Content-Type')
  }

  return fetch(apiUrl(path), {
    ...options,
    credentials: 'include',
    mode: 'cors',
    headers,
  })
}

export async function apiUploadPdf(files: FileList | File[]): Promise<{
  ok: boolean
  inserted: number
  message: string
  unknown: Array<{ course_code: string; name?: string; credit?: number }>
  progress?: unknown
}> {
  const formData = new FormData()
  const list = Array.from(files)
  list.forEach((file) => formData.append('file', file))

  const res = await apiFetch('/api/upload_pdf', {
    method: 'POST',
    body: formData,
  })

  const data = await res.json().catch(() => ({}))
  if (res.status === 401) {
    throw new Error('未登录，请先登录')
  }
  if (!res.ok) {
    throw new Error(data.error || data.message || `上传失败 HTTP ${res.status}`)
  }
  return data
}
