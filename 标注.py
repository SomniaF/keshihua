# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import numpy as np

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=13, weight='normal')
f_xlabel = FontProperties(family='Microsoft YaHei', size=10)     # 横轴(中文)
f_ylabel = FontProperties(family='Calibri', size=10)             # 纵轴(数字)
f_note   = FontProperties(family='Microsoft YaHei', size=9)      # 脚注

# 数据
goods  = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
values = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]

# 各柱独立配色（浅蓝、青绿、橙红、明黄、天蓝、深蓝、紫蓝、紫色）
bar_colors = ['#85C1E9', '#5AB9A6', '#E67E22', '#F4D03F',
              '#3498DB', '#1758A8', '#3A5FCC', '#4338CA']

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color   = '#1A1F3A'   # 深蓝背景
text_color = '#FFFFFF'   # 白色文字
grid_color = '#6A71A8'   # 网格线颜色

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 柱宽与间距（间隙宽度 100% => 柱宽 = 1/(1+1)）
bar_w = 1 / (1 + 1)
x_pos = np.arange(len(goods))

# 纯色柱形
bars = ax.bar(x_pos, values, width=bar_w, color=bar_colors,
              edgecolor='none', zorder=3)

# 柱顶带尖角气泡标签（气泡与柱子对齐，尖角斜向左/右指向柱顶中心）
box_w = 0.44      # 气泡框宽
box_h = 750       # 气泡框高
gap   = 350       # 气泡底部到柱顶的距离
tip_w = 0.05      # 尖角根部半宽
tip_shift = box_w / 5.5   # 尖角根部相对柱中心的偏移量
for i, (x, v, c) in enumerate(zip(x_pos, values, bar_colors)):
    bottom = v + gap          # 气泡底部y
    top    = bottom + box_h   # 气泡顶部y
    left  = x - box_w / 2
    right = x + box_w / 2
    # 偶数柱尖角根部偏右(尖端斜向左下)，奇数柱根部偏左(尖端斜向右下)
    shift = tip_shift if i % 2 == 0 else -tip_shift
    # 多边形：左上→右上→右下→尖角右根→尖角尖端(柱顶中心)→尖角左根→左下
    poly_x = [left, right, right,
              x + shift + tip_w, x, x + shift - tip_w, left]
    poly_y = [top, top, bottom,
              bottom, v, bottom, bottom]
    ax.fill(poly_x, poly_y, color=c, zorder=7, edgecolor='none')
    # 数值写在气泡框中央
    ax.text(x, bottom + box_h / 2, f'{v}', ha='center', va='center',
            fontsize=7.5, color=text_color, zorder=8)

# 横轴商品名称
ax.set_xticks(x_pos)
ax.set_xticklabels(goods, fontproperties=f_xlabel, color=text_color)

# 纵轴设置
ax.set_ylim(0, 11000)
ax.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
ax.set_yticklabels([])
ax.tick_params(axis='y', length=0, pad=6, labelleft=False)
ax.set_xlim(-0.5, len(goods) - 0.5)

# 纵轴刻度标签
for y_val, lbl in zip([0, 2000, 4000, 6000, 8000, 10000],
                      ['0', '2000', '4000', '6000', '8000', '10000']):
    ax.text(-0.04, y_val, lbl, transform=ax.get_yaxis_transform(),
            ha='right', va='center', fontproperties=f_ylabel,
            color=text_color, zorder=10, clip_on=False)

# 虚线网格
ax.xaxis.grid(False)
for y in [2000, 4000, 6000, 8000, 10000]:
    ax.axhline(y=y, linestyle='--', linewidth=0.6, color=grid_color,
               alpha=0.9, zorder=2)
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
fig.text(0.05, 0.94, '2021年商品销量情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题
fig.text(0.05, 0.86, '口红销量最好达9221，是眼影最低值2645近3.5倍',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.74, bottom=0.18)
plt.savefig('标注.png', facecolor=bg_color, dpi=150)
print('saved 标注.png')
