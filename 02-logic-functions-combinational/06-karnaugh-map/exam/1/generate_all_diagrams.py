#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_all_diagrams.py
────────────────────────────────────────────────────────────────────────────
สร้างสื่อภาพประกอบระดับตำราเรียนสำหรับเฉลยโจทย์ K-Map 5 ตัวแปร (Exam 1)
ตาราง 8 แถว × 4 คอลัมน์ (ตัวแปร A, B, C, D, E)

รันด้วย: python3 generate_all_diagrams.py
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon, Arc
from matplotlib.lines import Line2D
from matplotlib import font_manager

# ═══════════════════════════════════════════════════════════════════════════
# ฟอนต์
# ═══════════════════════════════════════════════════════════════════════════
_avail = {f.name for f in font_manager.fontManager.ttflist}
for _cand in ['Arial Unicode MS', 'Thonburi', 'Tahoma', 'Sarabun', 'Noto Sans Thai', 'IBM Plex Thai', 'Ayuthaya', 'DejaVu Sans']:
    if _cand in _avail:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [_cand, 'DejaVu Sans', 'Arial']
        THAI_FONT = _cand
        break
else:
    THAI_FONT = plt.rcParams['font.family']
plt.rcParams['axes.unicode_minus'] = False
print(f"[font] ใช้ฟอนต์: {THAI_FONT}")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
os.makedirs(OUT, exist_ok=True)
DPI = 300

# ═══════════════════════════════════════════════════════════════════════════
# ข้อมูล K-MAP 8x4
# ═══════════════════════════════════════════════════════════════════════════
ROW_LABELS = ['000', '001', '011', '010', '110', '111', '101', '100']
COL_LABELS = ['00', '01', '11', '10']

# ค่าในตาราง K-Map (8 แถว, 4 คอลัมน์)
GRID_VALUES = [
    [0, 1, 1, 0],  # 000 (m0, m1, m3, m2)
    [0, 1, 1, 0],  # 001 (m4, m5, m7, m6)
    [1, 1, 1, 1],  # 011 (m12, m13, m15, m14)
    [1, 1, 1, 1],  # 010 (m8, m9, m11, m10)
    [1, 1, 1, 1],  # 110 (m24, m25, m27, m26)
    [1, 1, 1, 0],  # 111 (m28, m29, m31, m30)
    [0, 1, 1, 1],  # 101 (m20, m21, m23, m22)
    [0, 1, 1, 0],  # 100 (m16, m17, m19, m18)
]

# คำนวณเลขมินเทอม
MINTERMS = {}
for r_idx, abc in enumerate(ROW_LABELS):
    for c_idx, de in enumerate(COL_LABELS):
        m_val = int(abc + de, 2)
        MINTERMS[(r_idx, c_idx)] = m_val

COLOR_ONE = '#B91C1C'      # สีแดงเข้มสำหรับเลข 1
COLOR_ZERO = '#718096'     # สีเทาสำหรับเลข 0

# สีกรุ๊ปต่างๆ
C_G1_RED     = '#EF4444'   # 16-cell: E
C_G2_MAGENTA = '#D946EF'   # 8-cell: A'·B
C_G3_BLUE    = '#3B82F6'   # 8-cell: B·D'
C_G4_ORANGE  = '#F97316'   # 8-cell: B·C'
C_G5_GREEN   = '#10B981'   # 2-cell: A·B'·C·D

def draw_kmap_exact(ax, title, subtitle=None, show_minterms=True):
    ax.set_xlim(-1.8, 4.4)
    ax.set_ylim(-0.9, 10.4)
    ax.axis('off')
    
    # วาดพื้นหลังตาราง
    bg_rect = FancyBboxPatch((-1.6, -0.7), 5.8, 10.8, boxstyle="round,pad=0.1,rounding_size=0.2",
                             facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5, zorder=0)
    ax.add_patch(bg_rect)
    
    ax.text(1.3, 10.0, title, ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    if subtitle:
        ax.text(1.3, 9.6, subtitle, ha='center', va='center', fontsize=9.2, color='#64748B')

    # ส่วนหัวคอลัมน์ DE
    ax.text(2.0, 8.6, "DE", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
    for c_idx, de in enumerate(COL_LABELS):
        ax.text(c_idx + 0.5, 8.2, de, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')
        
    # ส่วนหัวแถว ABC
    ax.text(-0.7, 8.6, "ABC", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
    for r_idx, abc in enumerate(ROW_LABELS):
        y_center = 8.0 - (r_idx + 0.5)
        ax.text(-0.7, y_center, abc, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')
        
    # วาดเส้นแบ่งแถวและคอลัมน์ (8 แถว: y จาก 0 ถึง 8)
    for x in range(5):
        ax.plot([x, x], [0, 8], color='#94A3B8', linewidth=1.2, zorder=1)
    for y in range(9):
        ax.plot([0, 4], [y, y], color='#94A3B8', linewidth=1.2, zorder=1)
    ax.plot([0, 4, 4, 0, 0], [0, 0, 8, 8, 0], color='#334155', linewidth=2, zorder=2)
    ax.plot([-1.4, 4], [8, 8], color='#334155', linewidth=1.5, zorder=2)
    ax.plot([0, 0], [0, 9], color='#334155', linewidth=1.5, zorder=2)

    # ใส่ค่า 0 และ 1
    for r_idx, row in enumerate(GRID_VALUES):
        y_center = 8.0 - (r_idx + 0.5)
        for c_idx, val in enumerate(row):
            x_center = c_idx + 0.5
            m_num = MINTERMS[(r_idx, c_idx)]
            
            txt_col = COLOR_ONE if val == 1 else COLOR_ZERO
            font_wt = 'bold' if val == 1 else 'normal'
            ax.text(x_center, y_center, str(val), ha='center', va='center',
                    fontsize=14, fontweight=font_wt, color=txt_col, zorder=10)
            
            if show_minterms:
                ax.text(x_center + 0.38, y_center + 0.35, f"m{m_num}", ha='right', va='top',
                        fontsize=6.5, color='#94A3B8', zorder=10)

def gen_fig09():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=DPI)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.5)
    ax.axis('off')
    
    bg_rect = FancyBboxPatch((-0.3, -0.3), 10.6, 6.6, boxstyle="round,pad=0.1,rounding_size=0.2",
                             facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5, zorder=0)
    ax.add_patch(bg_rect)
    
    ax.text(5.0, 6.1, "วงจรลอจิกเกตสำหรับฟังก์ชัน F = E + A'·B + B·C' + B·D' + A·B'·C·D",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')

    inputs = ['A', 'B', 'C', 'D', 'E']
    bus_x = [0.8, 1.2, 1.6, 2.0, 2.4]
    
    for idx, (name, x) in enumerate(zip(inputs, bus_x)):
        ax.plot([x, x], [0.8, 5.5], color='#64748B', linewidth=1.5)
        ax.text(x, 5.7, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
        
    gate_x = 4.8
    
    def draw_and_gate(ax, x, y, height=0.7, width=0.8):
        rect = Rectangle((x, y - height/2), width/2, height, facecolor='#EFF6FF', edgecolor='#1E40AF', lw=1.5)
        ax.add_patch(rect)
        arc = matplotlib.patches.Wedge((x + width/2, y), height/2, -90, 90, facecolor='#EFF6FF', edgecolor='#1E40AF', lw=1.5)
        ax.add_patch(arc)
        ax.text(x + width/3, y, "AND", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E40AF')

    # 1. A'·B
    draw_and_gate(ax, gate_x, 4.6)
    ax.plot([bus_x[0], gate_x - 0.15], [4.8, 4.8], color='#2563EB', lw=1.2)
    ax.plot([bus_x[0]], [4.8], 'o', color='#2563EB', markersize=4)
    bubble1 = Circle((gate_x - 0.08, 4.8), 0.06, facecolor='#FFFFFF', edgecolor='#2563EB', lw=1.2)
    ax.add_patch(bubble1)
    ax.plot([bus_x[1], gate_x], [4.4, 4.4], color='#2563EB', lw=1.2)
    ax.plot([bus_x[1]], [4.4], 'o', color='#2563EB', markersize=4)
    ax.plot([gate_x + 0.75, 7.2], [4.6, 4.6], color='#1E40AF', lw=1.5)
    ax.text(6.0, 4.8, "A'·B", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#A21CAF')

    # 2. B·C'
    draw_and_gate(ax, gate_x, 3.6)
    ax.plot([bus_x[1], gate_x], [3.8, 3.8], color='#2563EB', lw=1.2)
    ax.plot([bus_x[1]], [3.8], 'o', color='#2563EB', markersize=4)
    ax.plot([bus_x[2], gate_x - 0.15], [3.4, 3.4], color='#2563EB', lw=1.2)
    ax.plot([bus_x[2]], [3.4], 'o', color='#2563EB', markersize=4)
    bubble2 = Circle((gate_x - 0.08, 3.4), 0.06, facecolor='#FFFFFF', edgecolor='#2563EB', lw=1.2)
    ax.add_patch(bubble2)
    ax.plot([gate_x + 0.75, 7.2], [3.6, 3.6], color='#1E40AF', lw=1.5)
    ax.text(6.0, 3.8, "B·C'", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#C2410C')

    # 3. B·D'
    draw_and_gate(ax, gate_x, 2.6)
    ax.plot([bus_x[1], gate_x], [2.8, 2.8], color='#2563EB', lw=1.2)
    ax.plot([bus_x[1]], [2.8], 'o', color='#2563EB', markersize=4)
    ax.plot([bus_x[3], gate_x - 0.15], [2.4, 2.4], color='#2563EB', lw=1.2)
    ax.plot([bus_x[3]], [2.4], 'o', color='#2563EB', markersize=4)
    bubble3 = Circle((gate_x - 0.08, 2.4), 0.06, facecolor='#FFFFFF', edgecolor='#2563EB', lw=1.2)
    ax.add_patch(bubble3)
    ax.plot([gate_x + 0.75, 7.2], [2.6, 2.6], color='#1E40AF', lw=1.5)
    ax.text(6.0, 2.8, "B·D'", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1D4ED8')

    # 4. A·B'·C·D
    draw_and_gate(ax, gate_x, 1.4, height=0.9, width=0.8)
    ax.plot([bus_x[0], gate_x], [1.7, 1.7], color='#2563EB', lw=1.2)
    ax.plot([bus_x[0]], [1.7], 'o', color='#2563EB', markersize=4)
    ax.plot([bus_x[1], gate_x - 0.15], [1.5, 1.5], color='#2563EB', lw=1.2)
    ax.plot([bus_x[1]], [1.5], 'o', color='#2563EB', markersize=4)
    bubble4 = Circle((gate_x - 0.08, 1.5), 0.06, facecolor='#FFFFFF', edgecolor='#2563EB', lw=1.2)
    ax.add_patch(bubble4)
    ax.plot([bus_x[2], gate_x], [1.3, 1.3], color='#2563EB', lw=1.2)
    ax.plot([bus_x[2]], [1.3], 'o', color='#2563EB', markersize=4)
    ax.plot([bus_x[3], gate_x], [1.1, 1.1], color='#2563EB', lw=1.2)
    ax.plot([bus_x[3]], [1.1], 'o', color='#2563EB', markersize=4)
    ax.plot([gate_x + 0.75, 7.2], [1.4, 1.4], color='#1E40AF', lw=1.5)
    ax.text(6.0, 1.6, "A·B'·C·D", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#047857')

    # 5. อินพุต E
    ax.plot([bus_x[4], 7.2], [5.2, 5.2], color='#DC2626', lw=1.5)
    ax.plot([bus_x[4]], [5.2], 'o', color='#DC2626', markersize=4)
    ax.text(6.0, 5.35, "E (ตรง)", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#DC2626')

    # 5-Input OR Gate
    or_box = FancyBboxPatch((7.2, 0.9), 1.3, 4.6, boxstyle="round,pad=0.1,rounding_size=0.4",
                            facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=2, zorder=5)
    ax.add_patch(or_box)
    ax.text(7.85, 3.2, "5-Input\nOR GATE", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#DC2626', zorder=6)

    # เอาต์พุต F
    ax.plot([8.6, 9.8], [3.2, 3.2], color='#0F172A', lw=2.5)
    ax.plot([9.8], [3.2], '>', color='#0F172A', markersize=7)
    ax.text(10.0, 3.2, "F", ha='left', va='center', fontsize=16, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    path = os.path.join(OUT, '09_circuit_diagram.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] {path}")

def gen_fig10():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6), dpi=DPI)
    fig.suptitle("การมองแบบ 3 มิติ (3D Superposition): แยก 2 ตารางย่อย 4×4 ตามบิต A", fontsize=13, fontweight='bold', y=0.98)
    
    bc_labels = ['00', '01', '11', '10']
    de_labels = ['00', '01', '11', '10']
    
    # ตารางซ้าย: A = 0
    grid_a0 = [
        GRID_VALUES[0], # 000
        GRID_VALUES[1], # 001
        GRID_VALUES[2], # 011
        GRID_VALUES[3], # 010
    ]
    minterms_a0 = [
        [0, 1, 3, 2],
        [4, 5, 7, 6],
        [12, 13, 15, 14],
        [8, 9, 11, 10]
    ]
    
    # ตารางขวา: A = 1
    grid_a1 = [
        GRID_VALUES[7], # 100
        GRID_VALUES[6], # 101
        GRID_VALUES[5], # 111
        GRID_VALUES[4], # 110
    ]
    minterms_a1 = [
        [16, 17, 19, 18],
        [20, 21, 23, 22],
        [28, 29, 31, 30],
        [24, 25, 27, 26]
    ]

    for ax, grid_sub, m_sub, sub_title in [(ax1, grid_a0, minterms_a0, "ตารางที่ 1: A = 0 (m₀ – m₁₅)"),
                                           (ax2, grid_a1, minterms_a1, "ตารางที่ 2: A = 1 (m₁₆ – m₃₁)")]:
        ax.set_xlim(-1.2, 4.4)
        ax.set_ylim(-0.6, 5.6)
        ax.axis('off')
        
        bg_rect = FancyBboxPatch((-1.0, -0.4), 5.2, 5.8, boxstyle="round,pad=0.1,rounding_size=0.2",
                                 facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5, zorder=0)
        ax.add_patch(bg_rect)
        
        ax.text(1.5, 5.2, sub_title, ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
        
        ax.text(2.0, 4.5, "DE", ha='center', va='center', fontsize=10, fontweight='bold', color='#475569')
        for c_idx, de in enumerate(de_labels):
            ax.text(c_idx + 0.5, 4.2, de, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#475569')
            
        ax.text(-0.5, 4.5, "BC", ha='center', va='center', fontsize=10, fontweight='bold', color='#475569')
        for r_idx, bc in enumerate(bc_labels):
            y_center = 4.0 - (r_idx + 0.5)
            ax.text(-0.5, y_center, bc, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#475569')
            
        for x in range(5):
            ax.plot([x, x], [0, 4], color='#94A3B8', linewidth=1.2)
        for y in range(5):
            ax.plot([0, 4], [y, y], color='#94A3B8', linewidth=1.2)
        ax.plot([0, 4, 4, 0, 0], [0, 0, 4, 4, 0], color='#334155', linewidth=2)
        ax.plot([-0.9, 4], [4, 4], color='#334155', linewidth=1.5)
        ax.plot([0, 0], [0, 5], color='#334155', linewidth=1.5)

        for r_idx, row in enumerate(grid_sub):
            y_center = 4.0 - (r_idx + 0.5)
            for c_idx, val in enumerate(row):
                x_center = c_idx + 0.5
                m_num = m_sub[r_idx][c_idx]
                
                txt_col = COLOR_ONE if val == 1 else COLOR_ZERO
                font_wt = 'bold' if val == 1 else 'normal'
                ax.text(x_center, y_center, str(val), ha='center', va='center',
                        fontsize=13, fontweight=font_wt, color=txt_col, zorder=10)
                ax.text(x_center + 0.38, y_center + 0.35, f"m{m_num}", ha='right', va='top',
                        fontsize=6, color='#94A3B8', zorder=10)

    plt.tight_layout()
    path = os.path.join(OUT, '10_3d_two_map_equivalent.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] {path}")

def gen_fig11_exact():
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "การหา Minimal POS (วงกลุ่มของเลข 0)",
                    "Zeros (8 ช่อง): m0, m2, m4, m6, m16, m18, m20, m30")
    
    # 1. m0, m2, m4, m6: rows 0, 1 (y: 6..8), cols 0, 3 (x: 0..1 และ x: 3..4) => (A + B + E)
    p1_l = FancyBboxPatch((0.05, 6.05), 0.9, 1.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                          facecolor='#3B82F6', edgecolor='#1D4ED8', alpha=0.3, lw=2, zorder=5)
    p1_r = FancyBboxPatch((3.05, 6.05), 0.9, 1.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                          facecolor='#3B82F6', edgecolor='#1D4ED8', alpha=0.3, lw=2, zorder=5)
    ax.add_patch(p1_l); ax.add_patch(p1_r)

    # 2. m0, m2, m16, m18: row 0 (y: 7..8) and row 7 (y: 0..1), cols 0, 3 => (B + C + E)
    p2_top_l = FancyBboxPatch((0.05, 7.05), 0.9, 0.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                              facecolor='#10B981', edgecolor='#047857', alpha=0.3, lw=2, zorder=6)
    p2_top_r = FancyBboxPatch((3.05, 7.05), 0.9, 0.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                              facecolor='#10B981', edgecolor='#047857', alpha=0.3, lw=2, zorder=6)
    p2_bot_l = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                              facecolor='#10B981', edgecolor='#047857', alpha=0.3, lw=2, zorder=6)
    p2_bot_r = FancyBboxPatch((3.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                              facecolor='#10B981', edgecolor='#047857', alpha=0.3, lw=2, zorder=6)
    ax.add_patch(p2_top_l); ax.add_patch(p2_top_r); ax.add_patch(p2_bot_l); ax.add_patch(p2_bot_r)

    # 3. m0, m4, m16, m20: rows 0, 1, 6, 7 in col 0 => (B + D + E)
    p3 = FancyBboxPatch((0.05, 0.05), 0.9, 7.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                        facecolor='#F59E0B', edgecolor='#D97706', alpha=0.25, lw=2, zorder=4)
    ax.add_patch(p3)

    # 4. m30: row 5 (r5 is y: 2..3), col 3 (x: 3..4) => (A' + B' + C' + D' + E)
    p4 = FancyBboxPatch((3.05, 2.05), 0.9, 0.9, boxstyle="round,pad=0.04,rounding_size=0.1",
                        facecolor='#EF4444', edgecolor='#B91C1C', alpha=0.4, lw=2, zorder=7)
    ax.add_patch(p4)

    ax.text(2.0, -0.45, "สมการผลลัพธ์ขั้นต่ำ (Minimal POS):\nF = (A + B + E) · (B + C + E) · (B + D + E) · (A' + B' + C' + D' + E)",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#0F172A',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#F8FAFC', edgecolor='#0F172A', lw=1.5))
    plt.tight_layout()
    path = os.path.join(OUT, '11_pos_maxterm_grouping.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] {path}")

def build_all_figures():
    # 1. ปัญหาตั้งต้น
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "แผนผัง K-Map 5 ตัวแปร (โจทย์ต้นฉบับ)", "อินพุต A, B, C (แถว) และ D, E (คอลัมน์)", show_minterms=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '01_kmap_problem_clean.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 01_kmap_problem_clean.png")

    # 2. แผนที่มินเทอม
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    ax.set_xlim(-1.8, 4.4)
    ax.set_ylim(-0.9, 10.4)
    ax.axis('off')
    bg_rect = FancyBboxPatch((-1.6, -0.7), 5.8, 10.8, boxstyle="round,pad=0.1,rounding_size=0.2",
                             facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5, zorder=0)
    ax.add_patch(bg_rect)
    ax.text(1.3, 10.0, "ผังลำดับเลขมินเทอม (Minterm Index Map)", ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    ax.text(1.3, 9.6, "m = 16A + 8B + 4C + 2D + E (ตาม Gray Code)", ha='center', va='center', fontsize=9.2, color='#64748B')
    ax.text(2.0, 8.6, "DE", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
    for c_idx, de in enumerate(COL_LABELS):
        ax.text(c_idx + 0.5, 8.2, de, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')
    ax.text(-0.7, 8.6, "ABC", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')
    for r_idx, abc in enumerate(ROW_LABELS):
        y_center = 8.0 - (r_idx + 0.5)
        ax.text(-0.7, y_center, abc, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')
    for x in range(5):
        ax.plot([x, x], [0, 8], color='#94A3B8', linewidth=1.2, zorder=1)
    for y in range(9):
        ax.plot([0, 4], [y, y], color='#94A3B8', linewidth=1.2, zorder=1)
    ax.plot([0, 4, 4, 0, 0], [0, 0, 8, 8, 0], color='#334155', linewidth=2, zorder=2)
    ax.plot([-1.4, 4], [8, 8], color='#334155', linewidth=1.5, zorder=2)
    ax.plot([0, 0], [0, 9], color='#334155', linewidth=1.5, zorder=2)

    for r_idx, row in enumerate(GRID_VALUES):
        y_center = 8.0 - (r_idx + 0.5)
        for c_idx, val in enumerate(row):
            x_center = c_idx + 0.5
            m_num = MINTERMS[(r_idx, c_idx)]
            c_bg = '#FEE2E2' if val == 1 else '#F1F5F9'
            c_border = '#FCA5A5' if val == 1 else '#CBD5E1'
            cell_box = FancyBboxPatch((x_center-0.42, y_center-0.42), 0.84, 0.84,
                                      boxstyle="round,pad=0.02,rounding_size=0.08",
                                      facecolor=c_bg, edgecolor=c_border, linewidth=1, zorder=3)
            ax.add_patch(cell_box)
            ax.text(x_center, y_center + 0.12, f"m{m_num}", ha='center', va='center',
                    fontsize=10, fontweight='bold', color='#1E293B', zorder=10)
            ax.text(x_center, y_center - 0.22, f"({val})", ha='center', va='center',
                    fontsize=8, color=COLOR_ONE if val == 1 else COLOR_ZERO, fontweight='bold' if val == 1 else 'normal', zorder=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '02_kmap_minterm_indices.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 02_kmap_minterm_indices.png")

    # 3. กลุ่มที่ 1: แดง 16 ช่อง
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "กลุ่มที่ 1: ขนาด 16 ช่อง (สีแดงแนวตั้ง)", "คอลัมน์ DE = 01 และ 11 ครอบคลุมทั้ง 8 แถว ⇒ ลดรูปได้ E")
    p1 = FancyBboxPatch((1.05, 0.05), 1.9, 7.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G1_RED, edgecolor='#B91C1C', alpha=0.35, linewidth=2.5, zorder=5)
    ax.add_patch(p1)
    ax.text(2.0, -0.45, "กลุ่มสีแดง (16 ช่อง) = 8 แถว × 2 คอลัมน์ (E = 1 ตลอด)\nตัวแปร A, B, C, D เปลี่ยนสถานะครบทั้ง 0 และ 1 จึงถูกตัดทิ้งทั้งหมด ⇒ เหลือเพียง E",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#FEF2F2', edgecolor='#F87171', lw=1.2))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '03_group1_red_16cell.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 03_group1_red_16cell.png")

    # 4. กลุ่มที่ 2: ชมพู 8 ช่อง (rows 2, 3 => r2 is y:5..6, r3 is y:4..5 => y:4..6, x:0..4)
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "กลุ่มที่ 2: ขนาด 8 ช่อง (สีชมพู/ม่วงแนวนอน)", "แถว ABC = 011 และ 010 ครอบคลุมทั้ง 4 คอลัมน์ ⇒ ลดรูปได้ A'·B")
    p2 = FancyBboxPatch((0.05, 4.05), 3.9, 1.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G2_MAGENTA, edgecolor='#A21CAF', alpha=0.35, linewidth=2.5, zorder=5)
    ax.add_patch(p2)
    ax.text(2.0, -0.45, "กลุ่มสีชมพู (8 ช่อง) = 2 แถว × 4 คอลัมน์ (A=0, B=1 ตลอด)\nตัวแปร C, D, E เปลี่ยนครบทุกสถานะจึงถูกตัดทิ้ง ⇒ เหลือ A'·B (จำเป็นต้องมีเพื่อคลุม m14)",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#A21CAF',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#FDF4FF', edgecolor='#F472B6', lw=1.2))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '04_group2_magenta_8cell.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 04_group2_magenta_8cell.png")

    # 5. กลุ่มที่ 3: น้ำเงิน 8 ช่อง (rows 2, 3, 4, 5 => y:2..6, cols 0, 1 => x:0..2)
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "กลุ่มที่ 3: ขนาด 8 ช่อง (สีน้ำเงินบล็อกซ้าย)", "แถว ABC มี B=1 (r=2,3,4,5) และคอลัมน์ DE มี D=0 (c=0,1) ⇒ ลดรูปได้ B·D'")
    p3 = FancyBboxPatch((0.05, 2.05), 1.9, 3.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G3_BLUE, edgecolor='#1D4ED8', alpha=0.35, linewidth=2.5, zorder=5)
    ax.add_patch(p3)
    ax.text(2.0, -0.45, "กลุ่มสีน้ำเงิน (8 ช่อง) = 4 แถวที่มี B=1 × 2 คอลัมน์ที่มี D=0\nตัวแปร A, C, E เปลี่ยนครบทุกสถานะจึงถูกตัดทิ้ง ⇒ เหลือ B·D' (จำเป็นต้องมีเพื่อคลุม m28)",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1D4ED8',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#EFF6FF', edgecolor='#60A5FA', lw=1.2))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '05_group3_blue_8cell.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 05_group3_blue_8cell.png")

    # 6. กลุ่มที่ 4: ส้ม 8 ช่อง (rows 3, 4 => r3 is y:4..5, r4 is y:3..4 => y:3..5, x:0..4)
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "กลุ่มที่ 4: ขนาด 8 ช่อง (สีส้มแนวนอนกลางตาราง)", "แถว ABC = 010 (r=3) และ 110 (r=4) ครอบคลุมทั้ง 4 คอลัมน์ ⇒ ลดรูปได้ B·C'")
    p4 = FancyBboxPatch((0.05, 3.05), 3.9, 1.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G4_ORANGE, edgecolor='#C2410C', alpha=0.35, linewidth=2.5, zorder=5)
    ax.add_patch(p4)
    ax.text(2.0, -0.45, "กลุ่มสีส้ม (8 ช่อง) = 2 แถวติดกัน (B=1, C=0) × 4 คอลัมน์\nตัวแปร A, D, E เปลี่ยนสถานะจึงถูกตัดทิ้ง ⇒ เหลือ B·C' (จำเป็นต้องมีเพื่อคลุม m26)",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#C2410C',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#FFF7ED', edgecolor='#FB923C', lw=1.2))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '06_group4_orange_8cell.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 06_group4_orange_8cell.png")

    # 7. กลุ่มที่ 5: เขียว 2 ช่อง (row 6 => r6 is y:1..2, cols 2, 3 => x:2..4)
    fig, ax = plt.subplots(figsize=(6.5, 9.6), dpi=DPI)
    draw_kmap_exact(ax, "กลุ่มที่ 5: ขนาด 2 ช่อง (สีเขียวแถวล่าง)", "แถว ABC = 101 (r=6) คอลัมน์ DE = 11, 10 (c=2,3) ⇒ ลดรูปได้ A·B'·C·D")
    p5 = FancyBboxPatch((2.05, 1.05), 1.9, 0.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G5_GREEN, edgecolor='#047857', alpha=0.4, linewidth=2.5, zorder=5)
    ax.add_patch(p5)
    ax.text(2.0, -0.45, "กลุ่มสีเขียว (2 ช่อง) = แถว ABC=101 × 2 คอลัมน์ที่มี D=1 (DE=11, 10)\nตัวแปร E เปลี่ยนจาก 1 เป็น 0 จึงถูกตัดทิ้ง ⇒ เหลือ A·B'·C·D (จำเป็นต้องมีเพื่อคลุม m22)",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#047857',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#ECFDF5', edgecolor='#34D399', lw=1.2))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '07_group5_green_2cell.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 07_group5_green_2cell.png")

    # 8. ภาพรวม Master Composite
    fig, ax = plt.subplots(figsize=(7.5, 10.2), dpi=DPI)
    draw_kmap_exact(ax, "ผลการจัดกลุ่ม Essential Prime Implicants ทั้งหมด",
                    "ฟังก์ชัน F(A,B,C,D,E) = E + A'·B + B·C' + B·D' + A·B'·C·D")
    p1 = FancyBboxPatch((1.05, 0.05), 1.9, 7.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G1_RED, edgecolor='#B91C1C', alpha=0.25, linewidth=2, zorder=4)
    p2 = FancyBboxPatch((0.05, 4.05), 3.9, 1.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G2_MAGENTA, edgecolor='#A21CAF', alpha=0.25, linewidth=2, zorder=5)
    p3 = FancyBboxPatch((0.05, 2.05), 1.9, 3.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G3_BLUE, edgecolor='#1D4ED8', alpha=0.25, linewidth=2, zorder=6)
    p4 = FancyBboxPatch((0.05, 3.05), 3.9, 1.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G4_ORANGE, edgecolor='#C2410C', alpha=0.25, linewidth=2, zorder=7)
    p5 = FancyBboxPatch((2.05, 1.05), 1.9, 0.9, boxstyle="round,pad=0.05,rounding_size=0.15",
                        facecolor=C_G5_GREEN, edgecolor='#047857', alpha=0.4, linewidth=2, zorder=8)
    ax.add_patch(p1); ax.add_patch(p2); ax.add_patch(p3); ax.add_patch(p4); ax.add_patch(p5)

    ax.text(2.0, -0.45, "สมการผลลัพธ์ขั้นต่ำ (Minimal SOP):\nF = E + A'·B + B·C' + B·D' + A·B'·C·D",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0F172A',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8FAFC', edgecolor='#0F172A', lw=1.5))
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, '08_all_groups_composite.png'), dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"[saved] 08_all_groups_composite.png")

    # 9. วงจรเกต
    gen_fig09()
    # 10. 3D Superposition
    gen_fig10()
    # 11. POS Grouping
    gen_fig11_exact()

if __name__ == '__main__':
    print("🚀 กำลังสร้างภาพประกอบระดับตำราเรียนทั้งหมด...")
    build_all_figures()
    print("✅ สร้างภาพประกอบทั้งหมด 11 รูปแบบสำเร็จเรียบร้อยแล้ว!")
