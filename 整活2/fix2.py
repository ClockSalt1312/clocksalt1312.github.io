# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

p = r'D:\pentaig\整活2\预览\index.html'
with open(p, 'rb') as f:
    data = f.read()

text = data.decode('utf-8').replace('\r\n', '\n')

needle = '\\u6750\\u6599'
replacement = '材料'
before = text.count(needle)
text = text.replace(needle, replacement)
after_count = text.count(replacement)

print('before count =', before)
print('after count =', after_count)

final = text.replace('\n', '\r\n').encode('utf-8')
with open(p, 'wb') as f:
    f.write(final)

print('file size:', len(final))