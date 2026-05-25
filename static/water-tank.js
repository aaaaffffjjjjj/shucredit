/**
 * 圆柱形水桶完成度动画（Canvas + 共享 requestAnimationFrame）
 */
(function (global) {
    const tanks = new Set();
    let rafId = null;
    let lastTime = 0;

    function startLoop() {
        if (rafId != null) return;
        const tick = (ts) => {
            const dt = lastTime ? Math.min((ts - lastTime) / 1000, 0.05) : 0.016;
            lastTime = ts;
            tanks.forEach((t) => {
                if (t.visible) t.step(dt);
            });
            rafId = requestAnimationFrame(tick);
        };
        rafId = requestAnimationFrame(tick);
    }

    function stopLoopIfEmpty() {
        if (tanks.size === 0 && rafId != null) {
            cancelAnimationFrame(rafId);
            rafId = null;
            lastTime = 0;
        }
    }

    class WaterTank {
        constructor(container, options) {
            this.container = container;
            this.percent = Math.max(0, Math.min(100, options.percent || 0));
            this.earned = options.earned ?? 0;
            this.required = options.required ?? 0;
            this.label = options.label || '';
            this.wavePhase = Math.random() * Math.PI * 2;
            this.bubbles = [];
            this.visible = false;
            this.bubbleTimer = 0;

            this.wrap = document.createElement('div');
            this.wrap.className = 'water-tank-widget';
            this.wrap.title = `${this.label}\n已修 ${this.earned} / 要求 ${this.required}（${this.percent}%）`;

            this.canvas = document.createElement('canvas');
            this.canvas.className = 'water-tank-canvas';
            this.wrap.appendChild(this.canvas);

            const cap = document.createElement('div');
            cap.className = 'water-tank-cap';
            this.wrap.appendChild(cap);

            const info = document.createElement('div');
            info.className = 'water-tank-info text-ellipsis';
            info.textContent = this.label;
            this.wrap.appendChild(info);

            const pct = document.createElement('div');
            pct.className = 'water-tank-pct';
            pct.textContent = `${this.percent}%`;
            this.wrap.appendChild(pct);

            container.appendChild(this.wrap);
            this.ctx = this.canvas.getContext('2d');
            this.resize();
            this.drawStatic();

            this._io = new IntersectionObserver((entries) => {
                this.visible = entries[0]?.isIntersecting ?? false;
                if (this.visible) startLoop();
            }, { threshold: 0.1 });
            this._io.observe(this.wrap);
            tanks.add(this);
            startLoop();
        }

        resize() {
            const w = this.wrap.clientWidth || 88;
            const h = 120;
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            this.canvas.width = w * dpr;
            this.canvas.height = h * dpr;
            this.canvas.style.width = `${w}px`;
            this.canvas.style.height = `${h}px`;
            this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            this.w = w;
            this.h = h;
        }

        step(dt) {
            this.wavePhase += dt * 2.2;
            this.bubbleTimer += dt;
            if (this.bubbleTimer > 0.45 && this.percent > 2) {
                this.bubbleTimer = 0;
                this.bubbles.push({
                    x: this.w * (0.25 + Math.random() * 0.5),
                    y: this.h * (1 - this.percent / 100) + 8,
                    r: 1.5 + Math.random() * 2,
                    vy: 18 + Math.random() * 22,
                    life: 1,
                });
            }
            this.bubbles.forEach((b) => {
                b.y -= b.vy * dt;
                b.life -= dt * 0.9;
            });
            this.bubbles = this.bubbles.filter((b) => b.life > 0 && b.y > 4);
            this.draw();
        }

        drawStatic() {
            this.draw();
        }

        draw() {
            const { ctx, w, h } = this;
            ctx.clearRect(0, 0, w, h);
            const pad = 6;
            const rw = w - pad * 2;
            const rh = h - pad * 2;
            const x = pad;
            const y = pad;

            ctx.fillStyle = 'rgba(232, 232, 237, 0.9)';
            ctx.strokeStyle = 'rgba(210, 210, 215, 1)';
            ctx.lineWidth = 2;
            roundRect(ctx, x, y, rw, rh, 14);
            ctx.fill();
            ctx.stroke();

            const level = y + rh * (1 - this.percent / 100);
            if (this.percent <= 0) return;

            ctx.save();
            roundRect(ctx, x + 1, y + 1, rw - 2, rh - 2, 12);
            ctx.clip();

            const grad = ctx.createLinearGradient(0, level, 0, y + rh);
            grad.addColorStop(0, 'rgba(0, 113, 227, 0.55)');
            grad.addColorStop(1, 'rgba(0, 113, 227, 0.88)');
            ctx.fillStyle = grad;

            ctx.beginPath();
            ctx.moveTo(x, y + rh);
            ctx.lineTo(x + rw, y + rh);
            for (let i = rw; i >= 0; i -= 4) {
                const wave = Math.sin((i / rw) * Math.PI * 3 + this.wavePhase) * 3;
                ctx.lineTo(x + i, level + wave);
            }
            ctx.closePath();
            ctx.fill();

            this.bubbles.forEach((b) => {
                ctx.globalAlpha = b.life * 0.7;
                ctx.fillStyle = 'rgba(255,255,255,0.85)';
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fill();
            });
            ctx.globalAlpha = 1;
            ctx.restore();
        }

        destroy() {
            this._io?.disconnect();
            tanks.delete(this);
            this.wrap.remove();
            stopLoopIfEmpty();
        }
    }

    function roundRect(ctx, x, y, w, h, r) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + w - r, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + r);
        ctx.lineTo(x + w, y + h - r);
        ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        ctx.lineTo(x + r, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - r);
        ctx.lineTo(x, y + r);
        ctx.quadraticCurveTo(x, y, x + r, y);
        ctx.closePath();
    }

    global.WaterTank = {
        mount(container, options) {
            return new WaterTank(container, options);
        },
        destroyAll(container) {
            container.querySelectorAll('.water-tank-widget').forEach((el) => {
                const inst = [...tanks].find((t) => t.wrap === el);
                inst?.destroy();
            });
        },
    };
})(window);
