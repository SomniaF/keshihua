# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 字体定义
f_title  = FontProperties(family='Microsoft YaHei', size=18, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=11, weight='normal')
f_region = FontProperties(family='Microsoft YaHei', size=10, weight='normal')
f_value  = FontProperties(family='Microsoft YaHei', size=9, weight='normal')
f_note   = FontProperties(family='Microsoft YaHei', size=9)

# 数据（按图片从上到下顺序）
regions = ['华东', '西南', '西北', '东北', '华南', '华北']
sales   = [2109, 1369, 1872, 1536, 1946, 4321]   # 销量（深蓝段）
fill    = [2212, 2952, 2449, 2785, 2375, 0]       # 占位1（浅蓝段，补齐到统一长度）
yoy     = [-5.8, -17.9, -15.9, -9.3, -20.8, -13.6]  # 同比去年
bar_w   = 1080                                    # 占位2（红色同比条统一长度）

# 颜色
bg_color    = '#1A1F3C'
sales_color = '#0D3B7A'   # 销量条 深蓝
fill_color  = '#7BA3D1'   # 延伸条 浅蓝
yoy_color   = '#A04050'   # 同比条 暗红
text_color  = '#FFFFFF'
sub_color   = '#A0A8C0'

# 画布
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

n = len(regions)
# 反转 y 使华东在最上面
y_pos = [n - 1 - i for i in range(n)]
height = 0.62

# 三段堆叠：深蓝(销量) + 浅蓝(占位1) + 红色(同比)
ax.barh(y_pos, sales, height=height, color=sales_color, edgecolor='none', zorder=3)
ax.barh(y_pos, fill, left=sales, height=height, color=fill_color, edgecolor='none', zorder=3)
start_yoy = [s + f for s, f in zip(sales, fill)]
ax.barh(y_pos, [bar_w] * n, left=start_yoy, height=height, color=yoy_color, edgecolor='none', zorder=3)

# 销量数值（深蓝条内右对齐）
for y, s in zip(y_pos, sales):
    ax.text(s - 60, y, f'{s}', ha='right', va='center',
            fontproperties=f_value, color=text_color, zorder=8)

# 同比数值（红色条内居中）
for i, (y, yv) in enumerate(zip(y_pos, yoy)):
    x_center = start_yoy[i] + bar_w / 2
    ax.text(x_center, y, f'{yv}%', ha='center', va='center',
            fontproperties=f_value, color=text_color, zorder=8)

# 区域名称（左侧）
label_x = -220
for y, r in zip(y_pos, regions):
    ax.text(label_x, y, r, ha='right', va='center',
            fontproperties=f_region, color=text_color)

# 坐标范围
ax.set_xlim(label_x - 80, max(start_yoy) + bar_w + 150)
ax.set_ylim(-0.8, n - 0.2)
ax.axis('off')

# 主标题 / 副标题（左上）
fig.text(0.05, 0.94, '2021年各区域销量及同比情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
fig.text(0.05, 0.85, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%',
         ha='left', va='top', fontproperties=f_sub, color=text_color)

# 底部脚注
fig.text(0.05, 0.06, '*注：数据来源于公司销售系统，统计日期截至2022.01.01',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.10, right=0.97, top=0.80, bottom=0.12)
plt.savefig('数值.png', facecolor=bg_color, dpi=150)
print('saved 数值.png')