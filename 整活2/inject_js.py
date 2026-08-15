# -*- coding: utf-8 -*-
"""
Inject JS (config + popup + carousel logic) before </body>.
"""
p = r'D:\pentaig\整活2\预览\index.html'

JS_BLOCK = r'''
    <!-- ===== 整活夜：配置区（改这里就能换图/换链接/调时机） ===== -->
    <script>
    window.ZHENGHUO_CONFIG = {
        // 抽象弹窗：进站先弹 popup1，关掉后再弹 popup2
        popups: [
            {
                src: '\u6750\u6599/1.jpg',  // 图片路径（不存在就用 CSS 占位渐变）
                title: '\u62bd\u8c61\u5e7f\u544a 1',
                subtitle: '\u8fd9\u662f\u4e00\u4e2a\u62bd\u8c61\u7684\u5e7f\u544a\u5f39\u7a97\uff0c\u5173\u6389\u540e\u4f1a\u518d\u5f39\u4e00\u4e2a',
                actionText: '\u6211\u77e5\u9053\u4e86',
                link: null  // null=只关闭弹窗；或填完整URL（带https://）
            },
            {
                src: '\u6750\u6599/2.jpg',
                title: '\u62bd\u8c61\u5e7f\u544a 2',
                subtitle: '\u8fd9\u662f\u7b2c\u4e8c\u4e2a\u5f39\u7a97\uff0c\u540c\u6837\u62bd\u8c61',
                actionText: '\u6536\u4e0b',
                link: null
            }
        ],
        // 剧照轮播：点击图片跳转B站
        photos: [
            {
                src: '\u6750\u6599/3.jpg',
                link: 'https://www.bilibili.com/video/BV1wtgM6pEqU/?spm_id_from=333.1387.homepage.video_card.click',
                badge: '\u5267\u7167 3 \u2192 B\u7ad9'
            },
            {
                src: '\u6750\u6599/4.jpg',
                link: 'https://www.bilibili.com/video/BV1pjuX6yEyk/?spm_id_from=333.1387.upload.video_card.click',
                badge: '\u5267\u7167 4 \u2192 B\u7ad9'
            }
        ],
        // 调试：true = 不论何时都弹弹窗（开发完改回 false）
        debugAlwaysPopup: true
    };
    </script>

    <!-- ===== 整活夜：抽象弹窗逻辑 ===== -->
    <script>
    (function () {
        var cfg = window.ZHENGHUO_CONFIG;
        if (!cfg || !cfg.popups || !cfg.popups.length) return;

        var modal = document.getElementById('popupModal');
        var art   = document.getElementById('popupArt');
        var title = document.getElementById('popupTitle');
        var sub   = document.getElementById('popupSubtitle');
        var act   = document.getElementById('popupAction');
        if (!modal || !art || !title || !sub || !act) return;

        var today = new Date().toISOString().slice(0, 10);
        var seenKey = 'zhenghuo-popups-seen';
        var alreadySeen = false;
        try { alreadySeen = localStorage.getItem(seenKey) === today; } catch (e) {}

        var queue = cfg.popups.slice();
        var currentIdx = -1;

        function render(idx) {
            var p = queue[idx];
            art.setAttribute('data-src', p.src || '');
            // 尝试加载图片，加载成功就替换背景
            if (p.src) {
                var img = new Image();
                img.onload = function () {
                    art.style.backgroundImage = 'url("' + p.src + '")';
                    art.setAttribute('data-src', '');
                };
                img.onerror = function () {
                    // 保留 CSS 占位
                };
                img.src = p.src;
            }
            title.textContent = p.title || '';
            sub.textContent = p.subtitle || '';
            act.textContent = p.actionText || '\u5173\u95ed';
            // 按钮点击行为：若指定 link 就跳转，否则只关闭
            act.onclick = function (e) {
                e.preventDefault();
                if (p.link) {
                    window.open(p.link, '_blank', 'noopener,noreferrer');
                }
                closePopup();
            };
        }

        function openPopup(idx) {
            currentIdx = idx;
            render(idx);
            modal.hidden = false;
            modal.classList.remove('is-leaving');
            document.body.classList.add('popup-open');
            // 焦点落到关闭按钮，便于键盘 ESC
            var closeBtn = modal.querySelector('.popup-close');
            if (closeBtn) setTimeout(function () { closeBtn.focus(); }, 50);
        }

        function closePopup() {
            modal.classList.add('is-leaving');
            setTimeout(function () {
                modal.hidden = true;
                modal.classList.remove('is-leaving');
                document.body.classList.remove('popup-open');
                // 弹下一个
                if (currentIdx + 1 < queue.length) {
                    setTimeout(function () { openPopup(currentIdx + 1); }, 300);
                } else {
                    // 都弹完了，记今天已看过
                    try { localStorage.setItem(seenKey, today); } catch (e) {}
                }
            }, 200);
        }

        // 点击关闭：叉号 / 遮罩
        modal.addEventListener('click', function (e) {
            if (e.target.closest('[data-popup-close]')) {
                closePopup();
            }
        });

        // ESC 关闭
        document.addEventListener('keydown', function (e) {
            if (!modal.hidden && (e.key === 'Escape' || e.keyCode === 27)) {
                closePopup();
            }
        });

        // 启动
        if (cfg.debugAlwaysPopup || !alreadySeen) {
            // 等首屏稳定再弹，避免抢渲染
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', function () {
                    setTimeout(function () { openPopup(0); }, 400);
                });
            } else {
                setTimeout(function () { openPopup(0); }, 400);
            }
        }
    })();
    </script>

    <!-- ===== 整活夜：剧照轮播逻辑 ===== -->
    <script>
    (function () {
        var cfg = window.ZHENGHUO_CONFIG;
        if (!cfg || !cfg.photos || !cfg.photos.length) return;

        var strip = document.getElementById('photoStrip');
        var art   = document.getElementById('photoArt');
        var link  = document.getElementById('photoLink');
        var badge = document.getElementById('photoBadge');
        var prev  = document.getElementById('photoPrev');
        var next  = document.getElementById('photoNext');
        var dots  = document.getElementById('photoDots');
        if (!strip || !art || !link || !badge || !prev || !next || !dots) return;

        var idx = 0;
        var total = cfg.photos.length;
        var dotEls = dots.querySelectorAll('.dot');

        function applyPhoto(i, animate) {
            var p = cfg.photos[i];
            if (!p) return;
            if (animate) {
                art.classList.add('is-fading');
                setTimeout(function () {
                    setPhoto(p);
                    art.classList.remove('is-fading');
                }, 200);
            } else {
                setPhoto(p);
            }
            // 同步 dots
            for (var k = 0; k < dotEls.length; k++) {
                var on = (k === i);
                dotEls[k].classList.toggle('active', on);
                dotEls[k].setAttribute('aria-selected', on ? 'true' : 'false');
            }
            idx = i;
        }

        function setPhoto(p) {
            art.setAttribute('data-src', p.src || '');
            if (p.src) {
                var img = new Image();
                img.onload = function () {
                    art.style.backgroundImage = 'url("' + p.src + '")';
                    art.setAttribute('data-src', '');
                };
                img.src = p.src;
            }
            if (p.link) {
                link.href = p.link;
                link.setAttribute('aria-label', '\u67e5\u770b\u539f\u89c6\u9891\uff1a' + (p.badge || ''));
            }
            badge.textContent = p.badge || '';
        }

        prev.addEventListener('click', function () {
            applyPhoto((idx - 1 + total) % total, true);
        });
        next.addEventListener('click', function () {
            applyPhoto((idx + 1) % total, true);
        });

        // dots 点击
        for (var j = 0; j < dotEls.length; j++) {
            (function (k) {
                dotEls[k].addEventListener('click', function () {
                    applyPhoto(k, true);
                });
            })(j);
        }

        // 键盘左右
        strip.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft')  { applyPhoto((idx - 1 + total) % total, true); }
            if (e.key === 'ArrowRight') { applyPhoto((idx + 1) % total, true); }
        });
        strip.tabIndex = 0;

        // 触摸滑动
        var touchStartX = 0, touchStartY = 0, touchActive = false;
        strip.addEventListener('touchstart', function (e) {
            var t = e.touches[0];
            touchStartX = t.clientX;
            touchStartY = t.clientY;
            touchActive = true;
        }, { passive: true });
        strip.addEventListener('touchend', function (e) {
            if (!touchActive) return;
            touchActive = false;
            var t = e.changedTouches[0];
            var dx = t.clientX - touchStartX;
            var dy = t.clientY - touchStartY;
            // 横向滑动距离 > 50 且大于纵向 → 视为切换
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
                if (dx < 0) applyPhoto((idx + 1) % total, true);
                else        applyPhoto((idx - 1 + total) % total, true);
            }
        }, { passive: true });

        // 初始化：加载第一张
        applyPhoto(0, false);
    })();
    </script>
'''

with open(p, 'rb') as f:
    data = f.read()

# CRLF → LF
text = data.decode('utf-8').replace('\r\n', '\n')

marker = '</body>'
idx = text.rfind(marker)
assert idx != -1, 'no </body>'

text = text[:idx] + JS_BLOCK + '\n' + text[idx:]

final = text.replace('\n', '\r\n').encode('utf-8')
with open(p, 'wb') as f:
    f.write(final)

crlf_count = final.count(b'\r\n')
print(f'JS injected at char {idx}')
print(f'New file: {len(final)} bytes, CRLF: {crlf_count}')