#!/usr/bin/env python3
"""
305241 Digital Logic Design — Exam 2569 (Problem 02 Verification Suite)
4-Stage Combinational Network with Strict Max 2-Input Gates
IC Family: 74HC04 (NOT), 74HC86 (XOR), 74HC00 (NAND), 74HC02 (NOR), 74HC08 (AND), 74HC32 (OR)
"""

def solve_circuit(A, B, C, D, E):
    # Inverters (74HC04)
    not_A = 1 if not A else 0
    not_D = 1 if not D else 0
    not_E = 1 if not E else 0
    not_B = 1 if not B else 0
    not_C = 1 if not C else 0
    
    # Stage 1: Pre-Logic 2-Input Gates
    W1 = B ^ D                    # 74HC86 Quad 2-Input XOR: B'·D + B·D'
    W2 = 1 if not (A and C) else 0 # 74HC00 Quad 2-Input NAND: A' + C'
    W3 = 1 if not (B or E) else 0  # 74HC02 Quad 2-Input NOR: B' · E'
    
    # Stage 2: Product Term 2-Input Gates (74HC08 Quad 2-Input AND)
    W4 = W1 & not_A                # AND1: A' · (B ⊕ D) = A'·B'·D + A'·B·D'
    W5 = C & W2                    # AND2: C · (A·C)' = A' · C
    W6 = W3 & not_D                # AND3: (B+E)' · D' = B' · D' · E'
    W7 = A & D                     # AND4: A · D
    
    # Stage 3: Sub-Sum 2-Input Gates (74HC32 Quad 2-Input OR)
    W8 = W4 | W5                   # OR1: A'·(B ⊕ D) + A'·C
    W9 = W6 | W7                   # OR2: B'·D'·E' + A·D
    
    # Stage 4: Collector 2-Input Gate (74HC32 Quad 2-Input OR)
    F = W8 | W9                    # OR3: W8 + W9
    
    return {
        'W1': W1, 'W2': W2, 'W3': W3,
        'W4': W4, 'W5': W5, 'W6': W6, 'W7': W7,
        'W8': W8, 'W9': W9, 'F': F
    }

def solve_sop_minimal(A, B, C, D, E):
    not_A = 1 if not A else 0
    not_B = 1 if not B else 0
    not_D = 1 if not D else 0
    not_E = 1 if not E else 0
    
    # F_SOP = A·D + A'·C + B'·D + B'·E' + A'·B·D'
    t1 = A and D
    t2 = not_A and C
    t3 = not_B and D
    t4 = not_B and not_E
    t5 = not_A and B and not_D
    return 1 if (t1 or t2 or t3 or t4 or t5) else 0

def solve_pos_minimal(A, B, C, D, E):
    not_A = 1 if not A else 0
    not_B = 1 if not B else 0
    not_C = 1 if not C else 0
    not_D = 1 if not D else 0
    not_E = 1 if not E else 0
    
    # F_POS = (A' + B' + D) · (A' + D + E') · (A + B' + C + D') · (B + C + D + E')
    term1 = not_A or not_B or D
    term2 = not_A or D or not_E
    term3 = A or not_B or C or not_D
    term4 = B or C or D or not_E
    return 1 if (term1 and term2 and term3 and term4) else 0

def main():
    print("=" * 85)
    print("305241 Digital Logic Design — Exam 2569 (Problem 02 Full Verification)")
    print("=" * 85)
    print(f"{'Idx':>3} | {'A':^1} {'B':^1} {'C':^1} {'D':^1} {'E':^1} | "
          f"{'W1':^3} {'W2':^3} {'W3':^3} {'W4':^3} {'W5':^3} {'W6':^3} {'W7':^3} {'W8':^3} {'W9':^3} | "
          f"{'F_orig':^6} {'F_sop':^5} {'F_pos':^5} | {'Term':<12}")
    print("-" * 85)
    
    minterms = []
    maxterms = []
    
    for m in range(32):
        A = (m >> 4) & 1
        B = (m >> 3) & 1
        C = (m >> 2) & 1
        D = (m >> 1) & 1
        E = (m >> 0) & 1
        
        res = solve_circuit(A, B, C, D, E)
        f_sop = solve_sop_minimal(A, B, C, D, E)
        f_pos = solve_pos_minimal(A, B, C, D, E)
        
        assert res['F'] == f_sop == f_pos, f"Logic mismatch at minterm m_{m}!"
        
        if res['F'] == 1:
            minterms.append(m)
            term_str = f"m{m} (1)"
        else:
            maxterms.append(m)
            term_str = f"M{m} (0)"
            
        print(f"{m:3d} | {A} {B} {C} {D} {E} | "
              f"{res['W1']:3d} {res['W2']:3d} {res['W3']:3d} {res['W4']:3d} {res['W5']:3d} {res['W6']:3d} {res['W7']:3d} {res['W8']:3d} {res['W9']:3d} | "
              f"{res['F']:^6d} {f_sop:^5d} {f_pos:^5d} | {term_str:<12}")

    print("-" * 85)
    print(f"Total Minterms (F = 1): {len(minterms)} cases -> {minterms}")
    print(f"Total Maxterms (F = 0): {len(maxterms)} cases -> {maxterms}")
    print("\n✅ All 32/32 cases passed 100% equivalence!")

if __name__ == "__main__":
    main()
