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

COLOR_W1 = "#D35400"     # Orange (OR1 out)
COLOR_W2 = "#16A085"     # Teal (AND1 out)
COLOR_W3 = "#8E44AD"     # Purple (NOT1 out)
COLOR_W4 = "#C0392B"     # Dark Red (NOR1 out)
COLOR_W5 = "#D4AC0D"     # Gold (AND2 out)
COLOR_FINAL_OUT = "#1A5276"# Dark Navy (XOR1 out)

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

def draw_nand_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#FEF9E7", edge_color="#7D6608", bubble_r=0.08):
    in1, in2, _ = draw_and_gate(ax, x, y, width=width-bubble_r*2, height=height, label=label, fill_color=fill_color, edge_color=edge_color)
    bx = x + width - bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.2, zorder=4)
    ax.add_patch(bubble)
    return in1, in2, (x + width, y)

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

def draw_nor_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#FADBD8", edge_color="#78281F", bubble_r=0.08):
    in1, in2, _ = draw_or_gate(ax, x, y, width=width-bubble_r*2, height=height, label=label, fill_color=fill_color, edge_color=edge_color)
    bx = x + width - bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.2, zorder=4)
    ax.add_patch(bubble)
    return in1, in2, (x + width, y)

def draw_xor_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#FCF3CF", edge_color="#7D6608"):
    # Additional back curve offset
    x0 = x
    offset = 0.15
    path_back = [
        (Path.MOVETO, (x0 - offset, y - height/2)),
        (Path.CURVE3, (x0 - offset + width*0.25, y)),
        (Path.CURVE3, (x0 - offset, y + height/2))
    ]
    codes_b, verts_b = zip(*path_back)
    path_b = Path(verts_b, codes_b)
    patch_b = patches.PathPatch(path_b, facecolor='none', edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch_b)
    
    in1, in2, out = draw_or_gate(ax, x, y, width=width, height=height, label=label, fill_color=fill_color, edge_color=edge_color)
    return in1, in2, out

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
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Place Gates exactly matching image.png topology
    # Stage 1
    or1_in1, or1_in2, or1_out = draw_or_gate(ax, 3.5, 6.0, label="OR1")
    and1_in1, and1_in2, and1_out = draw_and_gate(ax, 3.5, 3.75, label="AND1")
    not1_in, not1_out = draw_not_gate(ax, 2.5, 1.2, label="NOT1")
    
    # Stage 2
    nor1_in1, nor1_in2, nor1_out = draw_nor_gate(ax, 7.5, 5.0, label="NOR1")
    and2_in1, and2_in2, and2_out = draw_and_gate(ax, 7.5, 1.8, label="AND2")
    
    # Stage 3 (Final)
    xor1_in1, xor1_in2, xor1_out = draw_xor_gate(ax, 11.5, 3.4, width=1.5, height=1.2, label="XOR1")
    
    # Input Terminals
    x_in = 0.5
    y_A = 6.25
    y_B = 5.75
    y_C = 3.75
    y_D = 1.2
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${text}$", fontsize=14, fontweight='bold', color=color, ha='right', va='center')

    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    
    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))

    # Wires & Buses
    # A (Line 1) -> OR1 top input
    ax.plot([x_in, or1_in1[0]], [y_A, y_A], color=COLOR_A, lw=2.5, zorder=2)
    # A junction -> AND1 bottom input (y = 3.5)
    x_branch_A = 1.8
    add_junc(x_branch_A, y_A, COLOR_A)
    ax.plot([x_branch_A, x_branch_A, and1_in2[0]], [y_A, and1_in2[1], and1_in2[1]], color=COLOR_A, lw=2.5, zorder=2)
    
    # B (Line 2) -> OR1 bottom input
    ax.plot([x_in, or1_in2[0]], [y_B, y_B], color=COLOR_B, lw=2.5, zorder=2)
    
    # C (Line 3) -> AND1 top input
    ax.plot([x_in, and1_in1[0]], [y_C, y_C], color=COLOR_C, lw=2.5, zorder=2)
    
    # D (Line 4) -> NOT1 input
    ax.plot([x_in, not1_in[0]], [y_D, y_D], color=COLOR_D, lw=2.5, zorder=2)
    
    # Intermediate Outputs
    # OR1 out -> NOR1 top input
    ax.plot([or1_out[0], 6.0, 6.0, nor1_in1[0]], [or1_out[1], or1_out[1], nor1_in1[1], nor1_in1[1]], color=COLOR_W1, lw=2.5, zorder=2)
    ax.text(or1_out[0] + 0.4, or1_out[1] + 0.25, r"$W_1 = A + B$", fontsize=11, color=COLOR_W1, fontweight='bold')
    
    # AND1 out -> NOR1 bottom input & AND2 top input
    x_branch_W2 = 5.8
    ax.plot([and1_out[0], x_branch_W2], [and1_out[1], and1_out[1]], color=COLOR_W2, lw=2.5, zorder=2)
    add_junc(x_branch_W2, and1_out[1], COLOR_W2)
    # branch UP to NOR1 bottom input
    ax.plot([x_branch_W2, x_branch_W2, nor1_in2[0]], [and1_out[1], nor1_in2[1], nor1_in2[1]], color=COLOR_W2, lw=2.5, zorder=2)
    # branch DOWN to AND2 top input
    ax.plot([x_branch_W2, x_branch_W2, and2_in1[0]], [and1_out[1], and2_in1[1], and2_in1[1]], color=COLOR_W2, lw=2.5, zorder=2)
    ax.text(and1_out[0] + 0.4, and1_out[1] + 0.25, r"$W_2 = A \cdot C$", fontsize=11, color=COLOR_W2, fontweight='bold')
    
    # NOT1 out -> AND2 bottom input
    ax.plot([not1_out[0], and2_in2[0]], [not1_out[1], and2_in2[1]], color=COLOR_W3, lw=2.5, zorder=2)
    ax.text(not1_out[0] + 0.5, not1_out[1] + 0.25, r"$W_3 = \bar{D}$", fontsize=11, color=COLOR_W3, fontweight='bold')
    
    # NOR1 out -> XOR1 top input
    ax.plot([nor1_out[0], 10.2, 10.2, xor1_in1[0]], [nor1_out[1], nor1_out[1], xor1_in1[1], xor1_in1[1]], color=COLOR_W4, lw=2.5, zorder=2)
    ax.text(nor1_out[0] + 0.2, nor1_out[1] + 0.3, r"$W_4 = \overline{(A+B)+(A\cdot C)} = \bar{A}\bar{B}$", fontsize=11, color=COLOR_W4, fontweight='bold')
    
    # AND2 out -> XOR1 bottom input
    ax.plot([and2_out[0], 10.2, 10.2, xor1_in2[0]], [and2_out[1], and2_out[1], xor1_in2[1], xor1_in2[1]], color=COLOR_W5, lw=2.5, zorder=2)
    ax.text(and2_out[0] + 0.4, and2_out[1] - 0.35, r"$W_5 = A \cdot C \cdot \bar{D}$", fontsize=11, color=COLOR_W5, fontweight='bold')
    
    # Final Output Terminal
    x_out_term = 14.0
    ax.plot([xor1_out[0], x_out_term], [xor1_out[1], xor1_out[1]], color=COLOR_FINAL_OUT, lw=3.0, zorder=2)
    ax.add_patch(patches.Circle((x_out_term, xor1_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, xor1_out[1], r"$Y = W_4 \oplus W_5$", fontsize=16, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    # Title & Subtitle
    ax.text(7.2, 7.5, "Example 02: Standard Redrawn Logic Circuit Diagram", fontsize=16, fontweight='bold', ha='center', color='#1A5276')
    ax.text(7.2, 6.95, r"Full Expression: $Y = \overline{(A + B) + (A \cdot C)} \oplus (A \cdot C \cdot \bar{D})$", 
            fontsize=12, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#AED6F1", lw=1.5))
            
    ax.set_xlim(-0.5, 15.2)
    ax.set_ylim(0.4, 7.9)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "digital_logic_circuit_redrawn.png"), bbox_inches='tight')
    plt.close()
    print("Saved digital_logic_circuit_redrawn.png")


def create_kmaps():
    # 1. SOP K-Map
    fig, ax = plt.subplots(figsize=(6.5, 6.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(2.0, 4.7, "Example 02: SOP Karnaugh Map (Grouping 1s)", fontsize=13, fontweight='bold', ha='center', color='#1A5276')
    
    row_labels = ['00', '01', '11', '10']
    col_labels = ['00', '01', '11', '10']
    for i in range(5):
        ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
    ax.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels):
        ax.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels):
        ax.text(-0.3, 3.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')

    # Grid values for Y = A'B' + AC D'
    grid_vals = [
        [1, 1, 1, 1], # AB=00 (m0, m1, m3, m2) -> ALL 1
        [0, 0, 0, 0], # AB=01 -> ALL 0
        [0, 0, 0, 1], # AB=11 -> m14=1 at CD=10
        [0, 0, 0, 1]  # AB=10 -> m10=1 at CD=10
    ]
    grid_minterms = [
        ["m0", "m1", "m3", "m2"],
        ["m4", "m5", "m7", "m6"],
        ["m12", "m13", "m15", "m14"],
        ["m8", "m9", "m11", "m10"]
    ]

    for r in range(4):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 3.5 - r
            x_pos = c + 0.5
            if val == 1:
                bg = patches.Rectangle((c, 3-r), 1, 1, facecolor='#D4EFDF', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=16, fontweight='bold', color='#196F3D', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=14, color='#7F8C8D', ha='center', va='center', zorder=3)
            ax.text(c + 0.85, 3.85 - r, grid_minterms[r][c], fontsize=7, color='#95A5A6', ha='right', va='top')

    # Group 1 (Quad m0,m1,m3,m2 in row AB=00): A'B'
    rect_quad = patches.Rectangle((0.05, 3.05), 3.9, 0.9, linewidth=2.5, edgecolor='#27AE60', facecolor='none', zorder=4)
    ax.add_patch(rect_quad)
    
    # Group 2 (Pair m10,m14 at CD=10 in rows AB=11,10): AC D'
    rect_pair = patches.Rectangle((3.05, 0.05), 0.9, 1.9, linewidth=2.5, edgecolor='#2980B9', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_pair)
    
    ax.text(2.0, -0.6, r"Minimal SOP: $Y = \bar{A}\bar{B} + A C \bar{D}$", fontsize=13, fontweight='bold', color='#196F3D', ha='center')
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-0.9, 5.0)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "kmap_sop_diagram.png"), bbox_inches='tight')
    plt.close()

    # 2. POS K-Map
    fig, ax = plt.subplots(figsize=(6.5, 6.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(2.0, 4.7, "Example 02: POS Karnaugh Map (Grouping 0s)", fontsize=13, fontweight='bold', ha='center', color='#78281F')
    
    for i in range(5):
        ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
    ax.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels):
        ax.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels):
        ax.text(-0.3, 3.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')

    for r in range(4):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 3.5 - r
            x_pos = c + 0.5
            if val == 0:
                bg = patches.Rectangle((c, 3-r), 1, 1, facecolor='#FADBD8', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=16, fontweight='bold', color='#943126', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=14, color='#7F8C8D', ha='center', va='center', zorder=3)
            ax.text(c + 0.85, 3.85 - r, grid_minterms[r][c], fontsize=7, color='#95A5A6', ha='right', va='top')

    # Group 1 (Quad 0s in row AB=01): (A + B')
    rect_p1 = patches.Rectangle((0.05, 2.05), 3.9, 0.9, linewidth=2.5, edgecolor='#E74C3C', facecolor='none', zorder=4)
    ax.add_patch(rect_p1)
    
    # Group 2 (Quad 0s in cols CD=00,01 of rows AB=11,10): (A' + C)
    rect_p2 = patches.Rectangle((0.05, 0.05), 1.9, 1.9, linewidth=2.5, edgecolor='#8E44AD', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_p2)
    
    # Group 3 (Quad 0s in cols CD=01,11 of rows AB=11,10): (A' + D')
    rect_p3 = patches.Rectangle((1.05, 0.05), 1.9, 1.9, linewidth=2.5, edgecolor='#2980B9', facecolor='none', linestyle=':', zorder=4)
    ax.add_patch(rect_p3)
    
    ax.text(2.0, -0.6, r"Minimal POS: $Y = (A + \bar{B}) \cdot (\bar{A} + C) \cdot (\bar{A} + \bar{D})$", fontsize=12, fontweight='bold', color='#78281F', ha='center')
    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-0.9, 5.0)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "kmap_pos_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved K-Map images")


def create_circuit_diagrams():
    # 1. Minimal SOP Circuit: Y = A'B' + AC D'
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Gates: NOT A, NOT B, NOT D, AND2 (A'B'), AND3 (AC D'), OR2 (final)
    notA_in, notA_out = draw_not_gate(ax, 2.0, 5.0, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax, 2.0, 3.8, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax, 2.0, 1.2, label="NOT D")
    
    and_sop1_in1, and_sop1_in2, and_sop1_out = draw_and_gate(ax, 5.2, 4.4, width=1.5, height=1.2, label="AND1")
    and_sop2_in1, and_sop2_in2, and_sop2_in3, and_sop2_out = draw_and3_gate(ax, 5.2, 1.8, width=1.6, height=1.4, label="AND2")
    
    or_final_in1, or_final_in2, or_final_out = draw_or_gate(ax, 9.2, 3.1, width=1.6, height=1.4, label="OR")
    
    x_in = 0.3
    y_A, y_B, y_C, y_D = 5.0, 3.8, 2.5, 1.2
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.1, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.2, y, f"${text}$", fontsize=13, fontweight='bold', color=color, ha='right', va='center')

    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    
    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))

    # Wires for SOP
    # A -> NOT A & AND2 top
    ax.plot([x_in, notA_in[0]], [y_A, y_A], color=COLOR_A, lw=2)
    ax.plot([notA_out[0], and_sop1_in1[0]], [notA_out[1], and_sop1_in1[1]], color=COLOR_A, lw=2)
    add_junc(1.2, y_A, COLOR_A)
    ax.plot([1.2, 1.2, and_sop2_in1[0]], [y_A, and_sop2_in1[1], and_sop2_in1[1]], color=COLOR_A, lw=2)
    
    # B -> NOT B
    ax.plot([x_in, notB_in[0]], [y_B, y_B], color=COLOR_B, lw=2)
    ax.plot([notB_out[0], and_sop1_in2[0]], [notB_out[1], and_sop1_in2[1]], color=COLOR_B, lw=2)
    
    # C -> AND2 middle
    ax.plot([x_in, and_sop2_in2[0]], [y_C, and_sop2_in2[1]], color=COLOR_C, lw=2)
    
    # D -> NOT D
    ax.plot([x_in, notD_in[0]], [y_D, y_D], color=COLOR_D, lw=2)
    ax.plot([notD_out[0], and_sop2_in3[0]], [notD_out[1], and_sop2_in3[1]], color=COLOR_D, lw=2)
    
    # Outputs to OR gate
    ax.plot([and_sop1_out[0], 8.2, 8.2, or_final_in1[0]], [and_sop1_out[1], and_sop1_out[1], or_final_in1[1], or_final_in1[1]], color=COLOR_W1, lw=2.5)
    ax.text(and_sop1_out[0] + 0.3, and_sop1_out[1] + 0.25, r"$\bar{A}\bar{B}$", fontsize=11, color=COLOR_W1, fontweight='bold')
    
    ax.plot([and_sop2_out[0], 8.2, 8.2, or_final_in2[0]], [and_sop2_out[1], and_sop2_out[1], or_final_in2[1], or_final_in2[1]], color=COLOR_W2, lw=2.5)
    ax.text(and_sop2_out[0] + 0.3, and_sop2_out[1] + 0.25, r"$A C \bar{D}$", fontsize=11, color=COLOR_W2, fontweight='bold')
    
    x_out_term = 12.0
    ax.plot([or_final_out[0], x_out_term], [or_final_out[1], or_final_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax.add_patch(patches.Circle((x_out_term, or_final_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, or_final_out[1], r"$Y = \bar{A}\bar{B} + A C \bar{D}$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(6.0, 6.0, "Minimal SOP Circuit Schematic (AND-OR Logic)", fontsize=15, fontweight='bold', ha='center', color='#1A5276')
    ax.set_xlim(-0.8, 14.5)
    ax.set_ylim(0.5, 6.4)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "sop_circuit_diagram.png"), bbox_inches='tight')
    plt.close()

    # 2. Minimal POS Circuit: Y = (A + B')(A' + C)(A' + D')
    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Gates: NOT A, NOT B, NOT D, OR1 (A+B'), OR2 (A'+C), OR3 (A'+D'), AND3 (final)
    notA_in, notA_out = draw_not_gate(ax, 2.0, 5.8, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax, 2.0, 4.4, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax, 2.0, 1.2, label="NOT D")
    
    or_p1_in1, or_p1_in2, or_p1_out = draw_or_gate(ax, 5.2, 5.0, width=1.5, height=1.2, label="OR1")
    or_p2_in1, or_p2_in2, or_p2_out = draw_or_gate(ax, 5.2, 3.2, width=1.5, height=1.2, label="OR2")
    or_p3_in1, or_p3_in2, or_p3_out = draw_or_gate(ax, 5.2, 1.4, width=1.5, height=1.2, label="OR3")
    
    and_final_in1, and_final_in2, and_final_in3, and_final_out = draw_and3_gate(ax, 9.2, 3.2, width=1.6, height=1.6, label="AND")
    
    y_A, y_B, y_C, y_D = 5.8, 4.4, 2.8, 1.2
    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    
    # Wires for POS
    # A -> OR1 top & NOT A
    add_junc(1.0, y_A, COLOR_A)
    ax.plot([x_in, 1.0, 1.0, or_p1_in1[0]], [y_A, y_A, or_p1_in1[1], or_p1_in1[1]], color=COLOR_A, lw=2)
    ax.plot([1.0, notA_in[0]], [y_A, y_A], color=COLOR_A, lw=2)
    
    # NOT A out -> OR2 top & OR3 top
    add_junc(4.2, y_A, COLOR_A)
    ax.plot([notA_out[0], 4.2], [notA_out[1], notA_out[1]], color=COLOR_A, lw=2)
    ax.plot([4.2, 4.2, or_p2_in1[0]], [y_A, or_p2_in1[1], or_p2_in1[1]], color=COLOR_A, lw=2)
    ax.plot([4.2, 4.2, or_p3_in1[0]], [y_A, or_p3_in1[1], or_p3_in1[1]], color=COLOR_A, lw=2)
    
    # B -> NOT B -> OR1 bottom
    ax.plot([x_in, notB_in[0]], [y_B, y_B], color=COLOR_B, lw=2)
    ax.plot([notB_out[0], 4.8, 4.8, or_p1_in2[0]], [notB_out[1], notB_out[1], or_p1_in2[1], or_p1_in2[1]], color=COLOR_B, lw=2)
    
    # C -> OR2 bottom
    ax.plot([x_in, or_p2_in2[0]], [y_C, or_p2_in2[1]], color=COLOR_C, lw=2)
    
    # D -> NOT D -> OR3 bottom
    ax.plot([x_in, notD_in[0]], [y_D, y_D], color=COLOR_D, lw=2)
    ax.plot([notD_out[0], or_p3_in2[0]], [notD_out[1], or_p3_in2[1]], color=COLOR_D, lw=2)
    
    # OR outputs to final AND
    ax.plot([or_p1_out[0], 8.2, 8.2, and_final_in1[0]], [or_p1_out[1], or_p1_out[1], and_final_in1[1], and_final_in1[1]], color=COLOR_W1, lw=2.5)
    ax.text(or_p1_out[0] + 0.3, or_p1_out[1] + 0.25, r"$A + \bar{B}$", fontsize=11, color=COLOR_W1, fontweight='bold')
    
    ax.plot([or_p2_out[0], and_final_in2[0]], [or_p2_out[1], and_final_in2[1]], color=COLOR_W2, lw=2.5)
    ax.text(or_p2_out[0] + 0.3, or_p2_out[1] + 0.25, r"$\bar{A} + C$", fontsize=11, color=COLOR_W2, fontweight='bold')
    
    ax.plot([or_p3_out[0], 8.2, 8.2, and_final_in3[0]], [or_p3_out[1], or_p3_out[1], and_final_in3[1], and_final_in3[1]], color=COLOR_W3, lw=2.5)
    ax.text(or_p3_out[0] + 0.3, or_p3_out[1] - 0.35, r"$\bar{A} + \bar{D}$", fontsize=11, color=COLOR_W3, fontweight='bold')
    
    x_out_term = 12.5
    ax.plot([and_final_out[0], x_out_term], [and_final_out[1], and_final_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax.add_patch(patches.Circle((x_out_term, and_final_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, and_final_out[1], r"$Y = (A + \bar{B})(\bar{A} + C)(\bar{A} + \bar{D})$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(6.5, 6.7, "Minimal POS Circuit Schematic (OR-AND Logic)", fontsize=15, fontweight='bold', ha='center', color='#78281F')
    ax.set_xlim(-0.8, 15.5)
    ax.set_ylim(0.4, 7.2)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "pos_circuit_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved circuit diagrams")


def create_comparisons():
    # 1. Simplified Circuit (SOP based)
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    notA_in, notA_out = draw_not_gate(ax, 2.0, 5.0, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax, 2.0, 3.8, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax, 2.0, 1.2, label="NOT D")
    
    and_sop1_in1, and_sop1_in2, and_sop1_out = draw_and_gate(ax, 5.2, 4.4, width=1.5, height=1.2, label="AND1")
    and_sop2_in1, and_sop2_in2, and_sop2_in3, and_sop2_out = draw_and3_gate(ax, 5.2, 1.8, width=1.6, height=1.4, label="AND2")
    
    or_final_in1, or_final_in2, or_final_out = draw_or_gate(ax, 9.2, 3.1, width=1.6, height=1.4, label="OR")
    
    x_in = 0.3
    y_A, y_B, y_C, y_D = 5.0, 3.8, 2.5, 1.2
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.1, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.2, y, f"${text}$", fontsize=13, fontweight='bold', color=color, ha='right', va='center')

    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    
    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))

    ax.plot([x_in, notA_in[0]], [y_A, y_A], color=COLOR_A, lw=2)
    ax.plot([notA_out[0], and_sop1_in1[0]], [notA_out[1], and_sop1_in1[1]], color=COLOR_A, lw=2)
    add_junc(1.2, y_A, COLOR_A)
    ax.plot([1.2, 1.2, and_sop2_in1[0]], [y_A, and_sop2_in1[1], and_sop2_in1[1]], color=COLOR_A, lw=2)
    
    ax.plot([x_in, notB_in[0]], [y_B, y_B], color=COLOR_B, lw=2)
    ax.plot([notB_out[0], and_sop1_in2[0]], [notB_out[1], and_sop1_in2[1]], color=COLOR_B, lw=2)
    ax.plot([x_in, and_sop2_in2[0]], [y_C, and_sop2_in2[1]], color=COLOR_C, lw=2)
    ax.plot([x_in, notD_in[0]], [y_D, y_D], color=COLOR_D, lw=2)
    ax.plot([notD_out[0], and_sop2_in3[0]], [notD_out[1], and_sop2_in3[1]], color=COLOR_D, lw=2)
    
    ax.plot([and_sop1_out[0], 8.2, 8.2, or_final_in1[0]], [and_sop1_out[1], and_sop1_out[1], or_final_in1[1], or_final_in1[1]], color=COLOR_W1, lw=2.5)
    ax.plot([and_sop2_out[0], 8.2, 8.2, or_final_in2[0]], [and_sop2_out[1], and_sop2_out[1], or_final_in2[1], or_final_in2[1]], color=COLOR_W2, lw=2.5)
    
    x_out_term = 12.0
    ax.plot([or_final_out[0], x_out_term], [or_final_out[1], or_final_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax.add_patch(patches.Circle((x_out_term, or_final_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, or_final_out[1], r"$Y = \bar{A}\bar{B} + A C \bar{D}$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(6.0, 6.0, "Simplified Equivalent Digital Logic Circuit", fontsize=15, fontweight='bold', ha='center', color='#1E8449')
    ax.set_xlim(-0.8, 14.5)
    ax.set_ylim(0.5, 6.4)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "digital_logic_circuit_simplified.png"), bbox_inches='tight')
    plt.close()

    # 2. Circuit Comparison (Redrawn vs Simplified)
    fig = plt.figure(figsize=(15, 14), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    for ax in [ax1, ax2]:
        ax.set_aspect('equal')
        ax.axis('off')
        
    # Top: Original 6-gate circuit
    or1_in1, or1_in2, or1_out = draw_or_gate(ax1, 3.5, 6.0, label="OR1")
    and1_in1, and1_in2, and1_out = draw_and_gate(ax1, 3.5, 3.75, label="AND1")
    not1_in, not1_out = draw_not_gate(ax1, 2.5, 1.2, label="NOT1")
    nor1_in1, nor1_in2, nor1_out = draw_nor_gate(ax1, 7.5, 5.0, label="NOR1")
    and2_in1, and2_in2, and2_out = draw_and_gate(ax1, 7.5, 1.8, label="AND2")
    xor1_in1, xor1_in2, xor1_out = draw_xor_gate(ax1, 11.5, 3.4, width=1.5, height=1.2, label="XOR1")
    
    x_in = 0.5
    y_A, y_B, y_C, y_D = 6.25, 5.75, 3.75, 1.2
    
    def add_t(ax, x, y, txt, col):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=col, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${txt}$", fontsize=14, fontweight='bold', color=col, ha='right', va='center')

    add_t(ax1, x_in, y_A, "A", COLOR_A)
    add_t(ax1, x_in, y_B, "B", COLOR_B)
    add_t(ax1, x_in, y_C, "C", COLOR_C)
    add_t(ax1, x_in, y_D, "D", COLOR_D)
    
    ax1.plot([x_in, or1_in1[0]], [y_A, y_A], color=COLOR_A, lw=2.5)
    ax1.plot([1.8, 1.8, and1_in2[0]], [y_A, and1_in2[1], and1_in2[1]], color=COLOR_A, lw=2.5)
    ax1.plot([x_in, or1_in2[0]], [y_B, y_B], color=COLOR_B, lw=2.5)
    ax1.plot([x_in, and1_in1[0]], [y_C, y_C], color=COLOR_C, lw=2.5)
    ax1.plot([x_in, not1_in[0]], [y_D, y_D], color=COLOR_D, lw=2.5)
    
    ax1.plot([or1_out[0], 6.0, 6.0, nor1_in1[0]], [or1_out[1], or1_out[1], nor1_in1[1], nor1_in1[1]], color=COLOR_W1, lw=2.5)
    ax1.plot([and1_out[0], 5.8], [and1_out[1], and1_out[1]], color=COLOR_W2, lw=2.5)
    ax1.plot([5.8, 5.8, nor1_in2[0]], [and1_out[1], nor1_in2[1], nor1_in2[1]], color=COLOR_W2, lw=2.5)
    ax1.plot([5.8, 5.8, and2_in1[0]], [and1_out[1], and2_in1[1], and2_in1[1]], color=COLOR_W2, lw=2.5)
    ax1.plot([not1_out[0], and2_in2[0]], [not1_out[1], and2_in2[1]], color=COLOR_W3, lw=2.5)
    ax1.plot([nor1_out[0], 10.2, 10.2, xor1_in1[0]], [nor1_out[1], nor1_out[1], xor1_in1[1], xor1_in1[1]], color=COLOR_W4, lw=2.5)
    ax1.plot([and2_out[0], 10.2, 10.2, xor1_in2[0]], [and2_out[1], and2_out[1], xor1_in2[1], xor1_in2[1]], color=COLOR_W5, lw=2.5)
    
    x_out_term = 14.0
    ax1.plot([xor1_out[0], x_out_term], [xor1_out[1], xor1_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax1.add_patch(patches.Circle((x_out_term, xor1_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax1.text(x_out_term + 0.3, xor1_out[1], r"$Y$", fontsize=16, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    ax1.text(7.2, 7.5, "(1) Original Complex Circuit (6 Gates)", fontsize=15, fontweight='bold', ha='center', color='#1A5276')
    ax1.set_xlim(-0.5, 15.2)
    ax1.set_ylim(0.4, 7.9)

    # Bottom: Simplified circuit
    notA_in, notA_out = draw_not_gate(ax2, 3.5, 5.0, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax2, 3.5, 3.8, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax2, 3.5, 1.2, label="NOT D")
    and_sop1_in1, and_sop1_in2, and_sop1_out = draw_and_gate(ax2, 6.7, 4.4, width=1.5, height=1.2, label="AND1")
    and_sop2_in1, and_sop2_in2, and_sop2_in3, and_sop2_out = draw_and3_gate(ax2, 6.7, 1.8, width=1.6, height=1.4, label="AND2")
    or_final_in1, or_final_in2, or_final_out = draw_or_gate(ax2, 10.7, 3.1, width=1.6, height=1.4, label="OR")
    
    add_t(ax2, x_in, y_A, "A", COLOR_A)
    add_t(ax2, x_in, y_B, "B", COLOR_B)
    add_t(ax2, x_in, y_C, "C", COLOR_C)
    add_t(ax2, x_in, y_D, "D", COLOR_D)
    
    ax2.plot([x_in, notA_in[0]], [y_A, y_A], color=COLOR_A, lw=2)
    ax2.plot([notA_out[0], and_sop1_in1[0]], [notA_out[1], and_sop1_in1[1]], color=COLOR_A, lw=2)
    ax2.plot([1.8, 1.8, and_sop2_in1[0]], [y_A, and_sop2_in1[1], and_sop2_in1[1]], color=COLOR_A, lw=2)
    ax2.plot([x_in, notB_in[0]], [y_B, y_B], color=COLOR_B, lw=2)
    ax2.plot([notB_out[0], and_sop1_in2[0]], [notB_out[1], and_sop1_in2[1]], color=COLOR_B, lw=2)
    ax2.plot([x_in, and_sop2_in2[0]], [y_C, and_sop2_in2[1]], color=COLOR_C, lw=2)
    ax2.plot([x_in, notD_in[0]], [y_D, y_D], color=COLOR_D, lw=2)
    ax2.plot([notD_out[0], and_sop2_in3[0]], [notD_out[1], and_sop2_in3[1]], color=COLOR_D, lw=2)
    ax2.plot([and_sop1_out[0], 9.7, 9.7, or_final_in1[0]], [and_sop1_out[1], and_sop1_out[1], or_final_in1[1], or_final_in1[1]], color=COLOR_W1, lw=2.5)
    ax2.plot([and_sop2_out[0], 9.7, 9.7, or_final_in2[0]], [and_sop2_out[1], and_sop2_out[1], or_final_in2[1], or_final_in2[1]], color=COLOR_W2, lw=2.5)
    
    ax2.plot([or_final_out[0], x_out_term], [or_final_out[1], or_final_out[1]], color=COLOR_FINAL_OUT, lw=3)
    ax2.add_patch(patches.Circle((x_out_term, or_final_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax2.text(x_out_term + 0.3, or_final_out[1], r"$Y = \bar{A}\bar{B} + A C \bar{D}$", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    ax2.text(7.2, 6.5, r"(2) Minimal Simplified Circuit ($Y = \bar{A}\bar{B} + A C \bar{D}$)", fontsize=15, fontweight='bold', ha='center', color='#1E8449')
    ax2.set_xlim(-0.5, 15.2)
    ax2.set_ylim(0.4, 7.2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "digital_logic_circuit_comparison.png"), bbox_inches='tight')
    plt.close()

    # 3. SOP vs POS Comparison
    fig = plt.figure(figsize=(15, 12), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    
    # Subplot 1: SOP K-Map
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.text(2.0, 4.7, "(A) SOP K-Map (Group 1s)", fontsize=13, fontweight='bold', ha='center', color='#1A5276')
    for i in range(5):
        ax1.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax1.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
    row_labels = ['00', '01', '11', '10']
    col_labels = ['00', '01', '11', '10']
    ax1.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels): ax1.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels): ax1.text(-0.3, 3.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')
    grid_vals = [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1]]
    for r in range(4):
        for c in range(4):
            v = grid_vals[r][c]
            if v == 1:
                ax1.add_patch(patches.Rectangle((c, 3-r), 1, 1, facecolor='#D4EFDF'))
                ax1.text(c+0.5, 3.5-r, str(v), fontsize=15, fontweight='bold', color='#196F3D', ha='center', va='center')
            else:
                ax1.text(c+0.5, 3.5-r, str(v), fontsize=13, color='#7F8C8D', ha='center', va='center')
    ax1.add_patch(patches.Rectangle((0.05, 3.05), 3.9, 0.9, linewidth=2, edgecolor='#27AE60', facecolor='none'))
    ax1.add_patch(patches.Rectangle((3.05, 0.05), 0.9, 1.9, linewidth=2, edgecolor='#2980B9', facecolor='none', linestyle='--'))
    ax1.set_xlim(-0.8, 4.8); ax1.set_ylim(-0.8, 5.0)

    # Subplot 2: POS K-Map
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.text(2.0, 4.7, "(B) POS K-Map (Group 0s)", fontsize=13, fontweight='bold', ha='center', color='#78281F')
    for i in range(5):
        ax2.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax2.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
    ax2.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    for j, col in enumerate(col_labels): ax2.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
    for i, row in enumerate(row_labels): ax2.text(-0.3, 3.5 - i, row, fontsize=11, fontweight='bold', ha='center', va='center')
    for r in range(4):
        for c in range(4):
            v = grid_vals[r][c]
            if v == 0:
                ax2.add_patch(patches.Rectangle((c, 3-r), 1, 1, facecolor='#FADBD8'))
                ax2.text(c+0.5, 3.5-r, str(v), fontsize=15, fontweight='bold', color='#943126', ha='center', va='center')
            else:
                ax2.text(c+0.5, 3.5-r, str(v), fontsize=13, color='#7F8C8D', ha='center', va='center')
    ax2.add_patch(patches.Rectangle((0.05, 2.05), 3.9, 0.9, linewidth=2, edgecolor='#E74C3C', facecolor='none'))
    ax2.add_patch(patches.Rectangle((0.05, 0.05), 1.9, 1.9, linewidth=2, edgecolor='#8E44AD', facecolor='none', linestyle='--'))
    ax2.add_patch(patches.Rectangle((1.05, 0.05), 1.9, 1.9, linewidth=2, edgecolor='#2980B9', facecolor='none', linestyle=':'))
    ax2.set_xlim(-0.8, 4.8); ax2.set_ylim(-0.8, 5.0)

    # Subplot 3: Minimal SOP Circuit
    ax3.set_aspect('equal'); ax3.axis('off')
    notA_in, notA_out = draw_not_gate(ax3, 2.0, 3.6, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax3, 2.0, 2.6, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax3, 2.0, 0.8, label="NOT D")
    and_sop1_in1, and_sop1_in2, and_sop1_out = draw_and_gate(ax3, 4.5, 3.1, width=1.4, height=1.2, label="AND1")
    and_sop2_in1, and_sop2_in2, and_sop2_in3, and_sop2_out = draw_and3_gate(ax3, 4.5, 1.2, width=1.4, height=1.2, label="AND2")
    or_final_in1, or_final_in2, or_final_out = draw_or_gate(ax3, 7.5, 2.1, width=1.4, height=1.2, label="OR")
    ax3.plot([and_sop1_out[0], 6.8, 6.8, or_final_in1[0]], [and_sop1_out[1], and_sop1_out[1], or_final_in1[1], or_final_in1[1]], color=COLOR_W1, lw=2)
    ax3.plot([and_sop2_out[0], 6.8, 6.8, or_final_in2[0]], [and_sop2_out[1], and_sop2_out[1], or_final_in2[1], or_final_in2[1]], color=COLOR_W2, lw=2)
    ax3.plot([or_final_out[0], 9.5], [or_final_out[1], or_final_out[1]], color=COLOR_FINAL_OUT, lw=2.5)
    ax3.text(9.7, or_final_out[1], r"$Y = \bar{A}\bar{B} + A C \bar{D}$", fontsize=12, fontweight='bold', color=COLOR_FINAL_OUT, va='center')
    ax3.text(4.0, 4.5, "(C) Minimal SOP Circuit (AND-OR)", fontsize=13, fontweight='bold', ha='center', color='#1A5276')
    ax3.set_xlim(-0.8, 12.0); ax3.set_ylim(0.2, 4.8)

    # Subplot 4: Minimal POS Circuit
    ax4.set_aspect('equal'); ax4.axis('off')
    notA_in, notA_out = draw_not_gate(ax4, 1.8, 3.8, label="NOT A")
    notB_in, notB_out = draw_not_gate(ax4, 1.8, 2.8, label="NOT B")
    notD_in, notD_out = draw_not_gate(ax4, 1.8, 0.8, label="NOT D")
    or_p1_in1, or_p1_in2, or_p1_out = draw_or_gate(ax4, 4.3, 3.4, width=1.3, height=1.1, label="OR1")
    or_p2_in1, or_p2_in2, or_p2_out = draw_or_gate(ax4, 4.3, 2.1, width=1.3, height=1.1, label="OR2")
    or_p3_in1, or_p3_in2, or_p3_out = draw_or_gate(ax4, 4.3, 0.8, width=1.3, height=1.1, label="OR3")
    and_final_in1, and_final_in2, and_final_in3, and_final_out = draw_and3_gate(ax4, 7.3, 2.1, width=1.4, height=1.4, label="AND")
    ax4.plot([or_p1_out[0], 6.5, 6.5, and_final_in1[0]], [or_p1_out[1], or_p1_out[1], and_final_in1[1], and_final_in1[1]], color=COLOR_W1, lw=2)
    ax4.plot([or_p2_out[0], and_final_in2[0]], [or_p2_out[1], and_final_in2[1]], color=COLOR_W2, lw=2)
    ax4.plot([or_p3_out[0], 6.5, 6.5, and_final_in3[0]], [or_p3_out[1], or_p3_out[1], and_final_in3[1], and_final_in3[1]], color=COLOR_W3, lw=2)
    ax4.plot([and_final_out[0], 9.5], [and_final_out[1], and_final_out[1]], color=COLOR_FINAL_OUT, lw=2.5)
    ax4.text(9.7, and_final_out[1], r"$Y = (A+\bar{B})(\bar{A}+C)(\bar{A}+\bar{D})$", fontsize=11, fontweight='bold', color=COLOR_FINAL_OUT, va='center')
    ax4.text(4.0, 4.5, "(D) Minimal POS Circuit (OR-AND)", fontsize=13, fontweight='bold', ha='center', color='#78281F')
    ax4.set_xlim(-0.8, 12.0); ax4.set_ylim(0.2, 4.8)

    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "sop_pos_comparison.png"), bbox_inches='tight')
    plt.close()
    print("Saved all comparisons")

if __name__ == "__main__":
    create_redrawn_circuit()
    create_kmaps()
    create_circuit_diagrams()
    create_comparisons()
