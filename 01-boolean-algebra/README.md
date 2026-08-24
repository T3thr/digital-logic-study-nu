# 📐 01 - Boolean Algebra & Minimization (พีชคณิตบูลีนและการลดรูป)

บทเรียนสรุปทฤษฎีพีชคณิตบูลีน (Boolean Algebra), กฎพื้นฐาน, รูปแบบมาตรฐาน **SOP (Sum of Products)**, **POS (Product of Sums)** และการลดรูปด้วย **Karnaugh Map (K-Map)** สำหรับวิชาวงจรดิจิทัล

---

## 📑 สารบัญบทเรียน

1. [กฎพื้นฐานของพีชคณิตบูลีน (Boolean Postulates & Theorems)](#1-กฎพื้นฐานของพีชคณิตบูลีน-boolean-postulates--theorems)
2. [SOP vs POS: ทฤษฎีและการประยุกต์ใช้งาน](#2-sop-vs-pos-ทฤษฎีและการประยุกต์ใช้งาน)
3. [หลักการอ่านและการจับกลุ่ม K-Map (K-Map Minimization Rules)](#3-หลักการอ่านและการจับกลุ่ม-k-map-k-map-minimization-rules)
4. [บทความเจาะลึกเฉพาะหัวข้อ (Deep Dives)](#4-บทความเจาะลึกเฉพาะหัวข้อ-deep-dives)
5. [ภาพไดอะแกรมประกอบบทเรียน (Visual Diagrams)](#5-ภาพไดอะแกรมประกอบบทเรียน-visual-diagrams)

---

## 1. กฎพื้นฐานของพีชคณิตบูลีน (Boolean Postulates & Theorems)

| ชื่อกฎ (Law Name) | รูปแบบ AND ($\cdot$) | รูปแบบ OR ($+$) | คำอธิบาย |
| :--- | :--- | :--- | :--- |
| **Identity Law** | $A \cdot 1 = A$ | $A + 0 = A$ | การคูณ 1 หรือบวก 0 จะได้ค่าเดิม |
| **Null / Domination Law** | $A \cdot 0 = 0$ | $A + 1 = 1$ | การคูณ 0 ได้ 0, บวก 1 ได้ 1 เสมอ |
| **Idempotence Law** | $A \cdot A = A$ | $A + A = A$ | ตัวแปรซ้ำตัวเดิม ยุบเหลือตัวเดียว |
| **Complement Law** | $A \cdot \bar{A} = 0$ | $A + \bar{A} = 1$ | ตัวแปรคูณตัวตรงข้ามได้ 0, บวกกันได้ 1 |
| **Double Inversion** | $\overline{\bar{A}} = A$ | - | ขีดบน 2 ชั้นหักล้างกัน |
| **Commutative Law** | $A \cdot B = B \cdot A$ | $A + B = B + A$ | สลับที่ได้ |
| **Associative Law** | $(A \cdot B) \cdot C = A \cdot (B \cdot C)$ | $(A + B) + C = A + (B + C)$ | จัดกลุ่มเปลี่ยนวงเล็บได้ |
| **Distributive Law** | $A \cdot (B + C) = (A \cdot B) + (A \cdot C)$ | $A + (B \cdot C) = (A + B) \cdot (A + C)$ | กระจายพจน์ได้ทั้ง AND และ OR |
| **Absorption Law** | $A \cdot (A + B) = A$ | $A + (A \cdot B) = A$ | การกลืนกลืนพจน์ย่อย |
| **De Morgan's Laws** | $\overline{A \cdot B} = \bar{A} + \bar{B}$ | $\overline{A + B} = \bar{A} \cdot \bar{B}$ | ผ่า Bar สลับเครื่องหมาย |

---

## 2. SOP vs POS: ทฤษฎีและการประยุกต์ใช้งาน

| ประเด็นเปรียบเทียบ | SOP (Sum of Products) | POS (Product of Sums) |
| :--- | :--- | :--- |
| **คำจำกัดความ** | ผลบวกของผลคูณ (AND terms บวกกันด้วย OR) | ผลคูณของผลบวก (OR terms คูณกันด้วย AND) |
| **มุมมองการวิเคราะห์** | สนใจเงื่อนไขที่เอาต์พุต **$Y = 1$** (ไฟติด) | สนใจเงื่อนไขที่เอาต์พุต **$Y = 0$** (ไฟดับ) |
| **หน่วยย่อยพื้นฐาน** | **Minterm ($m_i$)** | **Maxterm ($M_i$)** |
| **การแทนค่าตัวแปร** | $A=1 \rightarrow A, \quad A=0 \rightarrow \bar{A}$ | $A=0 \rightarrow A, \quad A=1 \rightarrow \bar{A}$ |
| **สัญลักษณ์ Canonical** | $\sum m(i_1, i_2, \dots)$ | $\prod M(j_1, j_2, \dots)$ |
| **โครงสร้างเกตมาตรฐาน** | Level 1: AND Gates $\rightarrow$ Level 2: OR Gate | Level 1: OR Gates $\rightarrow$ Level 2: AND Gate (หรือ NOR) |

---

## 3. หลักการอ่านและการจับกลุ่ม K-Map (K-Map Minimization Rules)

```
        CD   00    01    11    10
    AB    +-----+-----+-----+-----+
    00    |  m0 |  m1 |  m3 |  m2 |
          +-----+-----+-----+-----+
    01    |  m4 |  m5 |  m7 |  m6 |
          +-----+-----+-----+-----+
    11    | m12 | m13 | m15 | m14 |
          +-----+-----+-----+-----+
    10    |  m8 |  m9 | m11 | m10 |
          +-----+-----+-----+-----+
```

### กฎสำคัญในการวนกลุ่ม (Grouping Rules):
1. **ขนาดของกลุ่มต้องเป็นเลขยกกำลังสอง ($2^n$):** ได้แก่ $1, 2, 4, 8, 16, 32$ เซลล์ (ห้ามจับกลุ่ม 3 หรือ 6 ตัว)
2. **จับกลุ่มให้มีขนาดใหญ่ที่สุดเท่าที่เป็นไปได้:** ยิ่งกลุ่มใหญ่ ตัวแปรในพจน์ยิ่งลดลงมาก
3. **การม้วนขอบ (Wrap-around):** เซลล์ขอบซ้าย-ขวา และขอบบน-ล่างถือว่าเป็นเซลล์ติดกันตามลำดับ Grey Code
4. **กลุ่มต้องซ้อนทับกันได้ (Overlapping):** สามารถแชร์เซลล์ร่วมกับกลุ่มอื่นได้เพื่อขยายขนาดกลุ่มให้ใหญ่ขึ้น
5. **ห้ามมีกลุ่มที่เป็น Redundant:** ถ้าทุกเซลล์ในกลุ่มถูกครอบคลุมโดยกลุ่มอื่นหมดแล้ว กลุ่มนั้นจะถือว่าเกินและต้องตัดทิ้ง

---

## 4. บทความเจาะลึกเฉพาะหัวข้อ (Deep Dives)

- 🔍 [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](why_sop_1_pos_0.md) : อธิบายฟิสิกส์เบื้องหลัง Minterm vs Maxterm และการทำงานของ Logic Gate ในระดับวงจร
- 📜 [กฎของ De Morgan และข้อพิสูจน์ $\bar{A} \cdot \bar{B} \neq \overline{A \cdot B}$](demorgan_laws.md) : พิสูจน์ด้วยตารางความจริง และเทคนิคผ่า Bar สลับเครื่องหมาย

---

## 5. ภาพไดอะแกรมประกอบบทเรียน (Visual Diagrams)

| ภาพประกอบ | รายละเอียด |
| :--- | :--- |
| ![SOP K-Map](assets/kmap_sop_diagram.png) | **SOP 4x4 K-Map:** การจับกลุ่มเลข 1 แบบ Wrap-around |
| ![POS K-Map](assets/kmap_pos_diagram.png) | **POS 4x4 K-Map:** การจับกลุ่มเลข 0 สำหรับ Maxterm |
| ![SOP Circuit](assets/sop_circuit_diagram.png) | **SOP Logic Circuit:** วงจรโครงสร้าง AND-OR |
| ![POS Circuit](assets/pos_circuit_diagram.png) | **POS Logic Circuit:** วงจรโครงสร้าง NOR Logic |
| ![SOP vs POS](assets/sop_pos_comparison.png) | **SOP vs POS Infographic:** เปรียบเทียบฮาร์ดแวร์และโครงสร้าง |

---

## 📁 สรุปรายการไฟล์ในโฟลเดอร์นี้

```
01-boolean-algebra/
├── README.md                              # เอกสารสรุปบทเรียนหน้านี้
├── why_sop_1_pos_0.md                     # เจาะลึกทำไม SOP วง 1 และ POS วง 0
├── demorgan_laws.md                       # เจาะลึกกฎของเดอมอร์แกนและการแจกแจงนิเสธ
├── scripts/
│   └── generate_boolean_diagrams.py       # สคริปต์สร้างไดอะแกรม K-Map และวงจร
└── assets/
    ├── kmap_sop_diagram.png
    ├── kmap_pos_diagram.png
    ├── sop_circuit_diagram.png
    ├── pos_circuit_diagram.png
    └── sop_pos_comparison.png
```
