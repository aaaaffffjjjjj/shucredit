/**
 * Kurzgesagt 风格 2D 太阳系 - 固定全景视角 + 动态背景 + 悬浮动画
 */
window.SolarSystem2D = (function () {
    const SUN_REQUIRED_DEFAULT = 160;
    const SEMESTER_LABELS = ['第1学期', '第2学期', '第3学期', '第4学期', '第5学期', '第6学期', '第7学期', '第8学期'];
    const PLANET_COLORS = ['#3b82f6', '#f97316', '#8b5cf6', '#ec4899', '#10b981', '#06b6d4', '#f59e0b', '#ef4444'];
    const TEXTURE_TYPES = ['stripe', 'spot', 'ring'];

    let canvas, ctx;
    let animationId = null, isRunning = false, lastTime = 0;
    let modulesById = {}, rootModules = [];
    let sunData = { required: 160, earned: 0 };
    let timePercent = 100, viewMode = 'panoramic', focusedPlanetId = null, callbacks = {};
    let starsFar = [], starsNear = [], meteors = [], asteroidBelt = [];
    let planets = [], satellites = [], coronaParticles = [];
    let hoveredTarget = null;
    let canvasWidth = 0, canvasHeight = 0, centerX = 0, centerY = 0, dpr = 1;
    let offsetX = 0, offsetY = 0, targetOffsetX = 0, targetOffsetY = 0;
    let nextMeteorTime = 0;

    function hexToRgb(hex) {
        return { r: parseInt(hex.slice(1, 3), 16), g: parseInt(hex.slice(3, 5), 16), b: parseInt(hex.slice(5, 7), 16) };
    }
    function rgbToHex(r, g, b) {
        return '#' + [r, g, b].map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
    }
    function lerp(a, b, t) { return a + (b - a) * t; }
    function clamp(v, min, max) { return Math.max(min, Math.min(max, v)); }
    function adjustBrightness(hex, f) { const c = hexToRgb(hex); return rgbToHex(c.r * f, c.g * f, c.b * f); }
    function saturateColor(hex, s) {
        const c = hexToRgb(hex), gray = 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b;
        return rgbToHex(gray + s * (c.r - gray), gray + s * (c.g - gray), gray + s * (c.b - gray));
    }

    function scaledModule(mod, scale01) {
        const earned = (mod.earned || 0) * scale01, required = mod.required || 0;
        const percent = required > 0 ? Math.min(100, Math.round((earned / required) * 1000) / 10) : 0;
        return { earned: Math.round(earned * 100) / 100, percent, remaining: Math.max(0, required - earned) };
    }

    function buildModuleMaps(modules) {
        modulesById = {}; rootModules = [];
        modules.forEach(m => { modulesById[m.id] = { ...m, children: [] }; });
        modules.forEach(m => {
            const node = modulesById[m.id];
            if (m.parent_id == null) rootModules.push(node);
            else if (modulesById[m.parent_id]) modulesById[m.parent_id].children.push(node);
        });
        rootModules.sort((a, b) => a.name.localeCompare(b.name));
    }

    // ========== 动态背景 ==========
    function initBackground() {
        starsFar = [];
        for (let i = 0; i < 400; i++) {
            starsFar.push({ x: Math.random(), y: Math.random(), size: 0.5 + Math.random() * 1, opacity: 0.3 + Math.random() * 0.5 });
        }
        starsNear = [];
        for (let i = 0; i < 150; i++) {
            const colorChoice = Math.random();
            starsNear.push({
                x: Math.random(), y: Math.random(),
                size: 1.5 + Math.random() * 1.5,
                phase: Math.random() * Math.PI * 2,
                speed: 0.3 + Math.random() * 1.2,
                color: colorChoice > 0.7 ? '#aaccff' : (colorChoice > 0.4 ? '#ffeecc' : '#ffffff')
            });
        }
        asteroidBelt = [];
        for (let i = 0; i < 400; i++) {
            const angle = Math.random() * Math.PI * 2;
            const dist = 160 + Math.random() * 80;
            asteroidBelt.push({
                x: Math.cos(angle) * dist, y: Math.sin(angle) * dist * 0.4,
                size: 0.3 + Math.random() * 0.8,
                opacity: 0.2 + Math.random() * 0.3,
                rotation: Math.random() * Math.PI * 2,
                rotSpeed: (Math.random() - 0.5) * 0.02
            });
        }
        meteors = [];
        nextMeteorTime = Date.now() + 20000 + Math.random() * 10000;
    }

    function updateMeteors(currentTime) {
        if (currentTime > nextMeteorTime) {
            meteors.push({
                x: canvasWidth * 0.8 + Math.random() * canvasWidth * 0.2,
                y: Math.random() * canvasHeight * 0.4,
                vx: -(4 + Math.random() * 5), vy: 2 + Math.random() * 3,
                life: 1, length: 80 + Math.random() * 80
            });
            nextMeteorTime = currentTime + 20000 + Math.random() * 10000;
        }
        meteors = meteors.filter(m => {
            m.x += m.vx; m.y += m.vy; m.life -= 0.012;
            return m.life > 0;
        });
    }

    function drawNebula() {
        const nebulae = [
            { x: 0.12, y: 0.25, r: 0.28, c1: 'rgba(140, 80, 220, 0.07)', c2: 'transparent' },
            { x: 0.8, y: 0.55, r: 0.25, c1: 'rgba(60, 140, 220, 0.06)', c2: 'transparent' },
            { x: 0.55, y: 0.85, r: 0.22, c1: 'rgba(220, 100, 160, 0.05)', c2: 'transparent' }
        ];
        nebulae.forEach(n => {
            const g = ctx.createRadialGradient(n.x * canvasWidth, n.y * canvasHeight, 0, n.x * canvasWidth, n.y * canvasHeight, n.r * canvasWidth);
            g.addColorStop(0, n.c1); g.addColorStop(1, n.c2);
            ctx.fillStyle = g; ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        });
    }

    function drawBackground() {
        const bg = ctx.createLinearGradient(0, 0, 0, canvasHeight);
        bg.addColorStop(0, '#080c20'); bg.addColorStop(1, '#151a38');
        ctx.fillStyle = bg; ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        drawNebula();
        starsFar.forEach(s => {
            ctx.beginPath();
            ctx.arc(s.x * canvasWidth, s.y * canvasHeight, s.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${s.opacity})`;
            ctx.fill();
        });
    }

    function drawDynamicElements(time) {
        starsNear.forEach(s => {
            const alpha = 0.35 + 0.45 * Math.sin(time * 0.001 * s.speed + s.phase);
            ctx.beginPath();
            ctx.arc(s.x * canvasWidth, s.y * canvasHeight, s.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.fill();
        });
        asteroidBelt.forEach(a => {
            a.rotation += a.rotSpeed;
            ctx.save();
            ctx.translate(centerX + a.x, centerY + a.y);
            ctx.rotate(a.rotation);
            ctx.beginPath();
            ctx.arc(0, 0, a.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(200, 200, 220, ${a.opacity})`;
            ctx.fill();
            ctx.restore();
        });
        meteors.forEach(m => {
            const grad = ctx.createLinearGradient(m.x, m.y, m.x - m.vx * m.length / 3, m.y - m.vy * m.length / 3);
            grad.addColorStop(0, `rgba(255, 255, 255, ${m.life})`);
            grad.addColorStop(1, 'transparent');
            ctx.beginPath(); ctx.moveTo(m.x, m.y);
            ctx.lineTo(m.x - m.vx * m.length / 3, m.y - m.vy * m.length / 3);
            ctx.strokeStyle = grad; ctx.lineWidth = 2; ctx.stroke();
            ctx.beginPath(); ctx.arc(m.x, m.y, 1.5, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${m.life})`; ctx.fill();
        });
    }

    // ========== 太阳 ==========
    function initCoronaParticles() {
        coronaParticles = [];
        for (let i = 0; i < 14; i++) {
            coronaParticles.push({
                angle: (i / 14) * Math.PI * 2, radius: 38 + Math.random() * 14,
                speed: 0.0002 + Math.random() * 0.0004,
                size: 2 + Math.random() * 2.5, opacity: 0.4 + Math.random() * 0.4
            });
        }
    }

    function drawSun(time) {
        const pulse = 1 + 0.04 * Math.sin(time * 0.002);
        const sunR = 32, cx = centerX + offsetX, cy = centerY + offsetY - 20;
        const completion = clamp(sunData.earned / (sunData.required || SUN_REQUIRED_DEFAULT), 0, 1);

        coronaParticles.forEach(p => {
            p.angle += p.speed * (time - lastTime);
            const px = cx + Math.cos(p.angle) * (sunR + p.radius) * 0.85;
            const py = cy + Math.sin(p.angle) * (sunR + p.radius) * 0.5;
            ctx.beginPath(); ctx.arc(px, py, p.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 220, 100, ${p.opacity * completion})`; ctx.fill();
        });

        ctx.shadowBlur = 40; ctx.shadowColor = '#ffaa44';
        const sunGrad = ctx.createRadialGradient(cx - sunR * 0.2, cy - sunR * 0.2, 0, cx, cy, sunR * pulse);
        sunGrad.addColorStop(0, '#fff7b0'); sunGrad.addColorStop(0.4, '#ffcc33'); sunGrad.addColorStop(1, '#ffaa00');
        ctx.beginPath(); ctx.arc(cx, cy, sunR * pulse, 0, Math.PI * 2);
        ctx.fillStyle = sunGrad; ctx.fill(); ctx.shadowBlur = 0;

        ctx.font = 'bold 13px "Microsoft YaHei", sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        const label = `🎓 总要求 ${sunData.required} 学分`;
        const lw = ctx.measureText(label).width + 30, lh = 28;
        const ly = cy + sunR + 28;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        ctx.beginPath(); ctx.roundRect(cx - lw / 2, ly - lh / 2, lw, lh, 14); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.fillText(label, cx, ly);
    }

    // ========== 行星系统 ==========
    function getTextureType(i) { return TEXTURE_TYPES[i % TEXTURE_TYPES.length]; }

    function genTexture(type, radius) {
        const data = { type };
        if (type === 'stripe') {
            data.stripes = [];
            const count = 3 + Math.floor(Math.random() * 3);
            for (let i = 0; i < count; i++) {
                data.stripes.push({ y: -radius * 0.5 + (i / (count - 1)) * radius, w: 2 + Math.random() * 2.5, op: 0.2 + Math.random() * 0.25 });
            }
        } else if (type === 'spot') {
            data.spots = [];
            const count = 8 + Math.floor(Math.random() * 8);
            for (let i = 0; i < count; i++) {
                const a = Math.random() * Math.PI * 2, d = Math.random() * radius * 0.65;
                data.spots.push({ x: Math.cos(a) * d, y: Math.sin(a) * d, size: 1.5 + Math.random() * 3, op: 0.15 + Math.random() * 0.2 });
            }
        } else if (type === 'ring') {
            data.rings = [];
            const count = 2 + Math.floor(Math.random() * 2);
            for (let i = 0; i < count; i++) {
                data.rings.push({ r: radius * (0.35 + i * 0.28), op: 0.12 + Math.random() * 0.15 });
            }
        }
        return data;
    }

    function createPlanets() {
        planets = [];
        rootModules.forEach((mod, i) => {
            const orbitRX = 90 + i * 55, orbitRY = orbitRX / 1.4;
            const speed = 0.18 / Math.sqrt(orbitRX / 90);
            const radius = clamp(13, 30, 11 + Math.pow(mod.required || 10, 0.4));
            const baseColor = PLANET_COLORS[i % PLANET_COLORS.length];
            planets.push({
                id: mod.id, name: mod.name, data: mod,
                orbitRX, orbitRY, speed, angle: (i / rootModules.length) * Math.PI * 2,
                radius, baseColor, textureType: getTextureType(i),
                texture: genTexture(getTextureType(i), radius)
            });
        });
    }

    function drawOrbit(planet, dimmed) {
        const cx = centerX + offsetX, cy = centerY + offsetY - 20;
        ctx.beginPath();
        ctx.ellipse(cx, cy, planet.orbitRX, planet.orbitRY, 0, 0, Math.PI * 2);
        ctx.setLineDash([5, 10]);
        ctx.strokeStyle = dimmed ? 'rgba(255, 255, 255, 0.12)' : 'rgba(255, 255, 255, 0.3)';
        ctx.lineWidth = 1.5; ctx.stroke(); ctx.setLineDash([]);
    }

    function drawOrbitDot(planet) {
        const cx = centerX + offsetX, cy = centerY + offsetY - 20;
        const dx = cx + Math.cos(planet.angle) * planet.orbitRX;
        const dy = cy + Math.sin(planet.angle) * planet.orbitRY;
        ctx.shadowBlur = 8; ctx.shadowColor = '#fff';
        ctx.beginPath(); ctx.arc(dx, dy, 3, 0, Math.PI * 2);
        ctx.fillStyle = '#fff'; ctx.fill(); ctx.shadowBlur = 0;
    }

    function drawPlanetTexture(planet, px, py, radius) {
        const tex = planet.texture;
        ctx.save(); ctx.beginPath(); ctx.arc(px, py, radius, 0, Math.PI * 2); ctx.clip();
        if (tex.type === 'stripe' && tex.stripes) {
            tex.stripes.forEach(s => {
                ctx.beginPath(); ctx.moveTo(px - radius, py + s.y);
                ctx.lineTo(px + radius, py + s.y);
                ctx.strokeStyle = `rgba(255, 255, 255, ${s.op})`; ctx.lineWidth = s.w; ctx.stroke();
            });
        } else if (tex.type === 'spot' && tex.spots) {
            tex.spots.forEach(s => {
                ctx.beginPath(); ctx.arc(px + s.x, py + s.y, s.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${s.op})`; ctx.fill();
            });
        } else if (tex.type === 'ring' && tex.rings) {
            tex.rings.forEach(r => {
                ctx.beginPath(); ctx.arc(px, py, r.r, 0, Math.PI * 2);
                ctx.strokeStyle = `rgba(255, 255, 255, ${r.op})`; ctx.lineWidth = 1.5; ctx.stroke();
            });
        }
        ctx.restore();
    }

    function drawPlanet(planet, isHovered, dimmed) {
        const cx = centerX + offsetX, cy = centerY + offsetY - 20;
        const px = cx + Math.cos(planet.angle) * planet.orbitRX;
        const py = cy + Math.sin(planet.angle) * planet.orbitRY;
        const s = scaledModule(planet.data, timePercent / 100);
        const alpha = dimmed ? 0.2 : 1;
        const hoveredScale = isHovered ? 1.2 : 1;
        const radius = planet.radius * hoveredScale;
        const brightness = 0.4 + (s.percent / 100) * 0.6;
        const saturation = 0.55 + (s.percent / 100) * 0.45;
        let color = saturateColor(adjustBrightness(planet.baseColor, brightness), saturation);

        if (isHovered) { ctx.shadowBlur = 25; ctx.shadowColor = planet.baseColor; }

        const atmGrad = ctx.createRadialGradient(px, py, radius * 0.8, px, py, radius * 1.5);
        const atmC = hexToRgb(color);
        atmGrad.addColorStop(0, `rgba(${atmC.r}, ${atmC.g}, ${atmC.b}, 0)`);
        atmGrad.addColorStop(1, `rgba(${atmC.r}, ${atmC.g}, ${atmC.b}, 0.25)`);
        ctx.beginPath(); ctx.arc(px, py, radius * 1.5, 0, Math.PI * 2);
        ctx.fillStyle = atmGrad; ctx.fill();

        const planetGrad = ctx.createRadialGradient(px - radius * 0.3, py - radius * 0.3, 0, px, py, radius);
        const rgb = hexToRgb(color);
        planetGrad.addColorStop(0, `rgba(${Math.min(255, rgb.r + 50)}, ${Math.min(255, rgb.g + 50)}, ${Math.min(255, rgb.b + 50)}, ${alpha})`);
        planetGrad.addColorStop(0.7, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`);
        planetGrad.addColorStop(1, `rgba(${Math.max(0, rgb.r - 40)}, ${Math.max(0, rgb.g - 40)}, ${Math.max(0, rgb.b - 40)}, ${alpha})`);
        ctx.beginPath(); ctx.arc(px, py, radius, 0, Math.PI * 2);
        ctx.fillStyle = planetGrad; ctx.fill(); ctx.shadowBlur = 0;

        drawPlanetTexture(planet, px, py, radius);

        if (isHovered && s.percent > 0) {
            ctx.beginPath();
            ctx.arc(px, py, radius + 6, -Math.PI / 2, -Math.PI / 2 + (s.percent / 100) * Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 215, 80, 0.95)'; ctx.lineWidth = 3; ctx.stroke();
        } else if (s.percent > 0) {
            ctx.beginPath();
            ctx.arc(px, py, radius + 5, -Math.PI / 2, -Math.PI / 2 + (s.percent / 100) * Math.PI * 2);
            ctx.strokeStyle = `rgba(255, 255, 255, ${0.6 * alpha})`; ctx.lineWidth = 2; ctx.stroke();
        }

        const labelAngle = planet.angle + Math.PI * 0.18;
        const labelDist = planet.orbitRX + 32;
        const lx = cx + Math.cos(labelAngle) * labelDist;
        const ly = cy + Math.sin(labelAngle) * labelDist;
        const label = planet.name.length > 9 ? planet.name.slice(0, 8) + '…' : planet.name;

        ctx.font = '12px "Microsoft YaHei", sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        const lm = ctx.measureText(label);
        const lw = lm.width + 16, lh = 22;
        ctx.fillStyle = `rgba(0, 0, 0, ${0.55 * alpha})`;
        ctx.beginPath(); ctx.roundRect(lx - lw / 2, ly - lh / 2, lw, lh, 6); ctx.fill();
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`; ctx.fillText(label, lx, ly);

        return { type: 'planet', data: planet, x: px, y: py, radius };
    }

    // ========== 卫星系统 ==========
    function updateSatellites(planet) {
        satellites = [];
        if (!planet || !planet.data.children || planet.data.children.length === 0) return;
        const children = planet.data.children;
        const dist = planet.radius + 45;
        children.forEach((child, i) => {
            const angle = (i / children.length) * Math.PI * 2;
            const req = child.required || 10;
            const size = clamp(6, 12, 6 + Math.pow(req, 0.35) * 2.5);
            satellites.push({ id: child.id, name: child.name, data: child, angle, radius: size, dist, baseColor: planet.baseColor });
        });
    }

    function drawSatellites(planet, time, hoveredSatId) {
        if (!planet || satellites.length === 0) return;
        const cx = centerX + offsetX, cy = centerY + offsetY - 20;
        const px = cx + Math.cos(planet.angle) * planet.orbitRX;
        const py = cy + Math.sin(planet.angle) * planet.orbitRY;
        const selfRot = (time / 1000) * 0.35 * (Math.PI / 180);

        satellites.forEach(sat => {
            const angle = sat.angle + selfRot;
            const sx = px + Math.cos(angle) * sat.dist;
            const sy = py + Math.sin(angle) * sat.dist;
            const s = scaledModule(sat.data, timePercent / 100);
            const isHovered = sat.id === hoveredSatId;
            const hoveredScale = isHovered ? 1.2 : 1;
            const radius = sat.radius * hoveredScale;

            ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(sx, sy);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)'; ctx.lineWidth = 1; ctx.stroke();

            const brightness = 0.4 + (s.percent / 100) * 0.6;
            const color = adjustBrightness(sat.baseColor, brightness);
            const rgb = hexToRgb(color);
            const satGrad = ctx.createRadialGradient(sx - radius * 0.3, sy - radius * 0.3, 0, sx, sy, radius);
            satGrad.addColorStop(0, `rgba(${Math.min(255, rgb.r + 40)}, ${Math.min(255, rgb.g + 40)}, ${Math.min(255, rgb.b + 40)}, 1)`);
            satGrad.addColorStop(1, `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 1)`);
            ctx.beginPath(); ctx.arc(sx, sy, radius, 0, Math.PI * 2);
            ctx.fillStyle = satGrad; ctx.fill();

            ctx.beginPath(); ctx.arc(sx, sy, radius + 4, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)'; ctx.lineWidth = 1.5; ctx.stroke();

            if (isHovered) {
                ctx.beginPath();
                ctx.arc(sx, sy, radius + 4, -Math.PI / 2, -Math.PI / 2 + (s.percent / 100) * Math.PI * 2);
                ctx.strokeStyle = 'rgba(255, 215, 80, 0.95)'; ctx.lineWidth = 3; ctx.stroke();
            } else if (s.percent > 0) {
                ctx.beginPath();
                ctx.arc(sx, sy, radius + 4, -Math.PI / 2, -Math.PI / 2 + (s.percent / 100) * Math.PI * 2);
                ctx.strokeStyle = 'rgba(255, 215, 80, 0.7)'; ctx.lineWidth = 2; ctx.stroke();
            }
        });
    }

    // ========== 工具提示 ==========
    function showTooltip(obj, clientX, clientY) {
        const tip = document.getElementById('solar-tooltip');
        if (!tip || !obj) return;
        const s = scaledModule(obj.data, timePercent / 100);
        tip.innerHTML = `<strong>${obj.data.name}</strong><div>已修: ${s.earned} / ${obj.data.required} 学分</div><div>完成度: ${s.percent}%</div>`;
        tip.classList.add('visible');
        const rect = canvas.getBoundingClientRect();
        tip.style.left = (clientX - rect.left + 18) + 'px';
        tip.style.top = (clientY - rect.top - 15) + 'px';
    }
    function hideTooltip() {
        const tip = document.getElementById('solar-tooltip');
        if (tip) tip.classList.remove('visible');
    }

    // ========== 渲染循环 ==========
    function render(time) {
        if (!isRunning || !ctx) return;
        const dt = lastTime ? time - lastTime : 16;
        lastTime = time;

        offsetX = lerp(offsetX, targetOffsetX, 0.06);
        offsetY = lerp(offsetY, targetOffsetY, 0.06);

        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        drawBackground();
        drawDynamicElements(time);
        updateMeteors(time);

        let focusedPlanet = viewMode === 'focused' ? planets.find(p => p.id === focusedPlanetId) : null;
        let hoveredSatId = (hoveredTarget && hoveredTarget.type === 'satellite') ? hoveredTarget.data.id : null;

        planets.forEach(p => {
            const dimmed = focusedPlanet && p.id !== focusedPlanet.id;
            drawOrbit(p, dimmed);
        });
        if (!focusedPlanet) planets.forEach(p => drawOrbitDot(p));

        if (focusedPlanet) {
            drawSatellites(focusedPlanet, time, hoveredSatId);
        }

        planets.forEach(p => {
            const dimmed = focusedPlanet && p.id !== focusedPlanet.id;
            const isHovered = hoveredTarget && hoveredTarget.type === 'planet' && hoveredTarget.data.id === p.id;
            drawPlanet(p, isHovered, dimmed);
        });

        drawSun(time);

        animationId = requestAnimationFrame(render);
    }

    // ========== 交互 ==========
    function getWorldCoords(clientX, clientY) {
        const rect = canvas.getBoundingClientRect();
        return { x: clientX - rect.left, y: clientY - rect.top };
    }

    function hitTest(wx, wy) {
        let focusedPlanet = viewMode === 'focused' ? planets.find(p => p.id === focusedPlanetId) : null;

        if (focusedPlanet) {
            const cx = centerX + offsetX, cy = centerY + offsetY - 20;
            const px = cx + Math.cos(focusedPlanet.angle) * focusedPlanet.orbitRX;
            const py = cy + Math.sin(focusedPlanet.angle) * focusedPlanet.orbitRY;
            const selfRot = (Date.now() / 1000) * 0.35 * (Math.PI / 180);

            for (const sat of satellites) {
                const angle = sat.angle + selfRot;
                const sx = px + Math.cos(angle) * sat.dist;
                const sy = py + Math.sin(angle) * sat.dist;
                if (Math.hypot(wx - sx, wy - sy) <= sat.radius + 8) {
                    return { type: 'satellite', data: sat };
                }
            }
        }

        for (const p of planets) {
            const cx = centerX + offsetX, cy = centerY + offsetY - 20;
            const px = cx + Math.cos(p.angle) * p.orbitRX;
            const py = cy + Math.sin(p.angle) * p.orbitRY;
            if (Math.hypot(wx - px, wy - py) <= p.radius + 8) {
                return { type: 'planet', data: p };
            }
        }
        return null;
    }

    function handleMouseMove(e) {
        const coords = getWorldCoords(e.clientX, e.clientY);
        const hit = hitTest(coords.x, coords.y);

        if (hit && hit.type !== 'sun') {
            hoveredTarget = hit;
            showTooltip(hit, e.clientX, e.clientY);
            canvas.style.cursor = 'pointer';
        } else {
            hoveredTarget = null;
            hideTooltip();
            canvas.style.cursor = 'default';
        }
    }

    function handleClick(e) {
        const coords = getWorldCoords(e.clientX, e.clientY);
        const hit = hitTest(coords.x, coords.y);

        if (!hit) return;

        if (hit.type === 'planet') {
            focusOnPlanet(hit.data);
        } else if (hit.type === 'satellite') {
            if (callbacks.onSatelliteClick) {
                callbacks.onSatelliteClick(hit.data.id, hit.data.name);
            }
        }
    }

    function focusOnPlanet(planet) {
        if (viewMode === 'focused' && focusedPlanetId === planet.id) {
            resetView(); return;
        }
        viewMode = 'focused';
        focusedPlanetId = planet.id;
        updateSatellites(planet);

        const cx = centerX, cy = centerY - 20;
        const px = cx + Math.cos(planet.angle) * planet.orbitRX;
        const py = cy + Math.sin(planet.angle) * planet.orbitRY;
        targetOffsetX = cx - px;
        targetOffsetY = cy - py;

        const backBtn = document.getElementById('solar-back-btn');
        if (backBtn) backBtn.classList.add('visible');
    }

    function resetView() {
        viewMode = 'panoramic';
        focusedPlanetId = null;
        satellites = [];
        targetOffsetX = 0;
        targetOffsetY = 0;
        hoveredTarget = null;
        hideTooltip();

        const backBtn = document.getElementById('solar-back-btn');
        if (backBtn) backBtn.classList.remove('visible');
    }

    function handleResize() {
        if (!canvas) return;
        const parent = canvas.parentElement;
        const w = parent.clientWidth || 900;
        const h = Math.max(550, parent.clientHeight || 580);
        dpr = window.devicePixelRatio || 1;
        canvasWidth = w; canvasHeight = h;
        centerX = w / 2; centerY = h * 0.58;
        canvas.width = w * dpr; canvas.height = h * dpr;
        canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);
        initBackground();
        createPlanets();
    }

    function setLoading(hide) {
        const loading = document.querySelector('.solar-loading');
        if (loading) hide ? loading.classList.add('hidden') : loading.remove('hidden');
    }

    function updateSemesterLabel() {
        const label = document.getElementById('semester-label');
        if (label) {
            const idx = Math.round((timePercent / 100) * 7);
            label.textContent = SEMESTER_LABELS[Math.min(7, idx)];
        }
    }

    return {
        init(dom, data, cbs) {
            callbacks = cbs || {};
            canvas = dom;
            if (!canvas || canvas.tagName !== 'CANVAS') {
                canvas = document.createElement('canvas');
                dom.appendChild(canvas);
            }
            ctx = canvas.getContext('2d');
            dpr = window.devicePixelRatio || 1;

            const w = canvas.parentElement.clientWidth || 900;
            const h = Math.max(550, canvas.parentElement.clientHeight || 580);
            canvasWidth = w; canvasHeight = h;
            centerX = w / 2; centerY = h * 0.58;
            canvas.width = w * dpr; canvas.height = h * dpr;
            canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
            ctx.setTransform(1, 0, 0, 1, 0, 0);
            ctx.scale(dpr, dpr);

            canvas.addEventListener('mousemove', handleMouseMove, { passive: true });
            canvas.addEventListener('click', handleClick, { passive: true });
            window.addEventListener('resize', handleResize);

            const backBtn = document.getElementById('solar-back-btn');
            if (backBtn) backBtn.addEventListener('click', resetView);

            const slider = document.getElementById('solar-time-slider');
            if (slider) {
                slider.addEventListener('input', () => {
                    timePercent = parseInt(slider.value, 10);
                    updateSemesterLabel();
                });
            }

            this.updateData(data);
            initBackground();
            initCoronaParticles();
            createPlanets();

            isRunning = true; lastTime = 0;
            animationId = requestAnimationFrame(render);
            setLoading(true);
        },

        updateData(data) {
            if (!data) return;
            buildModuleMaps(data.modules || []);
            if (data.sun) {
                sunData.required = data.sun.required || SUN_REQUIRED_DEFAULT;
                sunData.earned = data.sun.earned || 0;
            }
            createPlanets();
            if (viewMode === 'focused' && focusedPlanetId) {
                const still = planets.find(p => p.id === focusedPlanetId);
                if (still) updateSatellites(still);
                else resetView();
            }
            updateSemesterLabel();
        },

        setTimeScale(percent) {
            timePercent = percent; updateSemesterLabel();
        },

        destroy() {
            isRunning = false;
            if (animationId) cancelAnimationFrame(animationId);
            canvas?.removeEventListener('mousemove', handleMouseMove);
            canvas?.removeEventListener('click', handleClick);
            window.removeEventListener('resize', handleResize);
        }
    };
})();