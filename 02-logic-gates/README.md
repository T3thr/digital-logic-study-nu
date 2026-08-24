# 🚪 02 - Logic Gates & Circuit Minimization (เกตตรรกะและการลดรูปวงจร)

โฟลเดอร์รวบรวมทฤษฎีพื้นฐานของ Logic Gates ทุกประเภท และ **คลังตัวอย่างโจทย์แบบฝึกหัด (Solved Problem Sets)** พร้อมภาพถ่ายโจทย์ต้นฉบับ วงจรวาดใหม่ ตารางความจริง การลดรูปด้วยพีชคณิตบูลีน/K-Map และการวิเคราะห์เปรียบเทียบฮาร์ดแวร์

---

## 📑 สารบัญ

1. [ตารางสรุปคุณสมบัติของ Logic Gates มาตรฐาน](#1-ตารางสรุปคุณสมบัติของ-logic-gates-มาตรฐาน)
2. [คลังตัวอย่างโจทย์และการเฉลยละเอียด (Problem Sets)](#2-คลังตัวอย่างโจทย์และการเฉลยละเอียด-problem-sets)
3. [โครงสร้างการจัดเก็บไฟล์ (Directory Structure)](#3-โครงสร้างการจัดเก็บไฟล์-directory-structure)

---

## 1. ตารางสรุปคุณสมบัติของ Logic Gates มาตรฐาน

| ประตูตรรกะ (Gate) | สัญลักษณ์ทางคณิตศาสตร์ | สมการเอาต์พุต ($Y$) | พฤติกรรมการทำงาน |
| :--- | :--- | :--- | :--- |
| **NOT (Inverter)** | $\bar{A}$ หรือ $A'$ | $Y = \bar{A}$ | กลับค่าสัญญาณตรงข้าม ($0 \rightarrow 1, 1 \rightarrow 0$) |
| **AND** | $A \cdot B$ หรือ $AB$ | $Y = A \cdot B$ | เป็น `1` เฉพาะเมื่ออินพุต **ทุกตัวเป็น 1** |
| **OR** | $A + B$ | $Y = A + B$ | เป็น `1` เมื่อมีอินพุต **ตัวใดตัวหนึ่งเป็น 1** |
| **NAND** | $\overline{A \cdot B}$ | $Y = \overline{A \cdot B} = \bar{A} + \bar{B}$ | Universal Gate: ตรงข้ามกับ AND |
| **NOR** | $\overline{A + B}$ | $Y = \overline{A + B} = \bar{A} \cdot \bar{B}$ | Universal Gate: ตรงข้ามกับ OR |
| **XOR** | $A \oplus B$ | $Y = \bar{A}B + A\bar{B}$ | เป็น `1` เมื่ออินพุต **ต่างกัน** (Odd Parity) |
| **XNOR** | $A \odot B$ หรือ $\overline{A \oplus B}$ | $Y = AB + \bar{A}\bar{B}$ | เป็น `1` เมื่ออินพุต **เหมือนกัน** (Equivalence) |

---

## 2. คลังตัวอย่างโจทย์และการเฉลยละเอียด (Problem Sets)

### 📌 [ตัวอย่างที่ 1: การลดรูปวงจร 4 ตัวแปรแบบ NAND-NOR-AND](examples/01/README.md)
- **โจทย์:** วิเคราะห์วงจร $Y = \overline{(A \cdot B) \cdot (A + C)} \cdot \overline{\bar{B} + D}$
- **สมการลดรูป:** $Y = \bar{A} \cdot B \cdot \bar{D}$
- **จุดเด่น:** อินพุต $C$ เป็น Don't-Care (ไม่มีผลต่อเอาต์พุต), ลดจำนวนเกตจาก 6 ตัวเหลือเพียง 2-3 ตัว
- **ไฟล์โจทย์:** [`examples/01/image.png`](examples/01/image.png) | 📄 [อ่านเฉลยเต็ม](examples/01/README.md)

---

### 📌 [ตัวอย่างที่ 2: การลดรูปวงจร 4 ตัวแปรที่มี XOR Gate](examples/02/README.md)
- **โจทย์:** วิเคราะห์วงจร $Y = W_4 \oplus W_5 = \overline{(A+B)+AC} \oplus (AC\bar{D})$
- **สมการลดรูป SOP:** $Y_{\text{SOP}} = \bar{A}\bar{B} + AC\bar{D}$
- **สมการลดรูป POS:** $Y_{\text{POS}} = (A+\bar{B})(\bar{A}+C)(\bar{A}+\bar{D})$
- **จุดเด่น:** การกระจายและลดรูปสมการ XOR ร่วมกับกฎการกลืนกลืน (Absorption Law)
- **ไฟล์โจทย์:** [`examples/02/image.png`](examples/02/image.png) | 📄 [อ่านเฉลยเต็ม](examples/02/README.md)

---

### 📌 [ตัวอย่างที่ 3: การลดรูปสมการ 5 ตัวแปรด้วย K-Map 8x4](examples/03/README.md)
- **โจทย์:** สมการ 5 ตัวแปร $F = \bar{A}B + A\bar{C} + \bar{B}DE + C\bar{D}\bar{E}$
- **ตารางความจริง:** 32 กรณี ($2^5 = 32$)
- **K-Map Structure:** แนวตั้ง $ABC$ (8 แถว) x แนวนอน $DE$ (4 คอลัมน์)
- **สมการ POS:** $F = (A+B+C+D)(A+B+\bar{D}+E)(B+\bar{C}+D+\bar{E})(\bar{A}+\bar{C}+\bar{D}+E)(\bar{A}+\bar{B}+\bar{C}+\bar{E})$
- **จุดเด่น:** การจับกลุ่มขนาด $2^3 = 8$ เซลล์ และการวนขอบใน K-Map 5 ตัวแปร
- 📄 [อ่านเฉลยเต็ม](examples/03/README.md)

---

## 3. โครงสร้างการจัดเก็บไฟล์ (Directory Structure)

```
02-logic-gates/
├── README.md                              # สารบัญและภาพรวมของบท
└── examples/                              # คลังตัวอย่างโจทย์
    ├── 01/                                # ตัวอย่างโจทย์ที่ 1 (NAND/NOR/AND)
    │   ├── README.md                      # เฉลยละเอียด
    │   ├── image.png                      # ภาพถ่ายโจทย์ต้นฉบับ
    │   ├── generate_all_diagrams.py       # สคริปต์วาดรูป
    │   └── *.png                          # ไดอะแกรมวงจรและ K-Map
    ├── 02/                                # ตัวอย่างโจทย์ที่ 2 (XOR Logic)
    │   ├── README.md                      # เฉลยละเอียด
    │   ├── image.png                      # ภาพถ่ายโจทย์ต้นฉบับ
    │   ├── generate_all_diagrams.py       # สคริปต์วาดรูป
    │   └── *.png                          # ไดอะแกรมวงจรและ K-Map
    └── 03/                                # ตัวอย่างโจทย์ที่ 3 (5-Variable 8x4 K-Map)
        ├── README.md                      # เฉลยละเอียด
        ├── generate_all_diagrams.py       # สคริปต์วาดรูป
        └── *.png                          # ไดอะแกรมวงจรและ K-Map
```
