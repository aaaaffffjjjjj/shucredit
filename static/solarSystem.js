/**
 * 学分进度 — 太阳系 3D 可视化 (Three.js)
 */
/* global THREE, TWEEN */
window.SolarSystem = (function () {
    const SUN_REQUIRED_DEFAULT = 160;
    const SEMESTER_LABELS = [
        '第1学期', '第2学期', '第3学期', '第4学期',
        '第5学期', '第6学期', '第7学期', '第8学期',
    ];

    let container = null;
    let scene = null;
    let camera = null;
    let renderer = null;
    let labelRenderer = null;
    let controls = null;
    let raycaster = null;
    let mouse = null;
    let animationId = null;
    let clock = null;

    let modulesById = {};
    let rootModules = [];
    let sunData = { required: 160, earned: 0 };
    let timePercent = 100;
    let focusedPlanet = null;
    let callbacks = {};

    const planets = [];
    let sunGroup = null;
    let starField = null;
    let coronaPoints = null;
    let satelliteGroup = null;
    let connectionLines = [];
    let isMobile = false;

    const hoverTooltip = () => document.getElementById('solar-tooltip');
    const backBtn = () => document.getElementById('solar-back-btn');

    function lerpColor(c1, c2, t) {
        const a = new THREE.Color(c1);
        const b = new THREE.Color(c2);
        return a.lerp(b, t).getHex();
    }

    function planetColorByPercent(pct) {
        if (pct >= 80) return 0xf4c542;
        if (pct >= 40) return lerpColor(0x6c5ce7, 0xa463f5, (pct - 40) / 40);
        return lerpColor(0x2d1b4e, 0x5e2a84, pct / 40);
    }

    function satelliteColorByPercent(pct) {
        if (pct >= 100) return 0xf4c542;
        if (pct >= 50) return 0x7bed9f;
        if (pct > 0) return 0xff9500;
        return 0x8b3a62;
    }

    function scaledModule(mod, scale01) {
        const earned = mod.earned * scale01;
        const required = mod.required || 0;
        const percent = required > 0
            ? Math.min(100, Math.round((earned / required) * 1000) / 10)
            : 0;
        return {
            earned: Math.round(earned * 100) / 100,
            percent,
            remaining: Math.max(0, required - earned),
        };
    }

    function buildModuleMaps(modules) {
        modulesById = {};
        modules.forEach((m) => {
            modulesById[m.id] = { ...m, children: [] };
        });
        rootModules = [];
        modules.forEach((m) => {
            const node = modulesById[m.id];
            if (m.parent_id == null) {
                rootModules.push(node);
            } else if (modulesById[m.parent_id]) {
                modulesById[m.parent_id].children.push(node);
            }
        });
    }

    function planetRadius(required) {
        const minR = isMobile ? 0.45 : 0.55;
        const maxR = isMobile ? 1.1 : 1.45;
        const ref = 30;
        return minR + Math.min(required / ref, 1.5) * (maxR - minR);
    }

    function createStarField(count) {
        const positions = new Float32Array(count * 3);
        const sizes = new Float32Array(count);
        for (let i = 0; i < count; i++) {
            const r = 40 + Math.random() * 80;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = (Math.random() - 0.5) * 30;
            positions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
            sizes[i] = 0.5 + Math.random() * 2.5;
        }
        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        const mat = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 1.2,
            transparent: true,
            opacity: 0.75,
            sizeAttenuation: true,
            depthWrite: false,
        });
        return new THREE.Points(geo, mat);
    }

    function createSun() {
        const g = new THREE.Group();
        const core = new THREE.Mesh(
            new THREE.SphereGeometry(2.2, 48, 48),
            new THREE.MeshStandardMaterial({
                color: 0xff6633,
                emissive: 0xffaa44,
                emissiveIntensity: 1.2,
                metalness: 0.2,
                roughness: 0.4,
            }),
        );
        g.add(core);

        const glow = new THREE.Sprite(
            new THREE.SpriteMaterial({
                color: 0xffaa44,
                transparent: true,
                opacity: 0.35,
                blending: THREE.AdditiveBlending,
                depthWrite: false,
            }),
        );
        glow.scale.set(14, 14, 1);
        g.add(glow);

        const coronaCount = isMobile ? 120 : 220;
        const pos = new Float32Array(coronaCount * 3);
        for (let i = 0; i < coronaCount; i++) {
            const a = Math.random() * Math.PI * 2;
            const d = 2.8 + Math.random() * 2;
            pos[i * 3] = Math.cos(a) * d;
            pos[i * 3 + 1] = (Math.random() - 0.5) * 0.8;
            pos[i * 3 + 2] = Math.sin(a) * d;
        }
        const cGeo = new THREE.BufferGeometry();
        cGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
        coronaPoints = new THREE.Points(
            cGeo,
            new THREE.PointsMaterial({
                color: 0xffcc66,
                size: isMobile ? 0.15 : 0.22,
                transparent: true,
                opacity: 0.7,
                blending: THREE.AdditiveBlending,
                depthWrite: false,
            }),
        );
        g.add(coronaPoints);

        const light = new THREE.PointLight(0xffaa88, 2.2, 80);
        g.add(light);
        scene.add(new THREE.AmbientLight(0x334466, 0.35));
        return g;
    }

    function createOrbitLine(a, b) {
        const curve = new THREE.EllipseCurve(0, 0, a, b, 0, 2 * Math.PI, false, 0);
        const pts = curve.getPoints(80);
        const points = pts.map((p) => new THREE.Vector3(p.x, 0, p.y));
        const geo = new THREE.BufferGeometry().setFromPoints(points);
        const mat = new THREE.LineBasicMaterial({
            color: 0x4d6cf0,
            transparent: true,
            opacity: 0.4,
        });
        return new THREE.Line(geo, mat);
    }

    function createProgressRing(radius, percent, color) {
        const pct = Math.max(0, Math.min(1, percent / 100));
        const geo = new THREE.RingGeometry(
            radius * 1.15, radius * 1.28, 48, 1, 0, Math.PI * 2 * pct,
        );
        const mat = new THREE.MeshBasicMaterial({
            color,
            transparent: true,
            opacity: 0.85,
            side: THREE.DoubleSide,
        });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.rotation.x = -Math.PI / 2;
        mesh.userData.baseOpacity = 0.85;
        return mesh;
    }

    function createPlanetLabel(text) {
        const div = document.createElement('div');
        div.className = 'module-label';
        div.textContent = text.length > 14 ? `${text.slice(0, 13)}…` : text;
        div.title = text;
        const label = new THREE.CSS2DObject(div);
        label.position.set(0, 1.2, 0);
        return label;
    }

    function updatePlanetVisual(p, scale01, animate) {
        const s = scaledModule(p.data, scale01);
        p.scaled = s;
        const col = planetColorByPercent(s.percent);
        p.mesh.material.color.setHex(col);
        p.mesh.material.emissive.setHex(col);
        p.mesh.material.emissiveIntensity = 0.25 + (s.percent / 100) * 0.45;

        const targetTheta = (s.percent / 100) * Math.PI * 2;
        const r = p.radius;
        const applyTheta = (theta) => {
            p.progressRing.geometry.dispose();
            p.progressRing.geometry = new THREE.RingGeometry(
                r * 1.15, r * 1.28, 48, 1, 0, theta,
            );
        };
        if (animate && typeof TWEEN !== 'undefined') {
            const from = p.userData.ringTheta ?? 0;
            new TWEEN.Tween({ t: from })
                .to({ t: targetTheta }, 600)
                .easing(TWEEN.Easing.Quadratic.Out)
                .onUpdate((o) => applyTheta(o.t))
                .onComplete(() => { p.userData.ringTheta = targetTheta; })
                .start();
        } else {
            applyTheta(targetTheta);
            p.userData.ringTheta = targetTheta;
        }
        p.progressRing.material.color.setHex(col);

        if (p.ring) {
            p.ring.material.opacity = 0.15 + (s.percent / 100) * 0.35;
        }
    }

    function clearSatellites() {
        if (satelliteGroup) {
            scene.remove(satelliteGroup);
            satelliteGroup.traverse((o) => {
                if (o.geometry) o.geometry.dispose();
                if (o.material) {
                    if (Array.isArray(o.material)) o.material.forEach((m) => m.dispose());
                    else o.material.dispose();
                }
            });
            satelliteGroup = null;
        }
        connectionLines.forEach((l) => {
            scene.remove(l);
            l.geometry.dispose();
            l.material.dispose();
        });
        connectionLines = [];
    }

    function showSatellites(planet) {
        clearSatellites();
        satelliteGroup = new THREE.Group();
        satelliteGroup.position.copy(planet.group.position);
        const children = planet.data.children || [];
        const count = children.length;
        if (!count) {
            scene.add(satelliteGroup);
            return;
        }

        const scale01 = timePercent / 100;
        children.forEach((child, i) => {
            const angle = (i / count) * Math.PI * 2;
            const dist = planet.radius + 1.8 + (i % 3) * 0.4;
            const st = scaledModule(child, scale01);
            const col = satelliteColorByPercent(st.percent);
            const size = 0.12 + (child.required / 40) * 0.12;

            const satMesh = new THREE.Mesh(
                new THREE.SphereGeometry(size, 12, 12),
                new THREE.MeshStandardMaterial({
                    color: col,
                    emissive: col,
                    emissiveIntensity: 0.6,
                    metalness: 0.5,
                    roughness: 0.3,
                }),
            );
            satMesh.position.set(Math.cos(angle) * dist, 0, Math.sin(angle) * dist);
            satMesh.userData = { type: 'satellite', module: child, planet };

            const ring = new THREE.Mesh(
                new THREE.RingGeometry(size * 1.4, size * 1.7, 24, 1, 0, (st.percent / 100) * Math.PI * 2),
                new THREE.MeshBasicMaterial({
                    color: col, transparent: true, opacity: 0.8, side: THREE.DoubleSide,
                }),
            );
            ring.rotation.x = -Math.PI / 2;
            satMesh.add(ring);

            const div = document.createElement('div');
            div.className = 'module-label satellite-label';
            div.textContent = child.name.length > 10 ? `${child.name.slice(0, 9)}…` : child.name;
            div.title = `${child.name}\n${st.earned}/${child.required}（${st.percent}%）`;
            const lbl = new THREE.CSS2DObject(div);
            lbl.position.set(0, size + 0.35, 0);
            satMesh.add(lbl);

            satelliteGroup.add(satMesh);

            const curve = new THREE.QuadraticBezierCurve3(
                new THREE.Vector3(0, 0, 0),
                new THREE.Vector3(
                    Math.cos(angle) * dist * 0.5,
                    0.4,
                    Math.sin(angle) * dist * 0.5,
                ),
                satMesh.position.clone(),
            );
            const lineGeo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(20));
            const line = new THREE.Line(
                lineGeo,
                new THREE.LineBasicMaterial({
                    color: 0x4d6cf0, transparent: true, opacity: 0.5,
                }),
            );
            connectionLines.push(line);
            scene.add(line);
        });

        satelliteGroup.userData.spin = 0;
        scene.add(satelliteGroup);
    }

    function setFocusPlanet(planet) {
        if (focusedPlanet === planet) {
            resetView();
            return;
        }
        if (focusedPlanet) {
            clearSatellites();
            planets.forEach((p) => {
                if (p.mesh.material) p.mesh.material.opacity = 1;
                if (p.label?.element) p.label.element.style.opacity = '1';
            });
        }
        focusedPlanet = planet;
        backBtn()?.classList.add('visible');

        planets.forEach((p) => {
            const fade = p === planet ? 1 : 0.22;
            if (p.mesh.material) {
                p.mesh.material.opacity = fade;
            }
            if (p.orbitLine.material) p.orbitLine.material.opacity = 0.4 * fade;
            if (p.orbitDot.material) p.orbitDot.material.opacity = fade;
            p.label.element.style.opacity = String(fade);
        });

        if (planet.ring) planet.ring.material.opacity = 0.55;
        showSatellites(planet);

        const target = new THREE.Vector3();
        planet.group.getWorldPosition(target);
        const offset = new THREE.Vector3(planet.radius + 4, 2.5, planet.radius + 3);
        const camPos = target.clone().add(offset);

        if (typeof TWEEN !== 'undefined') {
            new TWEEN.Tween(camera.position)
                .to({ x: camPos.x, y: camPos.y, z: camPos.z }, 1200)
                .easing(TWEEN.Easing.Cubic.InOut)
                .start();
            new TWEEN.Tween(controls.target)
                .to({ x: target.x, y: target.y, z: target.z }, 1200)
                .easing(TWEEN.Easing.Cubic.InOut)
                .onUpdate(() => controls.update())
                .start();
        } else {
            camera.position.copy(camPos);
            controls.target.copy(target);
        }
    }

    function resetView() {
        focusedPlanet = null;
        backBtn()?.classList.remove('visible');
        clearSatellites();

        planets.forEach((p) => {
            if (p.mesh.material) p.mesh.material.opacity = 1;
            if (p.orbitLine.material) p.orbitLine.material.opacity = 0.4;
            if (p.orbitDot.material) p.orbitDot.material.opacity = 1;
            if (p.label?.element) p.label.element.style.opacity = '1';
        });

        if (typeof TWEEN !== 'undefined') {
            new TWEEN.Tween(camera.position)
                .to({ x: 12, y: 22, z: 28 }, 1400)
                .easing(TWEEN.Easing.Cubic.InOut)
                .start();
            new TWEEN.Tween(controls.target)
                .to({ x: 0, y: 0, z: 0 }, 1400)
                .easing(TWEEN.Easing.Cubic.InOut)
                .onUpdate(() => controls.update())
                .start();
        }
    }

    function disposeObject(o) {
        if (o.geometry) o.geometry.dispose();
        if (o.material) {
            if (Array.isArray(o.material)) o.material.forEach((m) => m.dispose());
            else o.material.dispose();
        }
    }

    function createPlanets() {
        const holder = scene?.userData.planetHolder;
        const plane = scene?.userData.orbitPlane;
        planets.forEach((p) => {
            holder?.remove(p.group);
            plane?.remove(p.orbitLine);
            plane?.remove(p.orbitDot);
            p.group.traverse(disposeObject);
            p.orbitLine.geometry?.dispose();
            p.orbitLine.material?.dispose();
            p.orbitDot.geometry?.dispose();
            p.orbitDot.material?.dispose();
        });
        planets.length = 0;

        const scale01 = timePercent / 100;
        rootModules.forEach((mod, i) => {
            const radius = planetRadius(mod.required);
            const orbitA = 7 + i * 2.8;
            const orbitB = orbitA * 0.88;
            const speed = 0.35 / Math.sqrt(orbitA);
            const phase = (i / rootModules.length) * Math.PI * 2;

            const group = new THREE.Group();
            const col = planetColorByPercent(scaledModule(mod, scale01).percent);
            const mesh = new THREE.Mesh(
                new THREE.SphereGeometry(radius, 32, 32),
                new THREE.MeshStandardMaterial({
                    color: col,
                    emissive: col,
                    emissiveIntensity: 0.35,
                    metalness: 0.65,
                    roughness: 0.32,
                    transparent: true,
                    opacity: 1,
                }),
            );
            group.add(mesh);

            const band = new THREE.Mesh(
                new THREE.TorusGeometry(radius * 1.02, radius * 0.06, 8, 32),
                new THREE.MeshBasicMaterial({
                    color: 0xa463f5,
                    transparent: true,
                    opacity: 0.45,
                }),
            );
            band.rotation.x = Math.PI / 2;
            band.userData.spinSpeed = 0.4 + i * 0.05;
            group.add(band);

            const ring = new THREE.Mesh(
                new THREE.RingGeometry(radius * 1.35, radius * 1.42, 64),
                new THREE.MeshBasicMaterial({
                    color: 0x6c5ce7,
                    transparent: true,
                    opacity: 0.22,
                    side: THREE.DoubleSide,
                }),
            );
            ring.rotation.x = Math.PI / 2;
            group.add(ring);

            const prog = createProgressRing(radius, scaledModule(mod, scale01).percent, col);
            group.add(prog);

            const label = createPlanetLabel(mod.name);
            group.add(label);

            const orbitLine = createOrbitLine(orbitA, orbitB);
            const dot = new THREE.Mesh(
                new THREE.SphereGeometry(0.08, 8, 8),
                new THREE.MeshBasicMaterial({ color: 0xffd700 }),
            );

            const planet = {
                data: mod,
                group,
                mesh,
                band,
                ring,
                progressRing: prog,
                label,
                orbitLine,
                orbitDot: dot,
                radius,
                orbitA,
                orbitB,
                speed,
                phase,
                angle: phase,
            };
            updatePlanetVisual(planet, scale01, false);
            planets.push(planet);
        });
    }

    function updateAllProgress(animate) {
        const scale01 = timePercent / 100;
        planets.forEach((p) => updatePlanetVisual(p, scale01, animate));
        if (satelliteGroup && focusedPlanet) {
            showSatellites(focusedPlanet);
        }
        if (sunGroup && sunGroup.children[0]) {
            const se = sunData.earned * scale01;
            const sr = sunData.required || SUN_REQUIRED_DEFAULT;
            const pulse = 0.9 + Math.min(se / sr, 1) * 0.3;
            sunGroup.children[0].material.emissiveIntensity = pulse;
        }
    }

    function showTooltip(html, x, y) {
        const tip = hoverTooltip();
        if (!tip) return;
        tip.innerHTML = html;
        tip.classList.add('visible');
        tip.style.left = `${Math.min(x + 14, window.innerWidth - 300)}px`;
        tip.style.top = `${Math.min(y + 14, window.innerHeight - 120)}px`;
    }

    function hideTooltip() {
        hoverTooltip()?.classList.remove('visible');
    }

    function onPointerMove(event) {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);

        const targets = [];
        planets.forEach((p) => targets.push(p.mesh));
        if (satelliteGroup) {
            satelliteGroup.children.forEach((c) => targets.push(c));
        }

        const hits = raycaster.intersectObjects(targets, false);
        if (hits.length) {
            const obj = hits[0].object;
            container.style.cursor = 'pointer';
            if (obj.userData.type === 'satellite') {
                const m = obj.userData.module;
                const st = scaledModule(m, timePercent / 100);
                showTooltip(
                    `<strong>${m.name}</strong>`
                    + `已修 ${st.earned} / 要求 ${m.required}<br>完成 ${st.percent}%`,
                    event.clientX,
                    event.clientY,
                );
                obj.scale.set(1.3, 1.3, 1.3);
            } else {
                const p = planets.find((pl) => pl.mesh === obj);
                if (p) {
                    const st = p.scaled || scaledModule(p.data, timePercent / 100);
                    showTooltip(
                        `<strong>${p.data.name}</strong>`
                        + `已修 ${st.earned} / 要求 ${p.data.required}<br>完成 ${st.percent}%`,
                        event.clientX,
                        event.clientY,
                    );
                    p.mesh.scale.set(1.15, 1.15, 1.15);
                    if (p.progressRing) p.progressRing.visible = true;
                }
            }
        } else {
            container.style.cursor = 'grab';
            hideTooltip();
            planets.forEach((p) => {
                p.mesh.scale.set(1, 1, 1);
                if (p.progressRing) p.progressRing.visible = true;
            });
            if (satelliteGroup) {
                satelliteGroup.children.forEach((c) => {
                    c.scale.set(1, 1, 1);
                });
            }
        }
    }

    function onClick(event) {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);

        if (satelliteGroup) {
            const satHits = raycaster.intersectObjects(satelliteGroup.children, false);
            if (satHits.length && satHits[0].object.userData.type === 'satellite') {
                const m = satHits[0].object.userData.module;
                if (callbacks.onSatelliteClick) {
                    callbacks.onSatelliteClick(m.id, m.name);
                }
                return;
            }
        }

        const meshHits = raycaster.intersectObjects(
            planets.map((p) => p.mesh),
            false,
        );
        if (meshHits.length) {
            const p = planets.find((pl) => pl.mesh === meshHits[0].object);
            if (p) setFocusPlanet(p);
        }
    }

    function animate() {
        animationId = requestAnimationFrame(animate);
        const t = clock.getElapsedTime();
        const dt = clock.getDelta();

        if (typeof TWEEN !== 'undefined') TWEEN.update();

        if (coronaPoints) {
            coronaPoints.rotation.y = t * 0.15;
            const pos = coronaPoints.geometry.attributes.position.array;
            for (let i = 0; i < pos.length; i += 3) {
                pos[i + 1] += Math.sin(t * 2 + i) * 0.002;
            }
            coronaPoints.geometry.attributes.position.needsUpdate = true;
        }

        planets.forEach((p) => {
            if (!focusedPlanet || focusedPlanet === p) {
                p.angle += p.speed * dt * (focusedPlanet === p ? 0.3 : 1);
                const x = Math.cos(p.angle + p.phase) * p.orbitA;
                const z = Math.sin(p.angle + p.phase) * p.orbitB;
                p.group.position.set(x, 0, z);
                p.orbitDot.position.set(x, 0.05, z);
            }
            if (p.band) p.band.rotation.z += (p.band.userData.spinSpeed || 0.3) * dt;
        });

        if (satelliteGroup) {
            satelliteGroup.position.copy(focusedPlanet.group.position);
            satelliteGroup.rotation.y += dt * 0.25;
        }

        if (starField) {
            starField.material.opacity = 0.55 + Math.sin(t * 0.8) * 0.15;
        }

        controls.update();
        renderer.render(scene, camera);
        labelRenderer.render(scene, camera);
    }

    function setLoading(pct, text) {
        const fill = document.querySelector('.solar-loading-fill');
        const txt = document.querySelector('.solar-loading-text');
        if (fill) fill.style.width = `${pct}%`;
        if (txt && text) txt.textContent = text;
    }

    function hideLoading() {
        document.querySelector('.solar-loading')?.classList.add('hidden');
    }

    function init(dom, data, cbs) {
        container = dom;
        callbacks = cbs || {};
        isMobile = window.innerWidth < 768;

        if (data.sun) sunData = data.sun;
        buildModuleMaps(data.modules || []);
        timePercent = 100;

        setLoading(20, '初始化星空…');

        scene = new THREE.Scene();
        clock = new THREE.Clock();
        raycaster = new THREE.Raycaster();
        mouse = new THREE.Vector2();

        const w = container.clientWidth || 800;
        const h = container.clientHeight || 580;
        camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 200);
        camera.position.set(12, 22, 28);
        camera.lookAt(0, 0, 0);

        renderer = new THREE.WebGLRenderer({ antialias: !isMobile, alpha: true });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
        container.appendChild(renderer.domElement);

        labelRenderer = new THREE.CSS2DRenderer();
        labelRenderer.setSize(w, h);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0';
        labelRenderer.domElement.style.pointerEvents = 'none';
        container.appendChild(labelRenderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.06;
        controls.minDistance = 5;
        controls.maxDistance = 50;
        controls.minPolarAngle = THREE.MathUtils.degToRad(28);
        controls.maxPolarAngle = THREE.MathUtils.degToRad(28);
        controls.enableRotate = false;

        const tilt = new THREE.Group();
        tilt.rotation.x = THREE.MathUtils.degToRad(28);
        scene.add(tilt);
        const orbitPlane = tilt;

        setLoading(45, '创建恒星与行星…');
        starField = createStarField(isMobile ? 800 : 1600);
        orbitPlane.add(starField);

        sunGroup = createSun();
        orbitPlane.add(sunGroup);

        const planetHolder = new THREE.Group();
        orbitPlane.add(planetHolder);
        scene.userData.orbitPlane = orbitPlane;
        scene.userData.planetHolder = planetHolder;

        createPlanets();
        planets.forEach((p) => {
            planetHolder.add(p.group);
            orbitPlane.add(p.orbitLine);
            orbitPlane.add(p.orbitDot);
        });

        setLoading(90, '启动引擎…');
        container.addEventListener('pointermove', onPointerMove);
        container.addEventListener('click', onClick);
        backBtn()?.addEventListener('click', resetView);

        window.addEventListener('resize', onResize);
        hideLoading();
        setLoading(100, '就绪');
        animate();

        if (!rootModules.length) {
            const empty = document.createElement('div');
            empty.className = 'solar-empty';
            empty.textContent = '暂无培养方案模块数据，请先导入或联系管理员。';
            container.appendChild(empty);
        }
        return true;
    }

    function onResize() {
        if (!container || !camera || !renderer) return;
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
        labelRenderer.setSize(w, h);
    }

    function updateData(data) {
        if (data.sun) sunData = data.sun;
        buildModuleMaps(data.modules || []);
        if (!scene) return;
        const holder = scene.userData.planetHolder;
        createPlanets();
        const plane = scene.userData.orbitPlane;
        planets.forEach((p) => {
            holder.add(p.group);
            plane.add(p.orbitLine);
            plane.add(p.orbitDot);
        });
        if (focusedPlanet) {
            const still = planets.find((p) => p.data.id === focusedPlanet.data.id);
            focusedPlanet = still || null;
            if (still) setFocusPlanet(still);
            else resetView();
        }
        updateAllProgress(false);
    }

    function setTimeScale(percent) {
        timePercent = Math.max(0, Math.min(100, percent));
        const idx = Math.min(7, Math.floor((timePercent / 100) * 7));
        const label = document.getElementById('semester-label');
        if (label) label.textContent = SEMESTER_LABELS[idx];
        updateAllProgress(true);
    }

    function dispose() {
        if (animationId) cancelAnimationFrame(animationId);
        window.removeEventListener('resize', onResize);
        container?.removeEventListener('pointermove', onPointerMove);
        container?.removeEventListener('click', onClick);
        renderer?.dispose();
    }

    return {
        init,
        updateData,
        setTimeScale,
        resetView,
        dispose,
    };
})();
