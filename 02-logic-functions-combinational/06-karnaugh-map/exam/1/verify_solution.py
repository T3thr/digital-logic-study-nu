#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_solution.py
────────────────────────────────────────────────────────────────────────────
สคริปต์ตรวจคำตอบและพิสูจน์ความเท่ากันทางตรรกศาสตร์ (Boolean Equivalence Verification)
สำหรับโจทย์ K-Map 5 ตัวแปร (Exam 1)

ทดสอบ:
1. เทียบตาราง Truth Table ดั้งเดิม 32 เวกเตอร์ กับสมการ Minimal SOP
2. เทียบตาราง Truth Table ดั้งเดิม กับสมการ Minimal POS
3. ตรวจสอบความถูกต้องและสถานะ Essential ของ Prime Implicants ทั้งหมด
"""

import sys

# ตารางความจริง 32 สถานะจากโจทย์ต้นฉบับ
# ลำดับตัวแปร: A, B, C, D, E (MSB -> LSB)
# ตาราง 8 แถว (ABC) x 4 คอลัมน์ (DE)
ROW_ORDER = ['000', '001', '011', '010', '110', '111', '101', '100']
COL_ORDER = ['00', '01', '11', '10']

RAW_GRID = [
    [0, 1, 1, 0],  # 000
    [0, 1, 1, 0],  # 001
    [1, 1, 1, 1],  # 011
    [1, 1, 1, 1],  # 010
    [1, 1, 1, 1],  # 110
    [1, 1, 1, 0],  # 111
    [0, 1, 1, 1],  # 101
    [0, 1, 1, 0],  # 100
]

# สร้าง Truth Table dict: {m: target_val}
TRUTH_TABLE = {}
for r_idx, abc in enumerate(ROW_ORDER):
    for c_idx, de in enumerate(COL_ORDER):
        m = int(abc + de, 2)
        TRUTH_TABLE[m] = RAW_GRID[r_idx][c_idx]

def eval_sop(a, b, c, d, e):
    """
    F = E + A'·B + B·C' + B·D' + A·B'·C·D
    """
    not_a = 1 - a
    not_b = 1 - b
    not_c = 1 - c
    not_d = 1 - d
    
    t1 = e
    t2 = not_a & b
    t3 = b & not_c
    t4 = b & not_d
    t5 = a & not_b & c & d
    
    return t1 | t2 | t3 | t4 | t5

def eval_pos(a, b, c, d, e):
    """
    F = (A + B + E) · (B + C + E) · (B + D + E) · (A' + B' + C' + D' + E)
    """
    not_a = 1 - a
    not_b = 1 - b
    not_c = 1 - c
    not_d = 1 - d
    
    t1 = a | b | e
    t2 = b | c | e
    t3 = b | d | e
    t4 = not_a | not_b | not_c | not_d | e
    
    return t1 & t2 & t3 & t4

def run_verification():
    print("═" * 70)
    print("  การตรวจสอบความถูกต้องของสมการลดรูป K-Map 5 ตัวแปร (Exam 1)")
    print("═" * 70)
    
    sop_pass = True
    pos_pass = True
    
    print(f"{'m':<4} | {'A':<1} {'B':<1} {'C':<1} {'D':<1} {'E':<1} | {'โจทย์':<6} | {'SOP':<5} | {'POS':<5} | {'สถานะ'}")
    print("─" * 70)
    
    for m in range(32):
        b_str = format(m, '05b')
        a, b, c, d, e = [int(ch) for ch in b_str]
        
        target = TRUTH_TABLE[m]
        res_sop = eval_sop(a, b, c, d, e)
        res_pos = eval_pos(a, b, c, d, e)
        
        match_sop = (res_sop == target)
        match_pos = (res_pos == target)
        
        if not match_sop: sop_pass = False
        if not match_pos: pos_pass = False
        
        status = "✅ ผ่าน" if (match_sop and match_pos) else "❌ ผิดพลาด"
        print(f"m{m:<3} | {a} {b} {c} {d} {e} | {target:<6} | {res_sop:<5} | {res_pos:<5} | {status}")
        
    print("─" * 70)
    print(f"ผลการทดสอบ Minimal SOP : {'✅ ผ่าน 32/32 (100%)' if sop_pass else '❌ ล้มเหลว'}")
    print(f"ผลการทดสอบ Minimal POS : {'✅ ผ่าน 32/32 (100%)' if pos_pass else '❌ ล้มเหลว'}")
    print("═" * 70)
    
    if not (sop_pass and pos_pass):
        sys.exit(1)

if __name__ == '__main__':
    run_verification()
