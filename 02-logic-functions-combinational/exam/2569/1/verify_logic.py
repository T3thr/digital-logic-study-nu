"""
Logic Verification Script for Chapter 2 Exam 2569 (Question 1)
Multi-Stage 5-Variable Combinational Logic Circuit (Strict Max 2-Input Gates)
"""

def original_circuit(A, B, C, D, E):
    nB = 1 - B
    nE = 1 - E
    
    # Stage 1: 2-Input Universal & Exclusive Gates
    W1 = D ^ E                         # 74HC86 (2-in XOR): D ⊕ E
    W2 = 1 - (A & C)                   # 74HC00 (2-in NAND): (A . C)' = A' + C'
    W3 = 1 - (B | D)                   # 74HC02 (2-in NOR): (B + D)' = B' . D'
    
    # Stage 2: 2-Input AND Gates
    W4 = A and nB                      # 74HC08 (2-in AND1): A . B'
    W5 = C and W2                      # 74HC08 (2-in AND2): C . (A . C)' = A' . C
    W6 = W3 and nE                     # 74HC08 (2-in AND3): (B + D)' . E' = B' . D' . E'
    W7 = B and W1                      # 74HC08 (2-in AND4): B . (D ⊕ E) = B . D' . E + B . D . E'
    
    # Stage 3: 2-Input OR Gates
    W8 = W4 or W5                      # 74HC32 (2-in OR1): A.B' + A'.C
    W9 = W6 or W7                      # 74HC32 (2-in OR2): B'.D'.E' + B.(D ⊕ E)
    
    # Stage 4: 2-Input Output OR Gate
    F = int(W8 or W9)
    return F, (W1, W2, W3, W4, W5, W6, W7, W8, W9)

def minimal_sop(A, B, C, D, E):
    # Minimal SOP: A'C + AB' + B'D'E' + BD'E + BDE'
    nA = 1 - A
    nB = 1 - B
    nD = 1 - D
    nE = 1 - E
    
    t1 = nA and C                      # A' . C (Octet 8 cells)
    t2 = A and nB                      # A . B' (Octet 8 cells)
    t3 = nB and nD and nE              # B' . D' . E' (Quad 4 cells - Wraparound)
    t4 = B and nD and E                # B . D' . E (Quad 4 cells)
    t5 = B and D and nE                # B . D . E' (Quad 4 cells)
    return int(t1 or t2 or t3 or t4 or t5)

def minimal_pos(A, B, C, D, E):
    # Minimal POS: (A+B+C+E')(A+B+C+D')(B'+C+D+E)(B'+C+D'+E')(A'+B'+D+E)(A'+B'+D'+E')
    nA = 1 - A
    nB = 1 - B
    nC = 1 - C
    nD = 1 - D
    nE = 1 - E
    
    p1 = A or B or C or nE             # (A + B + C + E')
    p2 = A or B or C or nD             # (A + B + C + D')
    p3 = nB or C or D or E             # (B' + C + D + E)
    p4 = nB or C or nD or nE           # (B' + C + D' + E')
    p5 = nA or nB or D or E            # (A' + B' + D + E)
    p6 = nA or nB or nD or nE          # (A' + B' + D' + E')
    return int(p1 and p2 and p3 and p4 and p5 and p6)

def run_verification():
    print("=" * 105)
    print(" 305241 DIGITAL LOGIC DESIGN - EXAM 2569 QUESTION 1 VERIFICATION")
    print(" Multi-Stage 5-Variable Combinational Circuit (Strict Max 2-Input Gates)")
    print("=" * 105)
    print(f"{'Idx':>3} | {'A':>1} {'B':>1} {'C':>1} {'D':>1} {'E':>1} | {'W1':>2} {'W2':>2} {'W3':>2} {'W4':>2} {'W5':>2} {'W6':>2} {'W7':>2} {'W8':>2} {'W9':>2} | {'F_orig':>6} {'F_SOP':>5} {'F_POS':>5} | {'Status':>6} | {'Term':>15}")
    print("-" * 105)
    
    minterms = []
    maxterms = []
    mismatch_sop = 0
    mismatch_pos = 0
    
    for m in range(32):
        A = (m >> 4) & 1
        B = (m >> 3) & 1
        C = (m >> 2) & 1
        D = (m >> 1) & 1
        E = m & 1
        
        f_orig, (w1, w2, w3, w4, w5, w6, w7, w8, w9) = original_circuit(A, B, C, D, E)
        f_sop = minimal_sop(A, B, C, D, E)
        f_pos = minimal_pos(A, B, C, D, E)
        
        match = (f_orig == f_sop == f_pos)
        if f_orig != f_sop: mismatch_sop += 1
        if f_orig != f_pos: mismatch_pos += 1
        
        if f_orig == 1:
            minterms.append(m)
            term_str = f"m{m} (1)"
        else:
            maxterms.append(m)
            term_str = f"M{m} (0)"
            
        status = "OK" if match else "FAIL"
        print(f"{m:3d} | {A:1d} {B:1d} {C:1d} {D:1d} {E:1d} | {w1:2d} {w2:2d} {w3:2d} {w4:2d} {w5:2d} {w6:2d} {w7:2d} {w8:2d} {w9:2d} | {f_orig:6d} {f_sop:5d} {f_pos:5d} | {status:>6} | {term_str:>15}")
        
    print("-" * 105)
    print(f"Total Minterms (F=1): {len(minterms)} cases -> {minterms}")
    print(f"Total Maxterms (F=0): {len(maxterms)} cases -> {maxterms}")
    print(f"SOP Mismatches: {mismatch_sop}")
    print(f"POS Mismatches: {mismatch_pos}")
    if mismatch_sop == 0 and mismatch_pos == 0:
        print(">> ALL 32 CASES VERIFIED WITH 100% MATHEMATICAL INTEGRITY <<")
    else:
        print(">> VERIFICATION FAILED! <<")
    print("=" * 105)

if __name__ == "__main__":
    run_verification()
