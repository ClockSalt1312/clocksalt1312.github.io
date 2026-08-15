# -*- coding: utf-8 -*-
"""Fix CSS unicode escapes: \\uXXXX literal → real Chinese chars"""
p = r'D:\pentaig\整活2\预览\index.html'
with open(p, 'rb') as f:
    data = f.read()

text = data.decode('utf-8').replace('\r\n', '\n')

# Replace literal \uXXXX (in CSS) with actual Chinese chars
# Only do it INSIDE CSS (between </style> and </style>) — but easier: it's safe to replace globally,
# because JS uses unicode escapes too, but only inside JS string literals which we want to keep.
# Better: limit replacement to lines that are CSS selectors (start with .popup-art[data-src=" etc.)

import re

def replace_unicode_in_css(m):
    line = m.group(0)
    # Decode \uXXXX sequences
    def repl(u):
        return chr(int(u.group(1), 16))
    return re.sub(r'\\u([0-9a-fA-F]{4})', repl, line)

# Lines containing popup-art[ or photo-art[ with data-src attribute selectors
text = re.sub(
    r'^.*\.(popup-art|photo-art)\[data-src="\\u[0-9a-fA-F]+(/[0-9a-fA-F]+)+"\][^{]*\{[^}]*\}.*$',
    replace_unicode_in_css, text, flags=re.M
)

final = text.replace('\n', '\r\n').encode('utf-8')
with open(p, 'wb') as f:
    f.write(final)

# Verify
import io
buf = io.StringIO(final.decode('utf-8'))
hits = []
for i, line in enumerate(buf, 1):
    if 'popup-art[data-src=' in line or 'photo-art[data-src=' in line:
        hits.append((i, line.rstrip()))
for h in hits:
    print(h)