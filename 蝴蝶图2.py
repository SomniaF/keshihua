# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# 字体定义（参考蝴蝶图.py）
f_title  = FontProperties(family='Microsoft YaHei', size=14, weight='bold')
f_sub    = FontProperties(family='Microsoft YaHei', size=10, weight='normal')
f_label  = FontProperties(family='Microsoft YaHei', size=11)
f_value  = FontProperties(family='Microsoft YaHei', size=9)
f_note   = FontProperties(family='Microsoft YaHei', size=9)
f_legend = FontProperties(family='Microsoft YaHei', size=10)

# 数据（按2022年降序，配合 invert_yaxis 使最大值在顶部）
regions   = ['华东', '西北', '东北', '华北', '华南']
data_2022 = [36, 31, 18, 13, 9]
data_2021 = [42, 26, 19, 12, 5]

# 条形长度比例：42% 对应条形长度 17.25
scale = 17.25 / 42.0
len_2022 = [v * scale for v in data_2022]
len_2021 = [v * scale for v in data_2021]

# 尺寸 14.68cm x 10.47cm（参考蝴蝶图.py）
fig_w = 14.68 / 2.54
fig_h = 10.47 / 2.54
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)

# 颜色（参考蝴蝶图.py）
bg_color    = '#1A1F3A'
text_color  = '#FFFFFF'
sub_color   = '#EEF0F8'   # 副标题/数值：白但略暗于标题
color_2022  = '#0070C0'   # 2022 标准蓝
color_2021  = '#E85D75'   # 2021 红色

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# 蝴蝶图：左侧2022（向左延伸），右侧2021（向右延伸）
bar_h = 0.5
y_step = bar_h * 2.0
y_pos = np.arange(len(regions)) * y_step
max_val = max(max(len_2022), max(len_2021))

# 计算 1cm 对应的数据单位，中间留 2cm 空间放区域名称（每侧 1cm）
ax_w_inch = (0.97 - 0.08) * fig_w
ax_w_cm = ax_w_inch * 2.54
# xlim 总跨度按 (中心半宽 + 最大条长) * 2 * 1.18 估算
center_half_cm = 1.0
# 先用近似值算 cm_in_data，再迭代一次
total_span = (center_half_cm + max_val) * 2 * 1.18
cm_in_data = total_span / ax_w_cm
center_half = cm_in_data * center_half_cm

# 坐标轴设置（整体含数值标签左右居中）
outer_pad = max_val * 0.02
left_align_x = -(center_half + len_2022[0]) - outer_pad
right_align_x = (center_half + len_2021[0]) + outer_pad
mid = (left_align_x + right_align_x) / 2
span = (center_half + max_val) * 1.18
ax.set_ylim(-0.9, y_pos[-1] + 0.7)
ax.set_xlim(mid - span, mid + span)
ax.invert_yaxis()

# 左侧条形（2022）：从 -(center_half+len) 到 -center_half，可见长度 = len
ax.barh(y_pos, len_2022, left=[-(center_half + v) for v in len_2022],
        height=bar_h, color=color_2022, edgecolor='none', zorder=3,
        align='center')
# 右侧条形（2021）：从 center_half 到 center_half+len，可见长度 = len
ax.barh(y_pos, len_2021, left=center_half,
        height=bar_h, color=color_2021, edgecolor='none', zorder=3,
        align='center')

# 条形竖条纹纹理（按 REPT("|", 值*200) 计算竖线数量：百分比*2，等距排列）
stripe_color = (0, 0, 0, 0.3)
for y, v22, v21, l22, l21 in zip(y_pos, data_2022, data_2021, len_2022, len_2021):
    yb = y - bar_h / 2
    yt = y + bar_h / 2
    n22 = round(v22 * 2)
    if n22 > 0:
        step22 = l22 / n22
        xs = -(center_half + l22) + np.arange(n22) * step22
        ax.vlines(xs, yb, yt, colors=stripe_color, linewidth=0.5, zorder=4)
    n21 = round(v21 * 2)
    if n21 > 0:
        step21 = l21 / n21
        xs = center_half + np.arange(n21) * step21
        ax.vlines(xs, yb, yt, colors=stripe_color, linewidth=0.5, zorder=4)

# 数值写在条形外侧，左侧统一对齐到36%位置，右侧统一对齐到42%位置

for y, v22, v21 in zip(y_pos, data_2022, data_2021):
    ax.text(left_align_x, y, f'{v22}%', ha='right', va='center',
            fontproperties=f_value, color=sub_color, zorder=8)
    ax.text(right_align_x, y, f'{v21}%', ha='left', va='center',
            fontproperties=f_value, color=sub_color, zorder=8)

# 中间区域名称
for y, name in zip(y_pos, regions):
    ax.text(0, y, name, ha='center', va='center',
            fontproperties=f_label, color=text_color, zorder=9,
            bbox=dict(facecolor=bg_color, edgecolor='none', pad=3))

# 隐藏所有轴线和刻度
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(length=0)


# 主标题
fig.text(0.05, 0.94, '2022年第一季度销售目标完成情况',
         ha='left', va='top', fontproperties=f_title, color=text_color)
# 副标题
fig.text(0.05, 0.86, '华东区域完成率最高达到36%，但是相比去年的42%有所下降',
         ha='left', va='top', fontproperties=f_sub, color=sub_color)

# 底部脚注
fig.text(0.05, 0.035, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         ha='left', va='bottom', fontproperties=f_note, color=text_color)

plt.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.12)
plt.savefig('蝴蝶图2.png', facecolor=bg_color, dpi=150)
print('saved 蝴蝶图2.png')
