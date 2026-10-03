# ⚡ บทที่ 2 : ฟังก์ชันลอจิกและวงจรลอจิกผสม (Logic Functions & Combinational Logic Circuits)

เอกสารสรุปเนื้อหาทฤษฎี เกตตรรกศาสตร์ พีชคณิตบูลีน การแปลง SOP/POS แผนผังคาร์โน (K-Map) และคลังเฉลยโจทย์วิเคราะห์วงจร ประจำบทที่ 2 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 26 – 78)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **2.1** | [ลอจิกเกต](01-logic-gates/) | Logic Gates (AND, OR, NOT, NAND, NOR, XOR, XNOR) | [`01-logic-gates/`](01-logic-gates/) |
| **2.2-2.3** | [วงจรลอจิกผสมและการแปลงสมการ](02-combinational-circuits/) | Combinational Circuits & Expression Implementation | [`02-combinational-circuits/`](02-combinational-circuits/) |
| **2.4** | [พีชคณิตบูลีนและทฤษฎีบท](03-boolean-algebra/) | Boolean Algebra Laws, Theorems & De Morgan | [`03-boolean-algebra/`](03-boolean-algebra/) |
| **2.5** | [รูปแบบมาตรฐาน SOP และ POS](04-standard-forms/) | Standard Forms: Sum of Products vs Product of Sums | [`04-standard-forms/`](04-standard-forms/) |
| **2.6** | [วงจรเกตสมมูล](05-equivalent-circuits/) | Equivalent Gate Circuits (Universal NAND/NOR Logic) | [`05-equivalent-circuits/`](05-equivalent-circuits/) |
| **2.7** | [แผนผังคาร์โน (K-Map)](06-karnaugh-map/) | Karnaugh Mapping & Minimization | [`06-karnaugh-map/`](06-karnaugh-map/) |
| **KB** | [คลังองค์ความรู้และเทคนิคขั้นสูง (5-Var K-Map)](knowledge/) | Advanced Knowledge Hub & 5-Variable K-Map Guide | [`knowledge/`](knowledge/) |
| **Ex** | [คลังเฉลยตัวอย่างโจทย์และการลดรูป](exercises/) | Solved Combinational Logic Problems | [`exercises/`](exercises/) |
| **Exam** | [คลังข้อสอบและแบบฝึกหัด 2569](exam/2569/) | Exam Archive 2569 (K-Map 8x4 Web UI) | [`exam/2569/`](exam/2569/) |

---

## 🏆 คลังตัวอย่างโจทย์และการลดรูปวงจร (Solved Problem Sets)

| รหัสโจทย์ | ภาพโจทย์ต้นฉบับ | สมการโจทย์ต้นฉบับ | สมการลดรูป (Minimal Form) | เทคนิคเด่น | ลิงก์เฉลยละเอียด |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Ex 01** | [`image.png`](exercises/01/image.png) | `Y = ((A·B)(A+C))' · ((B)' + D)'` | **SOP:** `Y = A'·B·D'`<br>**POS:** `Y = (A + B' + D)'` | • `C` เป็น Don't-care input<br>• ลดจาก 6 เกตเหลือ 2-3 เกต | [📖 อ่านเฉลย Ex 01](exercises/01/README.md) |
| **Ex 02** | [`image.png`](exercises/02/image.png) | `Y = ((A+B)+AC)' ⊕ (A·C·D')` | **SOP:** `Y = A'·B' + A·C·D'`<br>**POS:** `Y = (A+B')(A'+C)(A'+D')` | • การกระจาย XOR ร่วมกับ Absorption<br>• K-Map 4x4 จับกลุ่ม Quad & Pair | [📖 อ่านเฉลย Ex 02](exercises/02/README.md) |
| **Ex 03** | - | `F = A'·B + A·C' + B'·D·E + C·D'·E'` | **SOP:** `F = A'·B + A·C' + B'·D·E + C·D'·E'`<br>**POS:** 5 Maxterm factors | • K-Map 5 ตัวแปร (8 แถว × 4 คอลัมน์)<br>• ตารางความจริง 32 กรณี | [📖 อ่านเฉลย Ex 03](exercises/03/README.md) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 2.1 ลอจิกเกต (Logic Gates)
* **เกตพื้นฐาน:** AND (`A · B`), OR (`A + B`), NOT (`A'`)
* **เกตสากล (Universal Gates):** NAND (`(A·B)'`), NOR (`(A+B)'`) สามารถนำมาต่อประกอบแทนเกตทุกชนิดในวงจรดิจิทัลได้
* **เกตทางคณิตศาสตร์:** XOR (`A ⊕ B = A'·B + A·B'`), XNOR (`(A ⊕ B)' = A·B + A'·B'`)

### 2.4 พีชคณิตบูลีนและกฎของเดอมอร์แกน (Boolean Algebra & De Morgan's Laws)
* **เอกลักษณ์พื้นฐาน:**
  * `A + 0 = A`, `A + 1 = 1`, `A · 0 = 0`, `A · 1 = A`
  * `A + A = A`, `A · A = A`, `A + A' = 1`, `A · A' = 0`
  * `(A')' = A`
* **กฎการดูดซับ (Absorption Law):** `A + A·B = A`, `A + A'·B = A + B`
* **กฎของเดอมอร์แกน (De Morgan's Theorems):**
  1. `(A · B)' = A' + B'` (ผ่า Bar ผลคูณ กลายเป็นผลบวกของ Bar เดี่ยว)
  2. `(A + B)' = A' · B'` (ผ่า Bar ผลบวก กลายเป็นผลคูณของ Bar เดี่ยว)
  * อ่านบทความเจาะลึก: [กฎของ De Morgan และข้อพิสูจน์](03-boolean-algebra/demorgan_laws.md)

### 2.5 รูปแบบมาตรฐาน SOP และ POS
* **SOP (Sum of Products):** ผลบวกของผลคูณ (`Y = A'·B + A·C`) เหมาะกับวงจร AND-OR (จับตาดูสถานะที่เป็น `1`)
* **POS (Product of Sums):** ผลคูณของผลบวก (`Y = (A+B')(A'+C)`) เหมาะกับวงจร OR-AND (กรองสถานะที่เป็น `0`)
* อ่านบทความเจาะลึก: [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](04-standard-forms/why_sop_1_pos_0.md)

### 2.7 แผนผังคาร์โน (K-Map)
* แผนผังจัดเรียงรหัส Gray Code ทำให้ช่องติดกันต่างกันเพียง 1 บิต
* การจับกลุ่มต้องเป็นขนาด `2ⁿ` (1, 2, 4, 8, 16 ช่อง) ยิ่งกลุ่มใหญ่ ตัวแปรยิ่งลดลงมาก
* สามารถรวมขอบซ้าย-ขวา ขอบบน-ล่าง และมุมทั้ง 4 เข้าด้วยกันได้ (Toroidal Adjacency)
* สามารถใช้สภาวะ **Don't Care (`X`)** ร่วมจับกลุ่มเป็น `1` หรือ `0` เพื่อให้ได้กลุ่มที่ใหญ่ที่สุด

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [01-number-systems/](../01-number-systems/README.md)
- ➡️ ไปยังบทถัดไป: [03-multiplexers-demultiplexers/](../03-multiplexers-demultiplexers/README.md)
