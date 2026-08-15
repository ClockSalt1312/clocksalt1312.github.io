# -*- coding: utf-8 -*-
"""
Inject CSS + HTML blocks into the v2 base file (CRLF-safe).
"""
import sys

p = r'D:\pentaig\整活2\预览\index.html'

CSS_BLOCK = r'''
/* ===== 整活夜：剧照轮播 ===== */
        .photo-strip {
            padding: 24px 0 8px;
            background: linear-gradient(180deg, transparent 0%, rgba(16,185,129,0.04) 100%);
        }
        .photo-strip-stage {
            position: relative;
            max-width: 960px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 56px 1fr 56px;
            align-items: center;
            gap: 12px;
            padding: 0 12px;
        }
        .photo-frame {
            position: relative;
            aspect-ratio: 16 / 9;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 36px rgba(0,0,0,0.18), 0 0 0 1px rgba(255,255,255,0.4) inset;
            background: #0f172a;
            isolation: isolate;
        }
        .photo-link {
            display: block;
            width: 100%; height: 100%;
            text-decoration: none;
            color: inherit;
            cursor: pointer;
        }
        .photo-link:focus-visible {
            outline: 3px solid var(--primary);
            outline-offset: 4px;
        }
        .photo-art {
            position: absolute; inset: 0;
            background-size: cover;
            background-position: center;
            transition: opacity 300ms ease, transform 600ms ease;
        }
        .photo-art[data-src] { background-image: none; }
        .photo-art[data-src]::before {
            content: "🖼  " attr(data-src);
            position: absolute; inset: 0;
            display: flex; align-items: center; justify-content: center;
            font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
            font-size: clamp(14px, 2.4vw, 22px);
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 12px rgba(0,0,0,0.6);
        }
        .photo-art[data-src="\u6750\u6599/3.jpg"]::before { background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%); }
        .photo-art[data-src="\u6750\u6599/4.jpg"]::before { background: linear-gradient(135deg, #f43f5e 0%, #fb923c 50%, #facc15 100%); }
        .photo-art.is-fading { opacity: 0; }
        .photo-badge {
            position: absolute;
            left: 16px; bottom: 16px;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(15,23,42,0.72);
            color: white;
            font-size: 13px;
            font-weight: 600;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            pointer-events: none;
        }
        .photo-badge i { margin-right: 6px; color: var(--primary); }
        .photo-arrow {
            width: 44px; height: 44px;
            border-radius: 50%;
            border: none;
            background: rgba(255,255,255,0.85);
            color: #0f172a;
            font-size: 26px;
            font-weight: 900;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(0,0,0,0.18);
            transition: transform .15s ease, background .15s ease;
            display: flex; align-items: center; justify-content: center;
        }
        .photo-arrow:hover { background: white; transform: scale(1.08); }
        .photo-arrow:active { transform: scale(0.95); }
        .photo-arrow:focus-visible { outline: 3px solid var(--primary); outline-offset: 3px; }
        html[data-theme="dark"] .photo-arrow {
            background: rgba(15,23,42,0.85);
            color: #f1f5f9;
        }
        html[data-theme="dark"] .photo-arrow:hover { background: #1e293b; }
        .photo-dots {
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 14px 0 4px;
        }
        .photo-dots .dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: rgba(15,23,42,0.2);
            transition: background .2s ease, width .2s ease;
        }
        .photo-dots .dot.active {
            background: var(--primary);
            width: 24px;
            border-radius: 4px;
        }
        html[data-theme="dark"] .photo-dots .dot { background: rgba(255,255,255,0.25); }

        /* ===== 整活夜：抽象广告弹窗 ===== */
        .popup-modal[hidden] { display: none !important; }
        .popup-modal {
            position: fixed; inset: 0;
            z-index: 9999;
            display: flex; align-items: center; justify-content: center;
            padding: 16px;
        }
        .popup-mask {
            position: absolute; inset: 0;
            background: rgba(15,23,42,0.55);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            animation: popupMaskIn 220ms ease both;
        }
        .popup-card {
            position: relative;
            max-width: 420px;
            width: 100%;
            background: var(--surface);
            color: var(--text-primary);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 24px 64px rgba(0,0,0,0.4);
            animation: popupCardIn 280ms cubic-bezier(.2,.9,.3,1.2) both;
        }
        @keyframes popupMaskIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes popupCardIn {
            from { opacity: 0; transform: scale(0.85) translateY(20px); }
            to   { opacity: 1; transform: scale(1) translateY(0); }
        }
        .popup-modal.is-leaving .popup-mask { animation: popupMaskOut 180ms ease both; }
        .popup-modal.is-leaving .popup-card { animation: popupCardOut 180ms ease both; }
        @keyframes popupMaskOut { from { opacity: 1; } to { opacity: 0; } }
        @keyframes popupCardOut {
            from { opacity: 1; transform: scale(1); }
            to   { opacity: 0; transform: scale(0.92); }
        }
        .popup-close {
            position: absolute;
            top: 10px; right: 10px;
            width: 32px; height: 32px;
            border-radius: 50%;
            border: none;
            background: rgba(255,255,255,0.92);
            color: #0f172a;
            font-size: 20px;
            font-weight: 900;
            line-height: 1;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            z-index: 2;
            transition: transform .15s ease;
        }
        .popup-close:hover { transform: rotate(90deg); }
        .popup-close:focus-visible { outline: 3px solid var(--primary); outline-offset: 2px; }
        .popup-art {
            position: relative;
            aspect-ratio: 4 / 3;
            background-size: cover;
            background-position: center;
        }
        .popup-art[data-src]::before {
            content: "📢  " attr(data-src);
            position: absolute; inset: 0;
            display: flex; align-items: center; justify-content: center;
            font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
            font-size: clamp(13px, 2vw, 18px);
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 12px rgba(0,0,0,0.6);
        }
        .popup-art[data-src="\u6750\u6599/1.jpg"]::before { background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%); }
        .popup-art[data-src="\u6750\u6599/2.jpg"]::before { background: linear-gradient(135deg, #ef4444 0%, #f59e0b 100%); }
        .popup-body {
            padding: 20px 22px 22px;
        }
        .popup-title {
            margin: 0 0 6px;
            font-size: 20px;
            font-weight: 800;
        }
        .popup-subtitle {
            margin: 0 0 16px;
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }
        .popup-action {
            width: 100%;
            padding: 11px 16px;
            border: none;
            border-radius: 10px;
            background: var(--primary);
            color: white;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: background .15s ease, transform .15s ease;
        }
        .popup-action:hover { background: var(--primary-hover); }
        .popup-action:active { transform: scale(0.98); }

        body.popup-open { overflow: hidden; }

        @media (max-width: 640px) {
            .photo-strip-stage {
                grid-template-columns: 40px 1fr 40px;
                gap: 8px;
                padding: 0 8px;
            }
            .photo-arrow { width: 36px; height: 36px; font-size: 22px; }
            .popup-card { max-width: 92vw; }
        }
'''

HTML_BLOCK = r'''
    <!-- ===== 整活夜：剧照轮播（放在 header 之上 = 主站最上面） ===== -->
    <section class="photo-strip" aria-label="\u56e2\u961f\u5267\u7167\u8f6e\u64ad" id="photoStrip">
        <div class="photo-strip-stage">
            <button class="photo-arrow photo-arrow--left" type="button" aria-label="\u4e0a\u4e00\u5f20" id="photoPrev">&#8249;</button>
            <div class="photo-frame" id="photoFrame">
                <a class="photo-link" id="photoLink" href="#" target="_blank" rel="noopener noreferrer">
                    <div class="photo-art" id="photoArt" data-src="\u6750\u6599/3.jpg"></div>
                    <span class="photo-badge"><i class="fas fa-clapperboard"></i><span id="photoBadge">\u5267\u7167 3</span></span>
                </a>
            </div>
            <button class="photo-arrow photo-arrow--right" type="button" aria-label="\u4e0b\u4e00\u5f20" id="photoNext">&#8250;</button>
        </div>
        <div class="photo-dots" id="photoDots" role="tablist" aria-label="\u5267\u7167\u9009\u62e9">
            <span class="dot active" role="tab" aria-selected="true"  data-dot-index="0"></span>
            <span class="dot"        role="tab" aria-selected="false" data-dot-index="1"></span>
        </div>
    </section>

    <!-- ===== 整活夜：抽象广告弹窗（HTML 占位，JS 按 config 渲染） ===== -->
    <div class="popup-modal" id="popupModal" hidden role="presentation">
        <div class="popup-mask" data-popup-close></div>
        <div class="popup-card" role="dialog" aria-modal="true" aria-labelledby="popupTitle">
            <button class="popup-close" type="button" aria-label="\u5173\u95ed\u5f39\u7a97" data-popup-close>×</button>
            <div class="popup-art" id="popupArt" data-src="\u6750\u6599/1.jpg"></div>
            <div class="popup-body">
                <h3 class="popup-title" id="popupTitle">\u62bd\u8c61\u5f39\u7a97</h3>
                <p class="popup-subtitle" id="popupSubtitle">\u526f\u6807\u9898\u5360\u4f4d\u6587\u672c</p>
                <button class="popup-action" type="button" id="popupAction">\u6309\u94ae\u5360\u4f4d</button>
            </div>
        </div>
    </div>
'''

with open(p, 'rb') as f:
    data = f.read()

# CRLF → LF for safer manipulation
crlf = data.count(b'\r\n')
print(f'Original: {len(data)} bytes, CRLF lines: {crlf}')
text = data.decode('utf-8')
text = text.replace('\r\n', '\n')

# 1. CSS inject before </style>
marker_css = '</style>'
idx_css = text.find(marker_css)
assert idx_css != -1, 'no </style>'
text = text[:idx_css] + CSS_BLOCK.lstrip('\n') + text[idx_css:]
print(f'CSS injected at char {idx_css}')

# 2. HTML inject before Header marker
marker_html = '<!-- ===== Header ===== -->'
idx_html = text.find(marker_html)
assert idx_html != -1, 'no Header marker'
text = text[:idx_html] + HTML_BLOCK + text[idx_html:]
print(f'HTML injected at char {idx_html}')

# Convert back to CRLF
final = text.replace('\n', '\r\n').encode('utf-8')
with open(p, 'wb') as f:
    f.write(final)

crlf_count = final.count(b'\r\n')
print(f'New file: {len(final)} bytes, CRLF: {crlf_count}')