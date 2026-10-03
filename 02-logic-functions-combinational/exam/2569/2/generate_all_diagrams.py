#!/usr/bin/env python3
"""
High-Resolution (300 DPI) Digital Logic Schematic & K-Map Generator
Exam 2569 — Problem 02 (4-Stage Combinational Network with Strict Max 2-Input Gates)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Ensure assets directory exists
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Common Palette
COLOR_INK = "#1E293B"
COLOR_BG = "#FFFFFF"
COLOR_ACCENT = "#0284C7"
COLOR_LINE = "#334155"
DPI = 300

# Color palette for 5 input rails
RAIL_COLORS = {
    'A': '#DC2626', # Red
    'B': '#2563EB', # Blue
    'C': '#16A34A', # Green
    'D': '#9333EA', # Purple
    'E': '#D97706'  # Amber
}

def draw_and_gate(ax, x0, y0, width=1.4, height=1.0, label="AND", color="#1E40AF", fill="#EFF6FF"):
    """Draws a standard IEEE AND gate"""
    r = height / 2.0
    w_rect = width - r
    
    # Body path
    rect = patches.Rectangle((x0, y0 - r), w_rect, height, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(rect)
    
    arc = patches.Wedge((x0 + w_rect, y0), r, -90, 90, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(arc)
    
    # Cover line between rect and wedge
    ax.plot([x0 + w_rect, x0 + w_rect], [y0 - r + 0.05, y0 + r - 0.05], color=fill, linewidth=3.0, zorder=4)
    
    if label:
        ax.text(x0 + width*0.38, y0, label, color=color, fontsize=9.5, fontweight='bold',
                ha='center', va='center', zorder=5)
    return x0 + width, y0

def draw_or_gate(ax, x0, y0, width=1.5, height=1.1, label="OR", color="#047857", fill="#ECFDF5"):
    """Draws a standard IEEE curved OR gate"""
    half_h = height / 2.0
    
    # Back curve
    theta = np.linspace(-np.pi/2.5, np.pi/2.5, 40)
    back_x = x0 + 0.3 * np.cos(theta) - 0.3 * np.cos(np.pi/2.5)
    back_y = y0 + half_h * np.sin(theta) / np.sin(np.pi/2.5)
    
    # Top curve to apex
    t_top = np.linspace(0, 1, 40)
    top_x = (1 - t_top)**2 * (back_x[-1]) + 2*(1 - t_top)*t_top * (x0 + width*0.6) + t_top**2 * (x0 + width)
    top_y = (1 - t_top)**2 * (y0 + half_h) + 2*(1 - t_top)*t_top * (y0 + half_h*0.85) + t_top**2 * y0
    
    # Bottom curve from apex
    t_bot = np.linspace(0, 1, 40)
    bot_x = (1 - t_bot)**2 * (x0 + width) + 2*(1 - t_bot)*t_bot * (x0 + width*0.6) + t_bot**2 * (back_x[0])
    bot_y = (1 - t_bot)**2 * y0 + 2*(1 - t_bot)*t_bot * (y0 - half_h*0.85) + t_bot**2 * (y0 - half_h)
    
    verts_x = np.concatenate([back_x, top_x, bot_x])
    verts_y = np.concatenate([back_y, top_y, bot_y])
    
    poly = patches.Polygon(np.column_stack([verts_x, verts_y]), closed=True,
                           facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(poly)
    
    if label:
        ax.text(x0 + width*0.45, y0, label, color=color, fontsize=9.5, fontweight='bold',
                ha='center', va='center', zorder=5)
    return x0 + width, y0

def draw_xor_gate(ax, x0, y0, width=1.5, height=1.1, label="XOR", color="#6D28D9", fill="#F5F3FF"):
    """Draws a standard IEEE XOR gate with separate back arc"""
    draw_or_gate(ax, x0, y0, width, height, label, color, fill)
    
    half_h = height / 2.0
    theta = np.linspace(-np.pi/2.5, np.pi/2.5, 40)
    arc_x = x0 - 0.22 + 0.3 * np.cos(theta) - 0.3 * np.cos(np.pi/2.5)
    arc_y = y0 + half_h * np.sin(theta) / np.sin(np.pi/2.5)
    ax.plot(arc_x, arc_y, color=color, linewidth=2.0, zorder=3)
    return x0 + width, y0

def draw_nand_gate(ax, x0, y0, width=1.4, height=1.0, label="NAND", color="#0D9488", fill="#F0FDFA"):
    """Draws a NAND gate with inversion bubble"""
    x_apex, y_apex = draw_and_gate(ax, x0, y0, width, height, label, color, fill)
    bubble_r = 0.09
    bubble = patches.Circle((x_apex + bubble_r, y_apex), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    return x_apex + 2*bubble_r, y_apex

def draw_nor_gate(ax, x0, y0, width=1.5, height=1.1, label="NOR", color="#B45309", fill="#FFFBEB"):
    """Draws a NOR gate with inversion bubble"""
    x_apex, y_apex = draw_or_gate(ax, x0, y0, width, height, label, color, fill)
    bubble_r = 0.09
    bubble = patches.Circle((x_apex + bubble_r, y_apex), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    return x_apex + 2*bubble_r, y_apex

def draw_inverter(ax, x0, y0, width=1.1, height=0.65, label="NOT", color="#B45309", fill="#FFFBEB"):
    """Draws a NOT inverter triangle with bubble"""
    half_h = height / 2.0
    tri_x = [x0, x0 + width, x0]
    tri_y = [y0 - half_h, y0, y0 + half_h]
    poly = patches.Polygon(np.column_stack([tri_x, tri_y]), closed=True,
                           facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(poly)
    
    bubble_r = 0.08
    bubble = patches.Circle((x0 + width + bubble_r, y0), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    
    if label:
        ax.text(x0 + width*0.35, y0, label, color=color, fontsize=8, fontweight='bold',
                ha='center', va='center', zorder=5)
    return x0 + width + 2*bubble_r, y0

# ==============================================================================
# 1. ORIGINAL 4-STAGE COMBINATIONAL CIRCUIT (STRICT MAX 2-INPUT GATES)
# ==============================================================================
def generate_original_circuit():
    fig, ax = plt.subplots(figsize=(20, 11), dpi=DPI)
    ax.set_xlim(-1.5, 23.5)
    ax.set_ylim(-1.5, 12.0)
    ax.axis('off')
    
    # Title & Subtitle Banner
    ax.text(11.0, 11.5, "305241 Digital Logic Design — Exam 2569 (Problem 02)",
            fontsize=17, fontweight='bold', ha='center', color="#0F172A")
    ax.text(11.0, 10.95,
            "5-Variable 4-Stage Combinational Network (Strict Max 2-Input Gates: 74HC04, 74HC86, 74HC00, 74HC02, 74HC08, 74HC32)",
            fontsize=11.5, ha='center', color="#334155",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.2))

    # Bus Rails X positions
    bus_x = {'A': -0.2, 'B': 0.5, 'C': 1.2, 'D': 1.9, 'E': 2.6}
    
    # Draw Vertical Bus Rails
    for var, x in bus_x.items():
        c = RAIL_COLORS[var]
        ax.plot([x, x], [0.8, 9.8], color=c, linewidth=2.4, zorder=2)
        # Input Terminal Circle & Label
        ax.plot(x, 10.1, marker='o', markersize=10, color=c, zorder=5)
        ax.text(x, 10.45, var, color=c, fontsize=15, fontweight='bold', ha='center', va='bottom')

    # STAGE 1: GATES (x = 4.2)
    stg1_x = 4.2

    # 1. NOT A (74HC04) at y = 8.8
    tip_notA_x, tip_notA_y = draw_inverter(ax, stg1_x, 8.8, width=1.1, height=0.6, label="NOT A", color=RAIL_COLORS['A'])
    ax.plot([bus_x['A'], stg1_x], [8.8, 8.8], color=RAIL_COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['A'], 8.8, marker='o', markersize=6, color=RAIL_COLORS['A'], zorder=4)
    ax.text(tip_notA_x + 0.3, tip_notA_y, "A'", color=RAIL_COLORS['A'], fontsize=11, fontweight='bold', va='center')

    # 2. XOR (74HC86): inputs B, D -> W1 = B ⊕ D at y = 7.1
    tip_xor_x, tip_xor_y = draw_xor_gate(ax, stg1_x, 7.1, width=1.5, height=1.1, label="XOR\n(7486)", color="#6D28D9", fill="#F5F3FF")
    # B into XOR
    ax.plot([bus_x['B'], stg1_x], [7.45, 7.45], color=RAIL_COLORS['B'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['B'], 7.45, marker='o', markersize=6, color=RAIL_COLORS['B'], zorder=4)
    # D into XOR
    ax.plot([bus_x['D'], stg1_x], [6.75, 6.75], color=RAIL_COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['D'], 6.75, marker='o', markersize=6, color=RAIL_COLORS['D'], zorder=4)
    # Badge W1
    ax.text(tip_xor_x + 0.2, tip_xor_y + 0.35, "W₁ = B ⊕ D", color="#6D28D9", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#6D28D9", linewidth=1.2))

    # 3. NAND (74HC00): inputs A, C -> W2 = (A · C)' at y = 5.3
    tip_nand_x, tip_nand_y = draw_nand_gate(ax, stg1_x, 5.3, width=1.4, height=1.0, label="NAND\n(7400)", color="#0D9488", fill="#F0FDFA")
    # A into NAND
    ax.plot([bus_x['A'], stg1_x], [5.65, 5.65], color=RAIL_COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['A'], 5.65, marker='o', markersize=6, color=RAIL_COLORS['A'], zorder=4)
    # C into NAND
    ax.plot([bus_x['C'], stg1_x], [4.95, 4.95], color=RAIL_COLORS['C'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['C'], 4.95, marker='o', markersize=6, color=RAIL_COLORS['C'], zorder=4)
    # Badge W2
    ax.text(tip_nand_x + 0.2, tip_nand_y + 0.35, "W₂ = (A·C)'", color="#0D9488", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#0D9488", linewidth=1.2))

    # 4. NOR (74HC02): inputs B, E -> W3 = (B + E)' at y = 3.6
    tip_nor_x, tip_nor_y = draw_nor_gate(ax, stg1_x, 3.6, width=1.5, height=1.1, label="NOR\n(7402)", color="#B45309", fill="#FFFBEB")
    # B into NOR
    ax.plot([bus_x['B'], stg1_x], [3.95, 3.95], color=RAIL_COLORS['B'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['B'], 3.95, marker='o', markersize=6, color=RAIL_COLORS['B'], zorder=4)
    # E into NOR
    ax.plot([bus_x['E'], stg1_x], [3.25, 3.25], color=RAIL_COLORS['E'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['E'], 3.25, marker='o', markersize=6, color=RAIL_COLORS['E'], zorder=4)
    # Badge W3
    ax.text(tip_nor_x + 0.2, tip_nor_y + 0.35, "W₃ = (B+E)'", color="#B45309", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#B45309", linewidth=1.2))

    # 5. NOT D (74HC04) at y = 1.9
    tip_notD_x, tip_notD_y = draw_inverter(ax, stg1_x, 1.9, width=1.1, height=0.6, label="NOT D", color=RAIL_COLORS['D'])
    ax.plot([bus_x['D'], stg1_x], [1.9, 1.9], color=RAIL_COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['D'], 1.9, marker='o', markersize=6, color=RAIL_COLORS['D'], zorder=4)
    ax.text(tip_notD_x + 0.3, tip_notD_y, "D'", color=RAIL_COLORS['D'], fontsize=11, fontweight='bold', va='center')

    # STAGE 2: 4 2-INPUT AND GATES (74HC08) at x = 9.2
    and_x = 9.2
    
    # AND1 (74HC08): A' and W1 at y = 8.0
    tip_and1_x, tip_and1_y = draw_and_gate(ax, and_x, 8.0, width=1.5, height=1.1, label="AND1\n(7408)", color="#1E40AF", fill="#EFF6FF")
    ax.plot([tip_notA_x, 7.9, 7.9, and_x], [8.8, 8.8, 8.35, 8.35], color=RAIL_COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot([tip_xor_x, 7.7, 7.7, and_x], [7.1, 7.1, 7.65, 7.65], color="#6D28D9", linewidth=1.8, zorder=2)
    ax.text(tip_and1_x + 0.25, tip_and1_y + 0.4, "W₄ = A'·(B ⊕ D)", color="#1E40AF", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.2))

    # AND2 (74HC08): C and W2 at y = 5.8
    tip_and2_x, tip_and2_y = draw_and_gate(ax, and_x, 5.8, width=1.5, height=1.1, label="AND2\n(7408)", color="#1E40AF", fill="#EFF6FF")
    ax.plot([bus_x['C'], 3.2, 3.2, and_x], [6.15, 6.15, 6.15, 6.15], color=RAIL_COLORS['C'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['C'], 6.15, marker='o', markersize=6, color=RAIL_COLORS['C'], zorder=4)
    ax.plot([tip_nand_x, 7.9, 7.9, and_x], [5.3, 5.3, 5.45, 5.45], color="#0D9488", linewidth=1.8, zorder=2)
    ax.text(tip_and2_x + 0.25, tip_and2_y + 0.4, "W₅ = A'·C", color="#1E40AF", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.2))

    # AND3 (74HC08): W3 and D' at y = 3.6
    tip_and3_x, tip_and3_y = draw_and_gate(ax, and_x, 3.6, width=1.5, height=1.1, label="AND3\n(7408)", color="#1E40AF", fill="#EFF6FF")
    ax.plot([tip_nor_x, 7.9, 7.9, and_x], [3.6, 3.6, 3.95, 3.95], color="#B45309", linewidth=1.8, zorder=2)
    ax.plot([tip_notD_x, 7.9, 7.9, and_x], [1.9, 1.9, 3.25, 3.25], color=RAIL_COLORS['D'], linewidth=1.8, zorder=2)
    ax.text(tip_and3_x + 0.25, tip_and3_y + 0.4, "W₆ = B'·D'·E'", color="#1E40AF", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.2))

    # AND4 (74HC08): A and D at y = 1.4
    tip_and4_x, tip_and4_y = draw_and_gate(ax, and_x, 1.4, width=1.5, height=1.1, label="AND4\n(7408)", color="#1E40AF", fill="#EFF6FF")
    ax.plot([bus_x['A'], 2.8, 2.8, and_x], [1.75, 1.75, 1.75, 1.75], color=RAIL_COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['A'], 1.75, marker='o', markersize=6, color=RAIL_COLORS['A'], zorder=4)
    ax.plot([bus_x['D'], 3.0, 3.0, and_x], [1.05, 1.05, 1.05, 1.05], color=RAIL_COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['D'], 1.05, marker='o', markersize=6, color=RAIL_COLORS['D'], zorder=4)
    ax.text(tip_and4_x + 0.25, tip_and4_y + 0.4, "W₇ = A·D", color="#1E40AF", fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.2))

    # STAGE 3: 2 2-INPUT OR GATES (74HC32) at x = 14.5
    or_x = 14.5
    
    # OR1 (74HC32) at y = 6.9
    tip_or1_x, tip_or1_y = draw_or_gate(ax, or_x, 6.9, width=1.6, height=1.2, label="OR1\n(7432)", color="#047857", fill="#ECFDF5")
    ax.plot([tip_and1_x, 13.5, 13.5, or_x], [8.0, 8.0, 7.3, 7.3], color="#1E40AF", linewidth=2.0, zorder=2)
    ax.plot([tip_and2_x, 13.5, 13.5, or_x], [5.8, 5.8, 6.5, 6.5], color="#1E40AF", linewidth=2.0, zorder=2)
    ax.text(tip_or1_x + 0.25, tip_or1_y + 0.4, "W₈ = W₄ + W₅", color="#047857", fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#047857", linewidth=1.2))

    # OR2 (74HC32) at y = 2.5
    tip_or2_x, tip_or2_y = draw_or_gate(ax, or_x, 2.5, width=1.6, height=1.2, label="OR2\n(7432)", color="#047857", fill="#ECFDF5")
    ax.plot([tip_and3_x, 13.5, 13.5, or_x], [3.6, 3.6, 2.9, 2.9], color="#1E40AF", linewidth=2.0, zorder=2)
    ax.plot([tip_and4_x, 13.5, 13.5, or_x], [1.4, 1.4, 2.1, 2.1], color="#1E40AF", linewidth=2.0, zorder=2)
    ax.text(tip_or2_x + 0.25, tip_or2_y + 0.4, "W₉ = W₆ + W₇", color="#047857", fontsize=10, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#047857", linewidth=1.2))

    # STAGE 4: FINAL 2-INPUT COLLECTOR OR GATE (74HC32) at x = 18.8
    or3_x = 18.8
    tip_or3_x, tip_or3_y = draw_or_gate(ax, or3_x, 4.7, width=1.7, height=1.3, label="OR3\n(7432)", color="#0F766E", fill="#F0FDFA")
    ax.plot([tip_or1_x, 18.0, 18.0, or3_x], [6.9, 6.9, 5.15, 5.15], color="#047857", linewidth=2.2, zorder=2)
    ax.plot([tip_or2_x, 18.0, 18.0, or3_x], [2.5, 2.5, 4.25, 4.25], color="#047857", linewidth=2.2, zorder=2)
    
    # Final Output Line & Node
    ax.plot([tip_or3_x, 21.6], [4.7, 4.7], color="#0F172A", linewidth=2.8, zorder=2)
    ax.plot(21.6, 4.7, marker='o', markersize=12, color="#0F172A", zorder=5)
    ax.text(22.0, 4.7, "F", color="#0F172A", fontsize=16, fontweight='bold', va='center')
    
    # Output Equation Banner
    ax.text(11.0, -0.6,
            "F = W₈ + W₉ = A'·(B ⊕ D) + A'·C + B'·D'·E' + A·D",
            fontsize=12.5, fontweight='bold', ha='center', color="#0F172A",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFFFFF", edgecolor="#0F172A", linewidth=1.5))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "digital_logic_circuit_redrawn.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# ==============================================================================
# 2. 8x4 K-MAP SOP DIAGRAM
# ==============================================================================
def generate_kmap_sop():
    fig, ax = plt.subplots(figsize=(15, 16), dpi=DPI)
    ax.set_xlim(-2.2, 7.2)
    ax.set_ylim(-1.5, 11.5)
    ax.axis('off')
    
    ax.text(2.5, 11.0, "5-Variable SOP Karnaugh Map (8×4 Matrix — Grouping 1s)",
            fontsize=16, fontweight='bold', ha='center', color="#047857")
    ax.text(2.5, 10.45, "Vertical Rows = ABC (8 Rows in Gray Code) | Horizontal Columns = DE (4 Columns in Gray Code)",
            fontsize=10.5, ha='center', color="#475569")

    x_start = 0.6
    cell_w = 1.15
    y_start = 9.2
    cell_h = 1.05
    
    row_labels = ['000', '001', '011', '010', '110', '111', '101', '100']
    col_labels = ['00', '01', '11', '10']
    
    # Headers
    ax.text(-0.3, 9.8, "ABC \\ DE", fontsize=12, fontweight='bold', ha='center', color="#1E293B")
    for c_idx, c_lbl in enumerate(col_labels):
        ax.text(x_start + c_idx*cell_w + cell_w/2, 9.8, c_lbl, fontsize=13, fontweight='bold', ha='center', color="#1E293B")
        
    for r_idx, r_lbl in enumerate(row_labels):
        ax.text(-0.3, y_start - r_idx*cell_h - cell_h/2, r_lbl, fontsize=13, fontweight='bold', ha='center', color="#1E293B")

    minterms_set = {0, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 18, 19, 20, 22, 23, 26, 27, 30, 31}
    
    for r_idx, r_lbl in enumerate(row_labels):
        for c_idx, c_lbl in enumerate(col_labels):
            x = x_start + c_idx * cell_w
            y = y_start - (r_idx + 1) * cell_h
            m_val = int(r_lbl + c_lbl, 2)
            is_one = m_val in minterms_set
            
            face = "#ECFDF5" if is_one else "#FFFFFF"
            rect = patches.Rectangle((x, y), cell_w, cell_h, facecolor=face, edgecolor="#334155", linewidth=1.5)
            ax.add_patch(rect)
            
            ax.text(x + cell_w - 0.08, y + cell_h - 0.12, f"m{m_val}", fontsize=8, color="#94A3B8", ha='right', va='top')
            
            val_txt = "1" if is_one else "0"
            val_col = "#047857" if is_one else "#94A3B8"
            ax.text(x + cell_w/2, y + cell_h/2 - 0.05, val_txt, fontsize=18, fontweight='bold',
                    color=val_col, ha='center', va='center')

    # Group 1: A·D (Octet 8 cells: rows 4,5,6,7, cols 2,3)
    g1_x = x_start + 2*cell_w + 0.06
    g1_y = y_start - 8*cell_h + 0.06
    g1_w = 2*cell_w - 0.12
    g1_h = 4*cell_h - 0.12
    ax.add_patch(patches.FancyBboxPatch((g1_x, g1_y), g1_w, g1_h, boxstyle="round,pad=0.08",
                                       facecolor="none", edgecolor="#2563EB", linewidth=3.2, zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 6*cell_h, "Group 1 (Octet 8):\nA · D",
            color="#2563EB", fontsize=11, fontweight='bold', va='center')

    # Group 2: A'·C (Octet 8 cells: rows 1,2, cols 0,1,2,3)
    g2_x = x_start + 0.06
    g2_y = y_start - 3*cell_h + 0.06
    g2_w = 4*cell_w - 0.12
    g2_h = 2*cell_h - 0.12
    ax.add_patch(patches.FancyBboxPatch((g2_x, g2_y), g2_w, g2_h, boxstyle="round,pad=0.08",
                                       facecolor="none", edgecolor="#DC2626", linewidth=3.2, zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 2*cell_h, "Group 2 (Octet 8):\nA' · C",
            color="#DC2626", fontsize=11, fontweight='bold', va='center')

    # Group 3: B'·D (Octet 8 cells Wraparound: rows 0,1,6,7 at cols 2,3)
    g3a_x = x_start + 2*cell_w + 0.08
    g3a_y = y_start - 2*cell_h + 0.08
    g3a_w = 2*cell_w - 0.16
    g3a_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g3a_x, g3a_y), g3a_w, g3a_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#9333EA", linewidth=2.8, linestyle="--", zorder=6))
    g3b_x = x_start + 2*cell_w + 0.08
    g3b_y = y_start - 8*cell_h + 0.08
    g3b_w = 2*cell_w - 0.16
    g3b_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g3b_x, g3b_y), g3b_w, g3b_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#9333EA", linewidth=2.8, linestyle="--", zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 7.5*cell_h, "Group 3 (Octet 8 Wrap):\nB' · D",
            color="#9333EA", fontsize=11, fontweight='bold', va='center')

    # Group 4: B'·E' (Octet 8 cells Wraparound: rows 0,1,6,7 at cols 0,3)
    # DE=00 top & bot
    g4a_x = x_start + 0.08
    g4a_y = y_start - 2*cell_h + 0.08
    g4a_w = 1*cell_w - 0.16
    g4a_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g4a_x, g4a_y), g4a_w, g4a_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    g4b_x = x_start + 0.08
    g4b_y = y_start - 8*cell_h + 0.08
    g4b_w = 1*cell_w - 0.16
    g4b_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g4b_x, g4b_y), g4b_w, g4b_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    # DE=10 top & bot
    g4c_x = x_start + 3*cell_w + 0.08
    g4c_y = y_start - 2*cell_h + 0.08
    g4c_w = 1*cell_w - 0.16
    g4c_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g4c_x, g4c_y), g4c_w, g4c_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    g4d_x = x_start + 3*cell_w + 0.08
    g4d_y = y_start - 8*cell_h + 0.08
    g4d_w = 1*cell_w - 0.16
    g4d_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g4d_x, g4d_y), g4d_w, g4d_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 0.7*cell_h, "Group 4 (Octet 8 Wrap):\nB' · E'",
            color="#D97706", fontsize=11, fontweight='bold', va='center')

    # Group 5: A'·B·D' (Quad 4 cells: rows 2,3, cols 0,1)
    g5_x = x_start + 0.08
    g5_y = y_start - 4*cell_h + 0.08
    g5_w = 2*cell_w - 0.16
    g5_h = 2*cell_h - 0.14
    ax.add_patch(patches.FancyBboxPatch((g5_x, g5_y), g5_w, g5_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#0D9488", linewidth=2.8, linestyle=":", zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 3.5*cell_h, "Group 5 (Quad 4):\nA' · B · D'",
            color="#0D9488", fontsize=11, fontweight='bold', va='center')

    # Minimal SOP Expression Result Box
    ax.text(2.5, -0.8,
            "Minimal SOP Expression:  F_SOP = A·D + A'·C + B'·D + B'·E' + A'·B·D'",
            fontsize=13, fontweight='bold', ha='center', color="#047857",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ECFDF5", edgecolor="#047857", linewidth=2.0))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "kmap_sop_diagram.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# ==============================================================================
# 3. 8x4 K-MAP POS DIAGRAM
# ==============================================================================
def generate_kmap_pos():
    fig, ax = plt.subplots(figsize=(15, 16), dpi=DPI)
    ax.set_xlim(-2.2, 7.2)
    ax.set_ylim(-1.5, 11.5)
    ax.axis('off')
    
    ax.text(2.5, 11.0, "5-Variable POS Karnaugh Map (8×4 Matrix — Grouping 0s)",
            fontsize=16, fontweight='bold', ha='center', color="#B91C1C")
    ax.text(2.5, 10.45, "Vertical Rows = ABC (8 Rows in Gray Code) | Horizontal Columns = DE (4 Columns in Gray Code)",
            fontsize=10.5, ha='center', color="#475569")

    x_start = 0.6
    cell_w = 1.15
    y_start = 9.2
    cell_h = 1.05
    
    row_labels = ['000', '001', '011', '010', '110', '111', '101', '100']
    col_labels = ['00', '01', '11', '10']
    
    # Headers
    ax.text(-0.3, 9.8, "ABC \\ DE", fontsize=12, fontweight='bold', ha='center', color="#1E293B")
    for c_idx, c_lbl in enumerate(col_labels):
        ax.text(x_start + c_idx*cell_w + cell_w/2, 9.8, c_lbl, fontsize=13, fontweight='bold', ha='center', color="#1E293B")
        
    for r_idx, r_lbl in enumerate(row_labels):
        ax.text(-0.3, y_start - r_idx*cell_h - cell_h/2, r_lbl, fontsize=13, fontweight='bold', ha='center', color="#1E293B")

    maxterms_set = {1, 10, 11, 17, 21, 24, 25, 28, 29}
    
    for r_idx, r_lbl in enumerate(row_labels):
        for c_idx, c_lbl in enumerate(col_labels):
            x = x_start + c_idx * cell_w
            y = y_start - (r_idx + 1) * cell_h
            m_val = int(r_lbl + c_lbl, 2)
            is_zero = m_val in maxterms_set
            
            face = "#FEF2F2" if is_zero else "#FFFFFF"
            rect = patches.Rectangle((x, y), cell_w, cell_h, facecolor=face, edgecolor="#334155", linewidth=1.5)
            ax.add_patch(rect)
            
            ax.text(x + cell_w - 0.08, y + cell_h - 0.12, f"M{m_val}", fontsize=8, color="#94A3B8", ha='right', va='top')
            
            val_txt = "0" if is_zero else "1"
            val_col = "#B91C1C" if is_zero else "#E2E8F0"
            ax.text(x + cell_w/2, y + cell_h/2 - 0.05, val_txt, fontsize=18, fontweight='bold',
                    color=val_col, ha='center', va='center')

    # POS Group 1 (Quad 4): rows 4,5 (110,111), cols 0,1 (00,01) -> (A' + B' + D)
    g1_x = x_start + 0.06
    g1_y = y_start - 6*cell_h + 0.06
    g1_w = 2*cell_w - 0.12
    g1_h = 2*cell_h - 0.12
    ax.add_patch(patches.FancyBboxPatch((g1_x, g1_y), g1_w, g1_h, boxstyle="round,pad=0.08",
                                       facecolor="none", edgecolor="#DC2626", linewidth=3.2, zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 5*cell_h, "Group 1 (Quad 4):\n(A' + B' + D)",
            color="#DC2626", fontsize=11, fontweight='bold', va='center')

    # POS Group 2 (Quad 4): rows 4,5,6,7 at col 1 (01) -> (A' + D + E')
    g2_x = x_start + 1*cell_w + 0.08
    g2_y = y_start - 8*cell_h + 0.08
    g2_w = 1*cell_w - 0.16
    g2_h = 4*cell_h - 0.16
    ax.add_patch(patches.FancyBboxPatch((g2_x, g2_y), g2_w, g2_h, boxstyle="round,pad=0.08",
                                       facecolor="none", edgecolor="#2563EB", linewidth=2.8, linestyle="--", zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 6.5*cell_h, "Group 2 (Quad 4):\n(A' + D + E')",
            color="#2563EB", fontsize=11, fontweight='bold', va='center')

    # POS Group 3 (Pair 2): row 3 (010), cols 2,3 (11,10) -> (A + B' + C + D')
    g3_x = x_start + 2*cell_w + 0.06
    g3_y = y_start - 4*cell_h + 0.06
    g3_w = 2*cell_w - 0.12
    g3_h = 1*cell_h - 0.12
    ax.add_patch(patches.FancyBboxPatch((g3_x, g3_y), g3_w, g3_h, boxstyle="round,pad=0.08",
                                       facecolor="none", edgecolor="#9333EA", linewidth=2.8, zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 3.5*cell_h, "Group 3 (Pair 2):\n(A + B' + C + D')",
            color="#9333EA", fontsize=11, fontweight='bold', va='center')

    # POS Group 4 (Pair 2 Wraparound): row 0 (000) and row 7 (100) at col 1 (01) -> (B + C + D + E')
    g4a_x = x_start + 1*cell_w + 0.09
    g4a_y = y_start - 1*cell_h + 0.09
    g4a_w = 1*cell_w - 0.18
    g4a_h = 1*cell_h - 0.18
    ax.add_patch(patches.FancyBboxPatch((g4a_x, g4a_y), g4a_w, g4a_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    g4b_x = x_start + 1*cell_w + 0.09
    g4b_y = y_start - 8*cell_h + 0.09
    g4b_w = 1*cell_w - 0.18
    g4b_h = 1*cell_h - 0.18
    ax.add_patch(patches.FancyBboxPatch((g4b_x, g4b_y), g4b_w, g4b_h, boxstyle="round,pad=0.06",
                                        facecolor="none", edgecolor="#D97706", linewidth=2.8, linestyle="-.", zorder=6))
    ax.text(x_start + 4*cell_w + 0.25, y_start - 0.5*cell_h, "Group 4 (Pair Wrap):\n(B + C + D + E')",
            color="#D97706", fontsize=11, fontweight='bold', va='center')

    # Minimal POS Expression Result Box
    ax.text(2.5, -0.8,
            "Minimal POS Expression:  F_POS = (A' + B' + D) · (A' + D + E') · (A + B' + C + D') · (B + C + D + E')",
            fontsize=12, fontweight='bold', ha='center', color="#B91C1C",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF2F2", edgecolor="#B91C1C", linewidth=2.0))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "kmap_pos_diagram.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# ==============================================================================
# 4. MINIMAL SOP CIRCUIT (AND-OR SYNTHESIS)
# ==============================================================================
def generate_sop_circuit():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=DPI)
    ax.set_xlim(-1.0, 18.0)
    ax.set_ylim(-1.0, 11.0)
    ax.axis('off')
    
    ax.text(8.5, 10.5, "Minimal SOP Logic Circuit Schematic (Two-Level AND-OR Synthesis)",
            fontsize=16, fontweight='bold', ha='center', color="#047857")
    ax.text(8.5, 9.9, "F_SOP = A·D + A'·C + B'·D + B'·E' + A'·B·D' (5 Product Terms, 12 Literals)",
            fontsize=11.5, ha='center', color="#334155",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#ECFDF5", edgecolor="#047857", linewidth=1.2))

    and_configs = [
        (8.5, "AND1\n(A·D)", [("A", RAIL_COLORS['A']), ("D", RAIL_COLORS['D'])]),
        (6.8, "AND2\n(A'·C)", [("A'", RAIL_COLORS['A']), ("C", RAIL_COLORS['C'])]),
        (5.1, "AND3\n(B'·D)", [("B'", RAIL_COLORS['B']), ("D", RAIL_COLORS['D'])]),
        (3.4, "AND4\n(B'·E')", [("B'", RAIL_COLORS['B']), ("E'", RAIL_COLORS['E'])]),
        (1.7, "AND5\n(A'·B·D')", [("A'", RAIL_COLORS['A']), ("B", RAIL_COLORS['B']), ("D'", RAIL_COLORS['D'])])
    ]
    
    and_tips = []
    for y, lbl, in_vars in and_configs:
        tip_x, tip_y = draw_and_gate(ax, 2.5, y, width=1.6, height=1.1, label=lbl, color="#1E40AF", fill="#EFF6FF")
        and_tips.append((tip_x, tip_y))
        
        n_in = len(in_vars)
        for idx, (v_name, v_col) in enumerate(in_vars):
            if n_in == 2:
                in_y = y + 0.3 if idx == 0 else y - 0.3
            else:
                in_y = y + 0.35 if idx == 0 else (y if idx == 1 else y - 0.35)
            ax.plot([1.2, 2.5], [in_y, in_y], color=v_col, linewidth=2.0, zorder=2)
            ax.text(1.0, in_y, v_name, color=v_col, fontsize=11, fontweight='bold', ha='right', va='center')

    # Collector OR Gate at x = 12.0, y = 5.1 (5-Input OR)
    or_x = 12.0
    or_y = 5.1
    tip_or_x, tip_or_y = draw_or_gate(ax, or_x, or_y, width=2.4, height=3.8, label="OR\n(5-In)", color="#047857", fill="#ECFDF5")
    
    or_pins = [6.5, 5.8, 5.1, 4.4, 3.7]
    channel_x = [9.0, 9.6, 10.2, 9.6, 9.0]
    line_colors = ["#DC2626", "#2563EB", "#9333EA", "#D97706", "#0D9488"]
    
    for (ax_x, ax_y), p_y, cx, col in zip(and_tips, or_pins, channel_x, line_colors):
        if abs(ax_y - p_y) < 0.05:
            ax.plot([ax_x, or_x], [ax_y, p_y], color=col, linewidth=2.4, zorder=2)
        else:
            ax.plot([ax_x, cx, cx, or_x], [ax_y, ax_y, p_y, p_y], color=col, linewidth=2.4, zorder=2)

    # Output terminal
    ax.plot([tip_or_x, 16.5], [or_y, or_y], color="#0F172A", linewidth=3.0, zorder=2)
    ax.plot(16.5, or_y, marker='o', markersize=12, color="#0F172A", zorder=5)
    ax.text(16.9, or_y, "F_SOP", color="#0F172A", fontsize=15, fontweight='bold', va='center')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "sop_circuit_diagram.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# ==============================================================================
# 5. MINIMAL POS CIRCUIT (OR-AND SYNTHESIS)
# ==============================================================================
def generate_pos_circuit():
    fig, ax = plt.subplots(figsize=(18, 12), dpi=DPI)
    ax.set_xlim(-1.0, 18.0)
    ax.set_ylim(-1.0, 11.0)
    ax.axis('off')
    
    ax.text(8.5, 10.5, "Minimal POS Logic Circuit Schematic (Two-Level OR-AND Synthesis)",
            fontsize=16, fontweight='bold', ha='center', color="#B91C1C")
    ax.text(8.5, 9.9, "F_POS = (A' + B' + D) · (A' + D + E') · (A + B' + C + D') · (B + C + D + E') (4 Sum Terms, 14 Literals)",
            fontsize=11.5, ha='center', color="#334155",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor="#B91C1C", linewidth=1.2))

    or_configs = [
        (8.0, "OR1\n(3-In)", [("A'", RAIL_COLORS['A']), ("B'", RAIL_COLORS['B']), ("D", RAIL_COLORS['D'])]),
        (5.8, "OR2\n(3-In)", [("A'", RAIL_COLORS['A']), ("D", RAIL_COLORS['D']), ("E'", RAIL_COLORS['E'])]),
        (3.6, "OR3\n(4-In)", [("A", RAIL_COLORS['A']), ("B'", RAIL_COLORS['B']), ("C", RAIL_COLORS['C']), ("D'", RAIL_COLORS['D'])]),
        (1.4, "OR4\n(4-In)", [("B", RAIL_COLORS['B']), ("C", RAIL_COLORS['C']), ("D", RAIL_COLORS['D']), ("E'", RAIL_COLORS['E'])])
    ]
    
    or_tips = []
    for y, lbl, in_vars in or_configs:
        tip_x, tip_y = draw_or_gate(ax, 2.5, y, width=1.7, height=1.3, label=lbl, color="#B91C1C", fill="#FEF2F2")
        or_tips.append((tip_x, tip_y))
        
        n_in = len(in_vars)
        for idx, (v_name, v_col) in enumerate(in_vars):
            if n_in == 3:
                in_y = y + 0.4 if idx == 0 else (y if idx == 1 else y - 0.4)
            else:
                in_y = y + 0.45 if idx == 0 else (y + 0.15 if idx == 1 else (y - 0.15 if idx == 2 else y - 0.45))
            ax.plot([1.2, 2.5], [in_y, in_y], color=v_col, linewidth=2.0, zorder=2)
            ax.text(1.0, in_y, v_name, color=v_col, fontsize=11, fontweight='bold', ha='right', va='center')

    # Collector AND Gate at x = 12.0, y = 4.7 (4-Input AND)
    and_x = 12.0
    and_y = 4.7
    tip_and_x, tip_and_y = draw_and_gate(ax, and_x, 4.7, width=2.4, height=3.4, label="AND\n(4-In)", color="#1E40AF", fill="#EFF6FF")
    
    and_pins = [5.9, 5.1, 4.3, 3.5]
    channel_x = [9.4, 10.2, 10.2, 9.4]
    line_colors = ["#DC2626", "#2563EB", "#9333EA", "#D97706"]
    
    for (ox, oy), p_y, cx, col in zip(or_tips, and_pins, channel_x, line_colors):
        ax.plot([ox, cx, cx, and_x], [oy, oy, p_y, p_y], color=col, linewidth=2.4, zorder=2)

    # Output terminal
    ax.plot([tip_and_x, 16.5], [and_y, and_y], color="#0F172A", linewidth=3.0, zorder=2)
    ax.plot(16.5, and_y, marker='o', markersize=12, color="#0F172A", zorder=5)
    ax.text(16.9, and_y, "F_POS", color="#0F172A", fontsize=15, fontweight='bold', va='center')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "pos_circuit_diagram.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

# ==============================================================================
# 6. HARDWARE IC PINOUT & INTERCONNECTION MAP
# ==============================================================================
def generate_ic_pinout():
    fig, ax = plt.subplots(figsize=(20, 13), dpi=DPI)
    ax.set_xlim(-1.0, 21.0)
    ax.set_ylim(-1.5, 12.5)
    ax.axis('off')
    
    ax.text(10.0, 12.0, "Hardware IC Package Pinout & Interconnection Map (Exam 2569 - Problem 02)",
            fontsize=17, fontweight='bold', ha='center', color="#0F172A")
    ax.text(10.0, 11.35, "Standard TTL/CMOS 74HC Series Logic DIP-14 Packages for Circuit Implementation",
            fontsize=11.5, ha='center', color="#475569")

    ic_list = [
        (0.5, 6.8, "74HC04", "Hex Inverters\n(A', D')", "#B45309", "#FFFBEB"),
        (5.5, 6.8, "74HC86", "Quad 2-In XOR\n(W₁ = B ⊕ D)", "#6D28D9", "#F5F3FF"),
        (10.5, 6.8, "74HC00", "Quad 2-In NAND\n(W₂ = (A·C)')", "#0D9488", "#F0FDFA"),
        (15.5, 6.8, "74HC02", "Quad 2-In NOR\n(W₃ = (B+E)')", "#B45309", "#FFFBEB"),
        (3.0, 1.8, "74HC08", "Quad 2-In AND\n(W₄, W₅, W₆, W₇)", "#1E40AF", "#EFF6FF"),
        (11.0, 1.8, "74HC32", "Quad 2-In OR\n(W₈, W₉, F)", "#991B1B", "#FEF2F2")
    ]
    
    for x, y, part, desc, col, fill in ic_list:
        w, h = 4.2, 3.0
        # DIP-14 Body
        body = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                     facecolor=fill, edgecolor=col, linewidth=2.2, zorder=2)
        ax.add_patch(body)
        
        # Notch on left
        notch = patches.Arc((x, y + h/2), 0.5, 0.5, angle=0, theta1=270, theta2=90, color=col, linewidth=2.2, zorder=3)
        ax.add_patch(notch)
        
        # IC Text
        ax.text(x + w/2, y + h*0.62, part, fontsize=13, fontweight='bold', ha='center', color=col)
        ax.text(x + w/2, y + h*0.38, desc, fontsize=8.5, ha='center', color="#475569", va='center')
        
        # VCC & GND badges
        ax.text(x + 0.45, y + h - 0.35, "VCC (14)", fontsize=7, fontweight='bold', color="#DC2626")
        ax.text(x + 3.75, y + 0.25, "GND (7)", fontsize=7, fontweight='bold', color="#1E293B", ha='right')
        
        # Pins: 1 to 7 on bottom, 14 down to 8 on top
        pin_w = 0.22
        pin_h = 0.35
        for p in range(7):
            px = x + 0.45 + p * 0.55
            # Bottom Pin (1-7)
            bot_pin = patches.Rectangle((px - pin_w/2, y - pin_h), pin_w, pin_h, facecolor="#94A3B8", edgecolor="#475569", linewidth=1.0)
            ax.add_patch(bot_pin)
            ax.text(px, y - pin_h - 0.22, str(p + 1), fontsize=8, ha='center', color="#334155")
            
            # Top Pin (14-8)
            top_pin = patches.Rectangle((px - pin_w/2, y + h), pin_w, pin_h, facecolor="#94A3B8", edgecolor="#475569", linewidth=1.0)
            ax.add_patch(top_pin)
            ax.text(px, y + h + pin_h + 0.12, str(14 - p), fontsize=8, ha='center', color="#334155")

    # IC Allocation Table / Bottom Legend
    leg_box = patches.FancyBboxPatch((-0.5, -1.2), 21.0, 2.3, boxstyle="round,pad=0.2",
                                    facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5, zorder=2)
    ax.add_patch(leg_box)
    
    ax.text(0.0, 0.7, "Standard 74HC Series Logic IC Packages (DIP-14 Hardware Allocation):",
            fontsize=11.5, fontweight='bold', color="#0F172A")
    ax.text(0.0, 0.25, "• Stage 1 (Pre-Logic): 74HC04 (Hex NOT - inverters A', D'), 74HC86 (XOR W₁), 74HC00 (NAND W₂), 74HC02 (NOR W₃)",
            fontsize=9.5, color="#334155")
    ax.text(0.0, -0.2, "• Stage 2 (Product Terms): 74HC08 (Quad 2-Input AND for W₄, W₅, W₆, W₇)",
            fontsize=9.5, color="#334155")
    ax.text(0.0, -0.65, "• Stage 3 & 4 (Collector ORs): 74HC32 (Quad 2-Input OR for W₈, W₉, and Output F)",
            fontsize=9.5, color="#334155")

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "ic_pinout_layout.png")
    fig.savefig(out_path, dpi=DPI, facecolor=COLOR_BG)
    plt.close(fig)
    print(f"Generated: {out_path}")

def main():
    print("Generating all high-resolution 300 DPI diagrams for Exam 2569 Problem 02...")
    generate_original_circuit()
    generate_kmap_sop()
    generate_kmap_pos()
    generate_sop_circuit()
    generate_pos_circuit()
    generate_ic_pinout()
    print("✅ All 6 diagrams successfully generated!")

if __name__ == "__main__":
    main()
