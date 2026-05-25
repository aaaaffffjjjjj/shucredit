function pad(n) {
    return String(n).padStart(2, '0');
}

function updateClock() {
    const el = document.getElementById('auth-clock');
    if (!el) return;
    const d = new Date();
    el.textContent = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} `
        + `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 1000);
});
