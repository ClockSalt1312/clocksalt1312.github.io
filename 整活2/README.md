# 🎪 整活夜 — 抽象弹窗 + 剧照轮播

> **版本**：测试版 v0.1（占位图骨架）  
> **基底**：`recon/v2/index.html` (2026-08-15 commit)  
> **状态**：✅ 真图已就位（4 张 png），交付完成

---

## 📁 目录结构

```
D:\pentaig\整活2\
├── README.md                  ← 你正在看这个
├── index.html.bak             ← 基底备份（出问题一键回滚）
├── 预览\
│   └── index.html             ← 当前可预览的版本（128 KB）
├── 素材\                      ← 👉 把你的图丢这里
│   ├── 1.png (../素材/1.png 引用)                  （广告弹窗 1）
│   ├── 2.png                  （广告弹窗 2）
│   ├── 3.png                  （剧照 3，点击跳 BV1wtgM6pEqU）
│   └── 4.png                  （剧照 4，点击跳 BV1pjuX6yEyk）
├── 截图\                      ← 自动化截图（4 个状态）
│   ├── 01_popup1.png
│   ├── 02_popup2.png
│   ├── 03_after_popups_carousel.png
│   └── 04_carousel_right.png
├── inject_html.py             ← 注入脚本（CSS+HTML 结构）
├── inject_js.py               ← 注入脚本（配置+逻辑）
├── fix_css_unicode.py         ← 修复 CSS 中文转义问题
├── drive.js                   ← 自动化截图脚本（Edge CDP）
└── check_*.js                 ← Node 语法体检产物（可删）
```

---

## 🚀 一键预览

本地 HTTP 服务已在 **8765 端口**后台运行。

```
打开浏览器 → http://127.0.0.1:8765/index.html
```

如果服务掉了，重启：
```bash
cd /d/pentaig/整活2/预览 && python -c "
import http.server, socketserver
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
with socketserver.TCPServer(('127.0.0.1', 8765), Q) as httpd:
    print('listening'); httpd.serve_forever()
"
```

---

## 🖼 换图步骤（最常用）

### 步骤 1：把图丢进 `素材/` 文件夹

**4 张图，文件名严格按下面**（大小写敏感）：

| 文件 | 用途 |
|---|---|
| `素材/1.png` | 弹窗 1（点叉掉前看到的） |
| `素材/2.png` | 弹窗 2（叉掉弹窗 1 后自动弹） |
| `素材/3.png` | 剧照 3（轮播默认显示，点击跳 BV_1） |
| `素材/4.png` | 剧照 4（点右键切换后，点击跳 BV_2） |

> **不强求 jpg** — 可以是 png / webp / gif。  
> **路径要写对** — 如果你改成 `素材/photo1.png`，下面的 config 也要跟着改。  
> **不存在也不会崩** — 加载失败时自动 fallback 到 CSS 渐变占位。

### 步骤 2：（可选）改文字 / 链接 / 行为

打开 `预览/index.html`，搜 `window.ZHENGHUO_CONFIG`，你会看到一段 JS 配置：

```javascript
window.ZHENGHUO_CONFIG = {
    popups: [
        {
            src: '素材/1.png',                  // ← 改这里换图
            title: '抽象广告 1',                // ← 改标题
            subtitle: '这是一个抽象的广告弹窗…', // ← 改副标题
            actionText: '我知道了',              // ← 改按钮文字
            link: null                          // ← 填链接则按钮跳链接；不填则只关弹窗
        },
        {
            src: '素材/2.png',
            title: '抽象广告 2',
            subtitle: '这是第二个弹窗，同样抽象',
            actionText: '收下',
            link: null
        }
    ],
    photos: [
        {
            src: '素材/3.png',
            link: 'https://www.bilibili.com/video/BV1wtgM6pEqU/?spm_id_from=333.1387.homepage.video_card.click', // ← 改 B 站链接
            badge: '剧照 3 → B站'                // ← 改徽章文字
        },
        {
            src: '素材/4.png',
            link: 'https://www.bilibili.com/video/BV1pjuX6yEyk/?spm_id_from=333.1387.upload.video_card.click',
            badge: '剧照 4 → B站'
        }
    ],
    debugAlwaysPopup: true    // ← 改成 false，每天只弹一次
};
```

**只改这一段就能调整所有行为，不用碰其他代码。**

### 步骤 3：刷新浏览器看效果

不用重启 server，浏览器 Ctrl+F5 强刷即可。

---

## 🎛 调参速查

| 想做的事 | 改哪里 |
|---|---|
| 弹窗不每天弹，刷新就重弹 | `debugAlwaysPopup: true` |
| 每天只弹一次 | `debugAlwaysPopup: false` |
| 加第 3 个弹窗 | `popups` 数组再加一项 |
| 弹窗点击按钮跳外链 | 该弹窗的 `link: 'https://...'` |
| 加更多剧照 | `photos` 数组里加，下方 `<div class="dot">` 也复制粘贴一份 |
| 改弹出延迟时间 | `</body>` 前的 JS，搜 `setTimeout(function () { openPopup(0); }, 400)` 改 400 |
| 改轮播切换动画时长 | `</body>` 前的 JS，搜 `applyPhoto((idx + 1) % total, true)` 改 `true` 为 `false` 即瞬切 |
| 改弹窗渐变色 | CSS 搜 `.popup-art[data-src="素材/1.png"]` 改 `linear-gradient` |

---

## 🌗 暗色模式兼容

全部组件已加暗色覆盖 — `<theme-button>` 切到暗色后：
- 弹窗卡片自动变深色背景（用 `var(--surface)`）
- 轮播箭头变成深色圆（圆里浅字）
- 占位渐变保持彩色（视觉冲击）

---

## 📱 兼容性

| 平台/特性 | 状态 |
|---|---|
| 桌面 Chrome / Edge / Firefox / Safari | ✅ |
| 移动端 Safari / Chrome（iOS / Android） | ✅ |
| 弹窗 ESC 关闭 | ✅ |
| 弹窗点遮罩关闭 | ✅ |
| 弹窗点 × 关闭 | ✅ |
| 轮播左右箭头切换 | ✅ |
| 轮播左右键盘（焦点在轮播上时） | ✅ |
| 轮播触摸左右滑动 | ✅ |
| 轮播点击图片跳转 | ✅（按当前显示的剧照对应链接） |
| 屏幕阅读器（aria-label / role） | ✅ |
| `prefers-reduced-motion` | ⚠️ 未做（下一步可加） |

---

## 🐛 已修问题

- **CSS unicode 转义未生效**：原版 `data-src="\u6750\u6599/1.jpg"` 选择器不匹配（CSS `\u` 要求 6 位 hex + 空格/结尾）。已统一改成真中文"材料/1.png"。
- **HTTP server `getfqdn` 崩溃**：中文主机名导致 `python -m http.server` 启动失败。已用显式 `bind 127.0.0.1` + 自定义 handler 绕过。

---

## 📸 验证截图（位于 `截图/`）

| 文件 | 状态 |
|---|---|
| `01_popup1.png` | 进站立即弹出 popup1 |
| `02_popup2.png` | 关 popup1 → 自动弹 popup2 |
| `03_after_popups_carousel.png` | 关完所有弹窗，剧照轮播可见 |
| `04_carousel_right.png` | 点右箭头切到剧照 4 |

---

## ⏳ 待办（可选）

- [x] 4 张真图已就位于 `素材/1.png … 4.png`
- [ ] 真正部署前把 `debugAlwaysPopup: true` 改成 `false`
- [ ] 真图很大时建议压缩到 ≤ 500 KB / 张（弹窗）+ ≤ 1 MB / 张（剧照）
- [ ] 暗色模式占位渐变可微调（目前偏鲜艳，暗色下可能过亮）

---

## 📌 不要做的事

- 不要直接编辑基底 `index.html.bak`（那是备份，给"出事回滚"用）
- 不要改 `</head><body>` 之间的原站内容（除非你要大改原站）
- 不要 commit 到 git（这个工作区独立于 recon，没初始化 git）

---

**有问题随时喊我** 🎬