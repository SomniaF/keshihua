# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, PathPatch, Circle, Rectangle
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path
import numpy as np


def top_rounded_path(x, y, w, h, r):
    """只有顶部圆角的矩形路径（三次贝塞尔精确圆弧）"""
    k = 0.5523 * r
    vertices = [
        (x, y),
        (x + w, y),
        (x + w, y + h - r),
        (x + w, y + h - r + k),
        (x + w - r + k, y + h),
        (x + w - r, y + h),
        (x + r, y + h),
        (x + r - k, y + h),
        (x, y + h - r + k),
        (x, y + h - r),
        (x, y),
    ]
    codes = [
        Path.MOVETO, Path.LINETO, Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY,
    ]
    return Path(vertices, codes)

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)             # 数据标签(数字)
f_xlabel = FontProperties(family='Microsoft YaHei', size=10)     # 横轴(中文)
f_ylabel = FontProperties(family='Calibri', size=10)             # 纵轴(数字)
f_note   = FontProperties(family='Microsoft YaHei', size=9)      # 脚注

# 数据
goods  = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
values = [653, 523, 648, 856, 714, 785]

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color   = '#1A1F3A'   # 深蓝背景
bar_color  = '#2E86DE'   # 亮蓝色柱体
text_color = '#FFFFFF'   # 白色文字
grid_color = '#6A71A8'   # 网格线颜色

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 柱宽与间距（间隙宽度 500% => 柱宽 = 1/(1+5)）
bar_w = 1 / (1 + 5)
x_pos = np.arange(len(goods))

# 柱形 + 渐变（仅顶端圆角，底部直角）— 用 numpy 直接生成圆角渐变图
radius_ratio = 0.25  # 圆角半径占柱宽比例，微凸
for x, v in zip(x_pos, values):
    img_w = 120
    img_h = max(int(v * 0.5), 50)
    r_px = int(img_w * radius_ratio)
    grad = np.zeros((img_h, img_w, 4), dtype=np.uint8)
    for i in range(img_h):
        t = i / max(img_h - 1, 1)  # 0=顶部, 1=底部
        if t < 0.3:
            r_c, g_c, b_c = 46, 238, 219       # 青绿
        else:
            tt = (t - 0.3) / 0.7
            r_c = int(46 + (26 - 46) * tt)
            g_c = int(238 + (138 - 238) * tt)
            b_c = int(219 + (232 - 219) * tt)
        grad[i, :, 0] = r_c
        grad[i, :, 1] = g_c
        grad[i, :, 2] = b_c
        grad[i, :, 3] = 255
    # 顶部圆角（数组开头 = 顶部，origin='upper'）
    for i in range(r_px):
        for j in range(img_w):
            if j < r_px:
                if (j - r_px) ** 2 + (i - r_px) ** 2 > r_px * r_px:
                    grad[i, j, 3] = 0
            elif j > img_w - r_px:
                if (j - (img_w - r_px)) ** 2 + (i - r_px) ** 2 > r_px * r_px:
                    grad[i, j, 3] = 0
    ax.imshow(grad, extent=[x - bar_w / 2, x + bar_w / 2, 0, v],
              aspect='auto', zorder=3, origin='upper')

# 柱顶竖线 + 蓝色方框（内含圆点 + 数值标签）
# 0.49cm 竖线：figure高10.47cm, axes高0.56*10.47=5.86cm, ylim=1200 => 1cm≈204.8数据单位
line_height = 50  # 方框往下，更靠近柱顶
box_w = 0.44       # 方框宽
box_h = 85         # 方框高
label_bg = '#1C2E66'  # 深蓝方框（微亮）
dot_color = '#2563EB'  # 亮蓝圆点

for x, v in zip(x_pos, values):
    # 蓝色方框：左侧靠近圆点左侧，不居中
    box_x = x - 0.04
    box_y = v + line_height
    ax.fill([box_x, box_x + box_w, box_x + box_w, box_x],
            [box_y, box_y, box_y + box_h, box_y + box_h],
            color=label_bg, zorder=6)
    # 圆点在方框垂直中央，与竖线连接
    dot_y = box_y + box_h / 2
    ax.plot(x, dot_y, 'o', markersize=5, color=dot_color, zorder=7)
    # 竖线：柱顶到圆点位置，zorder高于方框使其不被遮挡
    ax.plot([x, x], [v, dot_y], color=dot_color,
            linewidth=0.8, zorder=6.5)
    # 方框内竖线段加亮，确保穿过方框时清晰可见
    ax.plot([x, x], [box_y, dot_y], color='#4F8EF7',
            linewidth=1.2, zorder=6.6)
    # 数值文字（圆点右侧，方框中央）
    ax.text(x + 0.08, dot_y, f'{v}', ha='left', va='center',
            fontsize=7.5, color='#C0C8D8', zorder=8)

# 横轴商品名称
ax.set_xticks(x_pos)
ax.set_xticklabels(goods, fontproperties=f_xlabel, color=text_color)

# 纵轴设置
ax.set_ylim(0, 1200)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.set_yticklabels([])
ax.tick_params(axis='y', length=0, pad=6, labelleft=False)
ax.set_xlim(-0.5, len(goods) - 0.5)

# 纵轴刻度标签
for y_val, lbl in zip([0, 200, 400, 600, 800, 1000, 1200], ['0', '200', '400', '600', '800', '1000', '1200']):
    ax.text(-0.04, y_val, lbl, transform=ax.get_yaxis_transform(),
            ha='right', va='center', fontproperties=f_ylabel,
            color=text_color, zorder=10, clip_on=False)

# 虚线网格
ax.xaxis.grid(False)
for y in [200, 400, 600, 800, 1000, 1200]:
    ax.axhline(y=y, linestyle='--', linewidth=0.6, color=grid_color,
               alpha=0.9, zorder=2)
from matplotlib.lines import Line2D
fig.lines.append(Line2D([0.13, 0.97], [0.18, 0.18],
                        transform=fig.transFigure, linestyle='--',
                        linewidth=0.6, color=grid_color, alpha=0.9, zorder=6))


# 轴线：全部隐藏
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=8)

# 主标题
fig.text(0.05, 0.94, '3月商品销量对比',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题
fig.text(0.05, 0.86, '防晒销量最多，3月销量856；面膜最少，3月销量523',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.74, bottom=0.18)
plt.savefig('圆角.png', facecolor=bg_color, dpi=150)
print('saved 圆角.png')