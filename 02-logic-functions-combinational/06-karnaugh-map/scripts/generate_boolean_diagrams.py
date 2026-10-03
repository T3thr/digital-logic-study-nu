import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Set clean typography styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'

COLOR_A = "#E74C3C"      # Red
COLOR_B = "#2980B9"      # Blue
COLOR_C = "#27AE60"      # Green
COLOR_D = "#8E44AD"      # Purple
COLOR_FINAL_OUT = "#1A5276" # Dark Navy

# --- K-MAP DRAWING FUNCTION ---
def draw_kmap(ax, title, is_sop=True):
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    ax.text(2.0, 4.7, title, fontsize=14, fontweight='bold', ha='center', color='#1A5276')
    
    # K-map grid 4x4
    # Rows: AB (00, 01, 11, 10) -> y = 3, 2, 1, 0
    # Cols: CD (00, 01, 11, 10) -> x = 0, 1, 2, 3
    
    row_labels = ['00', '01', '11', '10']
    col_labels = ['00', '01', '11', '10']
    
    # Draw Grid background & lines
    for i in range(5):
        ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.5)
        ax.plot([i, i], [0, 4], color='#2C3E50', lw=1.5)
        
    # Headers
    ax.text(-0.5, 4.3, "AB \\ CD", fontsize=11, fontweight='bold', ha='center', va='center')
    
    for j, col in enumerate(col_labels):
        ax.text(j + 0.5, 4.2, col, fontsize=11, fontweight='bold', ha='center', va='center')
        
    for i, row in enumerate(row_labels):
        # row index in plot y: row 00 is y=3, 01 is y=2, 11 is y=1, 10 is y=0
        y_pos = 3.5 - i
        ax.text(-0.3, y_pos, row, fontsize=11, fontweight='bold', ha='center', va='center')

    # Values matrix (A,B \\ C,D)
    # minterms mapping:
    # AB=00: m0(0000), m1(0001), m3(0011), m2(0010)
    # AB=01: m4(0100), m5(0101), m7(0111), m6(0110)
    # AB=11: m12(1100), m13(1101), m15(1111), m14(1110)
    # AB=10: m8(1000), m9(1001), m11(1011), m10(1010)
    
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
            
            # Fill color based on SOP (highlight 1) or POS (highlight 0)
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
                
            # Minterm index small text
            ax.text(c + 0.85, 3.85 - r, grid_minterms[r][c], fontsize=7, color='#95A5A6', ha='right', va='top')

    # Draw Groupings
    if is_sop:
        # Group 1s at AB=01, CD=00 (m4) and CD=10 (m6)
        # In K-map, CD=00 and CD=10 are in row AB=01 (y=2)
        # Box around m4 (x=0, y=2) and m6 (x=3, y=2) -> wrap-around horizontal pair!
        
        # Left wrap box on m4
        rect1 = patches.Rectangle((0.05, 2.05), 0.9, 0.9, linewidth=2.5, edgecolor='#27AE60', facecolor='none', linestyle='--', zorder=4)
        # Right wrap box on m6
        rect2 = patches.Rectangle((3.05, 2.05), 0.9, 0.9, linewidth=2.5, edgecolor='#27AE60', facecolor='none', linestyle='--', zorder=4)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        
        # Connecting arc to indicate wrap-around grouping
        ax.annotate("", xy=(-0.1, 2.5), xytext=(4.1, 2.5),
                    arrowprops=dict(arrowstyle="<->", color="#27AE60", lw=2, connectionstyle="arc3,rad=-0.4"))
        ax.text(2.0, -0.6, r"Group (m4, m6): $\bar{A}B\bar{D}$", fontsize=12, fontweight='bold', color='#196F3D', ha='center')

    else:
        # For POS: group 0s!
        # All 0s except m4 and m6.
        # Group A (Row AB=00): all 4 zeros -> A+B
        rect_r0 = patches.Rectangle((0.05, 3.05), 3.9, 0.9, linewidth=2, edgecolor='#E74C3C', facecolor='none', zorder=4)
        ax.add_patch(rect_r0)
        
        # Group B (Rows AB=11, 10): 8 zeros in bottom two rows -> A' (eliminated to A)
        rect_r23 = patches.Rectangle((0.05, 0.05), 3.9, 1.9, linewidth=2, edgecolor='#2980B9', facecolor='none', zorder=4)
        ax.add_patch(rect_r23)
        
        # Group C (Cols CD=01, CD=11): 8 zeros in middle two columns -> D' (eliminated to D)
        rect_c12 = patches.Rectangle((1.05, 0.05), 1.9, 3.9, linewidth=2, edgecolor='#8E44AD', facecolor='none', linestyle=':', zorder=4)
        ax.add_patch(rect_c12)
        
        ax.text(2.0, -0.6, r"POS Grouping: $Y = (\bar{A})(B)(\bar{D}) = \overline{A + \bar{B} + D}$", fontsize=11, fontweight='bold', color='#78281F', ha='center')

    ax.set_xlim(-0.8, 4.8)
    ax.set_ylim(-1.0, 5.0)


def create_kmap_images():
    # 1. SOP K-map
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    draw_kmap(ax, "SOP Karnaugh Map (Grouping 1s)", is_sop=True)
    plt.tight_layout()
    plt.savefig("/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/digital-logic/boolean/kmap_sop_diagram.png", bbox_inches='tight')
    plt.close()
    
    # 2. POS K-map
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
    draw_kmap(ax, "POS Karnaugh Map (Grouping 0s)", is_sop=False)
    plt.tight_layout()
    plt.savefig("/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/digital-logic/boolean/kmap_pos_diagram.png", bbox_inches='tight')
    plt.close()
    print("Saved K-Map images successfully!")


# --- GATE DRAWING HELPERS ---
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
    
    # Bubble
    bx = x + width - bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.2, zorder=4)
    ax.add_patch(bubble)
    
    if label:
        ax.text(x + w_gate*0.35, y, label, fontsize=11, fontweight='bold', color=edge_color,
                ha='center', va='center', zorder=4)
    return (x0 + w_gate*0.1, y + height/3), (x0 + w_gate*0.1, y), (x0 + w_gate*0.1, y - height/3), (x + width, y)


def create_sop_circuit():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Inverters for A and D
    notA_in, notA_out = draw_not_gate(ax, 2.5, 4.0, label="NOT A")
    notD_in, notD_out = draw_not_gate(ax, 2.5, 1.8, label="NOT D")
    and3_in1, and3_in2, and3_in3, and3_out = draw_and3_gate(ax, 6.0, 2.9, width=1.6, height=1.6, label="AND")
    
    x_in = 0.5
    y_A = 4.0
    y_B = 2.9
    y_D = 1.8
    
    def add_terminal(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${text}$", fontsize=14, fontweight='bold', color=color, ha='right', va='center')

    add_terminal(x_in, y_A, "A", COLOR_A)
    add_terminal(x_in, y_B, "B", COLOR_B)
    add_terminal(x_in, y_D, "D", COLOR_D)
    
    # Wires
    ax.plot([x_in, notA_in[0]], [y_A, y_A], color=COLOR_A, lw=2.5, zorder=2)
    ax.plot([notA_out[0], and3_in1[0]], [notA_out[1], and3_in1[1]], color=COLOR_A, lw=2.5, zorder=2)
    ax.text(notA_out[0] + 0.4, notA_out[1] + 0.2, r"$\bar{A}$", fontsize=12, color=COLOR_A, fontweight='bold')
    
    ax.plot([x_in, and3_in2[0]], [y_B, and3_in2[1]], color=COLOR_B, lw=2.5, zorder=2)
    ax.text(3.8, y_B + 0.2, r"$B$", fontsize=12, color=COLOR_B, fontweight='bold')
    
    ax.plot([x_in, notD_in[0]], [y_D, y_D], color=COLOR_D, lw=2.5, zorder=2)
    ax.plot([notD_out[0], and3_in3[0]], [notD_out[1], and3_in3[1]], color=COLOR_D, lw=2.5, zorder=2)
    ax.text(notD_out[0] + 0.4, notD_out[1] - 0.25, r"$\bar{D}$", fontsize=12, color=COLOR_D, fontweight='bold')
    
    x_out_term = 9.5
    ax.plot([and3_out[0], x_out_term], [and3_out[1], and3_out[1]], color=COLOR_FINAL_OUT, lw=3.0, zorder=2)
    ax.add_patch(patches.Circle((x_out_term, and3_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, and3_out[1], r"$Y_{\text{SOP}} = \bar{A} \cdot B \cdot \bar{D}$", fontsize=16, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(5.0, 5.2, "Minimal SOP Circuit Schematic (AND-OR Logic)", fontsize=15, fontweight='bold', ha='center', color='#1A5276')
    ax.set_xlim(-0.8, 12.5)
    ax.set_ylim(0.5, 5.6)
    
    plt.tight_layout()
    plt.savefig("/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/digital-logic/boolean/sop_circuit_diagram.png", bbox_inches='tight')
    plt.close()
    print("Saved sop_circuit_diagram.png")


def create_pos_circuit():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Inverter for B
    notB_in, notB_out = draw_not_gate(ax, 2.5, 2.9, label="NOT B")
    nor3_in1, nor3_in2, nor3_in3, nor3_out = draw_nor3_gate(ax, 6.0, 2.9, width=1.6, height=1.6, label="NOR")
    
    x_in = 0.5
    y_A = 4.0
    y_B = 2.9
    y_D = 1.8
    
    def add_terminal(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.12, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.25, y, f"${text}$", fontsize=14, fontweight='bold', color=color, ha='right', va='center')

    add_terminal(x_in, y_A, "A", COLOR_A)
    add_terminal(x_in, y_B, "B", COLOR_B)
    add_terminal(x_in, y_D, "D", COLOR_D)
    
    # Wires
    ax.plot([x_in, 5.0, 5.0, nor3_in1[0]], [y_A, y_A, nor3_in1[1], nor3_in1[1]], color=COLOR_A, lw=2.5, zorder=2)
    ax.text(3.8, y_A + 0.25, r"$A$", fontsize=12, color=COLOR_A, fontweight='bold')
    
    ax.plot([x_in, notB_in[0]], [y_B, y_B], color=COLOR_B, lw=2.5, zorder=2)
    ax.plot([notB_out[0], nor3_in2[0]], [notB_out[1], nor3_in2[1]], color=COLOR_B, lw=2.5, zorder=2)
    ax.text(notB_out[0] + 0.4, notB_out[1] + 0.25, r"$\bar{B}$", fontsize=12, color=COLOR_B, fontweight='bold')
    
    ax.plot([x_in, 5.0, 5.0, nor3_in3[0]], [y_D, y_D, nor3_in3[1], nor3_in3[1]], color=COLOR_D, lw=2.5, zorder=2)
    ax.text(3.8, y_D - 0.25, r"$D$", fontsize=12, color=COLOR_D, fontweight='bold')
    
    x_out_term = 9.5
    ax.plot([nor3_out[0], x_out_term], [nor3_out[1], nor3_out[1]], color=COLOR_FINAL_OUT, lw=3.0, zorder=2)
    ax.add_patch(patches.Circle((x_out_term, nor3_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.3, nor3_out[1], r"$Y_{\text{POS}} = \overline{A + \bar{B} + D}$", fontsize=16, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.text(5.0, 5.2, "Minimal POS Circuit Schematic (NOR-NOR Logic)", fontsize=15, fontweight='bold', ha='center', color='#78281F')
    ax.set_xlim(-0.8, 12.5)
    ax.set_ylim(0.5, 5.6)
    
    plt.tight_layout()
    plt.savefig("/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/digital-logic/boolean/pos_circuit_diagram.png", bbox_inches='tight')
    plt.close()
    print("Saved pos_circuit_diagram.png")


def create_sop_pos_comparison():
    fig = plt.figure(figsize=(15, 12), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    ax1 = fig.add_subplot(2, 2, 1) # K-Map SOP
    ax2 = fig.add_subplot(2, 2, 2) # K-Map POS
    ax3 = fig.add_subplot(2, 2, 3) # Circuit SOP
    ax4 = fig.add_subplot(2, 2, 4) # Circuit POS
    
    draw_kmap(ax1, "(A) SOP K-Map (Group 1s)", is_sop=True)
    draw_kmap(ax2, "(B) POS K-Map (Group 0s)", is_sop=False)
    
    # Ax3 SOP Circuit
    ax3.set_aspect('equal')
    ax3.axis('off')
    notA_in, notA_out = draw_not_gate(ax3, 2.0, 3.5, label="NOT A")
    notD_in, notD_out = draw_not_gate(ax3, 2.0, 1.5, label="NOT D")
    and3_in1, and3_in2, and3_in3, and3_out = draw_and3_gate(ax3, 4.8, 2.5, width=1.4, height=1.4, label="AND")
    
    x_in = 0.2
    add_terminal = lambda ax, x, y, txt, col: (ax.add_patch(patches.Circle((x, y), 0.1, facecolor=col, zorder=5)), ax.text(x-0.2, y, f"${txt}$", fontsize=12, fontweight='bold', color=col, ha='right', va='center'))
    add_terminal(ax3, x_in, 3.5, "A", COLOR_A)
    add_terminal(ax3, x_in, 2.5, "B", COLOR_B)
    add_terminal(ax3, x_in, 1.5, "D", COLOR_D)
    
    ax3.plot([x_in, notA_in[0]], [3.5, 3.5], color=COLOR_A, lw=2)
    ax3.plot([notA_out[0], and3_in1[0]], [notA_out[1], and3_in1[1]], color=COLOR_A, lw=2)
    ax3.plot([x_in, and3_in2[0]], [2.5, and3_in2[1]], color=COLOR_B, lw=2)
    ax3.plot([x_in, notD_in[0]], [1.5, 1.5], color=COLOR_D, lw=2)
    ax3.plot([notD_out[0], and3_in3[0]], [notD_out[1], and3_in3[1]], color=COLOR_D, lw=2)
    
    ax3.plot([and3_out[0], 7.5], [and3_out[1], and3_out[1]], color=COLOR_FINAL_OUT, lw=2.5)
    ax3.text(7.7, and3_out[1], r"$Y = \bar{A}B\bar{D}$", fontsize=13, fontweight='bold', color=COLOR_FINAL_OUT, va='center')
    ax3.text(3.5, 4.5, "(C) Minimal SOP Circuit (2 NOTs + 1 AND)", fontsize=13, fontweight='bold', ha='center', color='#1A5276')
    ax3.set_xlim(-0.8, 9.5)
    ax3.set_ylim(0.5, 4.8)

    # Ax4 POS Circuit
    ax4.set_aspect('equal')
    ax4.axis('off')
    notB_in, notB_out = draw_not_gate(ax4, 2.0, 2.5, label="NOT B")
    nor3_in1, nor3_in2, nor3_in3, nor3_out = draw_nor3_gate(ax4, 4.8, 2.5, width=1.4, height=1.4, label="NOR")
    
    add_terminal(ax4, x_in, 3.5, "A", COLOR_A)
    add_terminal(ax4, x_in, 2.5, "B", COLOR_B)
    add_terminal(ax4, x_in, 1.5, "D", COLOR_D)
    
    ax4.plot([x_in, 4.0, 4.0, nor3_in1[0]], [3.5, 3.5, nor3_in1[1], nor3_in1[1]], color=COLOR_A, lw=2)
    ax4.plot([x_in, notB_in[0]], [2.5, 2.5], color=COLOR_B, lw=2)
    ax4.plot([notB_out[0], nor3_in2[0]], [notB_out[1], nor3_in2[1]], color=COLOR_B, lw=2)
    ax4.plot([x_in, 4.0, 4.0, nor3_in3[0]], [1.5, 1.5, nor3_in3[1], nor3_in3[1]], color=COLOR_D, lw=2)
    
    ax4.plot([nor3_out[0], 7.5], [nor3_out[1], nor3_out[1]], color=COLOR_FINAL_OUT, lw=2.5)
    ax4.text(7.7, nor3_out[1], r"$Y = \overline{A + \bar{B} + D}$", fontsize=13, fontweight='bold', color=COLOR_FINAL_OUT, va='center')
    ax4.text(3.5, 4.5, "(D) Minimal POS Circuit (1 NOT + 1 NOR)", fontsize=13, fontweight='bold', ha='center', color='#78281F')
    ax4.set_xlim(-0.8, 9.5)
    ax4.set_ylim(0.5, 4.8)

    plt.tight_layout()
    plt.savefig("/Users/3rapat/student/internship/CODEFIN/project/vahalla-wealth/private-docs/other-project/uni-work/engineering-problem/digital-logic/boolean/sop_pos_comparison.png", bbox_inches='tight')
    plt.close()
    print("Saved sop_pos_comparison.png successfully!")

if __name__ == "__main__":
    create_kmap_images()
    create_sop_circuit()
    create_pos_circuit()
    create_sop_pos_comparison()
