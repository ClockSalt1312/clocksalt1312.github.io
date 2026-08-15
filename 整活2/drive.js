// Drive headless Edge via CDP for timed screenshots
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const URL = 'http://127.0.0.1:8766/%E9%A2%84%E8%A7%88/index.html';
const PORT = 9333;

function fetchJSON(path) {
    return new Promise((resolve, reject) => {
        http.get({ host: '127.0.0.1', port: PORT, path }, (res) => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
        }).on('error', reject);
    });
}

async function send(ws, method, params = {}) {
    return new Promise((resolve, reject) => {
        const id = Math.floor(Math.random() * 1e9);
        const onMsg = (msg) => {
            const m = JSON.parse(msg.toString());
            if (m.id === id) {
                ws.off('message', onMsg);
                if (m.error) reject(new Error(m.error.message)); else resolve(m.result);
            }
        };
        ws.on('message', onMsg);
        ws.send(JSON.stringify({ id, method, params }));
    });
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function capture(pageWs, file) {
    const { data } = await send(pageWs, 'Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(file, Buffer.from(data, 'base64'));
    console.log(`Saved ${file}`);
}

(async () => {
    // Launch Edge with remote debugging
    const browser = spawn(EDGE, [
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        `--remote-debugging-port=${PORT}`,
        '--window-size=1280,800',
        URL,
    ], { stdio: 'ignore' });

    // Wait for browser to be ready
    await sleep(2000);

    // Get list of pages
    let pages;
    for (let i = 0; i < 20; i++) {
        try { pages = await fetchJSON('/json'); break; } catch { await sleep(300); }
    }
    const page = pages.find(p => p.type === 'page' && p.url.includes('index.html'));
    if (!page) { console.error('No page found', pages); browser.kill(); process.exit(1); }

    // Connect WS
    const WS = require('ws');
    const ws = new WS(page.webSocketDebuggerUrl);
    await new Promise(r => ws.on('open', r));

    await send(ws, 'Page.enable');
    await send(ws, 'Runtime.enable');

    // Wait for popup to appear (JS uses setTimeout 400ms)
    await sleep(1500);
    // Debug: report popup state
    const dbg1 = await send(ws, 'Runtime.evaluate', { expression: `
        JSON.stringify({
            modalHidden: document.getElementById('popupModal').hidden,
            modalClass: document.getElementById('popupModal').className,
            popupSrc: document.getElementById('popupArt').style.backgroundImage,
            photoSrc: document.getElementById('photoArt').style.backgroundImage,
        })
    `});
    console.log('debug 01:', dbg1.result.value);
    await capture(ws, 'D:\\pentaig\\整活2\\截图\\01_popup1.png');

    // Close popup 1 by clicking close button — we know selector
    await send(ws, 'Runtime.evaluate', { expression: `
        document.querySelector('#popupModal .popup-close').click();
    `});
    await sleep(700); // wait for second popup
    await capture(ws, 'D:\\pentaig\\整活2\\截图\\02_popup2.png');

    // Close popup 2
    await send(ws, 'Runtime.evaluate', { expression: `
        document.querySelector('#popupModal .popup-close').click();
    `});
    await sleep(700);
    await capture(ws, 'D:\\pentaig\\整活2\\截图\\03_after_popups_carousel.png');

    // Click right arrow on carousel
    await send(ws, 'Runtime.evaluate', { expression: `
        document.querySelector('#photoNext').click();
    `});
    await sleep(500);
    await capture(ws, 'D:\\pentaig\\整活2\\截图\\04_carousel_right.png');

    // Test mobile viewport
    await send(ws, 'Emulation.setDeviceMetricsOverride', {
        width: 390, height: 800, deviceScaleFactor: 2, mobile: true,
    });
    await send(ws, 'Runtime.evaluate', { expression: `
        // re-open popup to test mobile too
        document.querySelector('#photoStrip').scrollIntoView();
    `});
    await sleep(500);
    await capture(ws, 'D:\\pentaig\\整活2\\截图\\05_mobile_carousel.png');

    browser.kill();
    process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });