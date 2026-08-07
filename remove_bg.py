from PIL import Image, ImageFilter
def remove_white_bg_with_defringe(img_path, threshold=250, feather=15):
    # 1. 打开并转换RGBA
    img = Image.open(img_path).convert("RGBA")
    datas = img.getdata()
    new_data = []
    # 2. 阈值+羽化：去掉背景白
    for r, g, b, a in datas:
        dist = ((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2) ** 0.5
        if dist < threshold:
            new_data.append((r, g, b, 0))
        elif dist < threshold + feather:
            alpha = int((dist - threshold) / feather * 255)
            alpha = min(alpha, a)
            new_data.append((r, g, b, alpha))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    # 3. 关键：对Alpha通道做最小值滤波（3x3），让透明区域“侵蚀”白边
    r, g, b, a = img.split()
    a = a.filter(ImageFilter.MinFilter(3))  # 用3x3最小值滤波器
    img = Image.merge("RGBA", (r, g, b, a))
    # 4. 保存结果
    img.save("logo_final.png")
    print("完成喵~ 生成 logo_final.png，白边已被清除！")
# 改成你的图片名
remove_white_bg_with_defringe("幻象集团招聘.png", threshold=250, feather=15)