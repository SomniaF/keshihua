# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=20, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=14, weight='normal')
f_dlabel = FontProperties(family='Calibri', size=10)             # 数据标签(数字)
f_xlabel = FontProperties(family='Microsoft YaHei', size=9)      # 横轴(中文)
f_ylabel = FontProperties(family='Calibri', size=10)             # 纵轴(数字)
f_note   = FontProperties(family='Microsoft YaHei', size=9)      # 脚注

# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
values  = [2354, 1902, 3524, 2698, 2896, 2563]

# 尺寸 14.68cm x 10.47cm
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色
bg_color   = '#1A1F3A'   # 深蓝背景
text_color = '#FFFFFF'   # 白色文字
grid_color = '#6A71A8'   # 网格线颜色（调亮）

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 间隙宽度219% => 柱宽 = 1/(1+2.19)
bar_w = 1 / (1 + 2.19)

# 柱状图 - 使用渐变蓝色
x_pos = list(range(len(regions)))
bars = ax.bar(x_pos, values, width=bar_w, zorder=3)

# 为每个柱体创建垂直渐变效果（上深下浅：底部浅蓝 → 顶部标准蓝）
for bar in bars:
    bar.set_facecolor('none')
    x = bar.get_x()
    w = bar.get_width()
    h = bar.get_height()
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    cmap_grad = LinearSegmentedColormap.from_list('blue_grad',
                                                   ['#5BB5FF', '#0070C0'])
    ax.imshow(gradient, extent=[x, x + w, 0, h], aspect='auto',
              cmap=cmap_grad, zorder=3, alpha=1.0, origin='lower')

# 数据标签（柱顶，白色）
for x, v in zip(x_pos, values):
    ax.text(x, v + 70, f'{v}', ha='center', va='bottom',
            fontproperties=f_dlabel, color=text_color, zorder=5)

# 横轴区域名称（微软雅黑，白色）
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontproperties=f_xlabel, color=text_color)

# 纵轴设置
ax.set_ylim(0, 4000)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels([])
ax.tick_params(axis='y', length=0, pad=6, labelleft=False)
ax.set_xlim(-0.5, len(regions) - 0.5)

# 纵轴刻度标签（置于 axes 左侧，靠近虚线）
for y_val, lbl in zip([0, 1000, 2000, 3000, 4000], ['0', '1000', '2000', '3000', '4000']):
    ax.text(-0.04, y_val, lbl, transform=ax.get_yaxis_transform(),
            ha='right', va='center', fontproperties=f_ylabel,
            color=text_color, zorder=10, clip_on=False)

# 虚线网格（每 1000 一条，zorder 高于柱子）
ax.xaxis.grid(False)
for y in [1000, 2000, 3000, 4000]:
    ax.axhline(y=y, linestyle='--', linewidth=0.6, color=grid_color,
               alpha=0.9, zorder=6)
# y=0 虚线：在 figure 层面绘制，避开 axes 边界渲染异常
fig.lines.append(Line2D([0.13, 0.97], [0.18, 0.18],
                        transform=fig.transFigure, linestyle='--',
                        linewidth=0.6, color=grid_color, alpha=0.9, zorder=6))

# 轴线：全部隐藏
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0, pad=6)

# 主标题（左对齐，加粗，白色）
fig.text(0.05, 0.94, '3 月各区域销量分布',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题（不加粗，白色，与标题左对齐，距离增大）
fig.text(0.05, 0.86, '东北销量最多占比总销量的 22%，华南销量最低',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注（白色，与标题左对齐）
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至 2022.03.31',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.13, right=0.97, top=0.74, bottom=0.18)
plt.savefig('渐变2.png', facecolor=bg_color, dpi=150)
print('saved 渐变2.png')