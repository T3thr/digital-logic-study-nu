import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Set typography styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

COLOR_A = "#E74C3C"      # Red
COLOR_B = "#2980B9"      # Blue
COLOR_C = "#27AE60"      # Green
COLOR_D = "#8E44AD"      # Purple

COLOR_INTER1 = "#D35400"  # Orange (AND1 out)
COLOR_INTER2 = "#16A085"  # Teal (OR1 out)
COLOR_NAND_OUT = "#C0392B"# Dark Red
COLOR_NOT_OUT = "#8E44AD" # Purple
COLOR_NOR_OUT = "#D4AC0D" # Gold
COLOR_FINAL_OUT = "#1A5276"# Dark Navy

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

def draw_nor3_gate(ax, x, y, width=1.5, height=1.4, label="", fill_color="#FADBD8", edge_color="#78281F", bubble_r=0.08):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    w_gate = width - bubble_r*2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.CURVE3, (x0 + w_gate*0.25, y)),
        (Path.CURVE3, (x0, y_top)),
        (Path.CURVE3, (x0 + w_gate*0.65, y_top)),
        (Path.CURVE3, (x0 + w_gate, y)),
        (Path.CURVE3, (x0 + w_gate*0.65, y_bot)),
        (Path.CURVE3, (x0, y_bot)),
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
        ax.text(x + w_gate*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0 + w_gate*0.1, y + height/3), (x0 + w_gate*0.1, y), (x0 + w_gate*0.1, y - height/3), (x + width, y)

def draw_kmap(ax, title, is_sop=True):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(2.0, 4.7, title, fontsize=14, fontweight='bold', ha='center', color='#1A5276')
    
    row_labels = ['00', '01', '11', '10']
    col_labels = ['00', '01', '11', '10']
    
    for i in range(5):
        ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
        
    ax.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    
    for j, col in enumerate(col_labels):
        ax.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
        
    for i, row in enumerate(row_labels):
        y_pos = 3.5 - i
        ax.text(-0.3, y_pos, row, fontsize=11, fontweight='bold', ha='center', va='center')

    grid_vals = [
        [0, 0, 0, 0], # AB=00
        [1, 0, 0, 1], # AB=01 -> m4=1 at CD=00, m6=1 at CD=10
        [0, 0, 0, 0], # AB=11
        [0, 0, 0, 0]  # AB=10
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
            if is_sop and val == 1:
                bg = patches.Rectangle((c, 3-r), 1, 1, facecolor='#D4EFDF', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=16, fontweight='bold', color='#196F3D', ha='center', va='center', zorder=3)
            elif not is_sop and val == 0:
                bg = patches.Rectangle((c, 3-r), 1, 1, facecolor='#FADBD8', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=15, color='#943126', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=14, color='#7F8C8D', ha='center', va='center', zorder=3)
            ax.text(c + 0.85, 3.85 - r, grid_minterms[r][c], fontsize=7, color='#95A5A6', ha='right', va='top')

    if is_sop:
        rect1 = patches.Rectangle((0.05, 2.05), 0.9, 0.9, linewidth=2.5, edgecolor='#27AE60', facecolor='none', linestyle='--', zorder=4)
        rect2 = patches.Rectangle((3.05, 2.05), 0.9, 0.9, linewidth=2.5, edgecolor='#27AE60', facecolor='none', linestyle='--', zorder=4)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        ax.annotate("", xy=(-0.1, 2.5), xytext=(4.1, 2.5),
                    arrowprops=dict(arrowstyle="<->", color="#27AE60", lw=2, connectionstyle="arc3,rad=-0.4"))
        ax.text(2.0, -0.6, r"Group (m4, m6): $\bar{A}B\bar{D}$", fontsize=12, fontweight='bold', color='#196F3D', ha='center')
    else:
        rect_r0 = patches.Rectangle((0.05, 3.05), 3.9, 0.9, linewidth=2, edgecolor='#E74C3C', facecolor='none', zorder=4)
        ax.add_patch(rect_r0)
        rect_r23 = patches.Rectangle((0.05, 0.05), 3.9, 1.9, linewidth=2, edgecolor='#2980B9', facecolor='none', zorder=4)
        ax.add_patch(rect_r23)
        rect_c12 = patches.Rectangle((1.05, 0.05), 1.9, 3.9, linewidth=2, edgecolor='#8E44AD', facecolor='none', linestyle=':', zorder=4)
        ax.add_patch(rect_c12)
        ax.text(2.0, -0.6, r"POS Grouping: $Y = (\bar{A})(B)(\bar{D}) = \overline{A + \bar{B} + D}$", fontsize=11, fontweight='bold', color='#78281F', ha='center')

    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-1.0, 5.0)

def generate_all():
    # 1. Redrawn
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    and1_in1, and1_in2, and1_out = draw_and_gate(ax, 3.5, 6.0, label="AND1")
    or1_in1, or1_in2, or1_out = draw_or_gate(ax, 3.5, 4.0, label="OR1")
    not1_in, not1_out = draw_not_gate(ax, 2.5, 1.8, label="NOT1")
    nand1_in1, nand1_in2, nand1_out = draw_nand_gate(ax, 7.5, 5.0, label="NAND1")
    nor1_in1, nor1_in2, nor1_out = draw_nor_gate(ax, 6.5, 1.5, label="NOR1")
    and2_in1, and2_in2, and2_out = draw_and_gate(ax, 11.0, 3.25, width=1.5, height=1.2, label="AND2")
    
    x_in = 0.5
    y_A, y_B, y_C, y_D = 6.25, 5.75, 3.75, 1.0
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${text}$", fontsize=14, fontweight='bold', color=color, ha='right', va='center')

    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    
    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))

    ax.plot([x_in, and1_in1[0]], [y_A, y_A], color=COLOR_A, lw=2.5, zorder=2)
    add_junc(1.6, y_A, COLOR_A)
    ax.plot([1.6, 1.6, or1_in1[0]], [y_A, or1_in1[1], or1_in1[1]], color=COLOR_A, lw=2.5, zorder=2)
    
    ax.plot([x_in, and1_in2[0]], [y_B, y_B], color=COLOR_B, lw=2.5, zorder=2)
    add_junc(1.2, y_B, COLOR_B)
    ax.plot([1.2, 1.2, not1_in[0]], [y_B, not1_in[1], not1_in[1]], color=COLOR_B, lw=2.5, zorder=2)
    
    ax.plot([x_in, or1_in2[0]], [y_C, y_C], color=COLOR_C, lw=2.5, zorder=2)
    ax.plot([x_in, nor1_in2[0]], [y_D, nor1_in2[1]], color=COLOR_D, lw=2.5, zorder=2)
    
    ax.plot([and1_out[0], 6.0, 6.0, nand1_in1[0]], [and1_out[1], and1_out[1], nand1_in1[1], nand1_in1[1]], color=COLOR_INTER1, lw=2.5, zorder=2)
    ax.text(and1_out[0] + 0.4, and1_out[1] + 0.25, r"$A \cdot B$", fontsize=11, color=COLOR_INTER1, fontweight='bold')
    
    ax.plot([or1_out[0], 6.5, 6.5, nand1_in2[0]], [or1_out[1], or1_out[1], nand1_in2[1], nand1_in2[1]], color=COLOR_INTER2, lw=2.5, zorder=2)
    ax.text(or1_out[0] + 0.4, or1_out[1] + 0.25, r"$A + C$", fontsize=11, color=COLOR_INTER2, fontweight='bold')
    
    ax.plot([not1_out[0], nor1_in1[0]], [not1_out[1], nor1_in1[1]], color=COLOR_NOT_OUT, lw=2.5, zorder=2)
    ax.text(not1_out[0] + 0.3, not1_out[1] + 0.25, r"$\bar{B}$", fontsize=11, color=COLOR_NOT_OUT, fontweight='bold')
    
    ax.plot([nand1_out[0], 10.0, 10.0, and2_in1[0]], [nand1_out[1], nand1_out[1], and2_in1[1], and2_in1[1]], color=COLOR_NAND_OUT, lw=2.5, zorder=2)
    ax.text(nand1_out[0] + 0.2, nand1_out[1] + 0.3, r"$\overline{(A \cdot B) \cdot (A + C)}$", fontsize=11, color=COLOR_NAND_OUT, fontweight='bold')
    
    ax.plot([nor1_out[0], 10.0, 10.0, and2_in2[0]], [nor1_out[1], nor1_out[1], and2_in2[1], and2_in2[1]], color=COLOR_NOR_OUT, lw=2.5, zorder=2)
    ax.text(nor1_out[0] + 0.5, nor1_out[1] - 0.3, r"$\overline{\bar{B} + D}$", fontsize=11, color=COLOR_NOR_OUT, fontweight='bold')
    
    x_out_term = 13.5
    ax.plot([and2_out[0], x_out_term], [and2_out[1], and2_out[1]], color=COLOR_FINAL_OUT, lw=3.0, zorder=2)
    ax.add_patch(patches.Circle((x_out_term, and2_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, and2_out[1], r"$Y$", fontsize=16, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(7.0, 7.4, "Redrawn Digital Logic Circuit Diagram", fontsize=16, fontweight='bold', ha='center', color='#1A5276')
    ax.text(7.0, 6.9, r"Original Boolean Function: $Y = \overline{(A \cdot B) \cdot (A + C)} \cdot \overline{\bar{B} + D}$", 
            fontsize=12, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", edgecolor="#AED6F1", lw=1.5))
            
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(0.2, 7.9)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_PATH, "digital_logic_circuit_redrawn.png"), bbox_inches='tight')
    plt.close()

    print("All diagrams generated successfully in", DIR_PATH)

if __name__ == "__main__":
    generate_all()
