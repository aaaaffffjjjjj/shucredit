'use client'

import { useRef, useState } from 'react'
import { Upload, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react'
import { apiUploadPdf } from '@/lib/api'

interface UploadPdfProps {
  onSuccess?: (message: string, unknownCount: number) => void
  onError?: (message: string) => void
}

export default function UploadPdf({ onSuccess, onError }: UploadPdfProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [lastMessage, setLastMessage] = useState<string | null>(null)
  const [lastUnknown, setLastUnknown] = useState<string[]>([])

  const handleFiles = async (fileList: FileList | null) => {
    if (!fileList?.length) return

    const pdfs = Array.from(fileList).filter((f) =>
      f.name.toLowerCase().endsWith('.pdf'),
    )
    if (!pdfs.length) {
      const msg = '请选择 PDF 文件'
      setLastMessage(msg)
      onError?.(msg)
      return
    }

    setUploading(true)
    setLastMessage(null)
    setLastUnknown([])

    try {
      const data = await apiUploadPdf(pdfs)
      const unknownCodes = (data.unknown || []).map((u) => u.course_code)
      setLastMessage(data.message || `成功添加 ${data.inserted} 门课程`)
      setLastUnknown(unknownCodes)
      onSuccess?.(data.message, unknownCodes.length)
    } catch (err) {
      const msg = err instanceof Error ? err.message : '上传失败'
      setLastMessage(msg)
      onError?.(msg)
    } finally {
      setUploading(false)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  return (
    <div className="mb-6 p-4 rounded-xl border border-border bg-background/50 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs text-muted-foreground uppercase tracking-wider">
          上传课表
        </span>
        <Upload className="w-4 h-4 text-muted-foreground" />
      </div>

      <p className="text-xs text-muted-foreground mb-3 leading-relaxed">
        支持多选教务处官方 PDF，系统将自动识别课程编号并加入已修列表。
      </p>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,application/pdf"
        multiple
        className="hidden"
        disabled={uploading}
        onChange={(e) => handleFiles(e.target.files)}
      />

      <button
        type="button"
        disabled={uploading}
        onClick={() => inputRef.current?.click()}
        className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg border border-border bg-card/80 hover:bg-card text-sm font-medium transition-colors disabled:opacity-50"
      >
        {uploading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            解析中…
          </>
        ) : (
          <>
            <Upload className="w-4 h-4" />
            选择 PDF 文件
          </>
        )}
      </button>

      {lastMessage && (
        <div
          className={`mt-3 flex gap-2 text-xs p-2.5 rounded-lg border ${
            lastUnknown.length
              ? 'border-amber-500/30 bg-amber-500/10 text-amber-200'
              : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'
          }`}
        >
          {lastUnknown.length ? (
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          ) : (
            <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
          )}
          <div className="min-w-0">
            <p>{lastMessage}</p>
            {lastUnknown.length > 0 && (
              <p className="mt-1 opacity-80 break-all">
                未识别编号（{lastUnknown.length}）：
                {lastUnknown.slice(0, 5).join(', ')}
                {lastUnknown.length > 5 ? '…' : ''}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
