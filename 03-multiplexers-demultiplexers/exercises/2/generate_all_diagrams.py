#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_all_diagrams.py
────────────────────────────────────────────────────────────────────────────
สร้างสื่อประกอบเฉลยข้อสอบ MUX/DMUX ข้อที่ 2 (Special DEMUX Problem — IC 74138)
ระบบการรวมส่งสัญญาณและแยกรับสัญญาณแบบแบ่งเวลา (TDM Communication System)
เชื่อมต่อโดยตรงกับสัญญาณและวงจร MUX 74151 จากข้อที่ 1

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
C_EN      = '#DC2626'   # อีนาเบิล E / G1
C_DATA    = '#7C3AED'   # ข้อมูล D0, D2
C_Y       = '#059669'   # เอาต์พุต MUX Y / ข้อมูลสายส่ง
C_W       = '#EA580C'   # เอาต์พุต MUX W
C_DMUX    = '#0891B2'   # สัญญาณ DMUX Y0'..Y7'
C_REC     = '#2563EB'   # สัญญาณกู้คืน R0..R7
C_GATE    = '#9333EA'   # เอาต์พุตเกต F
C_DIS     = '#FEE2E2'   # แถบช่วงดิสเอเบิล
C_ACT     = '#ECFDF5'   # แถบช่วงแอ็กทีฟ
C_BOX     = '#F1F5F9'
C_HI      = '#FEF3C7'

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

# แผนที่ช่องสัญญาณภาคส่ง (MUX 74151 จากข้อที่ 1)
CH_SRC = {
    0: ('D0',  'D₀',             lambda x: val('D0', x)),
    1: ('+5V', '+5 V (1)',       lambda x: 1),
    2: ('D2',  'D₂',             lambda x: val('D2', x)),
    3: ('GND', 'GND (0)',        lambda x: 0),
    4: ('~D0', 'D̄₀',             lambda x: 1 - val('D0', x)),
    5: ('GND', 'GND (0)',        lambda x: 0),
    6: ('~D2', 'D̄₂',             lambda x: 1 - val('D2', x)),
    7: ('+5V', '+5 V (1)',       lambda x: 1),
}

def sel_code(x):
    a, b, c = val('A', x), val('B', x), val('C', x)
    return c, b, a, 4 * c + 2 * b + a

def Yf(x):
    """เอาต์พุต MUX 74151 จากข้อ 1 (สายส่งข้อมูล TDM Data Bus)"""
    if val('E', x) == 1:
        return 0
    return CH_SRC[sel_code(x)[3]][2](x)

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

# คำนวณสัญญาณ DMUX 74138:
# G1 = Y(x), G2A' = 0, G2B' = 0
# เมื่อ G1 = 1 และแอดเดรสตรงกับช่อง k: Yk' = 0 (Active-LOW pulse)
# ช่องอื่นๆ ที่ไม่ถูกเลือก หรือเมื่อ G1 = 0: ค้างที่ 1 เสมอ
def dmux_out_k(k):
    def fn(x):
        c, b, a, n = sel_code(x)
        data = Yf(x)
        if n == k and data == 1:
            return 0  # Active-LOW output pulse
        return 1      # Inactive / unselected state
    return fn

def rec_out_k(k):
    """สัญญาณกู้คืนปลายทาง R_k = (Yk')'"""
    def fn(x):
        return 1 - dmux_out_k(k)(x)
    return fn

def gate_F(x):
    """เอาต์พุตเกต NAND: F = (Y1' · Y4' · Y7')' = Y1 + Y4 + Y7"""
    y1 = dmux_out_k(1)(x)
    y4 = dmux_out_k(4)(x)
    y7 = dmux_out_k(7)(x)
    return 1 if (y1 == 0 or y4 == 0 or y7 == 0) else 0

Y_RUNS = to_runs(Yf)
DMUX_RUNS = [to_runs(dmux_out_k(k)) for k in range(8)]
REC_RUNS = [to_runs(rec_out_k(k)) for k in range(8)]
F_RUNS = to_runs(gate_F)

# ═══════════════════════════════════════════════════════════════════════════
# ตัวช่วยวาดรูปคลื่น
# ═══════════════════════════════════════════════════════════════════════════

def draw_wave(ax, runs, ybase, h, color, lw=2.4, ls='-'):
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
            ax.text(xc, ly, f"ช่วง {i+1}\n(n={n})", ha='center', va='bottom',
                    fontsize=fs, color=C_INK, fontweight='bold', clip_on=False)

def disable_bands(ax, ybot, ytop, alpha=0.8):
    for v, s, e in RUNS['E']:
        if v == 1:
            ax.add_patch(Rectangle((s, ybot), e + 1 - s, ytop - ybot,
                                   facecolor=C_DIS, edgecolor='none',
                                   zorder=0, alpha=alpha, clip_on=False))

def wave_label(ax, x, y, text, color, fs=13):
    ax.text(x, y, text, ha='right', va='center', fontsize=fs,
            color=color, fontweight='bold', clip_on=False)

def finish(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=DPI, facecolor=C_BG, bbox_inches='tight', pad_inches=0.25)
    plt.close(fig)
    kb = os.path.getsize(path) / 1024
    print(f"  ✓ {name}  ({kb:.0f} KB)")

# ═══════════════════════════════════════════════════════════════════════════
# 1. 01_dmux_concept.png
# ═══════════════════════════════════════════════════════════════════════════
def fig01_dmux_concept():
    fig, ax = plt.subplots(figsize=(13.6, 8.2))
    ax.set_xlim(0, 13.6); ax.set_ylim(0, 8.2); ax.axis('off')

    ax.text(6.8, 7.80, 'ดีมัลติเพล็กเซอร์ (Demultiplexer / DMUX) คืออะไร?',
            ha='center', fontsize=20, fontweight='bold', color=C_INK)
    ax.text(6.8, 7.32, 'อุปกรณ์กระจายสัญญาณข้อมูล (Data Distributor) — รับสัญญาณ 1 ช่อง แล้วกระจายออกไปยัง 1 ใน 2ⁿ ช่องเอาต์พุต',
            ha='center', fontsize=12.5, color='#475569')

    # ฝั่งซ้าย: อุปมาสวิตช์หมุนกระจายข้อมูล
    ax.text(3.4, 6.70, 'เปรียบเทียบ: สวิตช์หมุนกระจายข้อมูล (1:8 DMUX)',
            ha='center', fontsize=14, fontweight='bold', color=C_DMUX)
    box = Rectangle((1.2, 1.8), 4.4, 4.5, facecolor=C_BOX, edgecolor=C_INK, lw=2.0, zorder=1)
    ax.add_patch(box)

    # อินพุตข้อมูลเดี่ยว
    piv = (2.2, 4.05)
    ax.plot([0.3, piv[0]], [piv[1], piv[1]], color=C_Y, lw=3.0, zorder=3)
    ax.add_patch(Circle(piv, 0.11, facecolor=C_INK, edgecolor=C_INK, zorder=6))
    ax.text(0.2, piv[1], 'Data Input (D)', ha='right', va='center', fontsize=12.5, color=C_Y, fontweight='bold')

    # เอาต์พุต 8 ช่อง
    cy_top, cy_bot = 5.8, 2.3
    contacts = []
    for i in range(8):
        y = cy_top - i * (cy_top - cy_bot) / 7
        cx = 4.6
        ax.plot([cx, 5.6], [y, y], color=C_INK, lw=1.5, zorder=2)
        ax.plot([5.6, 6.3], [y, y], color=C_INK, lw=1.5, zorder=2)
        ax.add_patch(Circle((cx, y), 0.065, facecolor=C_INK, edgecolor=C_INK, zorder=4))
        ax.text(6.45, y, f'Ȳ{i}', ha='left', va='center', fontsize=12, color=C_INK, fontweight='bold')
        contacts.append((cx, y))

    # ก้านสวิตช์ชี้ไปช่อง Y2
    tgt = contacts[2]
    ax.plot([piv[0], tgt[0]], [piv[1], tgt[1]], color=C_DMUX, lw=3.4, zorder=5, solid_capstyle='round')
    ax.add_patch(Circle(tgt, 0.12, facecolor='none', edgecolor=C_DMUX, lw=2.5, zorder=6))
    ax.text(tgt[0] - 0.7, tgt[1] + 0.35, 'เลือกส่งออก\nช่อง Ȳ₂', fontsize=10.5, color=C_DMUX, fontweight='bold', va='bottom')

    # ขาเลือก S2, S1, S0
    for k, lab in enumerate(['S₂ (C)', 'S₁ (B)', 'S₀ (A)']):
        x = 2.4 + k * 0.9
        ax.plot([x, x], [0.9, 1.8], color=C_SEL, lw=2.0, zorder=3)
        ax.text(x, 0.7, lab, ha='center', va='top', fontsize=10.5, color=C_SEL, fontweight='bold')
    ax.text(3.3, 0.25, 'ขาเลือกแอดเดรส (Select Lines)', ha='center', fontsize=11, color=C_SEL, style='italic')

    # ฝั่งขวา: การเปรียบเทียบ MUX vs DMUX
    ax.text(10.0, 6.70, 'เปรียบเทียบโครงสร้าง MUX vs DMUX',
            ha='center', fontsize=14, fontweight='bold', color=C_INK)

    box_cmp = Rectangle((7.2, 1.8), 5.8, 4.5, facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.5)
    ax.add_patch(box_cmp)

    comp_items = [
        ("คุณสมบัติ", "มัลติเพล็กเซอร์ (MUX)", "ดีมัลติเพล็กเซอร์ (DMUX)"),
        ("บทบาทหลัก", "รวมสาย / เลือกข้อมูล (Data Selector)", "กระจายสาย / แจกจ่าย (Data Distributor)"),
        ("ทิศทางข้อมูล", "2ⁿ อินพุต → 1 เอาต์พุต", "1 อินพุต → 2ⁿ เอาต์พุต"),
        ("ขาเลือกแอดเดรส", "n ขา (ชี้ช่องอินพุตที่จะส่ง)", "n ขา (ชี้ช่องเอาต์พุตที่จะรับ)"),
        ("ไอซีมาตรฐาน", "74151 (8:1), 74150 (16:1)", "74138 (1:8), 74154 (1:16)"),
        ("ลอจิกเอาต์พุต", "True (Y) และ Invert (W)", "Active-LOW (Ȳ₀..Ȳ₇)"),
        ("ในระบบสื่อสาร", "ภาคส่ง (Transmitter)", "ภาครับ (Receiver)")
    ]

    ty = 5.9
    for row_idx, (c1, c2, c3) in enumerate(comp_items):
        weight = 'bold' if row_idx == 0 else 'normal'
        bg = '#F8FAFC' if row_idx % 2 == 1 else '#FFFFFF'
        if row_idx == 0: bg = '#EEF2F6'
        rect = Rectangle((7.3, ty - 0.28), 5.6, 0.52, facecolor=bg, edgecolor='none', zorder=2)
        ax.add_patch(rect)
        ax.text(7.45, ty, c1, fontsize=9.5, fontweight=weight, color=C_INK, va='center', zorder=3)
        ax.text(8.8, ty, c2, fontsize=9.5, fontweight=weight, color=C_Y if row_idx > 0 else C_INK, va='center', zorder=3)
        ax.text(10.8, ty, c3, fontsize=9.5, fontweight=weight, color=C_DMUX if row_idx > 0 else C_INK, va='center', zorder=3)
        ty -= 0.56

    finish(fig, '01_dmux_concept.png')

# ═══════════════════════════════════════════════════════════════════════════
# 2. 02_74138_function_table.png
# ═══════════════════════════════════════════════════════════════════════════
def fig02_74138_function_table():
    fig, ax = plt.subplots(figsize=(14.0, 8.8))
    ax.set_xlim(0, 14.0); ax.set_ylim(0, 8.8); ax.axis('off')

    ax.text(7.0, 8.35, 'ตารางแสดงการทำงานของไอซี 74138 (3-to-8 Line Decoder / Demultiplexer)',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text(7.0, 7.95, 'อ้างอิงจากสไลด์บรรยาย 305241_lecture.pdf หน้า 86-90 (เลขหน้าในเล่ม 73-77)',
            ha='center', fontsize=12, color='#64748B')

    # ตารางฟังก์ชันหลัก
    headers = ['Enable\nG1', 'Enable\nḠ2A', 'Enable\nḠ2B', 'Select\nC (MSB)', 'Select\nB', 'Select\nA (LSB)',
               'Ȳ₀', 'Ȳ₁', 'Ȳ₂', 'Ȳ₃', 'Ȳ₄', 'Ȳ₅', 'Ȳ₆', 'Ȳ₇', 'สถานะการทำงาน']
    
    col_x = [0.8, 1.6, 2.4, 3.4, 4.1, 4.8, 5.7, 6.4, 7.1, 7.8, 8.5, 9.2, 9.9, 10.6, 12.2]

    # วาดหัวตาราง
    ax.add_patch(Rectangle((0.4, 6.7), 13.2, 0.9, facecolor=C_INK, edgecolor='none'))
    for i, h in enumerate(headers):
        ax.text(col_x[i], 7.15, h, ha='center', va='center', color='#FFFFFF', fontsize=9.5, fontweight='bold')

    rows = [
        (['0', 'X', 'X', 'X', 'X', 'X'], ['1', '1', '1', '1', '1', '1', '1', '1'], 'Disabled (G1=0 บังคับ High หมด)', '#FEF2F2'),
        (['X', '1', 'X', 'X', 'X', 'X'], ['1', '1', '1', '1', '1', '1', '1', '1'], 'Disabled (Ḡ2A=1 บังคับ High หมด)', '#FEF2F2'),
        (['X', 'X', '1', 'X', 'X', 'X'], ['1', '1', '1', '1', '1', '1', '1', '1'], 'Disabled (Ḡ2B=1 บังคับ High หมด)', '#FEF2F2'),
        (['1', '0', '0', '0', '0', '0'], ['0', '1', '1', '1', '1', '1', '1', '1'], 'Active: เลือกช่อง Ȳ₀ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '0', '0', '1'], ['1', '0', '1', '1', '1', '1', '1', '1'], 'Active: เลือกช่อง Ȳ₁ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '0', '1', '0'], ['1', '1', '0', '1', '1', '1', '1', '1'], 'Active: เลือกช่อง Ȳ₂ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '0', '1', '1'], ['1', '1', '1', '0', '1', '1', '1', '1'], 'Active: เลือกช่อง Ȳ₃ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '1', '0', '0'], ['1', '1', '1', '1', '0', '1', '1', '1'], 'Active: เลือกช่อง Ȳ₄ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '1', '0', '1'], ['1', '1', '1', '1', '1', '0', '1', '1'], 'Active: เลือกช่อง Ȳ₅ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '1', '1', '0'], ['1', '1', '1', '1', '1', '1', '0', '1'], 'Active: เลือกช่อง Ȳ₆ (Active-LOW)', '#ECFDF5'),
        (['1', '0', '0', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '0'], 'Active: เลือกช่อง Ȳ₇ (Active-LOW)', '#ECFDF5'),
    ]

    ry = 6.25
    for r_idx, (inps, outs, desc, bg) in enumerate(rows):
        rect = Rectangle((0.4, ry - 0.22), 13.2, 0.44, facecolor=bg, edgecolor='#E2E8F0', lw=0.8)
        ax.add_patch(rect)
        for i, val in enumerate(inps):
            fw = 'bold' if val in ['0', '1'] and r_idx >= 3 else ('bold' if val == '0' and i==0 or val=='1' and i in [1,2] else 'normal')
            c = C_EN if i < 3 else C_SEL
            ax.text(col_x[i], ry, val, ha='center', va='center', fontsize=10, color=c, fontweight=fw)
        for j, val in enumerate(outs):
            c = C_EN if val == '0' else '#64748B'
            fw = 'bold' if val == '0' else 'normal'
            ax.text(col_x[6 + j], ry, val, ha='center', va='center', fontsize=10.5, color=c, fontweight=fw)
        ax.text(col_x[14], ry, desc, ha='center', va='center', fontsize=9, color=C_INK)
        ry -= 0.46

    # กล่องสรุปกฎ 3 ข้อ
    ax.add_patch(Rectangle((0.4, 0.4), 13.2, 0.85, facecolor='#FFFBEB', edgecolor='#F59E0B', lw=1.5))
    ax.text(0.7, 0.95, '★ หัวใจสำคัญของ IC 74138:', fontsize=11, fontweight='bold', color='#B45309')
    ax.text(0.7, 0.65, '1. ไอซีทำงานเมื่อ G1=1 AND Ḡ2A=0 AND Ḡ2B=0 เท่านั้น  |  2. เมื่อไอซีทำงาน ช่องที่ถูกเลือกจะมีค่าเป็น 0 (Active-LOW) ช่องอื่นเป็น 1 ทั้งหมด  |  3. เมื่อไอซีถูกปิด ทุกเอาต์พุตจะเป็น 1',
            fontsize=9.8, color=C_INK)

    finish(fig, '02_74138_function_table.png')

# ═══════════════════════════════════════════════════════════════════════════
# 3. 03_tdm_system_circuit.png
# ═══════════════════════════════════════════════════════════════════════════
def fig03_tdm_system_circuit():
    fig, ax = plt.subplots(figsize=(15.0, 9.0))
    ax.set_xlim(0, 15.0); ax.set_ylim(0, 9.0); ax.axis('off')

    ax.text(7.5, 8.65, 'ผังวงจรระบบรับส่งข้อมูล TDM ด้วย MUX 74151 และ DMUX 74138 (โจทย์ข้อที่ 2)',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text(7.5, 8.25, 'ภาคส่ง (ซ้าย: MUX 74151 จากข้อ 1) → สายส่งข้อมูลอนุกรม (กลาง: Data Bus) → ภาครับ (ขวา: DMUX 74138 + NAND Gate)',
            ha='center', fontsize=11.5, color='#475569')

    # กล่องกรอบภาคส่ง
    ax.add_patch(Rectangle((0.6, 1.0), 5.2, 6.9, facecolor='#FAF8F5', edgecolor='#94A3B8', lw=1.5, ls='--'))
    ax.text(3.2, 7.6, '【 ภาคส่งข้อมูล (Transmitter) 】\nวงจร MUX 74151 จากข้อที่ 1', ha='center', fontsize=11, fontweight='bold', color=C_INK)

    # ตัวถัง IC 74151
    ax.add_patch(Rectangle((2.4, 2.2), 2.8, 5.0, facecolor='#FFFFFF', edgecolor=C_INK, lw=2.0))
    ax.text(3.8, 6.7, '74151\n8:1 MUX', ha='center', fontsize=12, fontweight='bold', color=C_INK)

    # ขาข้อมูล D0..D7 ของ 74151
    pins_mux = ['D₀ (Waveform)', 'D₁ (+5V)', 'D₂ (Waveform)', 'D₃ (GND)', 'D₄ (D̄₀)', 'D₅ (GND)', 'D₆ (D̄₂)', 'D₇ (+5V)']
    for i in range(8):
        py = 6.2 - i * 0.52
        ax.plot([1.0, 2.4], [py, py], color=C_INK, lw=1.2)
        ax.text(0.9, py, pins_mux[i], ha='right', va='center', fontsize=8.5, color=C_INK)

    # ขาเลือกและ Enable ของ 74151
    ax.plot([3.1, 3.1], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.plot([3.8, 3.8], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.plot([4.5, 4.5], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.text(3.1, 1.1, 'A', ha='center', fontsize=10, fontweight='bold', color=C_SEL)
    ax.text(3.8, 1.1, 'B', ha='center', fontsize=10, fontweight='bold', color=C_SEL)
    ax.text(4.5, 1.1, 'C', ha='center', fontsize=10, fontweight='bold', color=C_SEL)

    # ขา Enable E ของ 74151
    ax.plot([2.0, 2.4], [2.6, 2.6], color=C_EN, lw=1.8)
    ax.add_patch(Circle((2.35, 2.6), 0.06, facecolor='#FFF', edgecolor=C_EN, lw=1.5))
    ax.text(1.9, 2.6, 'E (Active-LOW)', ha='right', va='center', fontsize=9, fontweight='bold', color=C_EN)

    # สายส่งข้อมูลอนุกรม (Serial Data Line Y)
    ax.plot([5.2, 8.8], [5.0, 5.0], color=C_Y, lw=3.5, zorder=5)
    ax.annotate('', xy=(8.7, 5.0), xytext=(5.3, 5.0),
                arrowprops=dict(arrowstyle="->", color=C_Y, lw=2.5))
    ax.add_patch(Rectangle((6.2, 5.25), 2.2, 0.9, facecolor='#ECFDF5', edgecolor=C_Y, lw=1.5))
    ax.text(7.3, 5.85, 'สายส่งข้อมูลอนุกรม (TDM)', ha='center', fontsize=9, color=C_Y, fontweight='bold')
    ax.text(7.3, 5.45, 'Data = Y (จากข้อ 1)', ha='center', fontsize=10.5, color=C_Y, fontweight='bold')

    # กล่องกรอบภาครับ
    ax.add_patch(Rectangle((8.2, 1.0), 6.4, 6.9, facecolor='#F0F9FF', edgecolor='#0284C7', lw=1.5, ls='--'))
    ax.text(11.4, 7.6, '【 ภาครับข้อมูล (Receiver) 】\nวงจร DMUX 74138 + เกตสังเคราะห์ฟังก์ชัน F', ha='center', fontsize=11, fontweight='bold', color='#0369A1')

    # ตัวถัง IC 74138
    ax.add_patch(Rectangle((8.8, 2.2), 2.8, 5.0, facecolor='#FFFFFF', edgecolor=C_INK, lw=2.0))
    ax.text(10.2, 6.7, '74138\n1:8 DMUX', ha='center', fontsize=12, fontweight='bold', color=C_INK)

    # ขาอินพุตของ 74138
    # ขา G1 ต่อกับ Data Line Y
    ax.text(8.9, 5.0, 'G1 (Pin 6)', ha='left', va='center', fontsize=8.5, fontweight='bold', color=C_Y)
    # ขา G2A' และ G2B' ต่อ GND
    ax.plot([8.2, 8.8], [3.8, 3.8], color=C_INK, lw=1.5)
    ax.plot([8.2, 8.8], [3.2, 3.2], color=C_INK, lw=1.5)
    ax.add_patch(Circle((8.75, 3.8), 0.05, facecolor='#FFF', edgecolor=C_INK, lw=1.2))
    ax.add_patch(Circle((8.75, 3.2), 0.05, facecolor='#FFF', edgecolor=C_INK, lw=1.2))
    ax.text(8.1, 3.8, 'Ḡ2A → GND', ha='right', va='center', fontsize=8.5, color=C_INK)
    ax.text(8.1, 3.2, 'Ḡ2B → GND', ha='right', va='center', fontsize=8.5, color=C_INK)

    # ขาเลือกของ 74138 ซิงค์กับภาคส่ง
    ax.plot([9.5, 9.5], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.plot([10.2, 10.2], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.plot([10.9, 10.9], [1.3, 2.2], color=C_SEL, lw=1.8)
    ax.text(9.5, 1.1, 'A', ha='center', fontsize=10, fontweight='bold', color=C_SEL)
    ax.text(10.2, 1.1, 'B', ha='center', fontsize=10, fontweight='bold', color=C_SEL)
    ax.text(10.9, 1.1, 'C', ha='center', fontsize=10, fontweight='bold', color=C_SEL)

    # ขาเอาต์พุต 74138 (Y0'..Y7')
    y_out_pos = {}
    for i in range(8):
        py = 6.2 - i * 0.52
        y_out_pos[i] = py
        ax.plot([11.6, 12.3], [py, py], color=C_DMUX, lw=1.5)
        ax.add_patch(Circle((11.65, py), 0.045, facecolor='#FFF', edgecolor=C_DMUX, lw=1.2))
        ax.text(12.35, py, f'Ȳ{i}', ha='left', va='center', fontsize=9, fontweight='bold', color=C_DMUX)

    # เกต NAND รวมสัญญาณ Y1', Y4', Y7'
    nand_x = 13.4
    nand_y = 4.2
    # ลากสายจาก Y1', Y4', Y7' เข้า NAND
    ax.plot([12.6, 13.0, 13.0, 13.3], [y_out_pos[1], y_out_pos[1], nand_y + 0.35, nand_y + 0.35], color=C_GATE, lw=1.3)
    ax.plot([12.6, 13.3], [y_out_pos[4], nand_y], color=C_GATE, lw=1.3)
    ax.plot([12.6, 13.0, 13.0, 13.3], [y_out_pos[7], y_out_pos[7], nand_y - 0.35, nand_y - 0.35], color=C_GATE, lw=1.3)

    # สัญลักษณ์ NAND
    ax.plot([13.3, 13.3, 13.7], [nand_y - 0.5, nand_y + 0.5, nand_y + 0.5], color=C_INK, lw=1.8)
    ax.plot([13.3, 13.7], [nand_y - 0.5, nand_y - 0.5], color=C_INK, lw=1.8)
    arc = plt.matplotlib.patches.Arc((13.7, nand_y), 0.8, 1.0, angle=0, theta1=-90, theta2=90, color=C_INK, lw=1.8)
    ax.add_patch(arc)
    ax.add_patch(Circle((14.15, nand_y), 0.055, facecolor='#FFF', edgecolor=C_INK, lw=1.5))
    ax.plot([14.22, 14.8], [nand_y, nand_y], color=C_GATE, lw=2.5)
    ax.text(14.85, nand_y, 'F', ha='left', va='center', fontsize=14, fontweight='bold', color=C_GATE)
    ax.text(13.6, nand_y - 0.85, 'F = (Ȳ₁·Ȳ₄·Ȳ₇)′\n  = Y₁ + Y₄ + Y₇', ha='center', fontsize=8.5, color=C_GATE, fontweight='bold')

    finish(fig, '03_tdm_system_circuit.png')

# ═══════════════════════════════════════════════════════════════════════════
# 4. 04_input_and_data_waveforms.png
# ═══════════════════════════════════════════════════════════════════════════
def fig04_input_and_data_waveforms():
    fig, ax = plt.subplots(figsize=(14.0, 9.2))
    ax.set_xlim(X0 - 30, X1 + 30); ax.set_ylim(-0.8, 7.8); ax.axis('off')

    ax.text((X0 + X1) / 2, 7.55, 'รูปคลื่นอินพุตและสัญญาณข้อมูลสายส่งอนุกรม Data = Y (โจทย์ข้อที่ 2)',
            ha='center', fontsize=17, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 7.15, 'ถอดรหัสรหัสตัวนับ CBA ใน 9 ช่วงเวลา พร้อมสัญญาณ Enable E และข้อมูล D0, D2',
            ha='center', fontsize=11.5, color='#475569')

    slot_grid(ax, 6.7, -0.4, show_labels=True, label_y=6.75)
    disable_bands(ax, -0.4, 6.7, alpha=0.5)

    signals = [
        ('A (LSB)', RUNS['A'], 5.8, C_SEL),
        ('B',       RUNS['B'], 4.8, C_SEL),
        ('C (MSB)', RUNS['C'], 3.8, C_SEL),
        ('E (Enable MUX)', RUNS['E'], 2.8, C_EN),
        ('D₀',      RUNS['D0'], 1.8, C_DATA),
        ('D₂',      RUNS['D2'], 0.8, C_DATA),
        ('Data = Y (สายส่ง)', Y_RUNS, -0.2, C_Y),
    ]

    for name, r, yb, col in signals:
        lw = 3.0 if 'สายส่ง' in name else 2.2
        draw_wave(ax, r, yb, 0.55, col, lw=lw)
        wave_label(ax, X0 - 35, yb + 0.28, name, col, fs=11)

    finish(fig, '04_input_and_data_waveforms.png')

# ═══════════════════════════════════════════════════════════════════════════
# 5. 05_enable_and_select_decoding.png
# ═══════════════════════════════════════════════════════════════════════════
def fig05_enable_and_select_decoding():
    fig, ax = plt.subplots(figsize=(14.0, 8.5))
    ax.set_xlim(0, 14.0); ax.set_ylim(0, 8.5); ax.axis('off')

    ax.text(7.0, 8.1, 'การถอดรหัสเลขที่อยู่ (CBA) และเงื่อนไขการเปิด-ปิด IC 74138 ใน 9 ช่วงเวลา',
            ha='center', fontsize=17, fontweight='bold', color=C_INK)
    ax.text(7.0, 7.65, 'พิจารณาขา G1 = Data(Y), Ḡ2A = 0, Ḡ2B = 0 เพื่อดูว่าช่วงใดและช่องใดที่ 74138 จะแอ็กทีฟ',
            ha='center', fontsize=11.5, color='#475569')

    # กล่องตารางสรุป 9 ช่วงเวลา
    table_headers = ['ช่วงที่', 'พิกัดเวลา x', 'CBA', 'แอดเดรส n', 'Enable E', 'Data Y', 'สถานะ 74138', 'ช่องที่ถูกเลือก', 'พฤติกรรมเอาต์พุต 74138']
    col_pos = [0.8, 2.0, 3.3, 4.4, 5.5, 6.6, 8.1, 9.8, 12.2]

    ax.add_patch(Rectangle((0.3, 6.7), 13.4, 0.6, facecolor=C_INK, edgecolor='none'))
    for i, h in enumerate(table_headers):
        ax.text(col_pos[i], 7.0, h, ha='center', va='center', color='#FFF', fontsize=9.5, fontweight='bold')

    slot_info = [
        ('1', '906-1342', '000→001', '0→1', '1→0', '0→1', 'ปิด→เปิด', 'Ȳ₁ (เฉพาะท้ายช่วง)', 'Ȳ₁ ตกเป็น 0 ที่ x=1220..1342 (ช่องอื่น 1)'),
        ('2', '1343-1546', '010', '2', '0', '0→1', 'เปิด (ช่วงหลัง)', 'Ȳ₂ (เฉพาะท้ายช่วง)', 'Ȳ₂ ตกเป็น 0 ที่ x=1466..1546 (ช่องอื่น 1)'),
        ('3', '1547-1742', '011', '3', '0', '0', 'ปิด (Y=0)', 'Ȳ₃ (แต่ปิด)', 'ทุกช่องเป็น 1 ทั้งหมด (ไม่มีพัลส์ 0)'),
        ('4', '1743-1942', '100', '4', '0', '1→0', 'เปิด (ช่วงแรก)', 'Ȳ₄ (เฉพาะต้นช่วง)', 'Ȳ₄ ตกเป็น 0 ที่ x=1743..1835 (ช่องอื่น 1)'),
        ('5', '1943-2142', '101', '5', '0', '0', 'ปิด (Y=0)', 'Ȳ₅ (แต่ปิด)', 'ทุกช่องเป็น 1 ทั้งหมด (ไม่มีพัลส์ 0)'),
        ('6', '2143-2343', '110', '6', '0', '0→1', 'เปิด (ช่วงหลัง)', 'Ȳ₆ (เฉพาะท้ายช่วง)', 'Ȳ₆ ตกเป็น 0 ที่ x=2205..2343 (ช่องอื่น 1)'),
        ('7', '2344-2545', '111', '7', '0', '1', 'เปิดตลอดช่วง', 'Ȳ₇', 'Ȳ₇ ตกเป็น 0 ตลอดช่วง (ช่องอื่น 1)'),
        ('8', '2546-2681', '000', '0', '0→1', '0→1→0', 'เปิดช่วงสั้นๆ', 'Ȳ₀ (ช่วงกลางสั้นๆ)', 'Ȳ₀ ตกเป็น 0 ที่ x=2575..2604 (ช่องอื่น 1)'),
    ]

    ty = 6.25
    for row in slot_info:
        bg = '#F8FAFC' if int(row[0]) % 2 == 1 else '#FFFFFF'
        if row[5] != '0': bg = '#ECFDF5' if 'เปิด' in row[6] else '#FFFBEB'
        rect = Rectangle((0.3, ty - 0.22), 13.4, 0.48, facecolor=bg, edgecolor='#CBD5E1', lw=0.8)
        ax.add_patch(rect)
        for i, val in enumerate(row):
            fw = 'bold' if i in [0, 3, 5, 7] else 'normal'
            c = C_DMUX if i == 7 else (C_Y if i == 5 else C_INK)
            ax.text(col_pos[i], ty, val, ha='center', va='center', fontsize=9.2, color=c, fontweight=fw)
        ty -= 0.54

    # กล่องข้อคิด
    ax.add_patch(Rectangle((0.3, 0.5), 13.4, 1.4, facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.5))
    ax.text(0.6, 1.6, '★ สรุปความสัมพันธ์ระหว่าง Data Y กับ Active-LOW เอาต์พุตของ 74138:', fontsize=11, fontweight='bold', color='#1D4ED8')
    ax.text(0.6, 1.25, '• เมื่อ Data = Y = 1: ขา G1 = 1 ทำให้ 74138 ถูกเปิด (Enabled) → ขาที่ตรงกับแอดเดรส n จะ "ตกเป็นลอจิก 0" (Active-LOW pulse)', fontsize=9.8, color=C_INK)
    ax.text(0.6, 0.90, '• เมื่อ Data = Y = 0: ขา G1 = 0 ทำให้ 74138 ถูกปิด (Disabled) → ทุกขาเอาต์พุต Ȳ₀..Ȳ₇ จะถูกดึงขึ้นเป็น "ลอจิก 1" ทั้งหมด', fontsize=9.8, color=C_INK)
    ax.text(0.6, 0.60, '• ช่องที่ไม่ถูกเลือก (Address ≠ k) จะมีสถานะเป็น 1 ตลอดเวลา ไม่ว่า Data จะเป็น 0 หรือ 1 ก็ตาม', fontsize=9.8, color=C_INK)

    finish(fig, '05_enable_and_select_decoding.png')

# ═══════════════════════════════════════════════════════════════════════════
# 6. 06_dmux_outputs_y0_y7.png
# ═══════════════════════════════════════════════════════════════════════════
def fig06_dmux_outputs_y0_y7():
    fig, ax = plt.subplots(figsize=(14.0, 10.5))
    ax.set_xlim(X0 - 30, X1 + 30); ax.set_ylim(-0.8, 9.6); ax.axis('off')

    ax.text((X0 + X1) / 2, 9.35, 'รูปคลื่นเอาต์พุต Active-LOW ทั้ง 8 ช่องของ DMUX 74138 (Ȳ₀ .. Ȳ₇)',
            ha='center', fontsize=17, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 8.95, 'สังเกต: ขาที่ไม่ถูกเลือกจะค้างที่ 1 (HIGH) เสมอ — เกิดพัลส์ 0 (LOW) เฉพาะช่องที่ถูกเลือกและ Data Y = 1',
            ha='center', fontsize=11.5, color='#475569')

    slot_grid(ax, 8.5, -0.4, show_labels=True, label_y=8.55)
    disable_bands(ax, -0.4, 8.5, alpha=0.4)

    # วาด Data Y ไว้บนสุดเพื่อเปรียบเทียบ
    draw_wave(ax, Y_RUNS, 7.8, 0.45, C_Y, lw=2.6)
    wave_label(ax, X0 - 35, 7.8 + 0.22, 'Data = Y', C_Y, fs=11)

    for k in range(8):
        yb = 6.8 - k * 0.95
        draw_wave(ax, DMUX_RUNS[k], yb, 0.50, C_DMUX, lw=2.4)
        wave_label(ax, X0 - 35, yb + 0.25, f'Ȳ{k} (Pin {15-k if k<=6 else 7})', C_DMUX, fs=10.5)

    finish(fig, '06_dmux_outputs_y0_y7.png')

# ═══════════════════════════════════════════════════════════════════════════
# 7. 07_recovered_signals_r0_r7.png
# ═══════════════════════════════════════════════════════════════════════════
def fig07_recovered_signals_r0_r7():
    fig, ax = plt.subplots(figsize=(14.0, 10.5))
    ax.set_xlim(X0 - 30, X1 + 30); ax.set_ylim(-0.8, 9.6); ax.axis('off')

    ax.text((X0 + X1) / 2, 9.35, 'รูปคลื่นสัญญาณกู้คืนปลายทาง R₀ .. R₇ = (Ȳ[n])′ (Active-HIGH Demultiplexed Data)',
            ha='center', fontsize=17, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 8.95, 'เมื่อผ่าน Inverter: สัญญาณแต่ละแชนเนลจะกลับสู่สถานะปกติ (Active-HIGH) ตรงกับข้อมูลที่ภาคส่งส่งมา',
            ha='center', fontsize=11.5, color='#475569')

    slot_grid(ax, 8.5, -0.4, show_labels=True, label_y=8.55)
    disable_bands(ax, -0.4, 8.5, alpha=0.4)

    draw_wave(ax, Y_RUNS, 7.8, 0.45, C_Y, lw=2.6)
    wave_label(ax, X0 - 35, 7.8 + 0.22, 'Data = Y', C_Y, fs=11)

    for k in range(8):
        yb = 6.8 - k * 0.95
        draw_wave(ax, REC_RUNS[k], yb, 0.50, C_REC, lw=2.4)
        wave_label(ax, X0 - 35, yb + 0.25, f'R{k} = (Ȳ{k})′', C_REC, fs=10.5)

    finish(fig, '07_recovered_signals_r0_r7.png')

# ═══════════════════════════════════════════════════════════════════════════
# 8. 08_gate_output_f.png
# ═══════════════════════════════════════════════════════════════════════════
def fig08_gate_output_f():
    fig, ax = plt.subplots(figsize=(14.0, 8.8))
    ax.set_xlim(X0 - 30, X1 + 30); ax.set_ylim(-0.8, 6.8); ax.axis('off')

    ax.text((X0 + X1) / 2, 6.55, 'รูปคลื่นเอาต์พุตลอจิกฟังก์ชัน F = (Ȳ₁ · Ȳ₄ · Ȳ₇)′ = Y₁ + Y₄ + Y₇',
            ha='center', fontsize=17, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 6.15, 'การใช้ 74138 เป็นตัวสร้างมินเทอม (Universal Decoder / Minterm Generator) รวมด้วยเกต NAND',
            ha='center', fontsize=11.5, color='#475569')

    slot_grid(ax, 5.7, -0.4, show_labels=True, label_y=5.75)
    disable_bands(ax, -0.4, 5.7, alpha=0.4)

    signals = [
        ('Data = Y (สายส่ง)', Y_RUNS, 4.8, C_Y),
        ('Ȳ₁ (ช่อง 1)', DMUX_RUNS[1], 3.8, C_DMUX),
        ('Ȳ₄ (ช่อง 4)', DMUX_RUNS[4], 2.8, C_DMUX),
        ('Ȳ₇ (ช่อง 7)', DMUX_RUNS[7], 1.8, C_DMUX),
        ('เอาต์พุตเกต F', F_RUNS, 0.4, C_GATE),
    ]

    for name, r, yb, col in signals:
        lw = 3.2 if 'F' in name else 2.2
        draw_wave(ax, r, yb, 0.55, col, lw=lw)
        wave_label(ax, X0 - 35, yb + 0.28, name, col, fs=11.5)

    finish(fig, '08_gate_output_f.png')

# ═══════════════════════════════════════════════════════════════════════════
# 9. 09_final_answer_waveforms.png
# ═══════════════════════════════════════════════════════════════════════════
def fig09_final_answer_waveforms():
    fig, ax = plt.subplots(figsize=(14.5, 11.5))
    ax.set_xlim(X0 - 35, X1 + 35); ax.set_ylim(-0.8, 12.0); ax.axis('off')

    ax.text((X0 + X1) / 2, 11.65, 'คำตอบสมบูรณ์ (Master Final Answer) — รูปคลื่นระบบ MUX/DMUX ข้อที่ 2',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text((X0 + X1) / 2, 11.25, 'แสดงสัญญาณควบคุม, สัญญาณข้อมูลสายส่ง, เอาต์พุต 74138 (Ȳ₀..Ȳ₇), สัญญาณกู้คืน (R[n]) และเอาต์พุตเกต F',
            ha='center', fontsize=11.5, color='#475569')

    slot_grid(ax, 10.7, -0.4, show_labels=True, label_y=10.75)
    disable_bands(ax, -0.4, 10.7, alpha=0.35)

    waves = [
        ('A (LSB)', RUNS['A'], 10.0, C_SEL, 1.8),
        ('B',       RUNS['B'], 9.2, C_SEL, 1.8),
        ('C (MSB)', RUNS['C'], 8.4, C_SEL, 1.8),
        ('Data = Y (สายส่ง)', Y_RUNS, 7.5, C_Y, 2.6),
        ('Ȳ₀',      DMUX_RUNS[0], 6.7, C_DMUX, 2.0),
        ('Ȳ₁',      DMUX_RUNS[1], 5.9, C_DMUX, 2.0),
        ('Ȳ₂',      DMUX_RUNS[2], 5.1, C_DMUX, 2.0),
        ('Ȳ₄',      DMUX_RUNS[4], 4.3, C_DMUX, 2.0),
        ('Ȳ₆',      DMUX_RUNS[6], 3.5, C_DMUX, 2.0),
        ('Ȳ₇',      DMUX_RUNS[7], 2.7, C_DMUX, 2.0),
        ('R₁ (กู้คืนช่อง 1)', REC_RUNS[1], 1.8, C_REC, 2.2),
        ('R₄ (กู้คืนช่อง 4)', REC_RUNS[4], 1.0, C_REC, 2.2),
        ('เอาต์พุตเกต F', F_RUNS, 0.0, C_GATE, 3.2),
    ]

    for name, r, yb, col, lw in waves:
        draw_wave(ax, r, yb, 0.45, col, lw=lw)
        wave_label(ax, X0 - 40, yb + 0.22, name, col, fs=10.5)

    finish(fig, '09_final_answer_waveforms.png')

# ═══════════════════════════════════════════════════════════════════════════
# 10. 10_summary_table.png
# ═══════════════════════════════════════════════════════════════════════════
def fig10_summary_table():
    fig, ax = plt.subplots(figsize=(15.0, 9.2))
    ax.set_xlim(0, 15.0); ax.set_ylim(0, 9.2); ax.axis('off')

    ax.text(7.5, 8.75, 'ตารางสรุปการทำงานและผลลัพธ์ทุกช่วงเวลาย่อย (Comprehensive Summary Table)',
            ha='center', fontsize=18, fontweight='bold', color=C_INK)
    ax.text(7.5, 8.35, 'วิเคราะห์ครบทั้ง 9 ช่วงเวลาหลักและ 15 เหตุการณ์ย่อย ตามขอบสัญญาณจริงของโจทย์ข้อที่ 2',
            ha='center', fontsize=11.5, color='#475569')

    headers = ['ช่วง', 'พิกัดเวลา x', 'CBA', 'n', 'E', 'D₀/D₂', 'Data Y', '74138 Enable', 'Active Output', 'Ȳ₀..Ȳ₇', 'F']
    col_x = [0.7, 2.0, 3.2, 4.0, 4.7, 5.7, 6.8, 8.3, 10.0, 12.3, 14.1]

    ax.add_patch(Rectangle((0.3, 7.4), 14.4, 0.65, facecolor=C_INK, edgecolor='none'))
    for i, h in enumerate(headers):
        ax.text(col_x[i], 7.72, h, ha='center', va='center', color='#FFF', fontsize=9.5, fontweight='bold')

    events = [
        ('1a', '906-1142', '000', '0', '1', 'D₀=0,D₂=1', '0', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('1b', '1143-1219', '001', '1', '1', 'D₀=1,D₂=1', '0', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('1c', '1220-1342', '001', '1', '0', 'D₀=0,D₂=0', '1 (+5V)', 'G1=1 (Active)', 'Ȳ₁ = 0', '10111111', '1'),
        ('2a', '1343-1465', '010', '2', '0', 'D₀=1,D₂=0', '0 (D₂=0)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('2b', '1466-1546', '010', '2', '0', 'D₀=0,D₂=1', '1 (D₂=1)', 'G1=1 (Active)', 'Ȳ₂ = 0', '11011111', '0'),
        ('3',  '1547-1742', '011', '3', '0', 'D₀=1,D₂=1', '0 (GND)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('4a', '1743-1835', '100', '4', '0', 'D₀=0,D₂=0', '1 (D̄₀=1)', 'G1=1 (Active)', 'Ȳ₄ = 0', '11110111', '1'),
        ('4b', '1836-1942', '100', '4', '0', 'D₀=1,D₂=0', '0 (D̄₀=0)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('5',  '1943-2142', '101', '5', '0', 'D₀=0/1,D₂=1', '0 (GND)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('6a', '2143-2204', '110', '6', '0', 'D₀=0,D₂=1', '0 (D̄₂=0)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('6b', '2205-2343', '110', '6', '0', 'D₀=1,D₂=0', '1 (D̄₂=1)', 'G1=1 (Active)', 'Ȳ₆ = 0', '11111101', '0'),
        ('7',  '2344-2545', '111', '7', '0', 'D₀=0/1,D₂=0', '1 (+5V)', 'G1=1 (Active)', 'Ȳ₇ = 0', '11111110', '1'),
        ('8a', '2546-2574', '000', '0', '0', 'D₀=0,D₂=1', '0 (D₀=0)', 'G1=0 (Disabled)', '-', '11111111', '0'),
        ('8b', '2575-2604', '000', '0', '0', 'D₀=1,D₂=1', '1 (D₀=1)', 'G1=1 (Active)', 'Ȳ₀ = 0', '01111111', '0'),
        ('8c', '2605-2681', '000', '0', '1', 'D₀=1,D₂=1', '0 (E=1)', 'G1=0 (Disabled)', '-', '11111111', '0'),
    ]

    ty = 7.05
    for row in events:
        is_active = 'Active' in row[7]
        bg = '#ECFDF5' if is_active else ('#F8FAFC' if '1' in row[0] or '4' in row[0] or '6' in row[0] or '8' in row[0] else '#FFFFFF')
        rect = Rectangle((0.3, ty - 0.18), 14.4, 0.38, facecolor=bg, edgecolor='#CBD5E1', lw=0.7)
        ax.add_patch(rect)
        for i, val in enumerate(row):
            fw = 'bold' if i in [0, 3, 6, 8, 10] or is_active else 'normal'
            c = C_GATE if i == 10 and val == '1' else (C_DMUX if i == 8 and val != '-' else (C_Y if i == 6 and '1' in val else C_INK))
            ax.text(col_x[i], ty, val, ha='center', va='center', fontsize=8.8, color=c, fontweight=fw)
        ty -= 0.42

    finish(fig, '10_summary_table.png')

# ═══════════════════════════════════════════════════════════════════════════
# รันสร้างรูปทั้งหมด
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("เริ่มสร้างรูปภาพประกอบเฉลยข้อสอบข้อที่ 2 (DMUX 74138)...")
    fig01_dmux_concept()
    fig02_74138_function_table()
    fig03_tdm_system_circuit()
    fig04_input_and_data_waveforms()
    fig05_enable_and_select_decoding()
    fig06_dmux_outputs_y0_y7()
    fig07_recovered_signals_r0_r7()
    fig08_gate_output_f()
    fig09_final_answer_waveforms()
    fig10_summary_table()
    print("✨ สร้างรูปภาพทั้งหมด 10 รูปเสร็จสมบูรณ์เรียบร้อยแล้ว!")
