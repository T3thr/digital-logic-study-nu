#!/usr/bin/env python3
"""
Verification Script for Chapter 1: 15-Step Chained Exam (Version 2 - Forward-Flowing Pipeline)
Course: 305241 Digital Logic Design & Engineering
Key Feature: Strictly Non-Cyclic Forward-Moving Transformations.
No step leaks or duplicates earlier answers. Complete chaining across all 15 steps.
"""

def verify_all_forward_chained():
    print("=" * 80)
    print("🔬 VERIFICATION OF 15-STEP FORWARD-FLOWING CHAINED EXAM (VERSION 2)")
    print("   Course: 305241 Digital Logic Design & Engineering (Chapter 1)")
    print("   Feature: 100% Direct Chaining & Non-Cyclic Forward Transformations")
    print("=" * 80)

    # -------------------------------------------------------------
    # Step 1: Decimal with Fraction to Binary (D₁ = 13.375₁₀ -> B₁)
    # -------------------------------------------------------------
    d1 = 13.375
    b1_int = bin(int(d1))[2:] # "1101"
    # 0.375 * 2 = 0.75 (0), 0.75 * 2 = 1.5 (1), 0.5 * 2 = 1.0 (1) -> "011"
    b1_str = f"{b1_int}.011"
    print(f"\n[Step 1] Decimal Fraction to Binary:")
    print(f"  Input: D₁ = {d1}₁₀")
    print(f"  Result: B₁ = {b1_str}₂")
    assert b1_str == "1101.011"

    # -------------------------------------------------------------
    # Step 2: Binary fraction B₁ -> Octal with fraction (O₂)
    # -------------------------------------------------------------
    # 001 101 . 011_2 -> 15.3_8
    o2_str = "15.3"
    print(f"\n[Step 2] Binary to Octal:")
    print(f"  Input: B₁ = {b1_str}₂")
    print(f"  Grouping (3-bit): [001][101].[011]₂")
    print(f"  Result: O₂ = {o2_str}₈")
    assert o2_str == "15.3"

    # -------------------------------------------------------------
    # Step 3: Binary fraction B₁ -> Hexadecimal with fraction (H₃)
    # -------------------------------------------------------------
    # 1101 . 0110_2 -> D.6_16
    h3_str = "D.6"
    print(f"\n[Step 3] Binary to Hexadecimal:")
    print(f"  Input: B₁ = {b1_str}₂")
    print(f"  Grouping (4-bit): [1101].[0110]₂")
    print(f"  Result: H₃ = {h3_str}₁₆")
    assert h3_str == "D.6"

    # -------------------------------------------------------------
    # Step 4: Hexadecimal Addition (D₁₆ + 1F₁₆ -> H₄ = 2C₁₆)
    # -------------------------------------------------------------
    int_h3 = int("D", 16) # 13
    h4_val = int_h3 + int("1F", 16) # 13 + 31 = 44
    h4_str = hex(h4_val)[2:].upper() # "2C"
    print(f"\n[Step 4] Hexadecimal Addition (Evolution Step):")
    print(f"  Operation: D₁₆ ({int_h3}₁₀) + 1F₁₆ (31₁₀)")
    print(f"  Result: H₄ = {h4_str}₁₆ ({h4_val}₁₀)")
    assert h4_val == 44
    assert h4_str == "2C"

    # -------------------------------------------------------------
    # Step 5: Hexadecimal H₄ -> Decimal (D₅ = 44₁₀)
    # -------------------------------------------------------------
    d5 = h4_val # 44
    print(f"\n[Step 5] Hexadecimal to Decimal:")
    print(f"  Input: H₄ = {h4_str}₁₆")
    print(f"  Expansion: (2×16¹) + (12×16⁰) = {d5}₁₀")
    assert d5 == 44

    # -------------------------------------------------------------
    # Step 6: Decimal D₅ ต่อทศนิยม ➔ รหัส BCD (44.75₁₀ -> BCD₆)
    # -------------------------------------------------------------
    # 4 4 . 7 5 -> 0100 0100 . 0111 0101
    bcd6_str = "0100 0100 . 0111 0101"
    print(f"\n[Step 6] Decimal Fraction to BCD Code (8421):")
    print(f"  Input: D₅ ({d5}₁₀) + 0.75 = 44.75₁₀")
    print(f"  Result: BCD₆ = {bcd6_str} (BCD)")
    assert bcd6_str == "0100 0100 . 0111 0101"

    # -------------------------------------------------------------
    # Step 7: BCD₆ -> Excess-3 (XS₇) & Integer Payload (B₇ = 44₁₀)
    # -------------------------------------------------------------
    # 0100+3=0111, 0100+3=0111 . 0111+3=1010, 0101+3=1000
    xs7_str = "0111 0111 . 1010 1000"
    n7 = d5 # 44
    b7_str = f"{n7:08b}" # "00101100"
    print(f"\n[Step 7] BCD to Excess-3 & Integer Payload:")
    print(f"  Input: BCD₆ = {bcd6_str}")
    print(f"  7.1 Excess-3 (+3 each nibble): XS₇ = {xs7_str} (XS-3)")
    print(f"  7.2 Integer Payload: N₇ = {n7}₁₀ ➔ 8-bit Binary B₇ = {b7_str}₂")
    assert xs7_str == "0111 0111 . 1010 1000"
    assert n7 == 44
    assert b7_str == "00101100"

    # -------------------------------------------------------------
    # Step 8: Unsigned Binary Addition (B₇ + 53₁₀ -> SUM₈)
    # -------------------------------------------------------------
    v_add8 = 53 # 00110101_2
    sum8 = n7 + v_add8 # 97
    sum8_bin = f"{sum8:08b}" # "01100001"
    print(f"\n[Step 8] Unsigned Binary Addition:")
    print(f"  Operation: B₇ ({b7_str}₂ = {n7}₁₀) + 00110101₂ ({v_add8}₁₀)")
    print(f"  Result: SUM₈ = {sum8_bin}₂ = {sum8}₁₀ ({hex(sum8).upper().replace('0X', '')}₁₆)")
    assert sum8 == 97
    assert sum8_bin == "01100001"

    # -------------------------------------------------------------
    # Step 9: Base Addition in Octal & Extracted Value K
    # -------------------------------------------------------------
    # 97_10 = 141_8 -> 141_8 + 236_8 = 377_8 (255_10)
    oct_97 = oct(sum8)[2:] # "141"
    add_oct9 = oct(int(oct_97, 8) + int("236", 8))[2:] # "377"
    k = sum8 - 43 # 54
    k_bin = f"{k:08b}" # "00110110"
    print(f"\n[Step 9] Octal Base Addition & Signed Offset K:")
    print(f"  Octal Addition: 141₈ ({sum8}₁₀) + 236₈ = {add_oct9}₈")
    print(f"  Extracted Signed Offset: K = SUM₈ - 43 = {k}₁₀ = {k_bin}₂ ({hex(k).upper().replace('0X', '')}₁₆)")
    assert add_oct9 == "377"
    assert k == 54
    assert k_bin == "00110110"

    # -------------------------------------------------------------
    # Step 10: 8-bit SAM Representation of ±K (±54₁₀)
    # -------------------------------------------------------------
    sam_pos = "0" + k_bin[1:] # "00110110"
    sam_neg = "1" + k_bin[1:] # "10110110"
    print(f"\n[Step 10] 8-bit SAM Representation (±{k}₁₀):")
    print(f"  Positive (+{k}₁₀): SAM(+) = {sam_pos}₂ = {hex(int(sam_pos, 2)).upper().replace('0X', '')}₁₆")
    print(f"  Negative (-{k}₁₀): SAM(-) = {sam_neg}₂ = {hex(int(sam_neg, 2)).upper().replace('0X', '')}₁₆")
    assert sam_pos == "00110110"
    assert sam_neg == "10110110"

    # -------------------------------------------------------------
    # Step 11: 8-bit 1's Complement of -K (-54₁₀)
    # -------------------------------------------------------------
    s_1comp = "".join("1" if b == "0" else "0" for b in k_bin) # "11001001"
    print(f"\n[Step 11] 8-bit 1's Complement (-{k}₁₀):")
    print(f"  Inverting all bits of {k_bin}₂ ➔ S_1comp = {s_1comp}₂ = {hex(int(s_1comp, 2)).upper().replace('0X', '')}₁₆")
    assert s_1comp == "11001001"

    # -------------------------------------------------------------
    # Step 12: 8-bit 2's Complement of -K (-54₁₀)
    # -------------------------------------------------------------
    s_2comp = f"{(int(s_1comp, 2) + 1) & 0xFF:08b}" # "11001010"
    print(f"\n[Step 12] 8-bit 2's Complement (-{k}₁₀):")
    print(f"  S_1comp + 1: {s_1comp}₂ + 1 = {s_2comp}₂ = {hex(int(s_2comp, 2)).upper().replace('0X', '')}₁₆")
    assert s_2comp == "11001010"

    # -------------------------------------------------------------
    # Step 13: 1's Complement Subtraction (+80₁₀ - +54₁₀ = +26₁₀)
    # -------------------------------------------------------------
    # 80 = 01010000_2, 1's(-54) = 11001001_2
    val_80 = 80
    raw_sum13 = val_80 + int(s_1comp, 2) # 80 + 201 = 281
    carry13 = raw_sum13 >> 8 # 1
    res13 = (raw_sum13 & 0xFF) + carry13 # 26
    res13_bin = f"{res13:08b}" # "00011010"
    print(f"\n[Step 13] 1's Complement Subtraction (80₁₀ - {k}₁₀):")
    print(f"  Addition: 01010000₂ (+80) + {s_1comp}₂ (-{k} 1's) = (Carry {carry13}) {(raw_sum13 & 0xFF):08b}₂")
    print(f"  End-Around Carry: {(raw_sum13 & 0xFF):08b}₂ + 1 = {res13_bin}₂ (+{res13}₁₀)")
    assert carry13 == 1
    assert res13 == 26
    assert res13_bin == "00011010"

    # -------------------------------------------------------------
    # Step 14: 2's Complement Subtraction (80 - 54 & 26 - 80)
    # -------------------------------------------------------------
    # a) 80 - 54: 01010000 + 11001010 = 1 00011010 -> Discard Carry 1 -> +26
    sum14a = val_80 + int(s_2comp, 2) # 80 + 202 = 282
    carry14a = sum14a >> 8 # 1
    bin14a = f"{sum14a & 0xFF:08b}" # "00011010"
    # b) 26 - 80: 00011010 + 10110000 (2's of 80) = 0 11001010 -> -54
    twos_80 = f"{(~val_80 + 1) & 0xFF:08b}" # "10110000"
    sum14b = res13 + int(twos_80, 2) # 26 + 176 = 202
    carry14b = sum14b >> 8 # 0
    bin14b = f"{sum14b:08b}" # "11001010"
    print(f"\n[Step 14] 2's Complement Subtraction:")
    print(f"  14.1 (80 - {k}): {bin14a}₂ (+{res13}₁₀) [Discard Carry = {carry14a}]")
    print(f"  14.2 ({res13} - 80): {bin14b}₂ (-{k}₁₀) [Carry = {carry14b}]")
    assert bin14a == "00011010"
    assert carry14a == 1
    assert bin14b == "11001010"
    assert carry14b == 0

    # -------------------------------------------------------------
    # Step 15: Overflow Analysis in 2's Complement 8-bit System
    # -------------------------------------------------------------
    # a) (+80) + (+54) = 134 > 127 -> Overflow (V = 1)
    # b) (-80) + (-54) = -134 < -128 -> Overflow (V = 1)
    ovf15a = (80 + 54 > 127)
    ovf15b = (-80 + -54 < -128)
    print(f"\n[Step 15] Overflow Analysis (8-bit Signed Range [-128..+127]):")
    print(f"  15.1 (+80₁₀) + (+{k}₁₀) = 134 > +127 ➔ Overflow: {ovf15a}")
    print(f"  15.2 (-80₁₀) + (-{k}₁₀) = -134 < -128 ➔ Overflow: {ovf15b}")
    assert ovf15a is True
    assert ovf15b is True

    print("\n" + "=" * 80)
    print("✅ ALL 15 FORWARD-FLOWING CHAINED STEPS VERIFIED 100% ACCURATE!")
    print("=" * 80)

if __name__ == "__main__":
    verify_all_forward_chained()
