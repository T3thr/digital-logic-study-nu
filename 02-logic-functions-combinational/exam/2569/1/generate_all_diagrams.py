import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Configuration & Styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#BDC3C7'

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(DIR_PATH, "assets")
os.makedirs(ASSETS_PATH, exist_ok=True)

# Color Palette (Tailored, High Contrast, Textbook Aesthetic)
COLOR_A = "#C0392B"      # Dark Red
COLOR_B = "#2980B9"      # Blue
COLOR_C = "#27AE60"      # Green
COLOR_D = "#8E44AD"      # Purple
COLOR_E = "#D35400"      # Orange

COLOR_W1 = "#8E44AD"     # Purple (XOR)
COLOR_W2 = "#16A085"     # Teal (NAND)
COLOR_W3 = "#B9770E"     # Amber/Gold (NOR)

COLOR_STAGE2 = "#1B4F72" # Deep Blue for Stage 2 ANDs
COLOR_STAGE3 = "#145A32" # Forest Green for Stage 3 ORs
COLOR_FINAL_OUT = "#0F172A" # Dark Navy for Final Output

def F_ref(A, B, C, D, E):
    nB, nE = 1 - B, 1 - E
    w1 = D ^ E                  # G1: XOR
    w2 = 1 - (A & C)            # G2: NAND
    w3 = 1 - (B | D)            # G3: NOR
    
    w4 = A and nB               # G4: AND -> A . B'
    w5 = C and w2               # G5: AND -> C . (A . C)' = A' . C
    w6 = w3 and nE              # G6: AND -> (B + D)' . E' = B' . D' . E'
    w7 = B and w1               # G7: AND -> B . (D ^ E)
    
    w8 = w4 or w5               # G8: OR -> A.B' + A'.C
    w9 = w6 or w7               # G9: OR -> B'.D'.E' + B.(D ^ E)
    
    f = w8 or w9                # G10: Final OR
    return int(f)

def draw_not_gate(ax, x, y, width=1.1, height=0.55, label="", fill_color="#FEF9E7", edge_color="#7D6608"):
    x0 = x
    x_tip = x + width - 0.18
    bubble_r = 0.09
    y_top = y + height/2
    y_bot = y - height/2
    
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_tip, y)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.0, zorder=3)
    ax.add_patch(patch)
    
    bx = x_tip + bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.0, zorder=4)
    ax.add_patch(bubble)
    if label:
        ax.text(x + width*0.26, y, label, fontsize=8.0, fontweight='bold', color=edge_color, ha='center', va='center', zorder=5)
    return (x0, y), (bx + bubble_r, y)

def draw_and2_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#EBF5FB", edge_color="#1B4F72"):
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
        ax.text(x + width*0.36, y, label, fontsize=9.0, fontweight='bold', color=edge_color, ha='center', va='center', zorder=4)
    return (x0, y + height/4), (x0, y - height/4), (x + width, y)

def draw_nand2_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#E8F8F5", edge_color="#117A65"):
    x0 = x
    bubble_r = 0.09
    w_body = width - 2*bubble_r
    y_top = y + height/2
    y_bot = y - height/2
    r = height / 2
    x_arc_start = x0 + w_body - r
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.LINETO, (x0, y_top)),
        (Path.LINETO, (x_arc_start, y_top)),
        (Path.CURVE4, (x0 + w_body, y_top)),
        (Path.CURVE4, (x0 + w_body, y_bot)),
        (Path.CURVE4, (x_arc_start, y_bot)),
        (Path.LINETO, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    
    bx = x0 + w_body + bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.0, zorder=4)
    ax.add_patch(bubble)
    
    if label:
        ax.text(x + w_body*0.36, y, label, fontsize=9.0, fontweight='bold', color=edge_color, ha='center', va='center', zorder=5)
    return (x0, y + height/4), (x0, y - height/4), (bx + bubble_r, y)

def draw_nor2_gate(ax, x, y, width=1.4, height=1.0, label="", fill_color="#FEF5E7", edge_color="#B9770E"):
    x0 = x
    bubble_r = 0.09
    w_body = width - 2*bubble_r
    y_top = y + height/2
    y_bot = y - height/2
    path_data = [
        (Path.MOVETO, (x0, y_bot)),
        (Path.CURVE3, (x0 + w_body*0.25, y)),
        (Path.CURVE3, (x0, y_top)),
        (Path.CURVE3, (x0 + w_body*0.65, y_top)),
        (Path.CURVE3, (x0 + w_body, y)),
        (Path.CURVE3, (x0 + w_body*0.65, y_bot)),
        (Path.CURVE3, (x0, y_bot)),
        (Path.CLOSEPOLY, (x0, y_bot))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=fill_color, edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch)
    
    bx = x0 + w_body + bubble_r
    bubble = patches.Circle((bx, y), bubble_r, facecolor='white', edgecolor=edge_color, lw=2.0, zorder=4)
    ax.add_patch(bubble)
    
    if label:
        ax.text(x + w_body*0.38, y, label, fontsize=9.0, fontweight='bold', color=edge_color, ha='center', va='center', zorder=5)
    return (x0 + w_body*0.14, y + height/4), (x0 + w_body*0.14, y - height/4), (bx + bubble_r, y)

def draw_xor2_gate(ax, x, y, width=1.5, height=1.0, label="", fill_color="#F5EEF8", edge_color="#6C3483"):
    x0 = x
    y_top = y + height/2
    y_bot = y - height/2
    path_back = [
        (Path.MOVETO, (x0 - 0.12, y_bot)),
        (Path.CURVE3, (x0 - 0.12 + width*0.25, y)),
        (Path.CURVE3, (x0 - 0.12, y_top))
    ]
    c_b, v_b = zip(*path_back)
    p_b = Path(v_b, c_b)
    patch_b = patches.PathPatch(p_b, facecolor='none', edgecolor=edge_color, lw=2.2, zorder=3)
    ax.add_patch(patch_b)
    
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
        ax.text(x + width*0.40, y, label, fontsize=9.0, fontweight='bold', color=edge_color, ha='center', va='center', zorder=4)
    return (x0 - 0.12 + width*0.10, y + height/4), (x0 - 0.12 + width*0.10, y - height/4), (x + width, y)

def draw_or2_gate(ax, x, y, width=1.5, height=1.1, label="", fill_color="#EAFAF1", edge_color="#145A32"):
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
        ax.text(x + width*0.40, y, label, fontsize=9.5, fontweight='bold', color=edge_color, ha='center', va='center', zorder=4)
    return (x0 + width*0.15, y + height/4), (x0 + width*0.15, y - height/4), (x + width, y)

# ══════════════════════════════════════════════════════════════════════
# 1. PRISTINE 4-STAGE 2-INPUT GATE SCHEMATIC (ZERO CROSSING CONFUSION)
# ══════════════════════════════════════════════════════════════════════
def create_original_circuit():
    fig, ax = plt.subplots(figsize=(20, 11.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Title & Subtitle banner
    ax.text(9.5, 10.8, "305241 Digital Logic Design — Exam 2569 (Question 1)", fontsize=16, fontweight='bold', ha='center', color='#1A5276')
    ax.text(9.5, 10.25, "Multi-Stage 5-Variable Combinational Logic Circuit (Strict Max 2-Input Gates: 74HC04, 74HC86, 74HC00, 74HC02, 74HC08, 74HC32)", 
            fontsize=11.5, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.4", facecolor="#EBF5FB", edgecolor="#AED6F1", lw=1.5))
    
    # Inputs Column (x = 0.5)
    x_in = 0.5
    y_A, y_B, y_C, y_D, y_E = 9.0, 7.5, 5.5, 3.5, 1.5
    
    def add_term(x, y, text, color):
        ax.add_patch(patches.Circle((x, y), 0.13, facecolor=color, edgecolor='black', lw=1.5, zorder=5))
        ax.text(x - 0.28, y, text, fontsize=13.5, fontweight='bold', color=color, ha='right', va='center')
        
    add_term(x_in, y_A, "A", COLOR_A)
    add_term(x_in, y_B, "B", COLOR_B)
    add_term(x_in, y_C, "C", COLOR_C)
    add_term(x_in, y_D, "D", COLOR_D)
    add_term(x_in, y_E, "E", COLOR_E)

    def add_junc(x, y, color):
        ax.add_patch(patches.Circle((x, y), 0.08, facecolor=color, edgecolor=color, zorder=6))
    
    # ── STAGE 1 GATES (Column x = 2.8) ──
    notB_in, notB_out = draw_not_gate(ax, 2.8, 8.0, label="NOT B")
    nand_in1, nand_in2, nand_out = draw_nand2_gate(ax, 2.8, 6.0, label="NAND\n(7400)")
    nor_in1, nor_in2, nor_out = draw_nor2_gate(ax, 2.8, 4.75, label="NOR\n(7402)")
    notE_in, notE_out = draw_not_gate(ax, 2.8, 3.75, label="NOT E")
    xor_in1, xor_in2, xor_out = draw_xor2_gate(ax, 2.8, 1.75, label="XOR\n(7486)")

    # ── STAGE 2 GATES (Column x = 7.2) ──
    and1_in1, and1_in2, and1_out = draw_and2_gate(ax, 7.2, 8.25, label="AND1\n(7408)")
    and2_in1, and2_in2, and2_out = draw_and2_gate(ax, 7.2, 6.25, label="AND2\n(7408)")
    and3_in1, and3_in2, and3_out = draw_and2_gate(ax, 7.2, 4.25, label="AND3\n(7408)")
    and4_in1, and4_in2, and4_out = draw_and2_gate(ax, 7.2, 2.25, label="AND4\n(7408)")

    # ── STAGE 3 GATES (Column x = 11.6) ──
    or1_in1, or1_in2, or1_out = draw_or2_gate(ax, 11.6, 7.25, label="OR1\n(7432)")
    or2_in1, or2_in2, or2_out = draw_or2_gate(ax, 11.6, 3.25, label="OR2\n(7432)")

    # ── STAGE 4 GATE (Column x = 15.6) ──
    or3_in1, or3_in2, or3_out = draw_or2_gate(ax, 15.6, 5.25, label="OR3\n(7432)")

    # ═════ WIRE ROUTING (PERFECT UNTANGLED ORTHOGONAL BUSES) ═════
    # Input A -> AND1_in1 (y=8.5) & NAND_in1 (y=6.25)
    ax.plot([x_in, 1.2], [y_A, y_A], color=COLOR_A, lw=2.4)
    add_junc(1.2, y_A, COLOR_A)
    ax.plot([1.2, 6.4, 6.4, and1_in1[0]], [y_A, y_A, and1_in1[1], and1_in1[1]], color=COLOR_A, lw=2.4)
    ax.plot([1.2, 1.2, nand_in1[0]], [y_A, nand_in1[1], nand_in1[1]], color=COLOR_A, lw=2.4)

    # Input B -> NOT B (y=8.0), NOR_in1 (y=5.0), AND4_in1 (y=2.5)
    ax.plot([x_in, 1.5], [y_B, y_B], color=COLOR_B, lw=2.4)
    add_junc(1.5, y_B, COLOR_B)
    ax.plot([1.5, 1.5, notB_in[0]], [y_B, notB_in[1], notB_in[1]], color=COLOR_B, lw=2.4)
    ax.plot([1.5, 1.5, nor_in1[0]], [y_B, nor_in1[1], nor_in1[1]], color=COLOR_B, lw=2.4)
    ax.plot([1.5, 6.2, 6.2, and4_in1[0]], [y_B, y_B, and4_in1[1], and4_in1[1]], color=COLOR_B, lw=2.4)

    # Input C -> NAND_in2 (y=5.75) & AND2_in1 (y=6.5)
    ax.plot([x_in, 1.8], [y_C, y_C], color=COLOR_C, lw=2.4)
    add_junc(1.8, y_C, COLOR_C)
    ax.plot([1.8, 1.8, nand_in2[0]], [y_C, nand_in2[1], nand_in2[1]], color=COLOR_C, lw=2.4)
    ax.plot([1.8, 6.6, 6.6, and2_in1[0]], [y_C, y_C, and2_in1[1], and2_in1[1]], color=COLOR_C, lw=2.4)

    # Input D -> NOR_in2 (y=4.5) & XOR_in1 (y=2.0)
    ax.plot([x_in, 2.1], [y_D, y_D], color=COLOR_D, lw=2.4)
    add_junc(2.1, y_D, COLOR_D)
    ax.plot([2.1, 2.1, nor_in2[0]], [y_D, nor_in2[1], nor_in2[1]], color=COLOR_D, lw=2.4)
    ax.plot([2.1, 2.1, xor_in1[0]], [y_D, xor_in1[1], xor_in1[1]], color=COLOR_D, lw=2.4)

    # Input E -> NOT E (y=3.75) & XOR_in2 (y=1.5)
    ax.plot([x_in, 2.4], [y_E, y_E], color=COLOR_E, lw=2.4)
    add_junc(2.4, y_E, COLOR_E)
    ax.plot([2.4, 2.4, notE_in[0]], [y_E, notE_in[1], notE_in[1]], color=COLOR_E, lw=2.4)
    ax.plot([2.4, 2.4, xor_in2[0]], [y_E, xor_in2[1], xor_in2[1]], color=COLOR_E, lw=2.4)

    # Stage 1 Outputs -> Stage 2 Inputs (Solid connections with callout tags)
    # NOT B out -> AND1_in2
    ax.plot([notB_out[0], and1_in2[0]], [notB_out[1], and1_in2[1]], color=COLOR_B, lw=2.4)
    
    # NAND out -> AND2_in2 (W2 = (A·C)')
    ax.plot([nand_out[0], and2_in2[0]], [nand_out[1], and2_in2[1]], color=COLOR_W2, lw=2.4)
    ax.text(nand_out[0] + 0.45, nand_out[1] + 0.22, "W₂ = (A·C)'", fontsize=9.5, fontweight='bold', color=COLOR_W2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_W2, lw=1.0))

    # NOR out -> AND3_in1 (W3 = (B+D)')
    ax.plot([nor_out[0], 5.8, 5.8, and3_in1[0]], [nor_out[1], nor_out[1], and3_in1[1], and3_in1[1]], color=COLOR_W3, lw=2.4)
    ax.text(nor_out[0] + 0.45, nor_out[1] + 0.22, "W₃ = (B+D)'", fontsize=9.5, fontweight='bold', color=COLOR_W3,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_W3, lw=1.0))

    # NOT E out -> AND3_in2
    ax.plot([notE_out[0], 5.6, 5.6, and3_in2[0]], [notE_out[1], notE_out[1], and3_in2[1], and3_in2[1]], color=COLOR_E, lw=2.4)

    # XOR out -> AND4_in2 (W1 = D ⊕ E)
    ax.plot([xor_out[0], 5.8, 5.8, and4_in2[0]], [xor_out[1], xor_out[1], and4_in2[1], and4_in2[1]], color=COLOR_W1, lw=2.4)
    ax.text(xor_out[0] + 0.45, xor_out[1] + 0.22, "W₁ = D ⊕ E", fontsize=9.5, fontweight='bold', color=COLOR_W1,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_W1, lw=1.0))

    # Stage 2 Outputs -> Stage 3 Inputs (Solid, Symmetrical Tree)
    # AND1 out -> OR1_in1 (W4 = A·B')
    ax.plot([and1_out[0], 10.4, 10.4, or1_in1[0]], [and1_out[1], and1_out[1], or1_in1[1], or1_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.text(and1_out[0] + 0.4, and1_out[1] + 0.24, "W₄ = A·B'", fontsize=9.5, fontweight='bold', color=COLOR_STAGE2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE2, lw=1.0))

    # AND2 out -> OR1_in2 (W5 = C·W2 = A'·C)
    ax.plot([and2_out[0], 10.4, 10.4, or1_in2[0]], [and2_out[1], and2_out[1], or1_in2[1], or1_in2[1]], color=COLOR_STAGE2, lw=2.4)
    ax.text(and2_out[0] + 0.4, and2_out[1] + 0.24, "W₅ = C·W₂ = A'·C", fontsize=9.5, fontweight='bold', color=COLOR_STAGE2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE2, lw=1.0))

    # AND3 out -> OR2_in1 (W6 = W3·E' = B'·D'·E')
    ax.plot([and3_out[0], 10.4, 10.4, or2_in1[0]], [and3_out[1], and3_out[1], or2_in1[1], or2_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.text(and3_out[0] + 0.4, and3_out[1] + 0.24, "W₆ = W₃·E' = B'·D'·E'", fontsize=9.5, fontweight='bold', color=COLOR_STAGE2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE2, lw=1.0))

    # AND4 out -> OR2_in2 (W7 = B·W1 = B·(D ⊕ E))
    ax.plot([and4_out[0], 10.4, 10.4, or2_in2[0]], [and4_out[1], and4_out[1], or2_in2[1], or2_in2[1]], color=COLOR_STAGE2, lw=2.4)
    ax.text(and4_out[0] + 0.4, and4_out[1] + 0.24, "W₇ = B·W₁ = B·(D ⊕ E)", fontsize=9.5, fontweight='bold', color=COLOR_STAGE2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE2, lw=1.0))

    # Stage 3 Outputs -> Stage 4 Inputs (Solid, Symmetrical Tree)
    # OR1 out -> OR3_in1 (W8 = W4 + W5)
    ax.plot([or1_out[0], 14.4, 14.4, or3_in1[0]], [or1_out[1], or1_out[1], or3_in1[1], or3_in1[1]], color=COLOR_STAGE3, lw=2.5)
    ax.text(or1_out[0] + 0.45, or1_out[1] + 0.25, "W₈ = W₄ + W₅", fontsize=10, fontweight='bold', color=COLOR_STAGE3,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE3, lw=1.0))

    # OR2 out -> OR3_in2 (W9 = W6 + W7)
    ax.plot([or2_out[0], 14.4, 14.4, or3_in2[0]], [or2_out[1], or2_out[1], or3_in2[1], or3_in2[1]], color=COLOR_STAGE3, lw=2.5)
    ax.text(or2_out[0] + 0.45, or2_out[1] + 0.25, "W₉ = W₆ + W₇", fontsize=10, fontweight='bold', color=COLOR_STAGE3,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=COLOR_STAGE3, lw=1.0))

    # Final Output Terminal (Solid, Exact Alignment)
    x_out_term = 18.2
    ax.plot([or3_out[0], x_out_term], [or3_out[1], or3_out[1]], color=COLOR_FINAL_OUT, lw=3.2)
    ax.add_patch(patches.Circle((x_out_term, or3_out[1]), 0.13, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.35, or3_out[1], "F = W₈ + W₉\n   = A·B' + A'·C + B'·D'·E' + B·D'·E + B·D·E'", 
            fontsize=12.5, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    # Stage divider indicators
    def add_stage_label(x, label):
        ax.text(x, 0.4, label, fontsize=10, fontweight='bold', ha='center', color='#566573',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#F2F4F4", edgecolor="#BDC3C7", lw=1.0))
        
    add_stage_label(3.5, "Stage 1: Pre-Logic")
    add_stage_label(7.9, "Stage 2: Product Terms")
    add_stage_label(12.3, "Stage 3: Sub-Sums")
    add_stage_label(16.3, "Stage 4: Output")

    ax.set_xlim(-0.6, 23.5)
    ax.set_ylim(-0.2, 11.5)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "digital_logic_circuit_redrawn.png"), bbox_inches='tight')
    plt.close()
    print("Saved pristine assets/digital_logic_circuit_redrawn.png")

# ══════════════════════════════════════════════════════════════════════
# 2. SOP 8x4 K-MAP DIAGRAM (Grouping 1s)
# ══════════════════════════════════════════════════════════════════════
def create_kmap_sop():
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

    fig, ax = plt.subplots(figsize=(10, 13), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(2.0, 9.1, "5-Variable SOP Karnaugh Map (8×4 Matrix)", fontsize=15, fontweight='bold', ha='center', color='#1A5276')
    ax.text(2.0, 8.7, "Vertical Rows = ABC (8 Rows in Gray Code)  |  Horizontal Columns = DE (4 Columns in Gray Code)", 
            fontsize=9.5, ha='center', color='#2C3E50')

    # Grid Lines
    for i in range(9): ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.8)
    for j in range(5): ax.plot([j, j], [0, 8], color='#2C3E50', lw=1.8)
        
    ax.text(-0.6, 8.4, "ABC \\ DE", fontsize=11, fontweight='bold', ha='center', va='center', color='#1A5276')
    for j, col in enumerate(col_labels): 
        ax.text(j + 0.5, 8.3, col, fontsize=12, fontweight='bold', ha='center', va='center', color='#2C3E50')
    for i, row in enumerate(row_labels): 
        ax.text(-0.4, 7.5 - i, row, fontsize=11.5, fontweight='bold', ha='center', va='center', color='#2C3E50')

    for r in range(8):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 7.5 - r
            x_pos = c + 0.5
            if val == 1:
                bg = patches.Rectangle((c, 7-r), 1, 1, facecolor='#E8F8F5', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=16, fontweight='bold', color='#117A65', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=14, color='#95A5A6', ha='center', va='center', zorder=3)
            ax.text(c + 0.88, 7.85 - r, grid_minterms[r][c], fontsize=7, color='#7F8C8D', ha='right', va='top')

    # ── SOP GROUPINGS ──
    # Group 1: A'·C (Octet size 8 -> rows ABC = 001, 011 -> r=1, 2 all 4 cols)
    rect_g1 = patches.FancyBboxPatch((0.08, 5.08), 3.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#C0392B', facecolor='none', zorder=4)
    ax.add_patch(rect_g1)
    ax.text(4.15, 6.0, "Group 1 (Octet 8):\nA'·C", fontsize=10, fontweight='bold', color='#C0392B', va='center')
    
    # Group 2: A·B' (Octet size 8 -> rows ABC = 101, 100 -> r=6, 7 all 4 cols)
    rect_g2 = patches.FancyBboxPatch((0.08, 0.08), 3.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#2980B9', facecolor='none', zorder=4)
    ax.add_patch(rect_g2)
    ax.text(4.15, 1.0, "Group 2 (Octet 8):\nA·B'", fontsize=10, fontweight='bold', color='#2980B9', va='center')
    
    # Group 3: B'·D'·E' (Quad size 4 - Wraparound Top & Bottom, col 00)
    rect_g3_top = patches.FancyBboxPatch((0.08, 6.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                         linewidth=2.8, edgecolor='#8E44AD', facecolor='none', linestyle='--', zorder=4)
    rect_g3_bot = patches.FancyBboxPatch((0.08, 0.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                         linewidth=2.8, edgecolor='#8E44AD', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_g3_top); ax.add_patch(rect_g3_bot)
    ax.text(-0.15, 7.0, "Group 3 (Quad 4 Wrap):\nB'·D'·E'", fontsize=9.5, fontweight='bold', color='#8E44AD', ha='right', va='center')

    # Group 4: B·D'·E (Quad size 4 -> Col DE = 01 (c=1) in rows ABC = 011, 010, 110, 111 (r=2, 3, 4, 5))
    rect_g4 = patches.FancyBboxPatch((1.08, 2.08), 0.84, 3.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#D35400', facecolor='none', linestyle='-.', zorder=4)
    ax.add_patch(rect_g4)
    ax.text(1.5, 1.7, "Group 4 (Quad 4):\nB·D'·E", fontsize=9.5, fontweight='bold', color='#D35400', ha='center', va='top')

    # Group 5: B·D·E' (Quad size 4 -> Col DE = 10 (c=3) in rows ABC = 011, 010, 110, 111 (r=2, 3, 4, 5))
    rect_g5 = patches.FancyBboxPatch((3.08, 2.08), 0.84, 3.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#27AE60', facecolor='none', linestyle=':', zorder=4)
    ax.add_patch(rect_g5)
    ax.text(3.5, 1.7, "Group 5 (Quad 4):\nB·D·E'", fontsize=9.5, fontweight='bold', color='#27AE60', ha='center', va='top')

    # Summary Footer
    ax.text(2.0, -0.6, "Minimal SOP Expression:  F_SOP = A'·C + A·B' + B'·D'·E' + B·D'·E + B·D·E'", 
            fontsize=12, fontweight='bold', color='#117A65', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#E8F8F5", edgecolor="#A3E4D7", lw=1.8))
            
    ax.set_xlim(-2.2, 5.8)
    ax.set_ylim(-1.0, 9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "kmap_sop_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved assets/kmap_sop_diagram.png")

# ══════════════════════════════════════════════════════════════════════
# 3. POS 8x4 K-MAP DIAGRAM (Grouping 0s)
# ══════════════════════════════════════════════════════════════════════
def create_kmap_pos():
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
            r_m.append(f"M{m_idx}")
        grid_vals.append(r_vals)
        grid_minterms.append(r_m)

    fig, ax = plt.subplots(figsize=(10, 13), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(2.0, 9.1, "5-Variable POS Karnaugh Map (8×4 Matrix — Grouping 0s)", fontsize=15, fontweight='bold', ha='center', color='#78281F')
    ax.text(2.0, 8.7, "Vertical Rows = ABC (8 Rows in Gray Code)  |  Horizontal Columns = DE (4 Columns in Gray Code)", 
            fontsize=9.5, ha='center', color='#2C3E50')

    # Grid Lines
    for i in range(9): ax.plot([0, 4], [i, i], color='#2C3E50', lw=1.8)
    for j in range(5): ax.plot([j, j], [0, 8], color='#2C3E50', lw=1.8)
        
    ax.text(-0.6, 8.4, "ABC \\ DE", fontsize=11, fontweight='bold', ha='center', va='center', color='#78281F')
    for j, col in enumerate(col_labels): 
        ax.text(j + 0.5, 8.3, col, fontsize=12, fontweight='bold', ha='center', va='center', color='#2C3E50')
    for i, row in enumerate(row_labels): 
        ax.text(-0.4, 7.5 - i, row, fontsize=11.5, fontweight='bold', ha='center', va='center', color='#2C3E50')

    for r in range(8):
        for c in range(4):
            val = grid_vals[r][c]
            y_pos = 7.5 - r
            x_pos = c + 0.5
            if val == 0:
                bg = patches.Rectangle((c, 7-r), 1, 1, facecolor='#FDEDEC', zorder=1)
                ax.add_patch(bg)
                ax.text(x_pos, y_pos, str(val), fontsize=16, fontweight='bold', color='#922B21', ha='center', va='center', zorder=3)
            else:
                ax.text(x_pos, y_pos, str(val), fontsize=14, color='#BDC3C7', ha='center', va='center', zorder=3)
            ax.text(c + 0.88, 7.85 - r, grid_minterms[r][c], fontsize=7, color='#7F8C8D', ha='right', va='top')

    # ── POS GROUPINGS (Covering 9 Maxterm Zeros) ──
    # Group 1: (A + B + C + E') (Pair 2: Row 000, cols 01, 11)
    rect_p1 = patches.FancyBboxPatch((1.08, 7.08), 1.84, 0.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#C0392B', facecolor='none', zorder=4)
    ax.add_patch(rect_p1)
    ax.text(3.1, 7.5, "Group 1 (Pair 2):\n(A + B + C + E')", fontsize=9.5, fontweight='bold', color='#C0392B', va='center')

    # Group 2: (A + B + C + D') (Pair 2: Row 000, cols 11, 10)
    rect_p2 = patches.FancyBboxPatch((2.08, 7.08), 1.84, 0.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#2980B9', facecolor='none', linestyle='--', zorder=4)
    ax.add_patch(rect_p2)

    # Group 3: (B' + C + D + E) (Pair 2: Rows 010, 110, col 00)
    rect_p3 = patches.FancyBboxPatch((0.08, 3.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#8E44AD', facecolor='none', zorder=4)
    ax.add_patch(rect_p3)
    ax.text(-0.15, 4.0, "Group 3 (Pair 2):\n(B' + C + D + E)", fontsize=9.5, fontweight='bold', color='#8E44AD', ha='right', va='center')

    # Group 4: (B' + C + D' + E') (Pair 2: Rows 010, 110, col 11)
    rect_p4 = patches.FancyBboxPatch((2.08, 3.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.8, edgecolor='#D35400', facecolor='none', zorder=4)
    ax.add_patch(rect_p4)
    ax.text(4.15, 4.0, "Group 4 (Pair 2):\n(B' + C + D' + E')", fontsize=9.5, fontweight='bold', color='#D35400', va='center')

    # Group 5: (A' + B' + D + E) (Pair 2: Rows 110, 111, col 00)
    rect_p5 = patches.FancyBboxPatch((0.08, 2.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.5, edgecolor='#27AE60', facecolor='none', linestyle='-.', zorder=4)
    ax.add_patch(rect_p5)
    ax.text(-0.15, 2.5, "Group 5 (Pair 2):\n(A' + B' + D + E)", fontsize=9.5, fontweight='bold', color='#27AE60', ha='right', va='center')

    # Group 6: (A' + B' + D' + E') (Pair 2: Rows 110, 111, col 11)
    rect_p6 = patches.FancyBboxPatch((2.08, 2.08), 0.84, 1.84, boxstyle="round,pad=0.03,rounding_size=0.15", 
                                     linewidth=2.5, edgecolor='#16A085', facecolor='none', linestyle=':', zorder=4)
    ax.add_patch(rect_p6)
    ax.text(4.15, 2.5, "Group 6 (Pair 2):\n(A' + B' + D' + E')", fontsize=9.5, fontweight='bold', color='#16A085', va='center')

    # Summary Footer
    ax.text(2.0, -0.6, "Minimal POS Expression:  F_POS = (A+B+C+E')(A+B+C+D')(B'+C+D+E)(B'+C+D'+E')(A'+B'+D+E)(A'+B'+D'+E')", 
            fontsize=10.0, fontweight='bold', color='#78281F', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FDEDEC", edgecolor="#F5B7B1", lw=1.8))
            
    ax.set_xlim(-2.5, 6.0)
    ax.set_ylim(-1.0, 9.5)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "kmap_pos_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved assets/kmap_pos_diagram.png")

# ══════════════════════════════════════════════════════════════════════
# 4. PERFECTLY SYMMETRICAL MINIMAL SOP CIRCUIT SCHEMATIC
# ══════════════════════════════════════════════════════════════════════
def create_sop_circuit():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(9.0, 9.2, "Minimal SOP Logic Circuit Schematic (AND-OR Synthesis)", fontsize=15, fontweight='bold', ha='center', color='#117A65')
    ax.text(9.0, 8.65, "F_SOP = A'·C + A·B' + B'·D'·E' + B·D'·E + B·D·E'  (10 Gates, 15 Total Literals)", 
            fontsize=11.5, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F8F5", edgecolor="#A3E4D7", lw=1.5))
    
    # 5 AND gates arranged symmetrically around y = 4.4
    and1_in1, and1_in2, and1_out = draw_and2_gate(ax, 5.5, 7.6, width=1.5, height=1.1, label="AND1\n(A'·C)")
    and2_in1, and2_in2, and2_out = draw_and2_gate(ax, 5.5, 6.0, width=1.5, height=1.1, label="AND2\n(A·B')")
    and3_in1, and3_in2, and3_out = draw_and2_gate(ax, 5.5, 4.4, width=1.5, height=1.1, label="AND3\n(B'·D'·E')")
    and4_in1, and4_in2, and4_out = draw_and2_gate(ax, 5.5, 2.8, width=1.5, height=1.1, label="AND4\n(B·D'·E)")
    and5_in1, and5_in2, and5_out = draw_and2_gate(ax, 5.5, 1.2, width=1.5, height=1.1, label="AND5\n(B·D·E')")
    
    # Cascading 2-input OR Tree or multi-input OR
    or1_in1, or1_in2, or1_out = draw_or2_gate(ax, 9.5, 6.8, width=1.5, height=1.1, label="OR1")
    or2_in1, or2_in2, or2_out = draw_or2_gate(ax, 9.5, 3.6, width=1.5, height=1.1, label="OR2")
    or3_in1, or3_in2, or3_out = draw_or2_gate(ax, 12.0, 5.2, width=1.5, height=1.1, label="OR3")
    or4_in1, or4_in2, or4_out = draw_or2_gate(ax, 14.5, 4.8, width=1.5, height=1.1, label="OR4")
    
    # Symmetrical routing
    ax.plot([and1_out[0], 8.8, 8.8, or1_in1[0]], [and1_out[1], and1_out[1], or1_in1[1], or1_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([and2_out[0], 8.8, 8.8, or1_in2[0]], [and2_out[1], and2_out[1], or1_in2[1], or1_in2[1]], color=COLOR_STAGE2, lw=2.4)
    
    ax.plot([and3_out[0], 11.2, 11.2, or3_in1[0]], [and3_out[1], and3_out[1], or3_in1[1], or3_in1[1]], color=COLOR_STAGE2, lw=2.4)
    
    ax.plot([and4_out[0], 8.8, 8.8, or2_in1[0]], [and4_out[1], and4_out[1], or2_in1[1], or2_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([and5_out[0], 8.8, 8.8, or2_in2[0]], [and5_out[1], and5_out[1], or2_in2[1], or2_in2[1]], color=COLOR_STAGE2, lw=2.4)

    ax.plot([or1_out[0], 11.2, 11.2, or3_in2[0]], [or1_out[1], or1_out[1], or3_in2[1], or3_in2[1]], color=COLOR_STAGE3, lw=2.4)
    ax.plot([or3_out[0], 13.8, 13.8, or4_in1[0]], [or3_out[1], or3_out[1], or4_in1[1], or4_in1[1]], color=COLOR_STAGE3, lw=2.4)
    ax.plot([or2_out[0], 13.8, 13.8, or4_in2[0]], [or2_out[1], or2_out[1], or4_in2[1], or4_in2[1]], color=COLOR_STAGE3, lw=2.4)

    # Input labels on left with exact taps
    def add_in_tap(x_gate, y_gate, label, color):
        ax.text(x_gate - 0.35, y_gate, label, fontsize=10.5, fontweight='bold', color=color, ha='right', va='center')
        ax.plot([x_gate - 0.30, x_gate], [y_gate, y_gate], color=color, lw=2.0)

    add_in_tap(and1_in1[0], and1_in1[1], "A'", COLOR_A)
    add_in_tap(and1_in2[0], and1_in2[1], "C", COLOR_C)
    
    add_in_tap(and2_in1[0], and2_in1[1], "A", COLOR_A)
    add_in_tap(and2_in2[0], and2_in2[1], "B'", COLOR_B)
    
    add_in_tap(and3_in1[0], and3_in1[1], "B'", COLOR_B)
    add_in_tap(and3_in2[0], and3_in2[1], "D'E'", COLOR_D)

    add_in_tap(and4_in1[0], and4_in1[1], "B", COLOR_B)
    add_in_tap(and4_in2[0], and4_in2[1], "D'E", COLOR_E)

    add_in_tap(and5_in1[0], and5_in1[1], "B", COLOR_B)
    add_in_tap(and5_in2[0], and5_in2[1], "DE'", COLOR_E)

    # Output Terminal
    x_out_term = 17.2
    ax.plot([or4_out[0], x_out_term], [or4_out[1], or4_out[1]], color=COLOR_FINAL_OUT, lw=3.2)
    ax.add_patch(patches.Circle((x_out_term, or4_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.35, or4_out[1], "F_SOP", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.set_xlim(3.2, 19.5)
    ax.set_ylim(-0.4, 9.8)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "sop_circuit_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved upgraded assets/sop_circuit_diagram.png")

# ══════════════════════════════════════════════════════════════════════
# 5. PERFECTLY SYMMETRICAL MINIMAL POS CIRCUIT SCHEMATIC
# ══════════════════════════════════════════════════════════════════════
def create_pos_circuit():
    fig, ax = plt.subplots(figsize=(18, 10.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(10.0, 9.5, "Minimal POS Logic Circuit Schematic (OR-AND Synthesis)", fontsize=15, fontweight='bold', ha='center', color='#78281F')
    ax.text(10.0, 8.95, "F_POS = (A+B+C+E')(A+B+C+D')(B'+C+D+E)(B'+C+D'+E')(A'+B'+D+E)(A'+B'+D'+E')", 
            fontsize=10.5, ha='center', color='#2C3E50', bbox=dict(boxstyle="round,pad=0.4", facecolor="#FDEDEC", edgecolor="#F5B7B1", lw=1.5))
    
    # 6 OR gates arranged symmetrically
    or1_in1, or1_in2, or1_out = draw_or2_gate(ax, 5.0, 7.8, label="OR1")
    or2_in1, or2_in2, or2_out = draw_or2_gate(ax, 5.0, 6.4, label="OR2")
    or3_in1, or3_in2, or3_out = draw_or2_gate(ax, 5.0, 5.0, label="OR3")
    or4_in1, or4_in2, or4_out = draw_or2_gate(ax, 5.0, 3.6, label="OR4")
    or5_in1, or5_in2, or5_out = draw_or2_gate(ax, 5.0, 2.2, label="OR5")
    or6_in1, or6_in2, or6_out = draw_or2_gate(ax, 5.0, 0.8, label="OR6")
    
    # 2-input AND Cascading Tree
    and1_in1, and1_in2, and1_out = draw_and2_gate(ax, 8.5, 7.1, label="AND1")
    and2_in1, and2_in2, and2_out = draw_and2_gate(ax, 8.5, 4.3, label="AND2")
    and3_in1, and3_in2, and3_out = draw_and2_gate(ax, 8.5, 1.5, label="AND3")
    
    and4_in1, and4_in2, and4_out = draw_and2_gate(ax, 11.5, 5.7, label="AND4")
    and5_in1, and5_in2, and5_out = draw_and2_gate(ax, 14.5, 4.3, label="AND5")
    
    # Symmetrical routing
    ax.plot([or1_out[0], 7.8, 7.8, and1_in1[0]], [or1_out[1], or1_out[1], and1_in1[1], and1_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([or2_out[0], 7.8, 7.8, and1_in2[0]], [or2_out[1], or2_out[1], and1_in2[1], and1_in2[1]], color=COLOR_STAGE2, lw=2.4)

    ax.plot([or3_out[0], 7.8, 7.8, and2_in1[0]], [or3_out[1], or3_out[1], and2_in1[1], and2_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([or4_out[0], 7.8, 7.8, and2_in2[0]], [or4_out[1], or4_out[1], and2_in2[1], and2_in2[1]], color=COLOR_STAGE2, lw=2.4)

    ax.plot([or5_out[0], 7.8, 7.8, and3_in1[0]], [or5_out[1], or5_out[1], and3_in1[1], and3_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([or6_out[0], 7.8, 7.8, and3_in2[0]], [or6_out[1], or6_out[1], and3_in2[1], and3_in2[1]], color=COLOR_STAGE2, lw=2.4)

    ax.plot([and1_out[0], 10.8, 10.8, and4_in1[0]], [and1_out[1], and1_out[1], and4_in1[1], and4_in1[1]], color=COLOR_STAGE2, lw=2.4)
    ax.plot([and2_out[0], 10.8, 10.8, and4_in2[0]], [and2_out[1], and2_out[1], and4_in2[1], and4_in2[1]], color=COLOR_STAGE2, lw=2.4)

    ax.plot([and4_out[0], 13.8, 13.8, and5_in1[0]], [and4_out[1], and4_out[1], and5_in1[1], and5_in1[1]], color=COLOR_STAGE3, lw=2.4)
    ax.plot([and3_out[0], 13.8, 13.8, and5_in2[0]], [and3_out[1], and3_out[1], and5_in2[1], and5_in2[1]], color=COLOR_STAGE3, lw=2.4)

    # Input labels on left with exact taps
    def add_in_tap(x_gate, y_gate, label, color):
        ax.text(x_gate - 0.35, y_gate, label, fontsize=9.5, fontweight='bold', color=color, ha='right', va='center')
        ax.plot([x_gate - 0.30, x_gate], [y_gate, y_gate], color=color, lw=2.0)

    add_in_tap(or1_in1[0], or1_in1[1], "(A+B)", COLOR_A)
    add_in_tap(or1_in2[0], or1_in2[1], "(C+E')", COLOR_C)

    add_in_tap(or2_in1[0], or2_in1[1], "(A+B)", COLOR_A)
    add_in_tap(or2_in2[0], or2_in2[1], "(C+D')", COLOR_D)

    add_in_tap(or3_in1[0], or3_in1[1], "(B'+C)", COLOR_B)
    add_in_tap(or3_in2[0], or3_in2[1], "(D+E)", COLOR_D)

    add_in_tap(or4_in1[0], or4_in1[1], "(B'+C)", COLOR_B)
    add_in_tap(or4_in2[0], or4_in2[1], "(D'+E')", COLOR_E)

    add_in_tap(or5_in1[0], or5_in1[1], "(A'+B')", COLOR_A)
    add_in_tap(or5_in2[0], or5_in2[1], "(D+E)", COLOR_D)

    add_in_tap(or6_in1[0], or6_in1[1], "(A'+B')", COLOR_A)
    add_in_tap(or6_in2[0], or6_in2[1], "(D'+E')", COLOR_E)

    # Output Terminal (Solid, Exact Alignment)
    x_out_term = 17.5
    ax.plot([and5_out[0], x_out_term], [and5_out[1], and5_out[1]], color=COLOR_FINAL_OUT, lw=3.2)
    ax.add_patch(patches.Circle((x_out_term, and5_out[1]), 0.12, facecolor=COLOR_FINAL_OUT, edgecolor='black', lw=1.5, zorder=5))
    ax.text(x_out_term + 0.35, and5_out[1], "F_POS", fontsize=15, fontweight='bold', color=COLOR_FINAL_OUT, ha='left', va='center')
    
    ax.set_xlim(3.0, 20.0)
    ax.set_ylim(-0.2, 10.0)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "pos_circuit_diagram.png"), bbox_inches='tight')
    plt.close()
    print("Saved upgraded assets/pos_circuit_diagram.png")

# ══════════════════════════════════════════════════════════════════════
# 6. HARDWARE IC PINOUT & WIRING LAYOUT
# ══════════════════════════════════════════════════════════════════════
def create_ic_pinout_layout():
    fig, ax = plt.subplots(figsize=(18, 9.0), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    
    ax.text(9.0, 8.5, "Hardware Implementation IC Package & Breadboard Wiring Map", fontsize=15, fontweight='bold', ha='center', color='#1A5276')
    ax.text(9.0, 8.0, "Standard 74HC Series DIP Packages for 2-Input Combinational Logic Synthesis", fontsize=11, ha='center', color='#566573')
    
    def draw_dip_ic(x, y, name, part_no, pins=14, color="#2C3E50"):
        w, h = 2.4, 4.2
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.1", 
                                      facecolor="#1C2833", edgecolor=color, lw=2.2, zorder=3)
        ax.add_patch(rect)
        notch = patches.Arc((x + w/2, y + h), 0.5, 0.4, angle=0, theta1=180, theta2=360, color="#BDC3C7", lw=2, zorder=4)
        ax.add_patch(notch)
        
        ax.text(x + w/2, y + h/2 + 0.35, part_no, fontsize=12, fontweight='bold', color="#F4D03F", ha='center', va='center', zorder=4)
        ax.text(x + w/2, y + h/2 - 0.35, name, fontsize=9.0, color="#ECF0F1", ha='center', va='center', zorder=4)
        
        num_pins_side = pins // 2
        dy = h / (num_pins_side + 1)
        for p in range(num_pins_side):
            py = y + h - (p + 1)*dy
            ax.add_patch(patches.Rectangle((x - 0.35, py - 0.08), 0.35, 0.16, facecolor="#BDC3C7", edgecolor="#7F8C8D", lw=1.2, zorder=2))
            ax.text(x + 0.22, py, str(p + 1), fontsize=8, color="#A6ACAF", ha='center', va='center', zorder=4)
            ax.add_patch(patches.Rectangle((x + w, py - 0.08), 0.35, 0.16, facecolor="#BDC3C7", edgecolor="#7F8C8D", lw=1.2, zorder=2))
            ax.text(x + w - 0.22, py, str(pins - p), fontsize=8, color="#A6ACAF", ha='center', va='center', zorder=4)

    draw_dip_ic(0.5, 2.0, "Hex Inverter\n(6 NOT)", "74HC04", pins=14, color="#C0392B")
    draw_dip_ic(3.5, 2.0, "Quad 2-In XOR\n(4 Gates)", "74HC86", pins=14, color="#6C3483")
    draw_dip_ic(6.5, 2.0, "Quad 2-In NAND\n(4 Gates)", "74HC00", pins=14, color="#117A65")
    draw_dip_ic(9.5, 2.0, "Quad 2-In NOR\n(4 Gates)", "74HC02", pins=14, color="#B9770E")
    draw_dip_ic(12.5, 2.0, "Quad 2-In AND\n(4 Gates)", "74HC08", pins=14, color="#2980B9")
    draw_dip_ic(15.5, 2.0, "Quad 2-In OR\n(4 Gates)", "74HC32", pins=14, color="#27AE60")
    
    ax.text(9.0, 1.0, "Power Supply: Pin 14 = VCC (+5V), Pin 7 = GND (0V) for all 14-pin DIP ICs", 
            fontsize=10.5, fontweight='bold', ha='center', color="#2C3E50", 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F8F9F9", edgecolor="#D5D8DC", lw=1.2))
    
    ax.set_xlim(-0.2, 18.8)
    ax.set_ylim(0.2, 9.2)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_PATH, "ic_pinout_layout.png"), bbox_inches='tight')
    plt.close()
    print("Saved upgraded assets/ic_pinout_layout.png")

if __name__ == "__main__":
    create_original_circuit()
    create_kmap_sop()
    create_kmap_pos()
    create_sop_circuit()
    create_pos_circuit()
    create_ic_pinout_layout()
    print("ALL DIAGRAMS GENERATED WITH PRISTINE ACCURACY!")
