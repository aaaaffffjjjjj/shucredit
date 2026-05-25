/* global SolarSystem2D */
(function () {
    const USER_ID = window.PROGRESS_USER_ID;
    const LS_UNKNOWN = `unknown_courses_${USER_ID}`;
    const PROGRESS_CACHE_KEY = `progress_cache_${USER_ID}`;
    const CACHE_MS = 30000;

    let progressData = null;
    let solarReady = false;

    const el = (id) => document.getElementById(id);

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function showToast(msg) {
        const t = el('toast');
        if (!t) return;
        t.textContent = msg;
        t.classList.add('show');
        setTimeout(() => t.classList.remove('show'), 2800);
    }

    function readProgressCache() {
        try {
            const raw = sessionStorage.getItem(PROGRESS_CACHE_KEY);
            if (!raw) return null;
            const { ts, data } = JSON.parse(raw);
            if (Date.now() - ts < CACHE_MS) return data;
        } catch (_) { /* ignore */ }
        return null;
    }

    function writeProgressCache(data) {
        try {
            sessionStorage.setItem(PROGRESS_CACHE_KEY, JSON.stringify({
                ts: Date.now(),
                data,
            }));
        } catch (_) { /* ignore */ }
    }

    function clearProgressCache() {
        sessionStorage.removeItem(PROGRESS_CACHE_KEY);
    }

    async function fetchJSON(url, options = {}) {
        const res = await fetch(url, {
            credentials: 'same-origin',
            headers: options.body instanceof FormData
                ? {}
                : { 'Content-Type': 'application/json' },
            ...options,
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || '请求失败');
        return data;
    }

    function updateStatusBanner(allMet) {
        const b = el('status-banner');
        if (!b) return;
        b.className = 'status-banner ' + (allMet ? 'ok' : 'warn');
        b.textContent = allMet
            ? '已完成所有顶级模块学分要求。'
            : '点击行星查看子模块；点击卫星查阅未修课程。请通过上传教务处官方 PDF 记录已修课。';
    }

    function applyProgressData(data) {
        progressData = data;
        updateStatusBanner(data.all_met);
        if (solarReady && window.SolarSystem2D) {
            SolarSystem2D.updateData(data);
        }
    }

    async function loadProgress(force) {
        if (!force) {
            const cached = readProgressCache();
            if (cached) {
                applyProgressData(cached);
                return cached;
            }
        }
        const data = await fetchJSON('/api/progress_data');
        writeProgressCache(data);
        applyProgressData(data);
        return data;
    }

    function renderCourseList(courses) {
        const box = el('course-list');
        if (!box) return;
        if (!courses.length) {
            box.innerHTML = '<p class="hint">暂无已修课程，请上传 PDF。</p>';
            return;
        }
        box.innerHTML = courses.map((c) => `
            <div class="course-item">
                <div title="${escapeHtml(c.course_code + ' ' + c.name)}">
                    <strong class="text-wrap">${escapeHtml(c.course_code)}</strong>
                    <span class="hint text-wrap">${escapeHtml(c.name)} · ${c.credit} 学分</span>
                </div>
                <button type="button" class="btn btn-danger btn-sm btn-remove"
                    data-code="${escapeHtml(c.course_code)}">删除</button>
            </div>
        `).join('');

        box.querySelectorAll('.btn-remove').forEach((btn) => {
            btn.addEventListener('click', async () => {
                if (!confirm('从已修列表移除该课程？')) return;
                try {
                    const data = await fetchJSON('/api/remove_enrollment', {
                        method: 'POST',
                        body: JSON.stringify({ course_code: btn.dataset.code }),
                    });
                    clearProgressCache();
                    if (data.progress) applyProgressData(data.progress);
                    renderCourseList(data.courses || []);
                    showToast('已移除');
                } catch (e) {
                    showToast(e.message);
                }
            });
        });
    }

    async function loadCourses() {
        const data = await fetchJSON('/api/my_courses');
        renderCourseList(data.courses);
    }

    function saveUnknownLocal(list) {
        localStorage.setItem(LS_UNKNOWN, JSON.stringify(list));
    }

    function loadUnknownLocal() {
        try {
            return JSON.parse(localStorage.getItem(LS_UNKNOWN) || '[]');
        } catch {
            return [];
        }
    }

    function buildModuleSelect(options) {
        let html = '<option value="">选择所属模块</option>';
        options.forEach((o) => {
            const pad = '　'.repeat(o.level) + (o.level ? '└ ' : '');
            html += `<option value="${o.id}">${pad}${escapeHtml(o.label)}</option>`;
        });
        return html;
    }

    async function renderUnknownPanel() {
        const panel = el('unknown-list');
        if (!panel) return;

        let serverList = [];
        try {
            const data = await fetchJSON('/api/unknown_courses');
            serverList = data.courses || [];
        } catch (_) { /* ignore */ }

        const merged = {};
        [...loadUnknownLocal(), ...serverList].forEach((item) => {
            merged[item.course_code] = { ...merged[item.course_code], ...item };
        });
        const list = Object.values(merged);
        saveUnknownLocal(list);

        const section = el('unknown-section');
        if (section) section.style.display = list.length ? 'block' : 'none';
        if (!list.length) {
            panel.innerHTML = '';
            return;
        }

        let moduleOpts = [];
        try {
            const mo = await fetchJSON('/api/module_options');
            moduleOpts = mo.options || [];
        } catch (_) { /* ignore */ }

        panel.innerHTML = list.map((item) => `
            <div class="unknown-item">
                <p><strong>${escapeHtml(item.course_code)}</strong></p>
                <div class="form-row">
                    <label>课程名称</label>
                    <input type="text" class="unk-name" value="${escapeHtml(item.name || '')}">
                </div>
                <div class="form-row">
                    <label>学分</label>
                    <input type="number" step="0.5" class="unk-credit" value="${item.credit || ''}">
                </div>
                <div class="form-row">
                    <label>所属模块</label>
                    <select class="unk-module">${buildModuleSelect(moduleOpts)}</select>
                </div>
                <button type="button" class="btn btn-sm btn-add-unknown"
                    data-code="${escapeHtml(item.course_code)}">添加至课程库</button>
            </div>
        `).join('');

        panel.querySelectorAll('.btn-add-unknown').forEach((btn) => {
            btn.addEventListener('click', async () => {
                const row = btn.closest('.unknown-item');
                const code = btn.dataset.code;
                const name = row.querySelector('.unk-name').value.trim();
                const credit = parseFloat(row.querySelector('.unk-credit').value) || 0;
                const moduleId = row.querySelector('.unk-module').value;
                if (!name || !moduleId) {
                    showToast('请填写名称并选择模块');
                    return;
                }
                try {
                    const data = await fetchJSON('/api/add_course_from_user', {
                        method: 'POST',
                        body: JSON.stringify({
                            course_code: code,
                            name,
                            credit,
                            module_id: moduleId,
                        }),
                    });
                    saveUnknownLocal(loadUnknownLocal().filter((x) => x.course_code !== code));
                    clearProgressCache();
                    if (data.progress) applyProgressData(data.progress);
                    await renderUnknownPanel();
                    await loadCourses();
                    showToast(data.message);
                } catch (e) {
                    showToast(e.message);
                }
            });
        });
    }

    async function openViewOnlyModal(moduleId, moduleName) {
        el('recommend-title').textContent = '本模块未修课程（仅供查看）';
        el('recommend-body').innerHTML = `
            <p class="view-only-note">以下课程尚未计入已修列表，仅供参考。
            请通过上传教务处官方 PDF 记录已修课程。</p>
            <p class="hint">模块：${escapeHtml(moduleName)} · 加载中…</p>`;
        el('recommend-modal').classList.add('open');

        try {
            const data = await fetchJSON(`/api/recommend_courses/${moduleId}`);
            const courses = data.courses || [];
            if (!courses.length) {
                el('recommend-body').innerHTML = `
                    <p class="view-only-note">请通过上传官方 PDF 记录已修课程。</p>
                    <p class="hint">模块「${escapeHtml(moduleName)}」下暂无未修课程。</p>`;
                return;
            }
            el('recommend-body').innerHTML = `
                <p class="view-only-note">共 ${courses.length} 门（仅供查阅，不可手动添加）。</p>
                ${courses.map((c) => `
                    <div class="recommend-row" title="${escapeHtml(c.course_code + ' ' + c.name)}">
                        <strong>${escapeHtml(c.course_code)}</strong>
                        <span class="text-wrap"> ${escapeHtml(c.name)}</span><br>
                        <span class="hint">${c.credit} 学分</span>
                    </div>
                `).join('')}`;
        } catch (e) {
            el('recommend-body').innerHTML = `<p class="hint">${escapeHtml(e.message)}</p>`;
        }
    }

    window.openModuleCourses = openViewOnlyModal;

    function setupUpload() {
        const form = el('upload-form');
        if (!form) return;
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData(form);
            try {
                const res = await fetch('/api/upload_pdf', {
                    method: 'POST',
                    body: fd,
                    credentials: 'same-origin',
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error);
                if (data.unknown?.length) {
                    const map = {};
                    [...loadUnknownLocal(), ...data.unknown].forEach((x) => {
                        map[x.course_code] = x;
                    });
                    saveUnknownLocal(Object.values(map));
                }
                clearProgressCache();
                if (data.progress) applyProgressData(data.progress);
                else await loadProgress(true);
                await loadCourses();
                await renderUnknownPanel();
                showToast(data.message);
                form.reset();
            } catch (err) {
                showToast(err.message);
            }
        });
    }

    function setupUI() {
        el('btn-close-recommend')?.addEventListener('click', () => {
            el('recommend-modal').classList.remove('open');
        });
        el('recommend-modal')?.addEventListener('click', (e) => {
            if (e.target === el('recommend-modal')) {
                el('recommend-modal').classList.remove('open');
            }
        });
        document.querySelectorAll('.collapsible-header').forEach((h) => {
            h.addEventListener('click', () => {
                h.classList.toggle('collapsed');
                h.nextElementSibling?.classList.toggle('collapsed');
            });
        });

        const slider = el('solar-time-slider');
        slider?.addEventListener('input', () => {
            const v = parseInt(slider.value, 10);
            const iframe = el('solar-iframe');
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.postMessage({ type: 'timeScale', scale: v }, '*');
            }
        });
    }

    async function initSolarSystem(data) {
        const iframe = el('solar-iframe');
        if (!iframe) return;
        iframe.addEventListener('load', () => {
            iframe.contentWindow.postMessage({ type: 'creditData', data: data }, '*');
            solarReady = true;
        }, { once: true });
        if (iframe.contentDocument?.readyState === 'complete') {
            iframe.contentWindow.postMessage({ type: 'creditData', data: data }, '*');
            solarReady = true;
        }
    }

    document.addEventListener('DOMContentLoaded', async () => {
        setupUI();
        setupUpload();
        try {
            const data = await loadProgress(false);
            await Promise.all([loadCourses(), renderUnknownPanel()]);
            await initSolarSystem(data);
        } catch (e) {
            showToast('加载失败：' + e.message);
            document.querySelector('.solar-loading-text').textContent = '加载失败，请刷新页面';
        }
    });
})();
