#!/usr/bin/env python3
"""
Verification Script for Exam 2569 Problem 03
100% Pure Python Truth Table, Minterms, Maxterms, SOP and POS Equivalence Verification
"""

def simulate_circuit(A, B, C, D, E):
    # Stage 1: Pre-Logic Gates (Strict Max 2-Input)
    notA = 1 - A            # 74HC04 (Hex Inverter: A')
    W1 = B ^ D              # 74HC86 (Quad 2-In XOR: B ⊕ D)
    W2 = 1 - (C ^ E)        # 74HC7266 (Quad 2-In XNOR: C ⊙ E)
    W3 = 1 - (A & D)        # 74HC00 (Quad 2-In NAND: (A · D)')
    
    # Stage 2: Product / Intermediate Terms
    W4 = notA & W1          # 74HC08 (Quad 2-In AND1: A' · W1 = A' · (B ⊕ D))
    W5 = W2 & C             # 74HC08 (Quad 2-In AND2: W2 · C = (C ⊙ E) · C = C · E)
    W6 = 1 - (W3 | E)       # 74HC02 (Quad 2-In NOR: (W3 + E)' = ((A · D)' + E)' = A · D · E')
    
    # Stage 3: Sub-Sum Stage
    W7 = W4 | W5            # 74HC32 (Quad 2-In OR1: W4 + W5 = A'·(B ⊕ D) + C·E)
    
    # Stage 4: Collector Output Stage
    F = W7 | W6             # 74HC32 (Quad 2-In OR2: W7 + W6 = A'·(B ⊕ D) + C·E + A·D·E')
    
    return notA, W1, W2, W3, W4, W5, W6, W7, F

def eval_minimal_sop(A, B, C, D, E):
    # F_SOP = C·E + A'·B'·D + A'·B·D' + A·D·E'
    term1 = C & E
    term2 = (1 - A) & (1 - B) & D
    term3 = (1 - A) & B & (1 - D)
    term4 = A & D & (1 - E)
    return term1 | term2 | term3 | term4

def eval_minimal_pos(A, B, C, D, E):
    # F_POS = (A' + D + E) · (A' + C + E') · (B + D + E) · (B + C + D) · (A + B' + D' + E) · (A + B' + C + D')
    max1 = (1 - A) | D | E
    max2 = (1 - A) | C | (1 - E)
    max3 = B | D | E
    max4 = B | C | D
    max5 = A | (1 - B) | (1 - D) | E
    max6 = A | (1 - B) | C | (1 - D)
    return max1 & max2 & max3 & max4 & max5 & max6

def main():
    print("=" * 80)
    print("305241 Digital Logic Design — Exam 2569 Problem 03 Verification")
    print("=" * 80)
    
    minterms = []
    maxterms = []
    
    print(f"{'m':<3} | {'A':<1} {'B':<1} {'C':<1} {'D':<1} {'E':<1} | {'A\'':<2} {'W₁':<2} {'W₂':<2} {'W₃':<2} | {'W₄':<2} {'W₅':<2} {'W₆':<2} | {'W₇':<2} | {'F_orig':<6} {'F_sop':<5} {'F_pos':<5} | Status")
    print("-" * 80)
    
    for m in range(32):
        A = (m >> 4) & 1
        B = (m >> 3) & 1
        C = (m >> 2) & 1
        D = (m >> 1) & 1
        E = m & 1
        
        notA, W1, W2, W3, W4, W5, W6, W7, F_orig = simulate_circuit(A, B, C, D, E)
        F_sop = eval_minimal_sop(A, B, C, D, E)
        F_pos = eval_minimal_pos(A, B, C, D, E)
        
        is_match = (F_orig == F_sop == F_pos)
        status_str = "✅ PASS" if is_match else "❌ FAIL"
        
        if F_orig == 1:
            minterms.append(m)
        else:
            maxterms.append(m)
            
        print(f"{m:<3} | {A:<1} {B:<1} {C:<1} {D:<1} {E:<1} | {notA:<2} {W1:<2} {W2:<2} {W3:<2} | {W4:<2} {W5:<2} {W6:<2} | {W7:<2} | {F_orig:<6} {F_sop:<5} {F_pos:<5} | {status_str}")
        assert is_match, f"Error at row {m}: orig={F_orig}, sop={F_sop}, pos={F_pos}"

    print("-" * 80)
    print(f"Total Minterms (F=1): {len(minterms)} cases -> {minterms}")
    print(f"Total Maxterms (F=0): {len(maxterms)} cases -> {maxterms}")
    print("\n✅ All 32 cases verified 100% equivalent across Original Circuit, Minimal SOP, and Minimal POS!")

if __name__ == "__main__":
    main()
