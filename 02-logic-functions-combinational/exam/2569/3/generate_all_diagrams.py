#!/usr/bin/env python3
"""
High-Resolution (300 DPI) Digital Logic Schematic & K-Map Generator
Exam 2569 — Problem 03 (4-Stage Combinational Network with All 7 Standard Gate Types & Strict Max 2-Input Limit)
Gates Used: 74HC04 (NOT), 74HC86 (XOR), 74HC7266 (XNOR), 74HC00 (NAND), 74HC08 (AND), 74HC02 (NOR), 74HC32 (OR)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

COLOR_BG = "#FFFFFF"
DPI = 300

# Color palette for 5 input variables
COLORS = {
    'A': '#DC2626', # Red
    'B': '#2563EB', # Blue
    'C': '#16A34A', # Green
    'D': '#9333EA', # Purple
    'E': '#D97706'  # Amber
}

def draw_and_gate(ax, x0, y0, width=1.4, height=1.0, label="AND", color="#1E40AF", fill="#EFF6FF"):
    """Standard IEEE AND Gate"""
    r = height / 2.0
    w_rect = width - r
    rect = patches.Rectangle((x0, y0 - r), w_rect, height, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(rect)
    arc = patches.Wedge((x0 + w_rect, y0), r, -90, 90, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(arc)
    ax.plot([x0 + w_rect, x0 + w_rect], [y0 - r + 0.05, y0 + r - 0.05], color=fill, linewidth=3.0, zorder=4)
    if label:
        ax.text(x0 + width*0.38, y0, label, color=color, fontsize=9.0, fontweight='bold', ha='center', va='center', zorder=5)
    return x0 + width, y0

def draw_or_gate(ax, x0, y0, width=1.5, height=1.1, label="OR", color="#047857", fill="#ECFDF5"):
    """Standard IEEE curved OR Gate"""
    half_h = height / 2.0
    theta = np.linspace(-np.pi/2.5, np.pi/2.5, 40)
    back_x = x0 + 0.3 * np.cos(theta) - 0.3 * np.cos(np.pi/2.5)
    back_y = y0 + half_h * np.sin(theta) / np.sin(np.pi/2.5)
    
    t_top = np.linspace(0, 1, 40)
    top_x = (1 - t_top)**2 * (back_x[-1]) + 2*(1 - t_top)*t_top * (x0 + width*0.6) + t_top**2 * (x0 + width)
    top_y = (1 - t_top)**2 * (y0 + half_h) + 2*(1 - t_top)*t_top * (y0 + half_h*0.85) + t_top**2 * y0
    
    t_bot = np.linspace(0, 1, 40)
    bot_x = (1 - t_bot)**2 * (x0 + width) + 2*(1 - t_bot)*t_bot * (x0 + width*0.6) + t_bot**2 * (back_x[0])
    bot_y = (1 - t_bot)**2 * y0 + 2*(1 - t_bot)*t_bot * (y0 - half_h*0.85) + t_bot**2 * (y0 - half_h)
    
    verts_x = np.concatenate([back_x, top_x, bot_x])
    verts_y = np.concatenate([back_y, top_y, bot_y])
    
    poly = patches.Polygon(np.column_stack([verts_x, verts_y]), closed=True,
                           facecolor=fill, edgecolor=color, linewidth=2.0, zorder=3)
    ax.add_patch(poly)
    if label:
        ax.text(x0 + width*0.45, y0, label, color=color, fontsize=9.0, fontweight='bold', ha='center', va='center', zorder=5)
    return x0 + width, y0

def draw_xor_gate(ax, x0, y0, width=1.5, height=1.1, label="XOR", color="#6D28D9", fill="#F5F3FF"):
    """Standard IEEE XOR Gate with detached back arc"""
    draw_or_gate(ax, x0, y0, width, height, label, color, fill)
    half_h = height / 2.0
    theta = np.linspace(-np.pi/2.5, np.pi/2.5, 40)
    arc_x = x0 - 0.22 + 0.3 * np.cos(theta) - 0.3 * np.cos(np.pi/2.5)
    arc_y = y0 + half_h * np.sin(theta) / np.sin(np.pi/2.5)
    ax.plot(arc_x, arc_y, color=color, linewidth=2.0, zorder=3)
    return x0 + width, y0

def draw_xnor_gate(ax, x0, y0, width=1.5, height=1.1, label="XNOR", color="#0284C7", fill="#F0F9FF"):
    """Standard IEEE XNOR Gate with detached back arc and output bubble"""
    x_apex, y_apex = draw_or_gate(ax, x0, y0, width, height, label, color, fill)
    half_h = height / 2.0
    theta = np.linspace(-np.pi/2.5, np.pi/2.5, 40)
    arc_x = x0 - 0.22 + 0.3 * np.cos(theta) - 0.3 * np.cos(np.pi/2.5)
    arc_y = y0 + half_h * np.sin(theta) / np.sin(np.pi/2.5)
    ax.plot(arc_x, arc_y, color=color, linewidth=2.0, zorder=3)
    
    bubble_r = 0.09
    bubble = patches.Circle((x_apex + bubble_r, y_apex), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    return x_apex + 2*bubble_r, y_apex

def draw_nand_gate(ax, x0, y0, width=1.4, height=1.0, label="NAND", color="#0D9488", fill="#F0FDFA"):
    """NAND Gate with inversion bubble"""
    x_apex, y_apex = draw_and_gate(ax, x0, y0, width, height, label, color, fill)
    bubble_r = 0.09
    bubble = patches.Circle((x_apex + bubble_r, y_apex), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    return x_apex + 2*bubble_r, y_apex

def draw_nor_gate(ax, x0, y0, width=1.5, height=1.1, label="NOR", color="#B45309", fill="#FFFBEB"):
    """NOR Gate with inversion bubble"""
    x_apex, y_apex = draw_or_gate(ax, x0, y0, width, height, label, color, fill)
    bubble_r = 0.09
    bubble = patches.Circle((x_apex + bubble_r, y_apex), bubble_r, facecolor=fill, edgecolor=color, linewidth=2.0, zorder=4)
    ax.add_patch(bubble)
    return x_apex + 2*bubble_r, y_apex

def draw_inverter(ax, x0, y0, width=1.0, height=0.6, label="NOT", color="#DC2626", fill="#FEF2F2"):
    """Inverter triangle with bubble"""
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
        ax.text(x0 + width*0.35, y0, label, color=color, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=5)
    return x0 + width + 2*bubble_r, y0

# ==============================================================================
# 1. ORIGINAL 4-STAGE COMBINATIONAL CIRCUIT (SOLUTION & STUDENT WORKSHEET VERSIONS)
# ==============================================================================
def generate_original_circuit_version(is_worksheet=False):
    fig, ax = plt.subplots(figsize=(24, 13), dpi=DPI)
    ax.set_xlim(-1.5, 24.5)
    ax.set_ylim(-2.0, 13.0)
    ax.axis('off')
    
    # Title & Subtitle Banner
    if is_worksheet:
        ax.text(11.5, 12.3, "305241 Digital Logic Design — Exam 2569 Problem 03 (Student Worksheet & Exercise)",
                fontsize=16.5, fontweight='bold', ha='center', color="#0F172A")
        ax.text(11.5, 11.65,
                "Instructions: Trace the 4-stage logic propagation, write the Boolean expressions for W₁ through W₇, and determine the output function F.",
                fontsize=11.0, ha='center', color="#334155",
                bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.4))
    else:
        ax.text(11.5, 12.3, "305241 Digital Logic Design — Exam 2569 Problem 03 (Full Circuit Schematic & Probe Equations)",
                fontsize=16.5, fontweight='bold', ha='center', color="#0F172A")
        ax.text(11.5, 11.65,
                "5-Variable 4-Stage Combinational Network Featuring All 7 Standard Gates (74HC04, 74HC86, 74HC7266, 74HC00, 74HC08, 74HC02, 74HC32 — Strict Max 2-Input Limit)",
                fontsize=11.0, ha='center', color="#334155",
                bbox=dict(boxstyle="round,pad=0.45", facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.2))

    # Stage Region Background Panels for Research-Grade Visual Clarity
    stage_panels = [
        ("STAGE 1: Pre-Logic Layer", 3.6, 7.8, -0.4, 10.6, "#F8FAFC", "#E2E8F0"),
        ("STAGE 2: Product / Intermediate Layer", 9.1, 13.3, -0.4, 10.6, "#F8FAFC", "#E2E8F0"),
        ("STAGE 3: Sub-Sum", 14.3, 17.5, -0.4, 10.6, "#F8FAFC", "#E2E8F0"),
        ("STAGE 4: Collector", 18.5, 21.7, -0.4, 10.6, "#F8FAFC", "#E2E8F0"),
    ]
    for lbl, x1, x2, y1, y2, bg, bdr in stage_panels:
        rect = patches.FancyBboxPatch((x1, y1), x2 - x1, y2 - y1, boxstyle="round,pad=0.15",
                                      facecolor=bg, edgecolor=bdr, linewidth=1.0, linestyle=':', zorder=1)
        ax.add_patch(rect)
        ax.text((x1 + x2)/2.0, 10.35, lbl, fontsize=9.0, fontweight='bold', ha='center', color="#64748B", zorder=2)

    # 5 Dedicated Input Bus Rails (A, B, C, D, E)
    bus_x = {'A': 0.0, 'B': 0.7, 'C': 1.4, 'D': 2.1, 'E': 2.8}
    for var, x in bus_x.items():
        c = COLORS[var]
        ax.plot([x, x], [0.4, 10.2], color=c, linewidth=2.2, zorder=2)
        ax.plot(x, 10.45, marker='o', markersize=9, color=c, zorder=5)
        ax.text(x, 10.8, var, color=c, fontsize=14, fontweight='bold', ha='center', va='bottom')

    # Stage X positions
    stg1_x = 4.3
    stg2_x = 9.8
    stg3_x = 15.0
    stg4_x = 19.2

    # STAGE 1: GATES (x = 4.3) — Mathematically Equidistant (Δy = 2.50)
    # 1. NOT A (y = 9.30)
    out_not_a = draw_inverter(ax, stg1_x, 9.30, width=1.1, height=0.6,
                              label="" if is_worksheet else "NOT A\n(7404)",
                              color="#DC2626", fill="#FEF2F2")
    ax.plot([bus_x['A'], stg1_x], [9.30, 9.30], color=COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['A'], 9.30, marker='o', markersize=5.5, color=COLORS['A'], zorder=4)
    # Wire from NOT to channel
    ax.plot([out_not_a[0], 8.2, 8.2, stg2_x], [9.30, 9.30, 8.30, 8.30], color="#DC2626", linewidth=1.8, zorder=2)
    if is_worksheet:
        ax.text(out_not_a[0] + 0.15, 9.30, " A' = [ ........... ] ", color="#DC2626", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#DC2626", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_not_a[0] + 0.15, 9.30, " A' ", color="#DC2626", fontsize=11, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#DC2626", linewidth=1.0))

    # 2. XOR (y = 6.80) -> W1 = B ⊕ D
    out_xor = draw_xor_gate(ax, stg1_x, 6.80, width=1.5, height=1.1,
                            label="" if is_worksheet else "XOR\n(7486)",
                            color="#6D28D9", fill="#F5F3FF")
    # Top In: B (y = 7.05)
    ax.plot([bus_x['B'], stg1_x], [7.05, 7.05], color=COLORS['B'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['B'], 7.05, marker='o', markersize=5.5, color=COLORS['B'], zorder=4)
    # Bot In: D (y = 6.55)
    ax.plot([bus_x['D'], stg1_x], [6.55, 6.55], color=COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['D'], 6.55, marker='o', markersize=5.5, color=COLORS['D'], zorder=4)
    # Wire from XOR to channel
    ax.plot([out_xor[0], 8.2, 8.2, stg2_x], [6.80, 6.80, 7.80, 7.80], color="#6D28D9", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_xor[0] + 0.15, 6.80, " W₁ = [ .................... ] ", color="#6D28D9", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#6D28D9", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_xor[0] + 0.15, 6.80, " W₁ = B ⊕ D ", color="#6D28D9", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#6D28D9", linewidth=1.0))

    # 3. XNOR (y = 4.30) -> W2 = C ⊙ E
    out_xnor = draw_xnor_gate(ax, stg1_x, 4.30, width=1.5, height=1.1,
                              label="" if is_worksheet else "XNOR\n(7266)",
                              color="#0284C7", fill="#F0F9FF")
    # Top In: C (y = 4.55)
    ax.plot([bus_x['C'], stg1_x], [4.55, 4.55], color=COLORS['C'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['C'], 4.55, marker='o', markersize=5.5, color=COLORS['C'], zorder=4)
    # Bot In: E (y = 4.05)
    ax.plot([bus_x['E'], stg1_x], [4.05, 4.05], color=COLORS['E'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['E'], 4.05, marker='o', markersize=5.5, color=COLORS['E'], zorder=4)
    # Wire from XNOR to channel
    ax.plot([out_xnor[0], 8.5, 8.5, stg2_x], [4.30, 4.30, 5.80, 5.80], color="#0284C7", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_xnor[0] + 0.15, 4.30, " W₂ = [ .................... ] ", color="#0284C7", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#0284C7", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_xnor[0] + 0.15, 4.30, " W₂ = C ⊙ E ", color="#0284C7", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#0284C7", linewidth=1.0))

    # 4. NAND (y = 1.80) -> W3 = (A · D)'
    out_nand = draw_nand_gate(ax, stg1_x, 1.80, width=1.4, height=1.0,
                              label="" if is_worksheet else "NAND\n(7400)",
                              color="#0D9488", fill="#F0FDFA")
    # Top In: A (y = 2.05)
    ax.plot([bus_x['A'], stg1_x], [2.05, 2.05], color=COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['A'], 2.05, marker='o', markersize=5.5, color=COLORS['A'], zorder=4)
    # Bot In: D (y = 1.55)
    ax.plot([bus_x['D'], stg1_x], [1.55, 1.55], color=COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['D'], 1.55, marker='o', markersize=5.5, color=COLORS['D'], zorder=4)
    # Wire from NAND to channel
    ax.plot([out_nand[0], 8.5, 8.5, stg2_x], [1.80, 1.80, 3.30, 3.30], color="#0D9488", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_nand[0] + 0.15, 1.80, " W₃ = [ .................... ] ", color="#0D9488", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#0D9488", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_nand[0] + 0.15, 1.80, " W₃ = (A·D)' ", color="#0D9488", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#0D9488", linewidth=1.0))

    # STAGE 2: GATES (x = 9.8) — Interleaved Symmetric Positions (y = 8.05, 5.55, 3.05)
    stg2_x = 9.8
    
    # 5. AND1 (y = 8.05) -> W4 = A' · W1
    out_and1 = draw_and_gate(ax, stg2_x, 8.05, width=1.4, height=1.0,
                             label="" if is_worksheet else "AND1\n(7408)",
                             color="#1E40AF", fill="#EFF6FF")
    # Wire from AND1 to Stage 3 channel
    ax.plot([out_and1[0], 13.8, 13.8, 15.0], [8.05, 8.05, 7.05, 7.05], color="#1E40AF", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_and1[0] + 0.15, 8.05, " W₄ = [ .................... ] ", color="#1E40AF", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_and1[0] + 0.15, 8.05, " W₄ = A'·(B ⊕ D) ", color="#1E40AF", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.0))

    # 6. AND2 (y = 5.55) -> W5 = W2 · C = C · E
    out_and2 = draw_and_gate(ax, stg2_x, 5.55, width=1.4, height=1.0,
                             label="" if is_worksheet else "AND2\n(7408)",
                             color="#1E40AF", fill="#EFF6FF")
    # Bot In directly from Bus C (y = 5.30) — Straight clear horizontal line between XOR and XNOR!
    ax.plot([bus_x['C'], stg2_x], [5.30, 5.30], color=COLORS['C'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['C'], 5.30, marker='o', markersize=5.5, color=COLORS['C'], zorder=4)
    # Wire from AND2 to Stage 3 channel
    ax.plot([out_and2[0], 13.8, 13.8, 15.0], [5.55, 5.55, 6.55, 6.55], color="#1E40AF", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_and2[0] + 0.15, 5.55, " W₅ = [ .................... ] ", color="#1E40AF", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_and2[0] + 0.15, 5.55, " W₅ = C · E ", color="#1E40AF", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.0))

    # 7. NOR (y = 3.05) -> W6 = (W3 + E)' = A · D · E'
    out_nor = draw_nor_gate(ax, stg2_x, 3.05, width=1.5, height=1.1,
                            label="" if is_worksheet else "NOR\n(7402)",
                            color="#B45309", fill="#FFFBEB")
    # Bot In directly from Bus E (y = 2.80) — Straight clear horizontal line between XNOR and NAND!
    ax.plot([bus_x['E'], stg2_x], [2.80, 2.80], color=COLORS['E'], linewidth=1.8, zorder=2)
    ax.plot(bus_x['E'], 2.80, marker='o', markersize=5.5, color=COLORS['E'], zorder=4)
    # Wire from NOR to Stage 4 channel
    ax.plot([out_nor[0], 18.0, 18.0, 19.2], [3.05, 3.05, 4.675, 4.675], color="#B45309", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_nor[0] + 0.15, 3.05, " W₆ = [ .................... ] ", color="#B45309", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#B45309", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_nor[0] + 0.15, 3.05, " W₆ = A·D·E' ", color="#B45309", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#B45309", linewidth=1.0))

    # STAGE 3: GATE (x = 15.0) -> OR1 (W7 = W4 + W5, y = 6.80)
    stg3_x = 15.0
    out_or1 = draw_or_gate(ax, stg3_x, 6.80, width=1.5, height=1.1,
                           label="" if is_worksheet else "OR1\n(7432)",
                           color="#047857", fill="#ECFDF5")
    # Wire from OR1 to Stage 4 channel
    ax.plot([out_or1[0], 18.0, 18.0, 19.2], [6.80, 6.80, 5.175, 5.175], color="#047857", linewidth=1.8, zorder=2)
    
    if is_worksheet:
        ax.text(out_or1[0] + 0.15, 6.80, " W₇ = [ .................... ] ", color="#047857", fontsize=9.5, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#047857", linestyle='--', linewidth=1.1))
    else:
        ax.text(out_or1[0] + 0.15, 6.80, " W₇ = W₄ + W₅ ", color="#047857", fontsize=10, fontweight='bold', va='center', zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor="#047857", linewidth=1.0))

    # STAGE 4: GATE (x = 19.2) -> OR2 (F = W7 + W6, y = 4.925)
    stg4_x = 19.2
    out_or2 = draw_or_gate(ax, stg4_x, 4.925, width=1.5, height=1.1,
                           label="" if is_worksheet else "OR2\n(7432)",
                           color="#047857", fill="#ECFDF5")

    # FINAL OUTPUT TERMINAL F
    ax.plot([out_or2[0], 22.2], [4.925, 4.925], color="#0F172A", linewidth=2.4, zorder=2)
    ax.plot(22.2, 4.925, marker='o', markersize=9, color="#0F172A", zorder=5)
    ax.text(22.6, 4.925, "F", color="#0F172A", fontsize=18, fontweight='bold', va='center')

    # Bottom Banner / Student Block
    if is_worksheet:
        ax.text(11.5, -1.15, "Final Output Expression: F(A, B, C, D, E) = [                                                                                                                              ]",
                fontsize=12.0, fontweight='bold', ha='center', color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFFFFF", edgecolor="#0F172A", linestyle='-', linewidth=1.8))
        ax.text(11.5, -1.75, "Student Name: ...................................................................  ID: ...................................  Section: ........  Score: [       / 10 ]",
                fontsize=10.5, ha='center', color="#475569")
    else:
        ax.text(11.5, -1.2, "F = W₇ + W₆ = A'·(B ⊕ D) + C·E + A·D·E' = C·E + A'·B'·D + A'·B·D' + A·D·E'",
                fontsize=13.0, fontweight='bold', ha='center', color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFFFFF", edgecolor="#0F172A", linewidth=1.8))

    plt.tight_layout()
    filename = "digital_logic_circuit_worksheet.png" if is_worksheet else "digital_logic_circuit_redrawn.png"
    out_path = os.path.join(ASSETS_DIR, filename)
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

def generate_original_circuit():
    # 1. Solution Full Schematic
    generate_original_circuit_version(is_worksheet=False)
    # 2. Student Worksheet Exercise Edition
    generate_original_circuit_version(is_worksheet=True)

# ==============================================================================
# 2. 8x4 K-MAP DIAGRAM FOR MINIMAL SOP (GROUPING 1s)
# ==============================================================================
def generate_kmap_sop():
    fig, ax = plt.subplots(figsize=(14, 11), dpi=DPI)
    ax.set_xlim(-1.5, 12.5)
    ax.set_ylim(-1.5, 11.5)
    ax.axis('off')

    ax.text(5.5, 10.9, "8x4 Karnaugh Map -- Minimal SOP (Grouping 1s)",
            fontsize=16, fontweight='bold', ha='center', color="#0F172A")
    ax.text(5.5, 10.4, "5-Variable Logic Minimization: 18 Minterms -> 4 Essential Prime Implicants",
            fontsize=11.5, ha='center', color="#475569")

    gx0 = 2.4
    gy0 = 1.0
    cell_w = 1.6
    cell_h = 1.0

    row_labels = ["000", "001", "011", "010", "110", "111", "101", "100"]
    col_labels = ["00", "01", "11", "10"]

    ax.text(gx0 - 0.7, gy0 + 8.5 * cell_h, "ABC \\ DE", fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")
    for c, clab in enumerate(col_labels):
        ax.text(gx0 + (c + 0.5)*cell_w, gy0 + 8.3*cell_h, clab, fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")

    sop_minterms = {2, 3, 5, 6, 7, 8, 9, 12, 13, 15, 18, 21, 22, 23, 26, 29, 30, 31}

    for r in range(8):
        y_top = gy0 + (7 - r) * cell_h
        rlab = row_labels[r]
        ax.text(gx0 - 0.7, y_top + 0.5*cell_h, rlab, fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")

        for c in range(4):
            x_left = gx0 + c * cell_w
            r_val = int(rlab, 2)
            c_val = int(col_labels[c], 2)
            m_num = (r_val << 2) | c_val
            is_one = m_num in sop_minterms

            rect = patches.Rectangle((x_left, y_top), cell_w, cell_h,
                                     facecolor="#F8FAFC" if not is_one else "#EFF6FF",
                                     edgecolor="#94A3B8", linewidth=1.2, zorder=1)
            ax.add_patch(rect)

            ax.text(x_left + 0.15, y_top + cell_h - 0.18, f"m{m_num}", fontsize=8.5, color="#64748B", zorder=3)
            val_str = "1" if is_one else "0"
            val_col = "#1E40AF" if is_one else "#94A3B8"
            ax.text(x_left + cell_w*0.5, y_top + cell_h*0.42, val_str,
                    fontsize=14.5, fontweight='bold', ha='center', va='center', color=val_col, zorder=3)

    # Group 1 (Octet 8 cells): C · E
    g1a = patches.FancyBboxPatch((gx0 + 1*cell_w + 0.08, gy0 + 5*cell_h + 0.08), 2*cell_w - 0.16, 2*cell_h - 0.16,
                                boxstyle="round,pad=0.08", facecolor="#2563EB", alpha=0.18, edgecolor="#2563EB", linewidth=2.4, zorder=4)
    ax.add_patch(g1a)
    g1b = patches.FancyBboxPatch((gx0 + 1*cell_w + 0.08, gy0 + 1*cell_h + 0.08), 2*cell_w - 0.16, 2*cell_h - 0.16,
                                boxstyle="round,pad=0.08", facecolor="#2563EB", alpha=0.18, edgecolor="#2563EB", linewidth=2.4, zorder=4)
    ax.add_patch(g1b)

    # Group 2 (Quad 4 cells): A' · B' · D
    g2 = patches.FancyBboxPatch((gx0 + 2*cell_w + 0.12, gy0 + 6*cell_h + 0.12), 2*cell_w - 0.24, 2*cell_h - 0.24,
                               boxstyle="round,pad=0.08", facecolor="#DC2626", alpha=0.20, edgecolor="#DC2626", linewidth=2.4, zorder=4)
    ax.add_patch(g2)

    # Group 3 (Quad 4 cells): A' · B · D'
    g3 = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.12, gy0 + 4*cell_h + 0.12), 2*cell_w - 0.24, 2*cell_h - 0.24,
                               boxstyle="round,pad=0.08", facecolor="#9333EA", alpha=0.20, edgecolor="#9333EA", linewidth=2.4, zorder=4)
    ax.add_patch(g3)

    # Group 4 (Quad 4 cells Vertical): A · D · E'
    g4 = patches.FancyBboxPatch((gx0 + 3*cell_w + 0.12, gy0 + 0*cell_h + 0.12), 1*cell_w - 0.24, 4*cell_h - 0.24,
                               boxstyle="round,pad=0.08", facecolor="#16A34A", alpha=0.22, edgecolor="#16A34A", linewidth=2.4, zorder=4)
    ax.add_patch(g4)

    # Legend / Summary Card on Right
    lx = 9.4
    ax.text(lx + 1.4, 8.8, "SOP Prime Implicants (4 Groups)", fontsize=13, fontweight='bold', color="#0F172A", ha='center')
    
    groups_info = [
        ("Group 1 (Octet 8)", "C · E", "#2563EB", "#EFF6FF", "m5, m7, m13, m15, m21, m23, m29, m31"),
        ("Group 2 (Quad 4)", "A' · B' · D", "#DC2626", "#FEF2F2", "m2, m3, m6, m7"),
        ("Group 3 (Quad 4)", "A' · B · D'", "#9333EA", "#F5F3FF", "m8, m9, m12, m13"),
        ("Group 4 (Quad 4 Vert)", "A · D · E'", "#16A34A", "#F0FDF4", "m18, m22, m26, m30")
    ]
    
    for i, (gname, gterm, gcol, gbg, gcov) in enumerate(groups_info):
        gy = 7.8 - i * 1.65
        card = patches.FancyBboxPatch((lx - 0.2, gy - 0.4), 3.4, 1.4, boxstyle="round,pad=0.15",
                                      facecolor=gbg, edgecolor=gcol, linewidth=1.5, zorder=2)
        ax.add_patch(card)
        ax.text(lx, gy + 0.65, gname, color=gcol, fontsize=10.5, fontweight='bold')
        ax.text(lx, gy + 0.25, f"Term: {gterm}", color="#0F172A", fontsize=11.5, fontweight='bold')
        ax.text(lx, gy - 0.15, f"Covers: {gcov}", color="#475569", fontsize=8.5)

    # Bottom Formula Card
    ax.text(5.5, -0.65, "Minimal SOP:  F_SOP = C·E + A'·B'·D + A'·B·D' + A·D·E'",
            fontsize=13, fontweight='bold', ha='center', color="#1E40AF",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFFFFF", edgecolor="#1E40AF", linewidth=1.8))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "kmap_sop_diagram.png")
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# 3. 8x4 K-MAP DIAGRAM FOR MINIMAL POS (GROUPING 0s)
# ==============================================================================
def generate_kmap_pos():
    fig, ax = plt.subplots(figsize=(14, 11), dpi=DPI)
    ax.set_xlim(-1.5, 12.5)
    ax.set_ylim(-1.5, 11.5)
    ax.axis('off')

    ax.text(5.5, 10.9, "8x4 Karnaugh Map -- Minimal POS (Grouping 0s)",
            fontsize=16, fontweight='bold', ha='center', color="#0F172A")
    ax.text(5.5, 10.4, "5-Variable Logic Minimization: 14 Maxterms -> 6 Prime Implicants",
            fontsize=11.5, ha='center', color="#475569")

    gx0 = 2.4
    gy0 = 1.0
    cell_w = 1.6
    cell_h = 1.0

    row_labels = ["000", "001", "011", "010", "110", "111", "101", "100"]
    col_labels = ["00", "01", "11", "10"]

    ax.text(gx0 - 0.7, gy0 + 8.5 * cell_h, "ABC \\ DE", fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")
    for c, clab in enumerate(col_labels):
        ax.text(gx0 + (c + 0.5)*cell_w, gy0 + 8.3*cell_h, clab, fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")

    pos_maxterms = {0, 1, 4, 10, 11, 14, 16, 17, 19, 20, 24, 25, 27, 28}

    for r in range(8):
        y_top = gy0 + (7 - r) * cell_h
        rlab = row_labels[r]
        ax.text(gx0 - 0.7, y_top + 0.5*cell_h, rlab, fontsize=12, fontweight='bold', ha='center', va='center', color="#1E293B")

        for c in range(4):
            x_left = gx0 + c * cell_w
            r_val = int(rlab, 2)
            c_val = int(col_labels[c], 2)
            m_num = (r_val << 2) | c_val
            is_zero = m_num in pos_maxterms

            rect = patches.Rectangle((x_left, y_top), cell_w, cell_h,
                                     facecolor="#FEF2F2" if is_zero else "#F8FAFC",
                                     edgecolor="#94A3B8", linewidth=1.2, zorder=1)
            ax.add_patch(rect)

            ax.text(x_left + 0.15, y_top + cell_h - 0.18, f"M{m_num}", fontsize=8.5, color="#64748B", zorder=3)
            val_str = "0" if is_zero else "1"
            val_col = "#DC2626" if is_zero else "#94A3B8"
            ax.text(x_left + cell_w*0.5, y_top + cell_h*0.42, val_str,
                    fontsize=14.5, fontweight='bold', ha='center', va='center', color=val_col, zorder=3)

    # Group 1 (Quad 4 cells Vert): (A' + D + E)
    g1 = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.08, gy0 + 0*cell_h + 0.08), 1*cell_w - 0.16, 4*cell_h - 0.16,
                                boxstyle="round,pad=0.08", facecolor="#DC2626", alpha=0.20, edgecolor="#DC2626", linewidth=2.4, zorder=4)
    ax.add_patch(g1)

    # Group 2 (Quad 4 cells): (A' + C + E')
    g2a = patches.FancyBboxPatch((gx0 + 1*cell_w + 0.12, gy0 + 3*cell_h + 0.12), 2*cell_w - 0.24, 1*cell_h - 0.24,
                                 boxstyle="round,pad=0.08", facecolor="#2563EB", alpha=0.20, edgecolor="#2563EB", linewidth=2.2, zorder=4)
    ax.add_patch(g2a)
    g2b = patches.FancyBboxPatch((gx0 + 1*cell_w + 0.12, gy0 + 0*cell_h + 0.12), 2*cell_w - 0.24, 1*cell_h - 0.24,
                                 boxstyle="round,pad=0.08", facecolor="#2563EB", alpha=0.20, edgecolor="#2563EB", linewidth=2.2, zorder=4)
    ax.add_patch(g2b)

    # Group 3 (Quad 4 cells Wraparound): (B + D + E)
    g3a = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.14, gy0 + 6*cell_h + 0.14), 1*cell_w - 0.28, 2*cell_h - 0.28,
                                 boxstyle="round,pad=0.08", facecolor="#9333EA", alpha=0.18, edgecolor="#9333EA", linewidth=2.2, zorder=4)
    ax.add_patch(g3a)
    g3b = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.14, gy0 + 0*cell_h + 0.14), 1*cell_w - 0.28, 2*cell_h - 0.28,
                                 boxstyle="round,pad=0.08", facecolor="#9333EA", alpha=0.18, edgecolor="#9333EA", linewidth=2.2, zorder=4)
    ax.add_patch(g3b)

    # Group 4 (Quad 4 cells Wraparound): (B + C + D)
    g4a = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.16, gy0 + 7*cell_h + 0.16), 2*cell_w - 0.32, 1*cell_h - 0.32,
                                 boxstyle="round,pad=0.08", facecolor="#D97706", alpha=0.20, edgecolor="#D97706", linewidth=2.2, zorder=4)
    ax.add_patch(g4a)
    g4b = patches.FancyBboxPatch((gx0 + 0*cell_w + 0.16, gy0 + 0*cell_h + 0.16), 2*cell_w - 0.32, 1*cell_h - 0.32,
                                 boxstyle="round,pad=0.08", facecolor="#D97706", alpha=0.20, edgecolor="#D97706", linewidth=2.2, zorder=4)
    ax.add_patch(g4b)

    # Group 5 (Pair 2 cells): (A + B' + D' + E)
    g5 = patches.FancyBboxPatch((gx0 + 3*cell_w + 0.10, gy0 + 4*cell_h + 0.10), 1*cell_w - 0.20, 2*cell_h - 0.20,
                                boxstyle="round,pad=0.08", facecolor="#0D9488", alpha=0.22, edgecolor="#0D9488", linewidth=2.4, zorder=4)
    ax.add_patch(g5)

    # Group 6 (Pair 2 cells): (A + B' + C + D')
    g6 = patches.FancyBboxPatch((gx0 + 2*cell_w + 0.10, gy0 + 4*cell_h + 0.10), 2*cell_w - 0.20, 1*cell_h - 0.20,
                                boxstyle="round,pad=0.08", facecolor="#E11D48", alpha=0.22, edgecolor="#E11D48", linewidth=2.4, zorder=4)
    ax.add_patch(g6)

    lx = 9.4
    ax.text(lx + 1.4, 8.8, "POS Prime Implicants (6 Groups)", fontsize=13, fontweight='bold', color="#0F172A", ha='center')
    
    pos_groups_info = [
        ("Group 1 (Quad Vert)", "(A' + D + E)", "#DC2626", "#FEF2F2", "M16, M20, M24, M28"),
        ("Group 2 (Quad Wrap)", "(A' + C + E')", "#2563EB", "#EFF6FF", "M17, M19, M25, M27"),
        ("Group 3 (Quad Wrap)", "(B + D + E)", "#9333EA", "#F5F3FF", "M0, M4, M16, M20"),
        ("Group 4 (Quad Wrap)", "(B + C + D)", "#D97706", "#FFFBEB", "M0, M1, M16, M17"),
        ("Group 5 (Pair 2)", "(A + B' + D' + E)", "#0D9488", "#F0FDFA", "M10, M14"),
        ("Group 6 (Pair 2)", "(A + B' + C + D')", "#E11D48", "#FFF1F2", "M10, M11")
    ]
    
    for i, (gname, gterm, gcol, gbg, gcov) in enumerate(pos_groups_info):
        gy = 7.9 - i * 1.32
        card = patches.FancyBboxPatch((lx - 0.2, gy - 0.35), 3.4, 1.15, boxstyle="round,pad=0.10",
                                      facecolor=gbg, edgecolor=gcol, linewidth=1.4, zorder=2)
        ax.add_patch(card)
        ax.text(lx, gy + 0.48, gname, color=gcol, fontsize=9.5, fontweight='bold')
        ax.text(lx, gy + 0.12, f"Term: {gterm}", color="#0F172A", fontsize=10.5, fontweight='bold')
        ax.text(lx, gy - 0.22, f"Covers: {gcov}", color="#475569", fontsize=8.0)

    # Bottom Formula Card
    ax.text(5.5, -0.65, "Minimal POS:  F_POS = (A'+D+E)(A'+C+E')(B+D+E)(B+C+D)(A+B'+D'+E)(A+B'+C+D')",
            fontsize=11.0, fontweight='bold', ha='center', color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFFFFF", edgecolor="#DC2626", linewidth=1.8))

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "kmap_pos_diagram.png")
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# 4. MINIMAL SOP SYNTHESIZED CIRCUIT DIAGRAM (AND-OR Two-Level with Dedicated Rails)
# ==============================================================================
def generate_sop_circuit():
    fig, ax = plt.subplots(figsize=(20, 11), dpi=DPI)
    ax.set_xlim(-1.5, 23.5)
    ax.set_ylim(-1.0, 11.5)
    ax.axis('off')

    ax.text(11.0, 10.9, "Minimal SOP Logic Circuit — Two-Level AND-OR Synthesis",
            fontsize=16, fontweight='bold', ha='center', color="#0F172A")
    ax.text(11.0, 10.35, "F_SOP = C·E + A'·B'·D + A'·B·D' + A·D·E' (4 Product Terms → 1 Collector OR Gate)",
            fontsize=11.5, ha='center', color="#475569",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.2))

    # 9 Vertical Rails: A, A', B, B', C, D, D', E, E'
    rails_x = {
        'A': -0.2, "A'": 0.5,
        'B': 1.4,  "B'": 2.1,
        'C': 3.0,
        'D': 3.9,  "D'": 4.6,
        'E': 5.5,  "E'": 6.2
    }
    
    # Draw Inverters at top of inverted rails
    inv_configs = [
        ('A', "A'", 9.2, "#DC2626"),
        ('B', "B'", 9.2, "#2563EB"),
        ('D', "D'", 9.2, "#9333EA"),
        ('E', "E'", 9.2, "#D97706"),
    ]
    for var, inv_var, iy, col in inv_configs:
        tx = rails_x[var]
        ix = rails_x[inv_var]
        # Inverter pointing rightwards or tap
        # Draw tap from True rail, into inverter, and out down to Inv rail
        out_inv = draw_inverter(ax, tx + 0.1, iy, width=ix - tx - 0.28, height=0.45, label="NOT", color=col)
        ax.plot([tx, tx + 0.1], [iy, iy], color=col, linewidth=1.8, zorder=2)
        ax.plot(tx, iy, marker='o', markersize=5, color=col, zorder=4)
        ax.plot([out_inv[0], ix, ix], [iy, iy, 0.8], color=col, linewidth=2.0, linestyle='--', zorder=2)

    # Draw True Rails
    for var, col in [('A', '#DC2626'), ('B', '#2563EB'), ('C', '#16A34A'), ('D', '#9333EA'), ('E', '#D97706')]:
        x = rails_x[var]
        ax.plot([x, x], [0.8, 9.8], color=col, linewidth=2.2, zorder=2)
        ax.plot(x, 10.0, marker='o', markersize=8, color=col, zorder=5)
        ax.text(x, 10.25, var, color=col, fontsize=13, fontweight='bold', ha='center', va='bottom')

    # Draw Inv Rail Labels at top
    for inv_var, col in [("A'", '#DC2626'), ("B'", '#2563EB'), ("D'", '#9333EA'), ("E'", '#D97706')]:
        x = rails_x[inv_var]
        ax.text(x, 9.45, inv_var, color=col, fontsize=10.5, fontweight='bold', ha='center')

    # 4 AND Gates at Level 1 (x = 9.5)
    and_x = 9.5
    
    # 1. AND1: C · E (y = 7.5)
    out_and1 = draw_and_gate(ax, and_x, 7.5, width=1.5, height=1.0, label="AND1", color="#1E40AF")
    ax.plot([rails_x['C'], and_x], [7.75, 7.75], color=COLORS['C'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['C'], 7.75, marker='o', markersize=5, color=COLORS['C'], zorder=4)
    ax.plot([rails_x['E'], and_x], [7.25, 7.25], color=COLORS['E'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['E'], 7.25, marker='o', markersize=5, color=COLORS['E'], zorder=4)
    ax.text(out_and1[0] + 0.3, 7.85, "C · E", color="#1E40AF", fontsize=11, fontweight='bold', va='bottom')

    # 2. AND2: A' · B' · D (y = 5.5)
    out_and2 = draw_and_gate(ax, and_x, 5.5, width=1.5, height=1.1, label="AND2", color="#1E40AF")
    ax.plot([rails_x["A'"], and_x], [5.8, 5.8], color=COLORS['A'], linewidth=1.8, linestyle='--', zorder=2)
    ax.plot(rails_x["A'"], 5.8, marker='o', markersize=5, color=COLORS['A'], zorder=4)
    ax.plot([rails_x["B'"], and_x], [5.5, 5.5], color=COLORS['B'], linewidth=1.8, linestyle='--', zorder=2)
    ax.plot(rails_x["B'"], 5.5, marker='o', markersize=5, color=COLORS['B'], zorder=4)
    ax.plot([rails_x['D'], and_x], [5.2, 5.2], color=COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['D'], 5.2, marker='o', markersize=5, color=COLORS['D'], zorder=4)
    ax.text(out_and2[0] + 0.3, 5.85, "A' · B' · D", color="#1E40AF", fontsize=11, fontweight='bold', va='bottom')

    # 3. AND3: A' · B · D' (y = 3.5)
    out_and3 = draw_and_gate(ax, and_x, 3.5, width=1.5, height=1.1, label="AND3", color="#1E40AF")
    ax.plot([rails_x["A'"], and_x], [3.8, 3.8], color=COLORS['A'], linewidth=1.8, linestyle='--', zorder=2)
    ax.plot(rails_x["A'"], 3.8, marker='o', markersize=5, color=COLORS['A'], zorder=4)
    ax.plot([rails_x['B'], and_x], [3.5, 3.5], color=COLORS['B'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['B'], 3.5, marker='o', markersize=5, color=COLORS['B'], zorder=4)
    ax.plot([rails_x["D'"], and_x], [3.2, 3.2], color=COLORS['D'], linewidth=1.8, linestyle='--', zorder=2)
    ax.plot(rails_x["D'"], 3.2, marker='o', markersize=5, color=COLORS['D'], zorder=4)
    ax.text(out_and3[0] + 0.3, 3.85, "A' · B · D'", color="#1E40AF", fontsize=11, fontweight='bold', va='bottom')

    # 4. AND4: A · D · E' (y = 1.5)
    out_and4 = draw_and_gate(ax, and_x, 1.5, width=1.5, height=1.1, label="AND4", color="#1E40AF")
    ax.plot([rails_x['A'], and_x], [1.8, 1.8], color=COLORS['A'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['A'], 1.8, marker='o', markersize=5, color=COLORS['A'], zorder=4)
    ax.plot([rails_x['D'], and_x], [1.5, 1.5], color=COLORS['D'], linewidth=1.8, zorder=2)
    ax.plot(rails_x['D'], 1.5, marker='o', markersize=5, color=COLORS['D'], zorder=4)
    ax.plot([rails_x["E'"], and_x], [1.2, 1.2], color=COLORS['E'], linewidth=1.8, linestyle='--', zorder=2)
    ax.plot(rails_x["E'"], 1.2, marker='o', markersize=5, color=COLORS['E'], zorder=4)
    ax.text(out_and4[0] + 0.3, 1.85, "A · D · E'", color="#1E40AF", fontsize=11, fontweight='bold', va='bottom')

    # Final Collector OR Gate (x = 16.5, y = 4.5)
    out_or = draw_or_gate(ax, 16.5, 4.5, width=2.0, height=2.4, label="OR\nCollector", color="#047857", fill="#ECFDF5")
    
    # Exact Routing from AND outputs directly to OR inputs with underlap to ensure no gap
    ax.plot([out_and1[0], 15.0, 15.0, 16.8], [7.5, 7.5, 5.3, 5.3], color="#1E40AF", linewidth=1.8, zorder=2)
    ax.plot([out_and2[0], 15.2, 15.2, 16.8], [5.5, 5.5, 4.8, 4.8], color="#1E40AF", linewidth=1.8, zorder=2)
    ax.plot([out_and3[0], 15.2, 15.2, 16.8], [3.5, 3.5, 4.2, 4.2], color="#1E40AF", linewidth=1.8, zorder=2)
    ax.plot([out_and4[0], 15.0, 15.0, 16.8], [1.5, 1.5, 3.7, 3.7], color="#1E40AF", linewidth=1.8, zorder=2)

    # Final Output Terminal F_SOP
    ax.plot([out_or[0], 21.0], [4.5, 4.5], color="#0F172A", linewidth=2.4, zorder=2)
    ax.plot(21.0, 4.5, marker='o', markersize=9, color="#0F172A", zorder=5)
    ax.text(21.4, 4.5, "F_SOP", color="#0F172A", fontsize=16, fontweight='bold', va='center')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "sop_circuit_diagram.png")
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# 5. MINIMAL POS SYNTHESIZED CIRCUIT DIAGRAM (OR-AND Two-Level with Dedicated Rails)
# ==============================================================================
def generate_pos_circuit():
    fig, ax = plt.subplots(figsize=(20, 12), dpi=DPI)
    ax.set_xlim(-1.5, 23.5)
    ax.set_ylim(-1.0, 12.5)
    ax.axis('off')

    ax.text(11.0, 11.9, "Minimal POS Logic Circuit — Two-Level OR-AND Synthesis",
            fontsize=16, fontweight='bold', ha='center', color="#0F172A")
    ax.text(11.0, 11.35, "F_POS = (A'+D+E)(A'+C+E')(B+D+E)(B+C+D)(A+B'+D'+E)(A+B'+C+D') (6 Sum Terms → 1 Collector AND Gate)",
            fontsize=10.5, ha='center', color="#475569",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.2))

    # 9 Vertical Rails: A, A', B, B', C, D, D', E, E'
    rails_x = {
        'A': -0.2, "A'": 0.5,
        'B': 1.4,  "B'": 2.1,
        'C': 3.0,
        'D': 3.9,  "D'": 4.6,
        'E': 5.5,  "E'": 6.2
    }
    
    # Inverters at top
    inv_configs = [
        ('A', "A'", 10.3, "#DC2626"),
        ('B', "B'", 10.3, "#2563EB"),
        ('D', "D'", 10.3, "#9333EA"),
        ('E', "E'", 10.3, "#D97706"),
    ]
    for var, inv_var, iy, col in inv_configs:
        tx = rails_x[var]
        ix = rails_x[inv_var]
        out_inv = draw_inverter(ax, tx + 0.1, iy, width=ix - tx - 0.28, height=0.45, label="NOT", color=col)
        ax.plot([tx, tx + 0.1], [iy, iy], color=col, linewidth=1.8, zorder=2)
        ax.plot(tx, iy, marker='o', markersize=5, color=col, zorder=4)
        ax.plot([out_inv[0], ix, ix], [iy, iy, 0.6], color=col, linewidth=2.0, linestyle='--', zorder=2)

    for var, col in [('A', '#DC2626'), ('B', '#2563EB'), ('C', '#16A34A'), ('D', '#9333EA'), ('E', '#D97706')]:
        x = rails_x[var]
        ax.plot([x, x], [0.6, 10.8], color=col, linewidth=2.2, zorder=2)
        ax.plot(x, 11.0, marker='o', markersize=8, color=col, zorder=5)
        ax.text(x, 11.25, var, color=col, fontsize=13, fontweight='bold', ha='center', va='bottom')

    for inv_var, col in [("A'", '#DC2626'), ("B'", '#2563EB'), ("D'", '#9333EA'), ("E'", '#D97706')]:
        x = rails_x[inv_var]
        ax.text(x, 10.55, inv_var, color=col, fontsize=10.5, fontweight='bold', ha='center')

    # 6 OR Gates (y = 9.0, 7.4, 5.8, 4.2, 2.6, 1.0)
    or_x = 9.5
    
    pos_specs = [
        ("OR1", "(A' + D + E)", 9.0, [("A'", 9.25), ('D', 9.0), ('E', 8.75)]),
        ("OR2", "(A' + C + E')", 7.4, [("A'", 7.65), ('C', 7.4), ("E'", 7.15)]),
        ("OR3", "(B + D + E)", 5.8, [('B', 6.05), ('D', 5.8), ('E', 5.55)]),
        ("OR4", "(B + C + D)", 4.2, [('B', 4.45), ('C', 4.2), ('D', 3.95)]),
        ("OR5", "(A + B' + D' + E)", 2.6, [('A', 2.85), ("B'", 2.7), ("D'", 2.5), ('E', 2.35)]),
        ("OR6", "(A + B' + C + D')", 1.0, [('A', 1.25), ("B'", 1.1), ('C', 0.9), ("D'", 0.75)])
    ]

    out_ors = []
    for lbl, term, gy, inputs in pos_specs:
        out_g = draw_or_gate(ax, or_x, gy, width=1.5, height=1.0, label=lbl, color="#047857", fill="#ECFDF5")
        out_ors.append((out_g, gy, term))
        # Draw input taps
        for in_var, in_y in inputs:
            rx = rails_x[in_var]
            col = COLORS[in_var[0]]
            ls = '--' if "'" in in_var else '-'
            ax.plot([rx, or_x + 0.15], [in_y, in_y], color=col, linewidth=1.8, linestyle=ls, zorder=2)
            ax.plot(rx, in_y, marker='o', markersize=5, color=col, zorder=4)
        ax.text(out_g[0] + 0.3, gy + 0.32, term, color="#047857", fontsize=10, fontweight='bold', va='bottom')

    # Final Collector AND Gate (x = 16.5, y = 5.0)
    out_and = draw_and_gate(ax, 16.5, 5.0, width=2.2, height=3.2, label="AND\nCollector", color="#1E40AF", fill="#EFF6FF")

    # Symmetric Routing from 6 OR Gates to Collector AND Gate (fully continuous)
    and_in_ys = [6.2, 5.7, 5.2, 4.8, 4.3, 3.8]
    for (out_g, gy, term), in_y in zip(out_ors, and_in_ys):
        gx = out_g[0]
        ax.plot([gx, 15.2, 15.2, 16.5], [gy, gy, in_y, in_y], color="#047857", linewidth=1.8, zorder=2)

    # Output Terminal
    ax.plot([out_and[0], 21.0], [5.0, 5.0], color="#0F172A", linewidth=2.4, zorder=2)
    ax.plot(21.0, 5.0, marker='o', markersize=9, color="#0F172A", zorder=5)
    ax.text(21.4, 5.0, "F_POS", color="#0F172A", fontsize=16, fontweight='bold', va='center')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "pos_circuit_diagram.png")
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# 6. HARDWARE IC PINOUT LAYOUT DIAGRAM
# ==============================================================================
def generate_ic_pinout():
    fig, ax = plt.subplots(figsize=(18, 11), dpi=DPI)
    ax.set_xlim(-1.0, 21.0)
    ax.set_ylim(-1.0, 11.5)
    ax.axis('off')

    ax.text(10.0, 10.9, "Hardware Implementation Layout — Standard 74HC Series DIP-14 ICs",
            fontsize=16, fontweight='bold', ha='center', color="#0F172A")
    ax.text(10.0, 10.35, "All 7 Logic Families: 74HC04 (NOT), 74HC86 (XOR), 74HC7266 (XNOR), 74HC00 (NAND), 74HC08 (AND), 74HC02 (NOR), 74HC32 (OR)",
            fontsize=11.0, ha='center', color="#475569")

    # Draw 7 DIP-14 Packages
    ic_configs = [
        ("U1: 74HC04", "Hex Inverter\n(A')", 1.0, 6.2, "#DC2626", "#FEF2F2"),
        ("U2: 74HC86", "Quad 2-In XOR\n(W₁ = B ⊕ D)", 6.0, 6.2, "#6D28D9", "#F5F3FF"),
        ("U3: 74HC7266", "Quad 2-In XNOR\n(W₂ = C ⊙ E)", 11.0, 6.2, "#0284C7", "#F0F9FF"),
        ("U4: 74HC00", "Quad 2-In NAND\n(W₃ = (A·D)')", 16.0, 6.2, "#0D9488", "#F0FDFA"),
        ("U5: 74HC08", "Quad 2-In AND\n(W₄, W₅)", 2.5, 1.2, "#1E40AF", "#EFF6FF"),
        ("U6: 74HC02", "Quad 2-In NOR\n(W₆ = A·D·E')", 8.5, 1.2, "#B45309", "#FFFBEB"),
        ("U7: 74HC32", "Quad 2-In OR\n(W₇, F)", 14.5, 1.2, "#047857", "#ECFDF5")
    ]

    for name, desc, x, y, col, bg in ic_configs:
        w, h = 3.6, 2.6
        # IC Body
        body = patches.Rectangle((x, y), w, h, facecolor="#1E293B", edgecolor="#0F172A", linewidth=2.0, zorder=2)
        ax.add_patch(body)
        
        # IC Notch (Top)
        notch = patches.Wedge((x + w/2, y + h), 0.22, 180, 360, facecolor="#334155", edgecolor="#0F172A", linewidth=1.5, zorder=3)
        ax.add_patch(notch)
        
        # IC Text
        ax.text(x + w/2, y + h*0.65, name, color="#FFFFFF", fontsize=11, fontweight='bold', ha='center', va='center', zorder=4)
        ax.text(x + w/2, y + h*0.32, desc, color="#94A3B8", fontsize=8.5, ha='center', va='center', zorder=4)

        # 7 Pins on Left (1-7) & 7 Pins on Right (14-8)
        pin_spacing = h / 8.0
        for p in range(7):
            py = y + h - (p + 1) * pin_spacing
            ax.plot([x - 0.35, x], [py, py], color="#94A3B8", linewidth=2.5, zorder=1)
            ax.text(x + 0.25, py, str(p + 1), color="#CBD5E1", fontsize=7.5, va='center', ha='left', zorder=4)
            ax.plot([x + w, x + w + 0.35], [py, py], color="#94A3B8", linewidth=2.5, zorder=1)
            ax.text(x + w - 0.25, py, str(14 - p), color="#CBD5E1", fontsize=7.5, va='center', ha='right', zorder=4)

        # Power Tags: Pin 14 = VCC, Pin 7 = GND
        ax.text(x + w + 0.45, y + h - pin_spacing, "+5V (VCC)", color="#DC2626", fontsize=7.5, fontweight='bold', va='center')
        ax.text(x - 0.45, y + pin_spacing, "GND", color="#1E293B", fontsize=7.5, fontweight='bold', va='center', ha='right')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "ic_pinout_layout.png")
    plt.savefig(out_path, dpi=DPI, bbox_inches='tight', facecolor=COLOR_BG)
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    print("Regenerating all 6 diagrams for Exam 2569 Problem 03...")
    generate_original_circuit()
    generate_kmap_sop()
    generate_kmap_pos()
    generate_sop_circuit()
    generate_pos_circuit()
    generate_ic_pinout()
    print("✅ All 6 diagrams successfully regenerated!")
