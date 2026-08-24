import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

COLOR_A = "#E74C3C"      # Red
COLOR_B = "#2980B9"      # Blue
COLOR_C = "#27AE60"      # Green
COLOR_D = "#8E44AD"      # Purple
COLOR_E = "#D35400"      # Orange

COLOR_X1 = "#C0392B"     # Dark Red
COLOR_X2 = "#16A085"     # Teal
COLOR_X3 = "#8E44AD"     # Purple
COLOR_X4 = "#D4AC0D"     # Gold
COLOR_FINAL_OUT = "#1A5276"# Dark Navy

def F_ref(A, B, C, D, E):
    x1 = (not A) and B
    x2 = A and (not C)
    x3 = (not B) and D and E
    x4 = C and (not D) and (not E)
    return int(x1 or x2 or x3 or x4)

def draw_and_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#EBF5FB", edge_color="#1B4F72"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    r = height / 2
    x_arc_start = x + width - r
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_arc_start, y_top)),
        (Path.CURVE4, (x + width, y_top)),
        (Path.CURVE4, (x + width, y_bot)),
        (Path.CURVE4, (x_arc_start, y_bot)),
        (Path.LINETO, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.4, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0, y + height/4), (x0, y - height/4), (x + width, y)

def draw_and3_gate(ax, x, y, width=1.5, height=1.4, label="", fill_color="#EBF5FB", edge_color="#1B4F72"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    r = height / 2
    x_arc_start = x + width - r
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_arc_start, y_top)),
        (Path.CURVE4, (x + width, y_top)),
        (Path.CURVE4, (x + width, y_bot)),
        (Path.CURVE4, (x_arc_start, y_bot)),
        (Path.LINETO, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0, y + height/3), (x0, y), (x0, y - height/3), (x + width, y)

def draw_or_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#EAFAF1", edge_color="#145A32"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.CURVE3, (x0 + width*0.25, y)),
        (Path.CURVE3, (x0, y_top)),
        (Path.CURVE3, (x0 + width*0.65, y_top)),
        (Path.CURVE3, (x0 + width, y)),
        (Path.CURVE3, (x0 + width*0.65, y_bot)),
        (Path.CURVE3, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.4, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0 + width*0.1, y + height/4), (x0 + width*0.1, y - height/4), (x + width, y)

def draw_or4_gate(ax, x, y, width=1.6, height=1.8, label="", fill_color="#EAFAF1", edge_color="#145A32"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.CURVE3, (x0 + width*0.25, y)),
        (Path.CURVE3, (x0, y_top)),
        (Path.CURVE3, (x0 + width*0.65, y_top)),
        (Path.CURVE3, (x0 + width, y)),
        (Path.CURVE3, (x0 + width*0.65, y_bot)),
        (Path.CURVE3, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    step = height / 5
    in1 = (x0 + width*0.1, y + step*1.8)
    in2 = (x0 + width*0.1, y + step*0.6)
    in3 = (x0 + width*0.1, y - step*0.6)
    in4 = (x0 + width*0.1, y - step*1.8)
    return in1, in2, in3, in4, (x + width, y)

def draw_or5_gate(ax, x, y, width=1.6, height=2.2, label="", fill_color="#EAFAF1", edge_color="#145A32"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.CURVE3, (x0 + width*0.25, y)),
        (Path.CURVE3, (x0, y_top)),
        (Path.CURVE3, (x0 + width*0.65, y_top)),
        (Path.CURVE3, (x0 + width, y)),
        (Path.CURVE3, (x0 + width*0.65, y_bot)),
        (Path.CURVE3, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    step = height / 6
    in1 = (x0 + width*0.1, y + step*2)
    in2 = (x0 + width*0.1, y + step*1)
    in3 = (x0 + width*0.1, y)
    in4 = (x0 + width*0.1, y - step*1)
    in5 = (x0 + width*0.1, y - step*2)
    return in1, in2, in3, in4, in5, (x + width, y)

def draw_and5_gate(ax, x, y, width=1.6, height=2.2, label="", fill_color="#EBF5FB", edge_color="#1B4F72"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    r = height / 2
    x_arc_start = x + width - r
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_arc_start, y_top)),
        (Path.CURVE4, (x + width, y_top)),
        (Path.CURVE4, (x + width, y_bot)),
        (Path.CURVE4, (x_arc_start, y_bot)),
        (Path.LINETO, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    if label:
        ax.text(x + width*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    step = height / 6
    in1 = (x0, y + step*2)
    in2 = (x0, y + step*1)
    in3 = (x0, y)
    in4 = (x0, y - step*1)
    in5 = (x0, y - step*2)
    return in1, in2, in3, in4, in5, (x + width, y)

def draw_not_gate(ax, x, y, width=1.1, height=0.7, label="", fill_color="#F4ECF7", edge_color="#512E5F", bubble_r=0.07):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    x_tip = x + width - bubble_r*2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_tip, y)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    bx = x + width - bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.2, zorder=4)
    ax.add_patch(bubble)
    if label:
        ax.text(x + width*0.3, y, label, fontsize=9, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0, y), (x + width, y)

def create_redrawn_circuit():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    x_in = 0.5
    y_A, y_B, y_C, y_D, y_E = 8.0, 6.4, 4.8, 3.2, 1.6
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${text}$", fontsize=14, fontweight='bold', color=color, ha='right', va='center')

    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    add_term(x_in, y_E, "E", COLOR_E)
    
    notA_in, notA_out = draw_not_gate(ax, 2.5, 7.3, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax, 2.5, 5.7, label="NOT B")
    notC_in, notC_out = draw_not_gate(ax, 2.5, 4.1, label="NOT C")
    notD_in, notD_out = draw_not_gate(ax, 2.5, 2.5, label="NOT D")
    notE_in, notE_out = draw_not_gate(ax, 2.5, 0.9, label="NOT E")
    
    and1_in1, and1_in2, and1_out = draw_and_gate(ax, 6.5, 7.5, width=1.5, height=1.2, label="AND1")
    and2_in1, and2_in2, and2_out = draw_and_gate(ax, 6.5, 5.5, width=1.5, height=1.2, label="AND2")
    and3_in1, and3_in2, and3_in3, and3_out = draw_and3_gate(ax, 6.5, 3.5, width=1.6, height=1.4, label="AND3")
    and4_in1, and4_in2, and4_in3, and4_out = draw_and3_gate(ax, 6.5, 1.5, width=1.6, height=1.4, label="AND4")
    
    or4_in1, or4_in2, or4_in3, or4_in4, or4_out = draw_or4_gate(ax, 11.5, 4.5, width=1.8, height=2.2, label="OR")
    
    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))

    ax.plot([x_in, 1.5], [y_A, y_A], color=COLOR_A, lw=2.5)
    add_junc(1.5, y_A, COLOR_A)
    ax.plot([1.5, 1.5, notA_in[0]], [y_A, notA_in[1], notA_in[1]], color=COLOR_A, lw=2.5)
    ax.plot([1.5, 5.5, 5.5, and2_in1[0]], [y_A, y_A, and2_in1[1], and2_in1[1]], color=COLOR_A, lw=2.5)
    
    ax.plot([x_in, 1.8], [y_B, y_B], color=COLOR_B, lw=2.5)
    add_junc(1.8, y_B, COLOR_B)
    ax.plot([1.8, 5.8, 5.8, and1_in2[0]], [y_B, y_B, and1_in2[1], and1_in2[1]], color=COLOR_B, lw=2.5)
    ax.plot([1.8, 1.8, notB_in[0]], [y_B, notB_in[1], notB_in[1]], color=COLOR_B, lw=2.5)
    
    ax.plot([x_in, 1.3], [y_C, y_C], color=COLOR_C, lw=2.5)
    add_junc(1.3, y_C, COLOR_C)
    ax.plot([1.3, 1.3, notC_in[0]], [y_C, notC_in[1], notC_in[1]], color=COLOR_C, lw=2.5)
    ax.plot([1.3, 5.3, 5.3, and4_in1[0]], [y_C, y_C, and4_in1[1], and4_in1[1]], color=COLOR_C, lw=2.5)
    
    ax.plot([x_in, 1.6], [y_D, y_D], color=COLOR_D, lw=2.5)
    add_junc(1.6, y_D, COLOR_D)
    ax.plot([1.6, 5.6, 5.6, and3_in2[0]], [y_D, y_D, and3_in2[1], and3_in2[1]], color=COLOR_D, lw=2.5)
    ax.plot([1.6, 1.6, notD_in[0]], [y_D, notD_in[1], notD_in[1]], color=COLOR_D, lw=2.5)
    
    ax.plot([x_in, 1.4], [y_E, y_E], color=COLOR_E, lw=2.5)
    add_junc(1.4, y_E, COLOR_E)
    ax.plot([1.4, 5.4, 5.4, and3_in3[0]], [y_E, y_E, and3_in3[1], and3_in3[1]], color=COLOR_E, lw=2.5)
    ax.plot([1.4, 1.4, notE_in[0]], [y_E, notE_in[1], notE_in[1]], color=COLOR_E, lw=2.5)
    
    ax.plot([notA_out[0], and1_in1[0]], [notA_out[1], and1_in1[1]], color=COLOR_A, lw=2.5)
    ax.plot([notB_out[0], and3_in1[0]], [notB_out[1], and3_in1[1]], color=COLOR_B, lw=2.5)
    ax.plot([notC_out[0], and2_in2[0]], [notC_out[1], and2_in2[1]], color=COLOR_C, lw=2.5)
    ax.plot([notD_out[0], and4_in2[0]], [notD_out[1], and4_in2[1]], color=COLOR_D, lw=2.5)
    ax.plot([notE_out[0], and4_in3[0]], [notE_out[1], and4_in3[1]], color=COLOR_E, lw=2.5)
    
    ax.plot([and1_out[0], 10.2, 10.2, or4_in1[0]], [and1_out[1], and1_out[1], or4_in1[1], or4_in1[1]], color=COLOR_X1, lw=2.5)
    ax.text(and1_out[0] + 0.4, and1_out[1] + 0.25, r"$X_1 = \bar{A}B$", fontsize=11, color=COLOR_X1, fontweight='bold')
    
    ax.plot([and2_out[0], 10.5, 10.5, or4_in2[0]], [and2_out[1], and2_out[1], or4_in2[1], or4_in2[1]], color=COLOR_X2, lw=2.5)
    ax.text(and2_out[0] + 0.4, and2_out[1] + 0.25, r"$X_2 = A\bar{C}$", fontsize=11, color=COLOR_X2, fontweight='bold')
    
    ax.plot([and3_out[0], 10.5, 10.5, or4_in3[0]], [and3_out[1], and3_out[1], or4_in3[1], or4_in3[1]], color=COLOR_X3, lw=2.5)
    ax.text(and3_out[0] + 0.4, and3_out[1] + 0.25, r"$X_3 = \bar{B}DE$", fontsize=11, color=COLOR_X3, fontweight='bold')
    
    ax.plot([and4_out[0], 10.2, 10.2, or4_in4[0]], [and4_out[1], and4_out[1], or4_in4[1], or4_in4[1]], color=COLOR_X4, lw=2.5)
    ax.text(and4_out[0] + 0.4, and4_out[1] + 0.25, r"$X_4 = C\bar{D}\bar{E}$", fontsize=11, color=COLOR_X4, fontweight='bold')
    
    x_out_term = 14.8
    ax.plot([or4_out[0], x_out_term], [or4_out[1], or4_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax.add_patch(patches.Circle((x_out_term, or4_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, or4_out[1], r"$F = X_1 + X_2 + X_3 + X_4$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(7.5, 9.0, "Example 03: Standard 5-Variable AND-OR-NOT Logic Circuit Diagram", fontsize=16, fontweight='bold', ha='center', color='#1A5276')
    ax.text(7.5, 8.45, r"Full Expression: $F(A,B,C,D,E) = \bar{A}B + A\bar{C} + \bar{B}DE + C\bar{D}\bar{E}$", 
            fontsize=12, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#AED6F1", lw=1.5))
            
    ax.set_xlim(-0.8, 16.0)
    ax.set_ylim(0.2, 9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "digital_logic_circuit_redrawn.png"), bbox_inches='tight')
    plt.close()
    print("Saved digital_logic_circuit_redrawn.png")


def create_kmaps_8x4():
    row_labels = ['000', '001', '011', '010', '110', '111', '101', '100']
    col_labels = ['00', '01', '11', '10']

    grid_vals = []
    grid_minterms = []
    for r_idx, r_str in enumerate(row_labels):
        r_vals = []
        r_m = []
        A, B, C = int(r_str[0]), int(r_str[1]), int(r_str[2])
        for c_str in col_labels:
            D, E = int(c_str[0]), int(c_str[1])
            m_idx = (A<<4) | (B<<3) | (C<<2) | (D<<1) | E
            val = F_ref(A, B, C, D, E)
            r_vals.append(val)
            r_m.append(f"m{m_idx}")
        grid_vals.append(r_vals)
        grid_minterms.append(r_m)

    # 1. SOP 8x4 K-Map
    fig, ax = plt.subplots(figsize=(8, 11), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(2.0, 8.7, "Example 03: 5-Variable SOP Karnaugh Map (Grouping 1s)", fontsize=13, fontweight='bold', ha='center', color='#1A5276')
    ax.text(2.0, 8.35, "Vertical Rows = ABC (8 rows) | Horizontal Cols = DE (4 cols)", fontsize=10, ha='center', color='#2C3E50')

    for i in range(9): ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
    for j in range(5): ax.plot([j, j], [0, 8], color='#2C3E50', lw=1.5)
        
    ax.text(-0.5, 8.3, "ABC \\ DE", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels): ax.text(j + 0.5, 8.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels): ax.text(-0.35, 7.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')

    for r in range(8):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 7.5 - r
            x_pos = c + 0.5
            if val == 1:
                bg = patches.Rectangle((c, 7-r), 1, 1, facecolor='#D4EFDF', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=15, fontweight='bold', color='#196F3D', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=13, color='#7F8C8D', ha='center', va='center', zorder=3)
            ax.text(c + 0.85, 7.85 - r, grid_minterms[r][c], fontsize=6.5, color='#95A5A6', ha='right', va='top')

    # SOP Groupings (Powers of 2^n):
    # Group 1 (Size 8): A_bar B -> Rows ABC = 011 and 010 (r=2 and r=3)
    rect_g1 = patches.Rectangle((0.05, 4.05), 3.9, 1.9, linewidth=2.5, edgecolor='#E74C3C', facecolor='none', zorder=4)
    ax.add_patch(rect_g1)
    
    # Group 2 (Size 8): A C_bar -> Rows ABC = 110 and 100 (r=4 and r=7)
    rect_g2a = patches.Rectangle((0.05, 3.05), 3.9, 0.9, linewidth=2.5, edgecolor='#2980B9', facecolor='none', linestyle='--', zorder=4)
    rect_g2b = patches.Rectangle((0.05, 0.05), 3.9, 0.9, linewidth=2.5, edgecolor='#2980B9', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_g2a); ax.add_patch(rect_g2b)
    
    # Group 3 (Size 4): B_bar D E -> Col DE = 11 (c=2) in rows B=0
    rect_g3 = patches.Rectangle((2.05, 0.05), 0.9, 7.9, linewidth=2, edgecolor='#8E44AD', facecolor='none', linestyle=':', zorder=4)
    ax.add_patch(rect_g3)
    
    # Group 4 (Size 4): C D_bar E_bar -> Col DE = 00 (c=0) in rows C=1
    rect_g4 = patches.Rectangle((0.05, 1.05), 0.9, 5.9, linewidth=2, edgecolor='#D35400', facecolor='none', linestyle='-.', zorder=4)
    ax.add_patch(rect_g4)

    ax.text(2.0, -0.6, r"Minimal SOP: $F = \bar{A}B + A\bar{C} + \bar{B}DE + C\bar{D}\bar{E}$", fontsize=12, fontweight='bold', color='#196F3D', ha='center')
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-0.9, 9.0)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "kmap_sop_diagram.png"), bbox_inches='tight')
    plt.close()

    # 2. POS 8x4 K-Map (Grouping 0s)
    fig, ax = plt.subplots(figsize=(8, 11), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(2.0, 8.7, "Example 03: 5-Variable POS Karnaugh Map (Grouping 0s)", fontsize=13, fontweight='bold', ha='center', color='#78281F')
    ax.text(2.0, 8.35, "Vertical Rows = ABC (8 rows) | Horizontal Cols = DE (4 cols)", fontsize=10, ha='center', color='#2C3E50')

    for i in range(9): ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
    for j in range(5): ax.plot([j, j], [0, 8], color='#2C3E50', lw=1.5)
    ax.text(-0.5, 8.3, "ABC \\ DE", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels): ax.text(j + 0.5, 8.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels): ax.text(-0.35, 7.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')

    for r in range(8):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 7.5 - r
            x_pos = c + 0.5
            if val == 0:
                bg = patches.Rectangle((c, 7-r), 1, 1, facecolor='#FADBD8', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=15, fontweight='bold', color='#943126', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=13, color='#7F8C8D', ha='center', va='center', zorder=3)
            ax.text(c + 0.85, 7.85 - r, grid_minterms[r][c], fontsize=6.5, color='#95A5A6', ha='right', va='top')

    # POS Groupings (5 Pairs of Size 2 = 2^1):
    rect_p1 = patches.Rectangle((0.05, 7.05), 1.9, 0.9, linewidth=2, edgecolor='#E74C3C', facecolor='none', zorder=4)
    ax.add_patch(rect_p1)
    
    rect_p2 = patches.Rectangle((3.05, 6.05), 0.9, 1.9, linewidth=2, edgecolor='#2980B9', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_p2)
    
    rect_p3a = patches.Rectangle((1.05, 6.05), 0.9, 0.9, linewidth=2, edgecolor='#27AE60', facecolor='none', linestyle=':', zorder=4)
    rect_p3b = patches.Rectangle((1.05, 1.05), 0.9, 0.9, linewidth=2, edgecolor='#27AE60', facecolor='none', linestyle=':', zorder=4)
    ax.add_patch(rect_p3a); ax.add_patch(rect_p3b)
    
    rect_p4 = patches.Rectangle((3.05, 1.05), 0.9, 1.9, linewidth=2, edgecolor='#8E44AD', facecolor='none', linestyle='-.', zorder=4)
    ax.add_patch(rect_p4)
    
    rect_p5 = patches.Rectangle((1.05, 2.05), 1.9, 0.9, linewidth=2, edgecolor='#D35400', facecolor='none', zorder=4)
    ax.add_patch(rect_p5)

    ax.text(2.0, -0.6, r"Minimal POS: $F = (A+B+C+D)(A+B+\bar{D}+E)(B+\bar{C}+D+\bar{E})(\bar{A}+\bar{C}+\bar{D}+E)(\bar{A}+\bar{B}+\bar{C}+\bar{E})$", fontsize=9.5, fontweight='bold', color='#78281F', ha='center')
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-0.9, 9.0)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "kmap_pos_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved 8x4 K-Maps")


def create_pos_circuit_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    # 5 OR gates + 1 AND5 gate
    or1_in1, or1_in2, or1_in3, or1_in4, or1_out = draw_or4_gate(ax, 5.5, 7.5, width=1.6, height=1.6, label="OR1")
    or2_in1, or2_in2, or2_in3, or2_in4, or2_out = draw_or4_gate(ax, 5.5, 5.7, width=1.6, height=1.6, label="OR2")
    or3_in1, or3_in2, or3_in3, or3_in4, or3_out = draw_or4_gate(ax, 5.5, 3.9, width=1.6, height=1.6, label="OR3")
    or4_in1, or4_in2, or4_in3, or4_in4, or4_out = draw_or4_gate(ax, 5.5, 2.1, width=1.6, height=1.6, label="OR4")
    or5_in1, or5_in2, or5_in3, or5_in4, or5_out = draw_or4_gate(ax, 5.5, 0.3, width=1.6, height=1.6, label="OR5")
    
    and_final_in1, and_final_in2, and_final_in3, and_final_in4, and_final_in5, and_final_out = draw_and5_gate(ax, 10.5, 3.9, width=1.8, height=2.4, label="AND")
    
    ax.plot([or1_out[0], 9.5, 9.5, and_final_in1[0]], [or1_out[1], or1_out[1], and_final_in1[1], and_final_in1[1]], color=COLOR_X1, lw=2.5)
    ax.plot([or2_out[0], 9.7, 9.7, and_final_in2[0]], [or2_out[1], or2_out[1], and_final_in2[1], and_final_in2[1]], color=COLOR_X2, lw=2.5)
    ax.plot([or3_out[0], and_final_in3[0]], [or3_out[1], and_final_in3[1]], color=COLOR_X3, lw=2.5)
    ax.plot([or4_out[0], 9.7, 9.7, and_final_in4[0]], [or4_out[1], or4_out[1], and_final_in4[1], and_final_in4[1]], color=COLOR_X4, lw=2.5)
    ax.plot([or5_out[0], 9.5, 9.5, and_final_in5[0]], [or5_out[1], or5_out[1], and_final_in5[1], and_final_in5[1]], color=COLOR_A, lw=2.5)
    
    x_out_term = 14.0
    ax.plot([and_final_out[0], x_out_term], [and_final_out[1], and_final_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax.add_patch(patches.Circle((x_out_term, and_final_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, and_final_out[1], r"$F_{\text{POS}}$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(7.5, 9.0, "Minimal POS Circuit Schematic (OR-AND Logic)", fontsize=15, fontweight='bold', ha='center', color='#78281F')
    ax.set_xlim(-0.8, 15.5)
    ax.set_ylim(-0.8, 9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "pos_circuit_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved pos_circuit_diagram.png")

if __name__ == "__main__":
    create_redrawn_circuit()
    create_kmaps_8x4()
    create_pos_circuit_diagram()
