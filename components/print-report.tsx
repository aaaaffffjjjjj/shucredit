'use client'

import type { ApiModule } from '@/lib/progress'

interface PrintReportProps {
  studentName?: string
  majorName?: string
  username?: string
  modules: ApiModule[]
  sun?: {
    required: number
    earned: number
  }
}

export function usePrintReport() {
  const printReport = ({ studentName, majorName, username, modules, sun }: PrintReportProps) => {
    const totalRequired = modules.reduce((sum, m) => sum + m.required, 0)
    const totalEarned = modules.reduce((sum, m) => sum + m.earned, 0)
    const totalRemaining = totalRequired - totalEarned
    const totalPercent = totalRequired > 0 ? Math.round((totalEarned / totalRequired) * 100) : 0

    const generateDate = new Date().toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })

    const topLevelModules = modules.filter(m => m.parent_id === null)

    const renderModuleRow = (module: ApiModule, level: number): string => {
      const hasChildren = modules.filter(m => m.parent_id === module.id).length > 0
      const isIncomplete = module.remaining > 0
      const indentPx = level * 18

      let html = `<tr style="page-break-inside: avoid;">
        <td style="padding-left: ${indentPx + 12}px; padding-top: 8px; padding-bottom: 8px;">
          <span style="font-weight: ${hasChildren ? '600' : '400'}; font-size: ${level === 0 ? '13px' : '12px'};">
            ${hasChildren ? '<span style="margin-right: 6px; color: #3b82f6;">▸</span>' : '<span style="margin-right: 6px; color: #9ca3af;">•</span>'}
            ${module.name}
          </span>
        </td>
        <td style="text-align: center; padding: 8px; font-size: 12px;">${module.required}</td>
        <td style="text-align: center; padding: 8px; font-size: 12px;">${module.earned}</td>
        <td style="text-align: center; padding: 8px; font-size: 12px; ${isIncomplete ? 'color: #dc2626; font-weight: 600;' : 'color: #374151;'}">
          ${module.remaining}
        </td>
        <td style="text-align: center; padding: 8px;">
          <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
            <div style="width: 90px; height: 10px; background: #e5e7eb; border-radius: 5px; overflow: hidden;">
              <div style="width: ${Math.min(module.percent, 100)}%; height: 100%; background: ${module.percent >= 100 ? '#10b981' : '#3b82f6'}; border-radius: 5px;"></div>
            </div>
            <span style="font-size: 12px; font-weight: 500; color: #6b7280;">${module.percent}%</span>
          </div>
        </td>
      </tr>`

      const children = modules.filter(m => m.parent_id === module.id)
      children.forEach(child => {
        html += renderModuleRow(child, level + 1)
      })

      return html
    }

    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>学分完成报告</title>
        <style>
          body {
            font-family: "PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 12px;
            line-height: 1.6;
            color: #1f2937;
            margin: 0;
            padding: 24px;
            background: #ffffff;
          }
          .report-container {
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
          }
          .report-header {
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 3px solid #3b82f6;
          }
          h1 {
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px 0;
            color: #111827;
          }
          .report-subtitle {
            font-size: 14px;
            color: #6b7280;
            margin: 0;
          }
          .info-section {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 28px;
            padding: 16px 20px;
            background: #f9fafb;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
          }
          .info-left {
            display: flex;
            flex-direction: column;
            gap: 6px;
          }
          .info-item {
            font-size: 14px;
            margin: 0;
          }
          .info-label {
            color: #6b7280;
            margin-right: 8px;
          }
          .info-value {
            color: #1f2937;
            font-weight: 500;
          }
          .info-right {
            text-align: right;
          }
          .progress-section {
            margin-bottom: 28px;
            padding: 20px;
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
            border-radius: 10px;
            border: 1px solid #e0f2fe;
          }
          h2 {
            font-size: 16px;
            font-weight: 600;
            margin: 0 0 16px 0;
            color: #1f2937;
            display: flex;
            align-items: center;
          }
          h2::before {
            content: '';
            width: 4px;
            height: 16px;
            background: #3b82f6;
            border-radius: 2px;
            margin-right: 10px;
          }
          .overall-progress {
            margin-bottom: 16px;
          }
          .progress-bar-wrapper {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 12px;
          }
          .progress-bar {
            flex: 1;
            height: 28px;
            background: #e5e7eb;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
          }
          .progress-fill {
            height: 100%;
            border-radius: 14px;
            background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
            transition: width 0.5s ease;
            position: relative;
          }
          .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
          }
          .progress-percent {
            font-size: 24px;
            font-weight: 700;
            color: #3b82f6;
            min-width: 70px;
            text-align: right;
          }
          .progress-details {
            display: flex;
            gap: 24px;
            font-size: 14px;
          }
          .detail-item {
            display: flex;
            align-items: center;
            gap: 8px;
          }
          .detail-label {
            color: #6b7280;
          }
          .detail-value {
            font-weight: 600;
            color: #1f2937;
          }
          .detail-value.completed {
            color: #10b981;
          }
          .detail-value.pending {
            color: #f59e0b;
          }
          .detail-value.warning {
            color: #dc2626;
          }
          .modules-section {
            margin-bottom: 28px;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
          }
          thead {
            background: #3b82f6;
          }
          th {
            text-align: left;
            padding: 14px 16px;
            font-weight: 600;
            font-size: 13px;
            color: #ffffff;
            white-space: nowrap;
          }
          th:first-child {
            width: auto;
          }
          th:not(:first-child) {
            text-align: center;
          }
          tbody tr {
            border-bottom: 1px solid #f3f4f6;
          }
          tbody tr:hover {
            background: #f9fafb;
          }
          tbody tr:last-child {
            border-bottom: none;
          }
          td {
            padding: 10px 16px;
            font-size: 12px;
            color: #374151;
          }
          .module-level-0 {
            background: #f9fafb;
          }
          .module-level-0 td:first-child {
            font-weight: 600;
            font-size: 13px;
          }
          .footer {
            margin-top: 32px;
            padding-top: 16px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
          }
          .footer p {
            font-size: 12px;
            color: #9ca3af;
            margin: 4px 0;
          }
          .page-break {
            page-break-after: always;
          }
          @page {
            size: A4;
            margin: 20mm 15mm;
          }
          @media print {
            body {
              padding: 0;
            }
            .report-container {
              max-width: none;
            }
          }
        </style>
      </head>
      <body>
        <div class="report-container">
          <div class="report-header">
            <h1>学分完成报告</h1>
            <p class="report-subtitle">Student Credit Completion Report</p>
          </div>

          <div class="info-section">
            <div class="info-left">
              <p class="info-item">
                <span class="info-label">学生姓名：</span>
                <span class="info-value">${studentName || username || '未知'}</span>
              </p>
              <p class="info-item">
                <span class="info-label">所学专业：</span>
                <span class="info-value">${majorName || '未知'}</span>
              </p>
              <p class="info-item">
                <span class="info-label">学号：</span>
                <span class="info-value">${username || '未知'}</span>
              </p>
            </div>
            <div class="info-right">
              <p style="margin: 0; color: #6b7280; font-size: 13px;">
                生成时间：${generateDate}
              </p>
            </div>
          </div>

          <div class="progress-section">
            <h2>总体学分进度</h2>
            <div class="overall-progress">
              <div class="progress-bar-wrapper">
                <div class="progress-bar">
                  <div class="progress-fill" style="width: ${Math.min(totalPercent, 100)}%;"></div>
                </div>
                <div class="progress-percent">${totalPercent}%</div>
              </div>
              <div class="progress-details">
                <div class="detail-item">
                  <span class="detail-label">已修学分：</span>
                  <span class="detail-value completed">${totalEarned}</span>
                  <span class="detail-label">/</span>
                  <span class="detail-value">${totalRequired}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">剩余学分：</span>
                  <span class="detail-value ${totalRemaining > 0 ? 'warning' : 'completed'}">${totalRemaining}</span>
                </div>
                ${sun ? `
                <div class="detail-item">
                  <span class="detail-label">太阳轨道：</span>
                  <span class="detail-value">${sun.earned}/${sun.required}</span>
                </div>
                ` : ''}
              </div>
            </div>
          </div>

          <div class="modules-section">
            <h2>模块学分详情</h2>
            <table>
              <thead>
                <tr>
                  <th>模块名称</th>
                  <th style="width: 90px;">要求学分</th>
                  <th style="width: 90px;">已修学分</th>
                  <th style="width: 90px;">剩余学分</th>
                  <th style="width: 140px;">完成进度</th>
                </tr>
              </thead>
              <tbody>
                ${topLevelModules.map(module => {
                  const children = modules.filter(m => m.parent_id === module.id)
                  return `
                    <tr class="module-level-0">
                      <td style="padding-left: 12px;">
                        <span style="font-weight: 600; color: #3b82f6;">▸</span>
                        <span style="margin-left: 6px;">${module.name}</span>
                      </td>
                      <td style="text-align: center;">${module.required}</td>
                      <td style="text-align: center;">${module.earned}</td>
                      <td style="text-align: center; ${module.remaining > 0 ? 'color: #dc2626; font-weight: 600;' : ''}">${module.remaining}</td>
                      <td style="text-align: center;">
                        <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                          <div style="width: 70px; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                            <div style="width: ${Math.min(module.percent, 100)}%; height: 100%; background: ${module.percent >= 100 ? '#10b981' : '#3b82f6'}; border-radius: 4px;"></div>
                          </div>
                          <span style="font-size: 11px; font-weight: 500;">${module.percent}%</span>
                        </div>
                      </td>
                    </tr>
                    ${children.map(child => {
                      const grandchildren = modules.filter(m => m.parent_id === child.id)
                      return `
                        <tr>
                          <td style="padding-left: 36px;">
                            <span style="color: #6b7280;">•</span>
                            <span style="margin-left: 6px;">${child.name}</span>
                          </td>
                          <td style="text-align: center;">${child.required}</td>
                          <td style="text-align: center;">${child.earned}</td>
                          <td style="text-align: center; ${child.remaining > 0 ? 'color: #dc2626; font-weight: 600;' : ''}">${child.remaining}</td>
                          <td style="text-align: center;">
                            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                              <div style="width: 70px; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                                <div style="width: ${Math.min(child.percent, 100)}%; height: 100%; background: ${child.percent >= 100 ? '#10b981' : '#3b82f6'}; border-radius: 4px;"></div>
                              </div>
                              <span style="font-size: 11px; font-weight: 500;">${child.percent}%</span>
                            </div>
                          </td>
                        </tr>
                        ${grandchildren.map(gc => `
                          <tr>
                            <td style="padding-left: 60px; font-size: 11px; color: #6b7280;">
                              └ ${gc.name}
                            </td>
                            <td style="text-align: center; font-size: 11px;">${gc.required}</td>
                            <td style="text-align: center; font-size: 11px;">${gc.earned}</td>
                            <td style="text-align: center; font-size: 11px; ${gc.remaining > 0 ? 'color: #dc2626; font-weight: 600;' : ''}">${gc.remaining}</td>
                            <td style="text-align: center;">
                              <div style="display: flex; align-items: center; justify-content: center; gap: 6px;">
                                <div style="width: 60px; height: 6px; background: #f3f4f6; border-radius: 3px; overflow: hidden;">
                                  <div style="width: ${Math.min(gc.percent, 100)}%; height: 100%; background: ${gc.percent >= 100 ? '#10b981' : '#3b82f6'}; border-radius: 3px;"></div>
                                </div>
                                <span style="font-size: 10px; color: #9ca3af;">${gc.percent}%</span>
                              </div>
                            </td>
                          </tr>
                        `).join('')}
                      `
                    }).join('')}
                  `
                }).join('')}
              </tbody>
            </table>
          </div>

          <div class="footer">
            <p>本报告仅作参考，非官方证明文件</p>
            <p>如有问题，请联系教务处</p>
          </div>
        </div>
      </body>
      </html>
    `

    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(html)
      printWindow.document.close()
      printWindow.focus()
      
      printWindow.addEventListener('load', () => {
        setTimeout(() => {
          printWindow.print()
          printWindow.close()
        }, 500)
      })
    }
  }

  return { printReport }
}
