#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_all_diagrams.py
────────────────────────────────────────────────────────────────────────────
สร้างสื่อประกอบเฉลยข้อสอบ MUX/DMUX ข้อที่ 1 (รูปที่ 3.40)
วงจรมัลติเพล็กเซอร์ 74151 — หารูปคลื่นเอาต์พุต Y และ W

ข้อมูลรูปคลื่นทั้งหมดสกัดจากต้นฉบับด้วยการวิเคราะห์พิกเซล และตรวจไขว้
ระหว่างภาพสแกน (example01.jpeg) กับต้นฉบับ vector (305241_lecture.pdf หน้า 110)
ผลตรงกันทุกบิต — ดูรายละเอียดใน VERIFICATION.md

รันด้วย:  python3 generate_all_diagrams.py
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrow, Polygon
from matplotlib.lines import Line2D
from matplotlib import font_manager

# ═══════════════════════════════════════════════════════════════════════════
# ตั้งค่าฟอนต์ไทย
# ═══════════════════════════════════════════════════════════════════════════
_avail = {f.name for f in font_manager.fontManager.ttflist}
for _cand in ['Arial Unicode MS', 'Thonburi', 'Tahoma', 'Sarabun', 'Noto Sans Thai', 'IBM Plex Thai', 'Ayuthaya']:
    if _cand in _avail:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [_cand, 'DejaVu Sans', 'Arial']
        THAI_FONT = _cand
        break
else:
    THAI_FONT = plt.rcParams['font.family']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'dejavusans'
print(f"[font] ใช้ฟอนต์: {THAI_FONT}")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(OUT, exist_ok=True)
DPI = 300

# ═══════════════════════════════════════════════════════════════════════════
# จานสี
# ═══════════════════════════════════════════════════════════════════════════
C_BG      = '#FFFFFF'
C_INK     = '#1A1A1A'
C_GRID    = '#D5D9E0'
C_SLOT    = '#94A3B8'
C_SEL     = '#2563EB'   # สัญญาณเลือก A,B,C
C_EN      = '#DC2626'   # อีนาเบิล E
C_DATA    = '#7C3AED'   # ข้อมูล D0, D2
C_Y       = '#059669'   # เอาต์พุต Y
C_W       = '#EA580C'   # เอาต์พุต W
C_DIS     = '#FEE2E2'   # แถบช่วงดิสเอเบิล
C_BOX     = '#F1F5F9'
C_HI      = '#FEF3C7'
C_ONE     = '#DC2626'
C_ZERO    = '#0F172A'

# ═══════════════════════════════════════════════════════════════════════════
# ข้อมูล GROUND TRUTH — run ของสัญญาณ (value, x_start, x_end) พิกเซล @400 DPI
# ═══════════════════════════════════════════════════════════════════════════
RUNS = {
    'A':  [(0, 906, 1142), (1, 1143, 1342), (0, 1343, 1546), (1, 1547, 1742),
           (0, 1743, 1942), (1, 1943, 2142), (0, 2143, 2343), (1, 2344, 2545),
           (0, 2546, 2681)],
    'B':  [(0, 906, 1342), (1, 1343, 1742), (0, 1743, 2142), (1, 2143, 2545),
           (0, 2546, 2681)],
    'C':  [(0, 906, 1742), (1, 1743, 2545), (0, 2546, 2681)],
    'E':  [(1, 906, 1219), (0, 1220, 2604), (1, 2605, 2681)],
    'D0': [(0, 906, 1096), (1, 1097, 1219), (0, 1220, 1342), (1, 1343, 1465),
           (0, 1466, 1588), (1, 1589, 1711), (0, 1712, 1835), (1, 1836, 1958),
           (0, 1959, 2081), (1, 2082, 2204), (0, 2205, 2327), (1, 2328, 2450),
           (0, 2451, 2574), (1, 2575, 2681)],
    'D2': [(1, 906, 1219), (0, 1220, 1465), (1, 1466, 1711), (0, 1712, 1958),
           (1, 1959, 2204), (0, 2205, 2450), (1, 2451, 2681)],
}
X0, X1 = 906, 2681
SLOT_EDGES = [906, 1143, 1343, 1547, 1743, 1943, 2143, 2344, 2546, 2682]
NSLOT = 9


def val(sig, x):
    for v, s, e in RUNS[sig]:
        if s <= x <= e:
            return v
    raise ValueError(f"{sig} @ {x}")


# แผนที่ช่องสัญญาณจากการต่อวงจรในรูปที่ 3.40
CH_SRC = {
    0: ('D0',  '$D_0$',              lambda x: val('D0', x)),
    1: ('+5V', '+5 V $\\Rightarrow 1$', lambda x: 1),
    2: ('D2',  '$D_2$',              lambda x: val('D2', x)),
    3: ('GND', 'GND $\\Rightarrow 0$',  lambda x: 0),
    4: ('~D0', '$\\overline{D_0}$',  lambda x: 1 - val('D0', x)),
    5: ('GND', 'GND $\\Rightarrow 0$',  lambda x: 0),
    6: ('~D2', '$\\overline{D_2}$',  lambda x: 1 - val('D2', x)),
    7: ('+5V', '+5 V $\\Rightarrow 1$', lambda x: 1),
}


def sel_code(x):
    a, b, c = val('A', x), val('B', x), val('C', x)
    return c, b, a, 4 * c + 2 * b + a


def Yf(x):
    if val('E', x) == 1:        # G-bar = H  →  ดิสเอเบิล  →  Y = L
        return 0
    return CH_SRC[sel_code(x)[3]][2](x)


def Wf(x):
    return 1 - Yf(x)


def to_runs(fn, x0=X0, x1=X1):
    out, cur, st = [], None, None
    for x in range(x0, x1 + 1):
        v = fn(x)
        if v != cur:
            if cur is not None:
                out.append((cur, st, x - 1))
            cur, st = v, x
    out.append((cur, st, x1))
    return out


Y_RUNS = to_runs(Yf)
W_RUNS = to_runs(Wf)

# ═══════════════════════════════════════════════════════════════════════════
# ตัวช่วยวาดรูปคลื่น
# ═══════════════════════════════════════════════════════════════════════════

def draw_wave(ax, runs, ybase, h, color, lw=2.6, ls='-'):
    """วาดรูปคลื่นดิจิทัลจาก run list ให้มีขอบตั้งฉากสมบูรณ์"""
    xs, ys, prev = [], [], None
    for v, s, e in runs:
        yv = ybase + (h if v else 0)
        if prev is not None:
            xs.append(s); ys.append(prev)
        xs.append(s); ys.append(yv)
        xs.append(e + 1); ys.append(yv)
        prev = yv
    ax.plot(xs, ys, color=color, lw=lw, ls=ls,
            solid_joinstyle='miter', solid_capstyle='butt',
            clip_on=False, zorder=5)


def slot_grid(ax, ytop, ybot, show_labels=True, label_y=None, fs=11):
    """เส้นแบ่งช่วงเวลา + หมายเลขช่วง"""
    for xe in SLOT_EDGES[1:-1]:
        ax.plot([xe, xe], [ybot, ytop], color=C_SLOT, lw=1.0,
                ls=(0, (4, 3)), zorder=1, clip_on=False)
    ax.plot([X0, X0], [ybot, ytop], color=C_SLOT, lw=1.0, ls=(0, (4, 3)),
            zorder=1, clip_on=False)
    ax.plot([X1 + 1, X1 + 1], [ybot, ytop], color=C_SLOT, lw=1.0,
            ls=(0, (4, 3)), zorder=1, clip_on=False)
    if show_labels:
        ly = ytop if label_y is None else label_y
        for i in range(NSLOT):
            xc = (SLOT_EDGES[i] + SLOT_EDGES[i + 1]) / 2
            c, b, a, n = sel_code(SLOT_EDGES[i])
            ax.text(xc, ly, f"{i+1}", ha='center', va='bottom',
                    fontsize=fs, color=C_INK, fontweight='bold', clip_on=False)


def disable_bands(ax, ybot, ytop, alpha=1.0):
    """แถบพื้นหลังแสดงช่วงที่ไอซีถูกดิสเอเบิล (E = 1)"""
    for v, s, e in RUNS['E']:
        if v == 1:
            ax.add_patch(Rectangle((s, ybot), e + 1 - s, ytop - ybot,
                                   facecolor=C_DIS, edgecolor='none',
                                   zorder=0, alpha=alpha, clip_on=False))


def wave_label(ax, x, y, text, color, fs=15):
    ax.text(x, y, text, ha='right', va='center', fontsize=fs,
            color=color, fontweight='bold', clip_on=False)


def finish(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, facecolor=C_BG, bbox_inches='tight', pad_inches=0.28)
    plt.close(fig)
    kb = os.path.getsize(path) / 1024
    print(f"  ✓ {name}  ({kb:.0f} KB)")


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 1 — พื้นฐาน MUX: เปรียบเทียบกับสวิตช์เลือกช่อง
# ═══════════════════════════════════════════════════════════════════════════
def fig01_mux_concept():
    fig, ax = plt.subplots(figsize=(13.6, 8.2))
    ax.set_xlim(0, 13.6); ax.set_ylim(0, 8.2); ax.axis('off')

    ax.text(6.8, 7.80, 'มัลติเพล็กเซอร์ (Multiplexer) คืออะไร?',
            ha='center', fontsize=20, fontweight='bold', color=C_INK)
    ax.text(6.8, 7.32, 'สวิตช์เลือกข้อมูล — เลือกอินพุตหนึ่งช่องจาก $2^n$ ช่อง ให้ออกสู่เอาต์พุตเพียงช่องเดียว',
            ha='center', fontsize=12.5, color='#475569')

    # ───── ซ้าย: อุปมาสวิตช์หมุน ─────
    ax.text(3.15, 6.68, 'เปรียบเทียบ: สวิตช์หมุนเลือกช่อง',
            ha='center', fontsize=14, fontweight='bold', color=C_SEL)
    box = Rectangle((1.25, 1.80), 3.8, 4.45, facecolor=C_BOX,
                    edgecolor=C_INK, lw=2.0, zorder=1)
    ax.add_patch(box)

    # ขาอินพุต 8 ช่อง + หน้าสัมผัส
    cy_top, cy_bot = 5.78, 2.36
    contacts = []
    for i in range(8):
        y = cy_top - i * (cy_top - cy_bot) / 7
        ax.plot([0.52, 1.25], [y, y], color=C_INK, lw=1.7, zorder=2)
        ax.text(0.40, y, f'$D_{i}$', ha='right', va='center',
                fontsize=12.5, color=C_INK)
        cx = 2.26
        ax.plot([1.25, cx], [y, y], color=C_INK, lw=1.4, zorder=2)
        ax.add_patch(Circle((cx, y), 0.062, facecolor=C_INK,
                            edgecolor=C_INK, zorder=4))
        contacts.append((cx, y))

    ax.text(0.40, 6.22, 'อินพุตข้อมูล', ha='right', fontsize=11.5,
            color='#64748B', style='italic')

    # แกนหมุน + ก้านสวิตช์ชี้ไปช่อง D2
    piv = (3.72, 4.07)
    ax.add_patch(Circle(piv, 0.10, facecolor=C_INK, edgecolor=C_INK, zorder=6))
    tgt = contacts[2]
    ax.plot([piv[0], tgt[0]], [piv[1], tgt[1]], color=C_SEL, lw=3.4,
            zorder=5, solid_capstyle='round')
    ax.add_patch(Circle(tgt, 0.115, facecolor='none', edgecolor=C_SEL,
                        lw=2.4, zorder=6))
    ax.text(tgt[0] + 0.30, tgt[1] + 0.30, 'ก้านสวิตช์\nชี้ช่องที่เลือก',
            fontsize=10.5, color=C_SEL, fontweight='bold', va='bottom')

    # เอาต์พุต
    ax.plot([piv[0], 5.72], [piv[1], piv[1]], color=C_INK, lw=2.2, zorder=3)
    ax.text(5.84, piv[1], '$Y$', fontsize=15, fontweight='bold',
            color=C_Y, va='center')
    ax.text(5.84, piv[1] - 0.38, 'เอาต์พุต', fontsize=11,
            color='#64748B', va='center')

    # ขาเลือกอินพุต
    for k, lab in enumerate(['$S_2$', '$S_1$', '$S_0$']):
        x = 2.40 + k * 0.78
        ax.plot([x, x], [1.80, 1.12], color=C_SEL, lw=1.9, zorder=2)
        ax.text(x, 0.94, lab, ha='center', va='top', fontsize=12.5,
                color=C_SEL, fontweight='bold')
    ax.text(3.18, 0.52, 'ขาเลือกอินพุต (Select Lines)', ha='center',
            fontsize=11.5, color=C_SEL, style='italic')

    # ───── ขวา: ตารางความจริง 8:1 ─────
    ax.text(9.95, 6.68, 'ตารางเลือกช่องของ MUX ขนาด 8:1',
            ha='center', fontsize=14, fontweight='bold', color=C_INK)
    tx, ty, cw, rh = 7.75, 5.70, 0.86, 0.50
    heads = ['$S_2$', '$S_1$', '$S_0$', 'ช่องที่ถูกเลือก']
    widths = [cw, cw, cw, 1.72]
    xoff = [0]
    for w in widths[:-1]:
        xoff.append(xoff[-1] + w)

    # ส่วนหัวของตาราง
    for j, (hd, w) in enumerate(zip(heads, widths)):
        ax.add_patch(Rectangle((tx + xoff[j], ty), w, rh,
                               facecolor='#334155', edgecolor=C_INK, lw=1.4, zorder=2))
        ax.text(tx + xoff[j] + w / 2, ty + rh / 2, hd, ha='center', va='center',
                fontsize=12.5, color='white', fontweight='bold', zorder=3)

    for i in range(8):
        b = format(i, '03b')
        yy = ty - (i + 1) * rh
        hl = (i == 2)
        for j, w in enumerate(widths):
            fc = C_HI if hl else ('#FFFFFF' if i % 2 == 0 else '#F8FAFC')
            ax.add_patch(Rectangle((tx + xoff[j], yy), w, rh,
                                   facecolor=fc, edgecolor=C_GRID, lw=1.0, zorder=2))
        for j in range(3):
            ax.text(tx + xoff[j] + widths[j] / 2, yy + rh / 2, b[j],
                    ha='center', va='center', fontsize=12.5, zorder=3,
                    color=C_ONE if b[j] == '1' else C_ZERO,
                    fontweight='bold' if b[j] == '1' else 'normal')
        ax.text(tx + xoff[3] + widths[3] / 2, yy + rh / 2, f'$D_{i}$',
                ha='center', va='center', fontsize=13, zorder=3,
                color=C_SEL if hl else C_INK,
                fontweight='bold' if hl else 'normal')

    ax.text(9.95, ty - 8 * rh - 0.32,
            'แถวไฮไลต์: $S_2S_1S_0 = 010$ (ฐานสิบ = 2) → เลือกช่อง $D_2$',
            ha='center', fontsize=11.5, color=C_SEL, fontweight='bold')
    ax.text(9.95, ty - 8 * rh - 0.72,
            'เลขฐานสองบนขาเลือก = "เลขที่อยู่" (address) ของช่องข้อมูล',
            ha='center', fontsize=11, color='#64748B', style='italic')

    # อ้างอิงด้านล่างสุด
    ax.text(6.8, 0.12, 'อ้างอิง: 305241 Lecture รูปที่ 3.1 (หน้า 71) — แผนภาพบล็อกของมัลติเพล็กเซอร์',
            ha='center', fontsize=10.5, color='#94A3B8', style='italic')
    finish(fig, '01_mux_concept.png')


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 2 — ตารางฟังก์ชัน 74151 (คัดจาก lecture รูปที่ 3.2)
# ═══════════════════════════════════════════════════════════════════════════
def fig02_74151_table():
    fig, ax = plt.subplots(figsize=(13.2, 9.6))
    ax.set_xlim(0, 13.2); ax.set_ylim(0, 9.6); ax.axis('off')

    ax.text(6.6, 9.15, 'ตารางแสดงการทำงานของมัลติเพล็กเซอร์เบอร์ 74151',
            ha='center', fontsize=19, fontweight='bold', color=C_INK)
    ax.text(6.6, 8.65, 'คัดลอกจาก 305241 Lecture รูปที่ 3.2 (หน้า 71) — นี่คือ "กฎ" ที่ใช้เฉลยทั้งข้อ',
            ha='center', fontsize=12, color='#475569', style='italic')

    tx, ty = 3.16, 7.15
    cw, rh = 0.92, 0.545
    wcol = [cw, cw, cw, 1.28, 1.42, 1.42]
    heads = ['C', 'B', 'A', '$\\overline{G}$', '$Y$', '$W$']
    xoff = [0]
    for w in wcol[:-1]:
        xoff.append(xoff[-1] + w)
    total_w = sum(wcol)

    # หัวตารางกลุ่ม (Group Header)
    ax.add_patch(Rectangle((tx, ty + rh), sum(wcol[:3]), rh * 0.86,
                           facecolor='#1E293B', edgecolor=C_INK, lw=1.5, zorder=2))
    ax.text(tx + sum(wcol[:3]) / 2, ty + rh + rh * 0.43, 'ตัวเลือกอินพุต',
            ha='center', va='center', fontsize=12.5, color='white',
            fontweight='bold', zorder=3)
    ax.add_patch(Rectangle((tx + xoff[3], ty + rh), wcol[3], rh * 0.86,
                           facecolor='#1E293B', edgecolor=C_INK, lw=1.5, zorder=2))
    ax.text(tx + xoff[3] + wcol[3] / 2, ty + rh + rh * 0.43, 'อีนาเบิล',
            ha='center', va='center', fontsize=12.5, color='white',
            fontweight='bold', zorder=3)
    ax.add_patch(Rectangle((tx + xoff[4], ty + rh), wcol[4] + wcol[5], rh * 0.86,
                           facecolor='#1E293B', edgecolor=C_INK, lw=1.5, zorder=2))
    ax.text(tx + xoff[4] + (wcol[4] + wcol[5]) / 2, ty + rh + rh * 0.43, 'เอาต์พุต',
            ha='center', va='center', fontsize=12.5, color='white',
            fontweight='bold', zorder=3)

    # ชื่อคอลัมน์
    for j, (hd, w) in enumerate(zip(heads, wcol)):
        ax.add_patch(Rectangle((tx + xoff[j], ty), w, rh,
                               facecolor='#475569', edgecolor=C_INK, lw=1.4, zorder=2))
        ax.text(tx + xoff[j] + w / 2, ty + rh / 2, hd, ha='center', va='center',
                fontsize=14, color='white', fontweight='bold', zorder=3)

    rows = [('X', 'X', 'X', 'H', 'L', 'H')]
    for i in range(8):
        b = format(i, '03b')
        rows.append((('L', 'H')[int(b[0])], ('L', 'H')[int(b[1])],
                      ('L', 'H')[int(b[2])], 'L', f'$D_{i}$', f'$\\overline{{D_{i}}}$'))

    for i, r in enumerate(rows):
        yy = ty - (i + 1) * rh
        dis = (i == 0)
        for j, w in enumerate(wcol):
            fc = '#FEE2E2' if dis else ('#FFFFFF' if i % 2 else '#F8FAFC')
            ax.add_patch(Rectangle((tx + xoff[j], yy), w, rh,
                                   facecolor=fc, edgecolor=C_GRID, lw=1.0, zorder=2))
        for j, cell in enumerate(r):
            col = C_INK
            fw = 'normal'
            if j == 3:
                col = C_EN; fw = 'bold'
            if j == 4:
                col = C_Y; fw = 'bold'
            if j == 5:
                col = C_W; fw = 'bold'
            if dis:
                fw = 'bold'
            ax.text(tx + xoff[j] + wcol[j] / 2, yy + rh / 2, cell,
                    ha='center', va='center', fontsize=13.5,
                    color=col, fontweight=fw, zorder=3)

    # กรอบเน้นแถวดิสเอเบิล
    ax.add_patch(Rectangle((tx, ty - rh), total_w, rh, facecolor='none',
                           edgecolor=C_EN, lw=2.6, zorder=5))
    ax.annotate('', xy=(tx - 0.06, ty - rh / 2), xytext=(tx - 1.25, ty - rh / 2),
                arrowprops=dict(arrowstyle='-|>', color=C_EN, lw=2.2))
    ax.text(tx - 1.32, ty - rh / 2, 'แถวนี้สำคัญที่สุด', ha='right', va='center',
            fontsize=12, color=C_EN, fontweight='bold')

    ybot = ty - len(rows) * rh
    ax.text(tx + total_w / 2, ybot - 0.38,
            r'$\overline{G}$ มีขีดบน → ทำงานที่ลอจิก "ต่ำ"  ·  '
            r'$\overline{G}=H$ → ดิสเอเบิล บังคับ $Y=L,\ W=H$ ทันที (ไม่สนใจ C,B,A)',
            ha='center', fontsize=12, color=C_EN, fontweight='bold')
    ax.text(tx + total_w / 2, ybot - 0.78,
            r'เมื่อ $\overline{G}=L$ → ทำงาน: $Y=D_n$ โดย $n=4C+2B+A$  และ  $W=\overline{Y}$ เสมอ',
            ha='center', fontsize=12, color=C_INK)

    ax.text(6.6, 0.55,
            'ข้อความใน lecture หน้า 71: "ไอซีเบอร์ 74151 มีอินพุตข้อมูล 8 ช่องทาง และมีตัวเลือกอินพุตขนาด 3 บิต\n'
            'และมีเอาต์พุตเป็นทั้งแบบให้ค่าจริงและแบบกลับค่า"  → ยืนยันว่า $W=\\overline{Y}$',
            ha='center', fontsize=11, color='#64748B', style='italic',
            bbox=dict(boxstyle='round,pad=0.45', facecolor='#F1F5F9', edgecolor=C_GRID))
    finish(fig, '02_74151_function_table.png')

 # ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 3 — วงจรที่โจทย์ให้มา วาดใหม่ + ป้ายกำกับค่าที่ต่ออยู่ทุกช่อง
# ═══════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 3 — วงจรที่โจทย์ให้มา วาดใหม่แบบตรงตามต้นฉบับ + กำกับค่าที่ต่ออยู่
# ═══════════════════════════════════════════════════════════════════════════
def fig03_circuit():
    """วงจรที่โจทย์กำหนด (รูปที่ 3.40) วาดใหม่อย่างเที่ยงตรง สวยงาม อ่านง่าย ไม่ซ้อนทับ"""
    fig, ax = plt.subplots(figsize=(16.0, 9.6))
    ax.set_xlim(0, 16.0); ax.set_ylim(0, 9.6); ax.axis('off')

    ax.text(8.0, 9.30, 'วงจรที่โจทย์กำหนด (รูปที่ 3.40) — วาดใหม่แบบตรงตามต้นฉบับ 100%',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text(8.0, 8.92, 'ถอดรหัสการต่อสายของไอซี 74151 (8:1 MUX) เทียบกับรูปวงจรต้นฉบับในข้อสอบ',
            ha='center', fontsize=12, color='#475569', style='italic')

    # ── ตัวไอซี 74151 ───────────────────────────────────────────────────
    bx, by, bw, bh = 5.20, 0.85, 3.20, 7.70
    ax.add_patch(Rectangle((bx, by), bw, bh, facecolor=C_BOX,
                           edgecolor=C_INK, lw=2.4, zorder=3))
    ax.text(bx + bw / 2, by + bh - 0.44, '74151', ha='center', fontsize=16.5,
            fontweight='bold', color=C_INK, zorder=4)
    ax.text(bx + bw / 2, by + bh - 0.86, '8:1', ha='center', fontsize=13.5,
            fontweight='bold', color=C_INK, zorder=4)
    ax.text(bx + bw / 2, by + bh - 1.26, 'MUX', ha='center', fontsize=13.5,
            fontweight='bold', color=C_INK, zorder=4)

    pins = ['G', 'A', 'B', 'C', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
    py = {
        'G':  7.70,
        'A':  7.10,
        'B':  6.50,
        'C':  5.90,
        'D0': 5.20,
        'D1': 4.60,
        'D2': 4.00,
        'D3': 3.40,
        'D4': 2.80,
        'D5': 2.20,
        'D6': 1.60,
        'D7': 1.00,
    }

    disp = {'G': '$\\overline{G}$', 'A': 'A', 'B': 'B', 'C': 'C'}
    for i in range(8):
        disp[f'D{i}'] = f'$D_{i}$'

    for p in pins:
        ax.text(bx + 0.18, py[p], disp[p], ha='left', va='center',
                fontsize=13, color=C_INK, zorder=4)

    # bubble ที่ขา G-bar (Active-LOW Enable)
    ax.add_patch(Circle((bx - 0.10, py['G']), 0.095, facecolor='white',
                        edgecolor=C_INK, lw=1.8, zorder=5))

    # ── สายควบคุม E, A, B, C ────────────────────────────────────────────
    X_LBL = 1.30
    for pin, lab, col in [('G', 'E', C_EN), ('A', 'A', C_SEL),
                          ('B', 'B', C_SEL), ('C', 'C', C_SEL)]:
        x_from = bx - 0.195 if pin == 'G' else bx
        ax.plot([X_LBL, x_from], [py[pin], py[pin]], color=col, lw=2.0, zorder=2)
        ax.text(X_LBL - 0.12, py[pin], lab, ha='right', va='center',
                fontsize=15, color=col, fontweight='bold')

    ax.text(X_LBL - 0.12, py['G'] + 0.34, 'อีนาเบิล (active LOW)', ha='right',
            fontsize=10.5, color=C_EN, style='italic')
    ax.text(X_LBL - 0.12, py['C'] - 0.34, 'ขาเลือกอินพุต (Select)', ha='right',
            fontsize=10.5, color=C_SEL, style='italic')

    # ── สายข้อมูล D0, D2 และ NOT Gates ─────────────────────────────────
    x_d0_branch = 2.05  # คอลัมน์กิ่ง D0 -> NOT -> D4
    x_d2_branch = 2.95  # คอลัมน์กิ่ง D2 -> NOT -> D6
    x_supply    = 4.05  # คอลัมน์ +5V & GND

    # เส้นหลัก D0
    ax.plot([X_LBL, bx], [py['D0'], py['D0']], color=C_DATA, lw=2.0, zorder=2)
    ax.text(X_LBL - 0.12, py['D0'], '$D_0$', ha='right', va='center',
            fontsize=15, color=C_DATA, fontweight='bold')
    ax.add_patch(Circle((x_d0_branch, py['D0']), 0.075, facecolor=C_DATA,
                        edgecolor=C_DATA, zorder=6))

    # เส้นหลัก D2
    ax.plot([X_LBL, bx], [py['D2'], py['D2']], color=C_DATA, lw=2.0, zorder=2)
    ax.text(X_LBL - 0.12, py['D2'], '$D_2$', ha='right', va='center',
            fontsize=15, color=C_DATA, fontweight='bold')
    ax.add_patch(Circle((x_d2_branch, py['D2']), 0.075, facecolor=C_DATA,
                        edgecolor=C_DATA, zorder=6))

    # Inverter 1 (D0 -> NOT -> D4)
    y_top1 = 3.60
    y_tip1 = 3.22
    y_bub1 = 3.14
    r_bub = 0.062
    w_tri = 0.15

    ax.plot([x_d0_branch, x_d0_branch], [py['D0'], y_top1], color=C_DATA, lw=2.0, zorder=2)
    ax.add_patch(Polygon([[x_d0_branch - w_tri, y_top1], [x_d0_branch + w_tri, y_top1], [x_d0_branch, y_tip1]],
                         closed=True, facecolor='white', edgecolor=C_INK, lw=1.8, zorder=5))
    ax.add_patch(Circle((x_d0_branch, y_bub1), r_bub, facecolor='white', edgecolor=C_INK, lw=1.8, zorder=6))
    ax.plot([x_d0_branch, x_d0_branch], [y_bub1 - r_bub, py['D4']], color=C_DATA, lw=2.0, zorder=2)
    ax.plot([x_d0_branch, bx], [py['D4'], py['D4']], color=C_DATA, lw=2.0, zorder=2)

    # Inverter 2 (D2 -> NOT -> D6)
    y_top2 = 2.40
    y_tip2 = 2.02
    y_bub2 = 1.94

    ax.plot([x_d2_branch, x_d2_branch], [py['D2'], y_top2], color=C_DATA, lw=2.0, zorder=2)
    ax.add_patch(Polygon([[x_d2_branch - w_tri, y_top2], [x_d2_branch + w_tri, y_top2], [x_d2_branch, y_tip2]],
                         closed=True, facecolor='white', edgecolor=C_INK, lw=1.8, zorder=5))
    ax.add_patch(Circle((x_d2_branch, y_bub2), r_bub, facecolor='white', edgecolor=C_INK, lw=1.8, zorder=6))
    ax.plot([x_d2_branch, x_d2_branch], [y_bub2 - r_bub, py['D6']], color=C_DATA, lw=2.0, zorder=2)
    ax.plot([x_d2_branch, bx], [py['D6'], py['D6']], color=C_DATA, lw=2.0, zorder=2)

    # ── แหล่งจ่าย +5 V และกราวด์ GND (ตรงตามรูป 3.40 ในข้อสอบ 100%) ───
    # D1 (+5V ชี้ขึ้นบน)
    ax.plot([x_supply, bx], [py['D1'], py['D1']], color=C_ONE, lw=2.0, zorder=2)
    ax.plot([x_supply, x_supply], [py['D1'], py['D1'] + 0.28], color=C_ONE, lw=2.0, zorder=2)
    ax.annotate('', xy=(x_supply, py['D1'] + 0.30), xytext=(x_supply, py['D1'] + 0.08),
                arrowprops=dict(arrowstyle='-|>', color=C_ONE, lw=2.0, mutation_scale=12))
    ax.text(x_supply + 0.12, py['D1'] + 0.26, '+5 V', ha='left', va='center',
            fontsize=11.5, fontweight='bold', color=C_ONE)

    # D7 (+5V ชี้ขึ้นบน)
    ax.plot([x_supply, bx], [py['D7'], py['D7']], color=C_ONE, lw=2.0, zorder=2)
    ax.plot([x_supply, x_supply], [py['D7'], py['D7'] + 0.28], color=C_ONE, lw=2.0, zorder=2)
    ax.annotate('', xy=(x_supply, py['D7'] + 0.30), xytext=(x_supply, py['D7'] + 0.08),
                arrowprops=dict(arrowstyle='-|>', color=C_ONE, lw=2.0, mutation_scale=12))
    ax.text(x_supply + 0.12, py['D7'] + 0.26, '+5 V', ha='left', va='center',
            fontsize=11.5, fontweight='bold', color=C_ONE)

    # D3 (GND ชี้ลงล่าง)
    ax.plot([x_supply, bx], [py['D3'], py['D3']], color=C_ZERO, lw=2.0, zorder=2)
    ax.plot([x_supply, x_supply], [py['D3'], py['D3'] - 0.14], color=C_ZERO, lw=2.0, zorder=2)
    for k, hw in enumerate([0.18, 0.11, 0.05]):
        yy = py['D3'] - 0.14 - k * 0.055
        ax.plot([x_supply - hw, x_supply + hw], [yy, yy], color=C_ZERO, lw=2.0, zorder=3)

    # D5 (GND ชี้ลงล่าง)
    ax.plot([x_supply, bx], [py['D5'], py['D5']], color=C_ZERO, lw=2.0, zorder=2)
    ax.plot([x_supply, x_supply], [py['D5'], py['D5'] - 0.14], color=C_ZERO, lw=2.0, zorder=2)
    for k, hw in enumerate([0.18, 0.11, 0.05]):
        yy = py['D5'] - 0.14 - k * 0.055
        ax.plot([x_supply - hw, x_supply + hw], [yy, yy], color=C_ZERO, lw=2.0, zorder=3)

    # ── เอาต์พุต Y, W ───────────────────────────────────────────────────
    yo, wo = 5.20, 4.00
    ax.plot([bx + bw, 9.40], [yo, yo], color=C_Y, lw=2.4, zorder=2)
    ax.text(9.55, yo, '$Y$', ha='left', va='center',
            fontsize=17, color=C_Y, fontweight='bold')
    ax.text(9.55, yo - 0.34, 'ค่าจริง (True Output)', ha='left', va='center',
            fontsize=10.5, color=C_Y, style='italic')

    ax.plot([bx + bw, 9.40], [wo, wo], color=C_W, lw=2.4, zorder=2)
    ax.text(9.55, wo, '$W = \\overline{Y}$', ha='left', va='center',
            fontsize=17, color=C_W, fontweight='bold')
    ax.text(9.55, wo - 0.34, 'กลับค่า (Inverted)', ha='left', va='center',
            fontsize=10.5, color=C_W, style='italic')

    ax.text(bx + bw - 0.18, yo, 'Y', ha='right', va='center',
            fontsize=13.5, fontweight='bold', color=C_INK, zorder=4)
    ax.text(bx + bw - 0.18, wo, 'W', ha='right', va='center',
            fontsize=13.5, fontweight='bold', color=C_INK, zorder=4)

    # ── ตารางสรุปด้านขวา (เว้นระยะห่างไม่ทับป้าย Y, W) ───────────────────
    sx, sy = 12.30, 7.10
    rw, rh2 = 3.30, 0.44
    ax.text(sx + rw / 2, sy + 0.50, 'สรุป: ช่องไหนต่อกับอะไร',
            ha='center', fontsize=13, fontweight='bold', color=C_INK)
    ax.add_patch(Rectangle((sx, sy), rw, rh2, facecolor='#1E293B',
                           edgecolor=C_INK, lw=1.3, zorder=2))
    ax.text(sx + 0.65, sy + rh2 / 2, 'ช่อง', ha='center', va='center',
            fontsize=11.5, color='white', fontweight='bold', zorder=3)
    ax.text(sx + 2.10, sy + rh2 / 2, 'ค่าที่ส่งออก $Y$', ha='center', va='center',
            fontsize=11.5, color='white', fontweight='bold', zorder=3)

    sumrows = [('$D_0$', '$D_0$', C_DATA), ('$D_1$', '$1$', C_ONE),
               ('$D_2$', '$D_2$', C_DATA), ('$D_3$', '$0$', C_ZERO),
               ('$D_4$', '$\\overline{D_0}$', C_DATA), ('$D_5$', '$0$', C_ZERO),
               ('$D_6$', '$\\overline{D_2}$', C_DATA), ('$D_7$', '$1$', C_ONE)]
    for i, (ch, v, col) in enumerate(sumrows):
        yy = sy - (i + 1) * rh2
        ax.add_patch(Rectangle((sx, yy), rw, rh2,
                               facecolor='#FFFFFF' if i % 2 else '#F8FAFC',
                               edgecolor=C_GRID, lw=0.9, zorder=2))
        ax.text(sx + 0.65, yy + rh2 / 2, ch, ha='center', va='center',
                fontsize=12.5, color=C_INK, zorder=3)
        ax.text(sx + 2.10, yy + rh2 / 2, v, ha='center', va='center',
                fontsize=13, color=col, fontweight='bold', zorder=3)

    # กล่องข้อสังเกต
    nb_y = sy - 8 * rh2 - 0.45
    ax.add_patch(Rectangle((sx - 0.08, nb_y - 1.75), rw + 0.16, 1.75,
                           facecolor='#FEF2F2', edgecolor='#EF4444', lw=1.5,
                           linestyle='-', zorder=2))
    ax.text(sx + rw / 2, nb_y - 0.32, 'ข้อสังเกตสำคัญตามโจทย์:',
            ha='center', fontsize=11, fontweight='bold', color='#B91C1C', zorder=3)
    ax.text(sx + rw / 2, nb_y - 0.70, '• มีจุดต่อทึบ (•) = เชื่อมถึงกัน',
            ha='center', fontsize=10.5, color='#B91C1C', zorder=3)
    ax.text(sx + rw / 2, nb_y - 1.08, '• เส้นตัดผ่านโดยไม่มีจุด = ไม่เชื่อมกัน',
            ha='center', fontsize=10.5, color='#B91C1C', zorder=3)
    ax.text(sx + rw / 2, nb_y - 1.46, '• NOT gate คว่ำลง = สัญญาณกลับค่า',
            ha='center', fontsize=10.5, color='#B91C1C', zorder=3)

    finish(fig, '03_circuit_annotated.png')


# ═══════════════════════════════════════════════════════════════════════════
def fig04_input_waves():
    fig, ax = plt.subplots(figsize=(15.0, 8.6))
    span = X1 + 1 - X0
    ax.set_xlim(X0 - span * 0.085, X1 + 1 + span * 0.045)
    ax.set_ylim(-1.05, 8.45)
    ax.axis('off')

    ax.text((X0 + X1) / 2, 7.74, 'รูปคลื่นอินพุตที่โจทย์กำหนด (วาดใหม่จากต้นฉบับ)',
            ha='center', fontsize=18.5, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 7.34,
            'เส้นประแนวตั้ง = ขอบเปลี่ยนของ A ซึ่งใช้แบ่ง "ช่วงเวลา" ทั้ง 9 ช่วง',
            ha='center', fontsize=12, color='#475569', style='italic')

    h = 0.60
    rows = [('A', 'A', C_SEL, 6.30), ('B', 'B', C_SEL, 5.20),
            ('C', 'C', C_SEL, 4.10), ('E', 'E', C_EN, 3.00),
            ('D0', '$D_0$', C_DATA, 1.75), ('D2', '$D_2$', C_DATA, 0.55)]

    disable_bands(ax, -0.30, 6.98)
    slot_grid(ax, 6.98, -0.30, show_labels=True, label_y=7.02, fs=13)

    # คำโปรยระดับ 0/1 วาดครั้งเดียวด้านซ้ายสุด (ไม่ซ้ำต่อแถว — กันชนกับป้ายชื่อ)
    ax.text(X0 - span * 0.072, rows[-1][3], '0', ha='center', va='center',
            fontsize=9.5, color='#94A3B8')
    ax.text(X0 - span * 0.072, rows[0][3] + h, '1', ha='center', va='center',
            fontsize=9.5, color='#94A3B8')

    for sig, lab, col, yb in rows:
        # เส้นฐาน 0 / 1 เพื่อให้อ่านระดับง่าย
        ax.plot([X0, X1 + 1], [yb, yb], color=C_GRID, lw=0.8, zorder=1)
        ax.plot([X0, X1 + 1], [yb + h, yb + h], color=C_GRID, lw=0.8, zorder=1)
        draw_wave(ax, RUNS[sig], yb, h, col)
        wave_label(ax, X0 - span * 0.018, yb + h / 2, lab, col, fs=17)

    # ป้ายบอกกลุ่มสัญญาณ
    ax.text(X0 - span * 0.048, 5.15, 'ตัวนับ 3 บิต\n(ขาเลือกอินพุต)', ha='right',
            va='center', fontsize=11, color=C_SEL, style='italic')
    ax.text(X0 - span * 0.048, 3.30, 'อีนาเบิล', ha='right', va='center',
            fontsize=11, color=C_EN, style='italic')
    ax.text(X0 - span * 0.048, 1.35, 'สัญญาณข้อมูล', ha='right', va='center',
            fontsize=11, color=C_DATA, style='italic')

    # แถบอธิบายช่วงดิสเอเบิล — วาด "เหนือ" แถวเลขช่วง (ไม่ทับตัวเลข)
    for v, s, e in RUNS['E']:
        if v == 1:
            ax.text((s + e + 1) / 2, 7.30, 'E=1 → ดิสเอเบิล', ha='center',
                    va='bottom', fontsize=10, color=C_EN, fontweight='bold')

    # แสดงรหัสเลือกช่องใต้แต่ละช่วง
    ax.text(X0 - span * 0.018, -0.60, 'CBA =', ha='right', va='center',
            fontsize=12, color=C_INK, fontweight='bold')
    for i in range(NSLOT):
        xc = (SLOT_EDGES[i] + SLOT_EDGES[i + 1]) / 2
        c, b, a, n = sel_code(SLOT_EDGES[i])
        ax.text(xc, -0.60, f'{c}{b}{a}', ha='center', va='center',
                fontsize=12.5, color=C_SEL, fontweight='bold')
        ax.text(xc, -0.92, f'({n})', ha='center', va='center',
                fontsize=10.5, color='#64748B')

    ax.text((X0 + X1) / 2, -1.02,
            'ตรวจสอบแล้ว: ลำดับลอจิกตรงกันทุกบิตระหว่างภาพสแกนกับต้นฉบับ vector (ดู VERIFICATION.md)',
            ha='center', va='top', fontsize=10, color='#94A3B8', style='italic')
    finish(fig, '04_input_waveforms.png')


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 5 — A,B,C คือตัวนับฐานสองขึ้น 0→7
# ═══════════════════════════════════════════════════════════════════════════
def fig05_counter():
    """A,B,C = ตัวนับฐานสอง — เวอร์ชันอ่านง่าย:
    • แยกโซนชัดเจน: หัวเรื่อง / เลขช่วง / รูปคลื่น / ตารางถอดรหัส / สรุป
    • เส้นประแบ่งช่วงวาดเฉพาะในโซนรูปคลื่นเท่านั้น (ไม่ลากทับตัวอักษร)
    • ถอดรหัสใช้คอลัมน์พื้นสลับสีแบบตาราง ไม่ใช้วงกลม/ลูกศรยาว
    """
    fig, ax = plt.subplots(figsize=(15.5, 9.4))
    span = X1 + 1 - X0
    L, R = X0 - span * 0.105, X1 + 1 + span * 0.035
    ax.set_xlim(L, R)
    ax.set_ylim(-3.15, 7.15)
    ax.axis('off')

    # ── โซนหัวเรื่อง (ไม่มีเส้นใดยื่นเข้ามา) ─────────────────────────────
    ax.text((X0 + X1) / 2, 6.68,
            'ขั้นที่ 1 — อ่านขาเลือกอินพุต: A, B, C คือ "ตัวนับฐานสอง" นับ 0 → 7',
            ha='center', fontsize=19, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 6.12,
            'A สลับทุก 1 ช่วง (เร็วสุด = LSB) · B สลับทุก 2 ช่วง · C สลับทุก 4 ช่วง (ช้าสุด = MSB)',
            ha='center', fontsize=12.5, color='#475569', style='italic')

    # ── เลขช่วงเวลา (แถวบนโซนรูปคลื่น) ─────────────────────────────────
    h = 0.66
    WAVE_TOP, WAVE_BOT = 5.42, 1.52          # ขอบเขตโซนรูปคลื่น
    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        # พื้นคอลัมน์สลับสีเฉพาะโซนรูปคลื่น (ช่วยตาไล่ช่วง)
        if i % 2 == 0:
            ax.add_patch(Rectangle((xs, WAVE_BOT), xe - xs, WAVE_TOP - WAVE_BOT,
                                   facecolor='#F4F7FB', edgecolor='none', zorder=0))
        xc = (xs + xe) / 2
        ax.text(xc, 5.58, f'{i+1}', ha='center', va='bottom', fontsize=14,
                fontweight='bold', color=C_INK)
        # เส้นประแบ่งช่วง — วาดเฉพาะภายในโซนรูปคลื่น
        if i > 0:
            ax.plot([xs, xs], [WAVE_BOT, WAVE_TOP], color=C_SLOT, lw=1.1,
                    ls=(0, (4, 3)), zorder=1)

    # ── รูปคลื่น C, B, A ────────────────────────────────────────────────
    rows = [('C', '$C$  (MSB · น้ำหนัก 4)', 4.28),
            ('B', '$B$  (น้ำหนัก 2)',      3.23),
            ('A', '$A$  (LSB · น้ำหนัก 1)', 2.18)]
    for sig, lab, yb in rows:
        ax.plot([X0, X1 + 1], [yb, yb], color=C_GRID, lw=0.9, zorder=1)
        ax.plot([X0, X1 + 1], [yb + h, yb + h], color=C_GRID, lw=0.9, zorder=1)
        draw_wave(ax, RUNS[sig], yb, h, C_SEL, lw=2.8)
        ax.text(X0 - span * 0.022, yb + h / 2, lab, ha='right', va='center',
                fontsize=13.5, color=C_SEL, fontweight='bold')
        ax.text(X0 - span * 0.085, yb, '0', ha='center', va='center',
                fontsize=9.5, color='#94A3B8')
        ax.text(X0 - span * 0.085, yb + h, '1', ha='center', va='center',
                fontsize=9.5, color='#94A3B8')
    ax.plot([X0, X1 + 1], [WAVE_BOT + 0.06, WAVE_BOT + 0.06],
            color=C_SLOT, lw=1.2)

    # ── โซนตารางถอดรหัส (พื้นคอลัมน์ต่อเนื่องจากด้านบน) ────────────────
    T_TOP, T_BOT = 1.46, -0.34
    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        fc = '#EFF6FF' if i % 2 == 0 else '#FFFFFF'
        ax.add_patch(Rectangle((xs, T_BOT), xe - xs, T_TOP - T_BOT,
                               facecolor=fc, edgecolor='#C7D2FE', lw=1.1, zorder=2))
        if i > 0:
            ax.plot([xs, xs], [T_BOT, T_TOP], color='#93C5FD', lw=1.1, zorder=3)
        xc = (xs + xe) / 2
        c, b, a, n = sel_code(xs)
        ax.text(xc, 1.02, f'{c} {b} {a}', ha='center', va='center',
                fontsize=13.5, color=C_SEL, fontweight='bold', zorder=4)
        ax.text(xc, 0.36, str(n), ha='center', va='center', fontsize=14.5,
                color='#1D4ED8', fontweight='bold', zorder=4)
        ax.text(xc, -0.02, f'$D_{n}$', ha='center', va='center', fontsize=13.5,
                color=C_INK, fontweight='bold', zorder=4)
    # ป้ายคอลัมน์ซ้ายของตาราง
    ax.text(X0 - span * 0.022, 1.02, 'CBA', ha='right', va='center',
            fontsize=12.5, color=C_INK, fontweight='bold')
    ax.text(X0 - span * 0.022, 0.36, 'ฐานสิบ', ha='right', va='center',
            fontsize=12.5, color=C_INK, fontweight='bold')
    ax.text(X0 - span * 0.022, -0.02, 'ช่องที่เลือก', ha='right', va='center',
            fontsize=12.5, color=C_INK, fontweight='bold')

    # ── บรรทัดลำดับการนับ (ข้อความเดียว ไม่ใช้ลูกศรยาว) ─────────────────
    ax.text((X0 + X1) / 2, -0.92,
            'ไล่เลือกช่อง $D_0 \\to D_1 \\to D_2 \\to D_3 \\to D_4 \\to D_5 \\to D_6 \\to D_7$'
            '  ครบรอบ  แล้ววนกลับมา $D_0$ ในช่วงที่ 9 (ตัวนับ 3 บิตล้น)',
            ha='center', va='center', fontsize=13, color=C_SEL, fontweight='bold')

    # ── กล่องสูตร ───────────────────────────────────────────────────────
    ax.text((X0 + X1) / 2, -1.88,
            'สูตรถอดรหัส:   $n = 4C + 2B + A$\n'
            '(C คูณ 4 เพราะเป็นบิตสูงสุด · B คูณ 2 · A คูณ 1)',
            ha='center', va='center', fontsize=14, color=C_INK, linespacing=1.9,
            bbox=dict(boxstyle='round,pad=0.55', facecolor='#EFF6FF',
                      edgecolor=C_SEL, lw=1.8))

    ax.text((L + R) / 2, -3.00,
            'อ่านยังไง: มองแต่ละคอลัมน์จากบนลงล่าง — ระดับสัญญาณ A,B,C → รหัส CBA → เลขฐานสิบ → ช่องที่ MUX เลือก',
            ha='center', fontsize=11, color='#94A3B8', style='italic')
    finish(fig, '05_select_counter.png')


def fig06_enable():
    """อีนาเบิล E — เลย์เอาต์ 4 ชั้น สะอาดตา สัดส่วนลงตัว อ่านง่าย ตรงตามเฉลย:
    ชั้น 1: หัวเรื่อง + คำอธิบาย Active-LOW
    ชั้น 2: รูปคลื่น E + จุดเปลี่ยนสถานะ (กลางช่วง 2 และ 9)
    ชั้น 3: ตารางวิเคราะห์สถานะและเอาต์พุต Y, W ทั้ง 9 ช่วง
    ชั้น 4: สัญลักษณ์สี + กล่องข้อสรุปกฎ ชิดขอบล่างพอดี
    """
    fig, ax = plt.subplots(figsize=(15.5, 8.6))
    span = X1 + 1 - X0
    L, R = X0 - span * 0.11, X1 + 1 + span * 0.04
    ax.set_xlim(L, R)
    ax.set_ylim(-1.55, 6.75)
    ax.axis('off')

    # ── ชั้น 1: หัวเรื่อง (เว้นระยะไม่ชนตัวเลข) ─────────────────────────
    ax.text((X0 + X1) / 2, 6.42,
            'ขั้นที่ 2 — อ่านขาอีนาเบิล: ช่วงไหนไอซี "ทำงาน" ช่วงไหน "ถูกปิด"',
            ha='center', fontsize=18.5, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 5.96,
            'E ต่อเข้าขา $\\overline{G}$ (Active LOW) ⇒ E = 0 : ไอซีทำงานตามช่องที่เลือก · E = 1 : ไอซีถูกปิด บังคับ Y = 0, W = 1',
            ha='center', fontsize=12, color='#475569', style='italic')

    # ── ชั้น 2: รูปคลื่น E ───────────────────────────────────────────────
    h = 0.75
    WAVE_BOT, WAVE_TOP = 4.30, 5.05

    # เลขช่วง 1-9 บนรูปคลื่น
    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        xc = (xs + xe) / 2
        ax.text(xc, 5.42, f'{i+1}', ha='center', va='center',
                fontsize=13.5, fontweight='bold', color=C_INK)
        if i > 0:
            ax.plot([xs, xs], [WAVE_BOT - 0.15, 5.30], color=C_SLOT, lw=1.1,
                    ls=(0, (4, 3)), zorder=1)

    # แถบสีแดงอ่อนสำหรับช่วง E = 1 (ถูกปิด)
    for v, s, e in RUNS['E']:
        if v == 1:
            ax.add_patch(Rectangle((s, WAVE_BOT), e + 1 - s, h,
                                   facecolor='#FEE2E2', edgecolor='none', alpha=0.7, zorder=1))

    # เส้นแนวนอน 0 และ 1
    ax.plot([X0, X1 + 1], [WAVE_BOT, WAVE_BOT], color=C_GRID, lw=0.9, zorder=1)
    ax.plot([X0, X1 + 1], [WAVE_BOT + h, WAVE_BOT + h], color=C_GRID, lw=0.9, zorder=1)

    # วาดรูปคลื่น E
    for v, s, e in RUNS['E']:
        y_val = WAVE_BOT + h if v == 1 else WAVE_BOT
        ax.plot([s, e + 1], [y_val, y_val], color=C_EN, lw=3.2, zorder=4)

    FALL_X, RISE_X = 1220, 2605
    ax.plot([FALL_X, FALL_X], [WAVE_BOT, WAVE_BOT + h], color=C_EN, lw=3.2, zorder=4)
    ax.plot([RISE_X, RISE_X], [WAVE_BOT, WAVE_BOT + h], color=C_EN, lw=3.2, zorder=4)

    # จุด Transition Markers
    ax.scatter([FALL_X, RISE_X], [WAVE_BOT, WAVE_BOT + h], s=80, color='#DC2626',
               edgecolors='white', linewidths=1.8, zorder=8)

    ax.text(X0 - span * 0.022, WAVE_BOT + h / 2, '$E$', ha='right', va='center',
            fontsize=18, color=C_EN, fontweight='bold')
    ax.text(X0 - span * 0.075, WAVE_BOT, '0', ha='center', va='center', fontsize=10, color='#94A3B8')
    ax.text(X0 - span * 0.075, WAVE_BOT + h, '1', ha='center', va='center', fontsize=10, color='#94A3B8')

    ax.text(X1 + 1 + span * 0.012, WAVE_BOT + h / 2,
            '● = E เปลี่ยนค่า\n(กลางช่วง 2 และ 9)',
            ha='left', va='center', fontsize=10.5, color='#B91C1C', fontweight='bold')

    # ── ชั้น 3: ตารางสรุป 9 ช่อง ─────────────────────────────────────────
    T_TOP = 3.65
    row_h = {
        'num':   0.40,
        'cba':   0.44,
        'e':     0.48,
        'state': 0.50,
        'y':     0.64,
        'w':     0.64,
    }
    ys = {}
    ycur = T_TOP
    for k in ['num', 'cba', 'e', 'state', 'y', 'w']:
        ys[k] = ycur - row_h[k] / 2
        ycur -= row_h[k]
    T_BOT = ycur

    # ข้อมูลเอาต์พุตรายช่วงตรงตามเฉลย 100%
    table_data = [
        ('0', '1'),
        ('0 / 1', '1 / 0'),
        ('$D_2$', '$\\overline{D_2}$'),
        ('0', '1'),
        ('$\\overline{D_0}$', '$D_0$'),
        ('0', '1'),
        ('$\\overline{D_2}$', '$D_2$'),
        ('1', '0'),
        ('$D_0$ / 0', '$\\overline{D_0}$ / 1')
    ]

    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        c, b, a, n = sel_code(xs)
        es = to_runs(lambda x: val('E', x), xs, xe - 1)
        disabled_all = all(v == 1 for v, _, _ in es)
        enabled_all = all(v == 0 for v, _, _ in es)
        split = not (disabled_all or enabled_all)

        if disabled_all:
            fc, ed = '#FEF2F2', '#FCA5A5'
        elif enabled_all:
            fc, ed = '#F0FDF4', '#86EFAC'
        else:
            fc, ed = '#FFFBEB', '#FCD34D'

        ax.add_patch(Rectangle((xs, T_BOT), xe - xs, T_TOP - T_BOT,
                               facecolor=fc, edgecolor=ed, lw=1.2, zorder=2))
        if i > 0:
            ax.plot([xs, xs], [T_BOT, T_TOP], color='#CBD5E1', lw=1.0, zorder=3)
        xc = (xs + xe) / 2

        ax.text(xc, ys['num'], f'{i+1}', ha='center', va='center', fontsize=13,
                fontweight='bold', color=C_INK, zorder=4)
        ax.text(xc, ys['cba'], f'{c}{b}{a}', ha='center', va='center', fontsize=12,
                color=C_SEL, fontweight='bold', zorder=4)

        if split:
            etxt = '/'.join(str(v) for v, _, _ in es)
            stxt = 'แบ่ง 2 ส่วน'
            sc = '#B45309'
        elif disabled_all:
            etxt, stxt, sc = '1', 'ปิด', C_EN
        else:
            etxt, stxt, sc = '0', 'ทำงาน', '#047857'

        ax.text(xc, ys['e'], etxt, ha='center', va='center', fontsize=13,
                fontweight='bold', color=sc, zorder=4)
        ax.text(xc, ys['state'], stxt, ha='center', va='center', fontsize=11,
                fontweight='bold', color=sc, zorder=4)

        yt, wt = table_data[i]
        ax.text(xc, ys['y'], yt, ha='center', va='center', fontsize=13,
                fontweight='bold', color=C_Y, zorder=4)
        ax.text(xc, ys['w'], wt, ha='center', va='center', fontsize=13,
                fontweight='bold', color=C_W, zorder=4)

    # Table Left Labels
    labels = [('num', 'ช่วงที่'), ('cba', 'CBA'), ('e', '$E$'),
              ('state', 'สถานะไอซี'), ('y', 'เอาต์พุต $Y$'), ('w', 'เอาต์พุต $W$')]
    for k, lab in labels:
        ax.text(X0 - span * 0.020, ys[k], lab, ha='right', va='center',
                fontsize=12, color=C_INK, fontweight='bold')

    # Table Grid lines
    ax.plot([X0, X1 + 1], [T_TOP, T_TOP], color=C_INK, lw=1.8, zorder=4)
    ax.plot([X0, X1 + 1], [ys['e'] + row_h['e'] / 2, ys['e'] + row_h['e'] / 2],
            color=C_INK, lw=1.4, zorder=4)
    ax.plot([X0, X1 + 1], [ys['state'] - row_h['state'] / 2, ys['state'] - row_h['state'] / 2],
            color=C_INK, lw=1.4, zorder=4)
    ax.plot([X0, X1 + 1], [T_BOT, T_BOT], color=C_INK, lw=1.8, zorder=4)

    # ── ชั้น 4: Legend และ กล่องข้อความสรุป (จัดวางชิดขอบล่างพอดี) ─────────
    ly = T_BOT - 0.28
    swatch_w, swatch_h = span * 0.035, 0.20

    leg_items = [
        (0.18, '#FEF2F2', '#FCA5A5', 'พื้นแดง = ไอซีถูกปิดทั้งช่วง ($E = 1$)'),
        (0.50, '#FFFBEB', '#FCD34D', 'พื้นเหลือง = แบ่ง 2 ส่วน ($E$ เปลี่ยนกลางช่วง)'),
        (0.82, '#F0FDF4', '#86EFAC', 'พื้นเขียว = ไอซีทำงานทั้งช่วง ($E = 0$)')
    ]
    for xfrac, fc, ec, lab in leg_items:
        lx = X0 + span * xfrac
        ax.add_patch(Rectangle((lx - swatch_w - span * 0.008, ly - swatch_h / 2),
                               swatch_w, swatch_h, facecolor=fc, edgecolor=ec, lw=1.2, zorder=3))
        ax.text(lx, ly, lab, ha='left', va='center', fontsize=11, fontweight='bold', color=C_INK)

    box_y = T_BOT - 0.86
    rule_text = (
        '• กฎหัวใจสำคัญ:  เมื่อ $E = 1$  ⇒  ไอซีจะถูกปิดทันที บังคับเอาต์พุต $Y = 0$ และ $W = 1$ เสมอ (ไม่สนใจว่าขาเลือกหรือข้อมูลจะเป็นอะไร)\n'
        '• เมื่อ $E = 0$  ⇒  ไอซีจะเปิดทำงานปกติ เอาต์พุต $Y$ จะส่งผ่านสัญญาณตามช่องที่ถูกเลือก ($n = 4C + 2B + A$)  และ  $W = \\overline{Y}$'
    )
    ax.text((X0 + X1) / 2, box_y, rule_text,
            ha='center', va='center', fontsize=12, color=C_INK, linespacing=1.6,
            bbox=dict(boxstyle='round,pad=0.50', facecolor='#EFF6FF', edgecolor=C_SEL, lw=1.6))

    ax.text((X0 + X1) / 2, box_y - 0.50,
        '* ข้อควรระวังในห้องสอบ: ช่วงที่ 2 และช่วงที่ 9 สัญญาณ E มีการสลับค่ากลางช่วง ต้องแบ่งคำนวณเอาต์พุตออกเป็น 2 ท่อน',
        ha='center', va='center', fontsize=10.5, color='#B91C1C', style='italic')

    finish(fig, '06_enable_analysis.png')

# ═══════════════════════════════════════════════════════════════════════════
def fig07_inverted():
    fig, ax = plt.subplots(figsize=(15.2, 8.2))
    span = X1 + 1 - X0
    ax.set_xlim(X0 - span * 0.14, X1 + 1 + span * 0.045)
    ax.set_ylim(-1.20, 6.60); ax.axis('off')

    ax.text((X0 + X1) / 2, 6.28,
            'ขั้นที่ 3 — เตรียมสัญญาณที่ต่ออยู่จริงในวงจร: $\\overline{D_0}$ และ $\\overline{D_2}$',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 5.90,
            'ช่อง $D_4$ ต่อผ่านอินเวอร์เตอร์จาก $D_0$  และช่อง $D_6$ ต่อผ่านอินเวอร์เตอร์จาก $D_2$ '
            '→ ต้องวาดสัญญาณกลับค่าไว้ล่วงหน้า',
            ha='center', fontsize=12, color='#475569', style='italic')

    inv_D0 = [(1 - v, s, e) for v, s, e in RUNS['D0']]
    inv_D2 = [(1 - v, s, e) for v, s, e in RUNS['D2']]

    h = 0.58
    rows = [
        ('$D_0$', RUNS['D0'], 4.72, C_DATA, 'สัญญาณต้นทาง → เข้าช่อง $D_0$'),
        ('$\\overline{D_0}$', inv_D0, 3.58, '#DB2777', 'สัญญาณกลับค่า → เข้าช่อง $D_4$'),
        ('$D_2$', RUNS['D2'], 2.10, C_DATA, 'สัญญาณต้นทาง → เข้าช่อง $D_2$'),
        ('$\\overline{D_2}$', inv_D2, 0.96, '#DB2777', 'สัญญาณกลับค่า → เข้าช่อง $D_6$'),
    ]
    slot_grid(ax, 5.50, 0.66, show_labels=True, label_y=5.54, fs=12.5)
    for lab, runs, yb, col, note in rows:
        ax.plot([X0, X1 + 1], [yb, yb], color=C_GRID, lw=0.8, zorder=1)
        ax.plot([X0, X1 + 1], [yb + h, yb + h], color=C_GRID, lw=0.8, zorder=1)
        draw_wave(ax, runs, yb, h, col, lw=2.6)
        ax.text(X0 - span * 0.012, yb + h / 2, lab, ha='right', va='center',
                fontsize=17, color=col, fontweight='bold')
        ax.text(X0 - span * 0.065, yb + h / 2, note, ha='right', va='center',
                fontsize=10.2, color='#64748B', style='italic')

    # ลูกศรแสดงการกลับค่า
    for y_from, y_to in [(4.72, 3.58 + h), (2.10, 0.96 + h)]:
        xm = X0 + span * 0.045
        ax.annotate('', xy=(xm, y_to + 0.06), xytext=(xm, y_from - 0.06),
                    arrowprops=dict(arrowstyle='-|>', color='#DB2777', lw=2.0))
        ax.text(xm + span * 0.010, (y_from + y_to) / 2, 'NOT',
                fontsize=10.5, color='#DB2777', fontweight='bold', va='center')

    ax.text((X0 + X1) / 2, 0.28,
            'ข้อสังเกตที่เป็นกุญแจของข้อนี้:  $D_2$ คือ $D_0$ "หารสอง" '
            '(ขอบเปลี่ยนของ $D_2$ ตรงกับขอบขาลงของ $D_0$ ทุกจุด — ตรวจด้วยพิกเซลแล้ว)',
            ha='center', va='center', fontsize=12.5, color=C_DATA, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.46', facecolor='#F5F3FF',
                      edgecolor=C_DATA, lw=1.5))
    ax.text((X0 + X1) / 2, -0.55,
            'อีกจุดสำคัญ: คาบของ $D_0$ ≈ 1.23 เท่าของความกว้างช่วงเวลา → $D_0$ "ไม่ซิงค์" กับตัวนับ\n'
            'ดังนั้นภายในหนึ่งช่วงเวลา เอาต์พุตอาจเปลี่ยนค่าได้หลายครั้ง — ห้ามคิดว่า 1 ช่วง = 1 ค่าคงที่',
            ha='center', va='center', fontsize=11.8, color='#B45309', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.46', facecolor='#FFFBEB',
                      edgecolor='#B45309', lw=1.5))
    finish(fig, '07_inverted_signals.png')


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 8 — ไล่ทีละช่วง 9 แผง: ช่วงไหนเลือกช่องไหน ได้ Y เท่าไร
# ═══════════════════════════════════════════════════════════════════════════
def fig08_slot_by_slot():
    fig = plt.figure(figsize=(15.4, 12.4))
    fig.suptitle('ขั้นที่ 4 — ไล่ทีละช่วงเวลา: "ช่วงนี้เลือกช่องไหน → ช่องนั้นต่ออะไร → $Y$ เป็นเท่าไร"',
                 fontsize=17.5, fontweight='bold', color=C_INK, y=0.988)
    fig.text(0.5, 0.9505,
             'แต่ละแผงคือ 1 ช่วงเวลา — เส้นม่วงคือค่าที่ช่องนั้นส่งอยู่ เส้นเขียวหนาคือ $Y$ ที่ได้',
             ha='center', fontsize=11.5, color='#475569', style='italic')

    for i in range(NSLOT):
        ax = fig.add_subplot(3, 3, i + 1)
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        c, b, a, n = sel_code(xs)
        pad = (xe - xs) * 0.09
        ax.set_xlim(xs - pad, xe + pad)
        ax.set_ylim(-0.62, 3.32)
        ax.axis('off')

        # กรอบแผง
        disabled_any = any(val('E', x) == 1 for x in range(xs, xe))
        fc = '#FEF2F2' if disabled_any else '#F8FAFC'
        ax.add_patch(Rectangle((xs - pad, -0.62), (xe - xs) + 2 * pad, 3.94,
                               facecolor=fc, edgecolor=C_GRID, lw=1.4,
                               zorder=0, clip_on=False))

        srcname, srclabel, srcfn = CH_SRC[n]
        title = f'ช่วงที่ {i+1}   ·   CBA = {c}{b}{a} = {n}   →   เลือกช่อง $D_{n}$'
        ax.text((xs + xe) / 2, 3.06, title, ha='center', fontsize=11.6,
                fontweight='bold', color=C_SEL)
        ax.text((xs + xe) / 2, 2.74, f'ช่อง $D_{n}$ ต่อกับ  {srclabel}',
                ha='center', fontsize=10.8, color=C_DATA, fontweight='bold')

        # แถบดิสเอเบิลภายในช่วง
        for v, s, e in RUNS['E']:
            if v == 1:
                a0, a1 = max(s, xs), min(e + 1, xe)
                if a1 > a0:
                    ax.add_patch(Rectangle((a0, -0.20), a1 - a0, 2.56,
                                           facecolor='#FECACA', edgecolor='none',
                                           zorder=1, alpha=0.75))

        h = 0.48
        # เส้น E
        yE = 1.78
        ax.plot([xs, xe], [yE, yE], color=C_GRID, lw=0.7, zorder=1)
        eruns = [(v, max(s, xs), min(e, xe - 1)) for v, s, e in RUNS['E']
                 if max(s, xs) <= min(e, xe - 1)]
        draw_wave(ax, eruns, yE, h * 0.72, C_EN, lw=2.0)
        ax.text(xs - pad * 0.30, yE + h * 0.36, '$E$', ha='right', va='center',
                fontsize=11, color=C_EN, fontweight='bold')

        # ค่าที่ช่องส่งอยู่
        ySrc = 0.94
        ax.plot([xs, xe], [ySrc, ySrc], color=C_GRID, lw=0.7, zorder=1)
        sruns = to_runs(srcfn, xs, xe - 1)
        draw_wave(ax, sruns, ySrc, h * 0.72, C_DATA, lw=2.0, ls=(0, (3, 2)))
        ax.text(xs - pad * 0.30, ySrc + h * 0.36, srclabel, ha='right', va='center',
                fontsize=11, color=C_DATA, fontweight='bold')

        # Y ที่ได้
        yY = 0.08
        ax.plot([xs, xe], [yY, yY], color=C_GRID, lw=0.7, zorder=1)
        yruns = to_runs(Yf, xs, xe - 1)
        draw_wave(ax, yruns, yY, h * 0.72, C_Y, lw=3.0)
        ax.text(xs - pad * 0.30, yY + h * 0.36, '$Y$', ha='right', va='center',
                fontsize=12.5, color=C_Y, fontweight='bold')

        # สรุปข้อความใต้แผง
        if disabled_any and all(val('E', x) == 1 for x in range(xs, xe)):
            msg = 'ถูกดิสเอเบิลทั้งช่วง → $Y=0$'
            mc = C_EN
        elif disabled_any:
            msg = 'ครึ่งช่วงถูกดิสเอเบิล → ต้องแบ่ง 2 ส่วน'
            mc = C_EN
        elif srcname in ('+5V',):
            msg = 'ค่าคงที่ → $Y=1$ ทั้งช่วง'
            mc = C_ONE
        elif srcname == 'GND':
            msg = 'ค่าคงที่ → $Y=0$ ทั้งช่วง'
            mc = C_ZERO
        else:
            msg = f'$Y$ ตามรูปคลื่น {srclabel}'
            mc = C_DATA
        ax.text((xs + xe) / 2, -0.46, msg, ha='center', fontsize=10.4,
                color=mc, fontweight='bold')

    fig.subplots_adjust(top=0.926, bottom=0.022, hspace=0.30, wspace=0.13)
    finish(fig, '08_slot_by_slot.png')


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 9 — คำตอบสมบูรณ์: อินพุตทั้งหมด + Y + W เรียงบนแกนเวลาเดียวกัน
# ═══════════════════════════════════════════════════════════════════════════
def fig09_final_answer():
    fig, ax = plt.subplots(figsize=(15.6, 11.4))
    span = X1 + 1 - X0
    ax.set_xlim(X0 - span * 0.095, X1 + 1 + span * 0.05)
    ax.set_ylim(-1.95, 11.40); ax.axis('off')

    ax.text((X0 + X1) / 2, 11.05, 'คำตอบ — รูปคลื่นเอาต์พุต $Y$ และ $W$',
            ha='center', fontsize=21, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 10.62,
            'อินพุตด้านบน (ตามที่โจทย์ให้) · คำตอบด้านล่างในกรอบ — อ่านเทียบกันได้ตรงแกนเวลาเดียวกัน',
            ha='center', fontsize=12.5, color='#475569', style='italic')

    h = 0.545
    inputs = [('A', 'A', C_SEL, 9.30), ('B', 'B', C_SEL, 8.36),
              ('C', 'C', C_SEL, 7.42), ('E', 'E', C_EN, 6.48),
              ('D0', '$D_0$', C_DATA, 5.36), ('D2', '$D_2$', C_DATA, 4.42)]

    disable_bands(ax, 0.28, 9.98)
    slot_grid(ax, 9.98, 0.28, show_labels=True, label_y=10.02, fs=13)

    for sig, lab, col, yb in inputs:
        ax.plot([X0, X1 + 1], [yb, yb], color=C_GRID, lw=0.8, zorder=1)
        ax.plot([X0, X1 + 1], [yb + h, yb + h], color=C_GRID, lw=0.8, zorder=1)
        draw_wave(ax, RUNS[sig], yb, h, col, lw=2.4)
        wave_label(ax, X0 - span * 0.020, yb + h / 2, lab, col, fs=16)

    ax.text(X0 - span * 0.088, 8.60, 'อินพุต\nที่โจทย์ให้', ha='center',
            va='center', fontsize=11, color='#64748B', style='italic')

    # กรอบเน้นคำตอบ
    ans_top, ans_bot = 3.62, 0.34
    ax.add_patch(Rectangle((X0 - span * 0.045, ans_bot), span * 1.055,
                           ans_top - ans_bot, facecolor='#F0FDF4',
                           edgecolor='#059669', lw=2.6, zorder=0.5))
    ax.text(X0 - span * 0.020, 3.30, 'คำตอบ', ha='left', va='center',
            fontsize=13, color='#059669', fontweight='bold')

    for sig_runs, lab, col, yb in [(Y_RUNS, '$Y$', C_Y, 2.30),
                                   (W_RUNS, '$W$', C_W, 0.86)]:
        ax.plot([X0, X1 + 1], [yb, yb], color='#BBF7D0', lw=0.9, zorder=1)
        ax.plot([X0, X1 + 1], [yb + h * 1.18, yb + h * 1.18],
                color='#BBF7D0', lw=0.9, zorder=1)
        draw_wave(ax, sig_runs, yb, h * 1.18, col, lw=3.4)
        wave_label(ax, X0 - span * 0.020, yb + h * 0.59, lab, col, fs=20)

    ax.text(X1 + 1 + span * 0.008, 2.30 + h * 0.59, 'ค่าจริง', ha='left',
            va='center', fontsize=10.5, color=C_Y, style='italic')
    ax.text(X1 + 1 + span * 0.008, 0.86 + h * 0.59, '$=\\overline{Y}$', ha='left',
            va='center', fontsize=13, color=C_W, fontweight='bold')

    # แถวข้อมูลสรุปใต้กราฟ
    ax.text(X0 - span * 0.020, -0.20, 'ช่องที่เลือก', ha='right', va='center',
            fontsize=11.5, color=C_INK, fontweight='bold')
    ax.text(X0 - span * 0.020, -0.68, 'ต่อกับ', ha='right', va='center',
            fontsize=11.5, color=C_INK, fontweight='bold')
    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        xc = (xs + xe) / 2
        c, b, a, n = sel_code(xs)
        ax.text(xc, -0.20, f'$D_{n}$', ha='center', va='center',
                fontsize=12.5, color=C_SEL, fontweight='bold')
        srclabel = CH_SRC[n][1]
        ax.text(xc, -0.68, srclabel, ha='center', va='center',
                fontsize=11, color=C_DATA)

    ax.text((X0 + X1) / 2, -1.42,
            'ขณะ $E=1$ (พื้นสีแดงอ่อน ต้นและปลายกราฟ) ไอซีถูกปิด → บังคับ $Y=0$ และ $W=1$ '
            'โดยไม่สนใจ $C,B,A$ และไม่สนใจสัญญาณข้อมูลเลย',
            ha='center', va='center', fontsize=12, color=C_EN, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.48', facecolor='#FEF2F2',
                      edgecolor=C_EN, lw=1.5))
    finish(fig, '09_final_answer.png')


# ═══════════════════════════════════════════════════════════════════════════
# รูปที่ 10 — ตารางสรุปคำตอบรายช่วง (ใช้ทบทวนก่อนสอบ)
# ═══════════════════════════════════════════════════════════════════════════
def fig10_summary_table():
    fig, ax = plt.subplots(figsize=(15.6, 9.6))
    ax.set_xlim(0, 15.6); ax.set_ylim(0, 9.6); ax.axis('off')

    ax.text(7.8, 9.18, 'ตารางสรุปคำตอบรายช่วงเวลา (ใช้ทบทวนก่อนสอบ)',
            ha='center', fontsize=19, fontweight='bold', color=C_INK)
    ax.text(7.8, 8.70,
            'ช่วงที่ 2 และ 9 มีเครื่องหมาย (*) เพราะ $E$ เปลี่ยนค่ากลางช่วง จึงต้องแยกเป็น 2 ส่วนย่อย',
            ha='center', fontsize=11.5, color='#B91C1C', style='italic')

    heads = ['ช่วง', 'C B A', 'ช่อง', 'ช่องต่อกับ', '$E$', 'ผล $Y$ ในช่วงนี้', 'ผล $W=\\overline{Y}$']
    wcol = [0.90, 1.28, 0.96, 2.28, 0.94, 4.34, 4.34]
    tx, ty, rh = 0.28, 7.95, 0.545
    xoff = [0]
    for w in wcol[:-1]:
        xoff.append(xoff[-1] + w)
    total_w = sum(wcol)

    for j, (hd, w) in enumerate(zip(heads, wcol)):
        ax.add_patch(Rectangle((tx + xoff[j], ty), w, rh * 1.06,
                               facecolor='#1E293B', edgecolor=C_INK, lw=1.4, zorder=2))
        ax.text(tx + xoff[j] + w / 2, ty + rh * 0.53, hd, ha='center', va='center',
                fontsize=12, color='white', fontweight='bold', zorder=3)

    def describe(runs, lo='0', hi='1'):
        """แปลง run เป็นข้อความอ่านง่าย"""
        if len(runs) == 1:
            return f'คงที่ {hi if runs[0][0] else lo} ทั้งช่วง'
        parts = []
        for v, s, e in runs:
            parts.append(f'{hi if v else lo}')
        return ' → '.join(parts) + f'  ({len(runs)} ท่อน)'

    for i in range(NSLOT):
        xs, xe = SLOT_EDGES[i], SLOT_EDGES[i + 1]
        c, b, a, n = sel_code(xs)
        yy = ty - (i + 1) * rh
        split = len(to_runs(lambda x: val('E', x), xs, xe - 1)) > 1
        base_fc = '#FEF2F2' if split else ('#FFFFFF' if i % 2 else '#F8FAFC')
        for j, w in enumerate(wcol):
            ax.add_patch(Rectangle((tx + xoff[j], yy), w, rh,
                                   facecolor=base_fc, edgecolor=C_GRID,
                                   lw=1.0, zorder=2))

        yruns = to_runs(Yf, xs, xe - 1)
        wruns = to_runs(Wf, xs, xe - 1)
        eruns = to_runs(lambda x: val('E', x), xs, xe - 1)
        edesc = '/'.join(str(v) for v, _, _ in eruns)

        cells = [
            (f'{i+1}' + (' (*)' if split else ''), C_INK, 'bold' if split else 'normal'),
            (f'{c} {b} {a}', C_SEL, 'bold'),
            (f'$D_{n}$', C_INK, 'bold'),
            (CH_SRC[n][1], C_DATA, 'bold'),
            (edesc, C_EN, 'bold'),
            (describe(yruns), C_Y, 'bold'),
            (describe(wruns), C_W, 'bold'),
        ]
        for j, (txt, col, fw) in enumerate(cells):
            ax.text(tx + xoff[j] + wcol[j] / 2, yy + rh / 2, txt,
                    ha='center', va='center', fontsize=11.2,
                    color=col, fontweight=fw, zorder=3)

    ybot = ty - NSLOT * rh

    # กล่องสรุปคำตอบสุดท้าย
    ax.text(tx, ybot - 0.44, 'คำตอบในรูปลำดับลอจิก (นับจากซ้ายไปขวา):',
            ha='left', fontsize=12.5, fontweight='bold', color=C_INK)
    yseq = ''.join(str(v) for v, _, _ in Y_RUNS)
    wseq = ''.join(str(v) for v, _, _ in W_RUNS)
    ax.text(tx + 0.10, ybot - 0.92,
            f'$Y$  :  {yseq}      ({len(Y_RUNS)} ท่อน)',
            ha='left', fontsize=13, color=C_Y, fontweight='bold')
    ax.text(tx + 0.10, ybot - 1.34,
            f'$W$  :  {wseq}      ({len(W_RUNS)} ท่อน)  — เป็นส่วนกลับของ $Y$ ทุกจุด',
            ha='left', fontsize=13, color=C_W, fontweight='bold')

    ax.text(tx + total_w, ybot - 1.14,
            'กฎที่ใช้ตลอดข้อ:\n'
            '$E=1 \\Rightarrow Y=0,\\ W=1$ (บังคับ)\n'
            '$E=0 \\Rightarrow Y=D_n,\\ n=4C+2B+A$\n'
            '$W=\\overline{Y}$ เสมอ',
            ha='right', va='top', fontsize=11.5, color=C_INK,
            bbox=dict(boxstyle='round,pad=0.50', facecolor='#EFF6FF',
                      edgecolor=C_SEL, lw=1.6))
    finish(fig, '10_summary_table.png')


# ═══════════════════════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('สร้างสื่อประกอบเฉลย MUX/DMUX ข้อที่ 1 (รูปที่ 3.40)')
    print('-' * 62)
    fig01_mux_concept()
    fig02_74151_table()
    fig03_circuit()
    fig04_input_waves()
    fig05_counter()
    fig06_enable()
    fig07_inverted()
    fig08_slot_by_slot()
    fig09_final_answer()
    fig10_summary_table()
    print('-' * 62)
    print(f'เสร็จสิ้น — บันทึกไว้ที่ {OUT}')
