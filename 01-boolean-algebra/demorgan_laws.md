# 📜 บทเรียน: NOT A · NOT B เท่ากับ NOT(A · B) หรือไม่? (De Morgan's Laws)

เอกสารเฉลยคำถามและอธิบายความแตกต่างระหว่าง $\bar{A} \cdot \bar{B}$ กับ $\overline{A \cdot B}$ ด้วยตารางความจริง และกฎของ De Morgan

---

## ❌ คำตอบสั้น: "ไม่เท่ากัน!"

$$\bar{A} \cdot \bar{B} \neq \overline{A \cdot B}$$

- **$\bar{A} \cdot \bar{B}$ (NOT A AND NOT B):** เท่ากับ **$\overline{A + B}$** (NOR Gate)
- **$\overline{A \cdot B}$ (NOT of A AND B):** เท่ากับ **$\bar{A} + \bar{B}$** (NAND Gate)

---

## 📊 1. พิสูจน์ด้วยตารางความจริง (Truth Table Proof)

| $A$ | $B$ | $\bar{A}$ | $\bar{B}$ | **$\bar{A} \cdot \bar{B}$** <br> (NOT A $\cdot$ NOT B) | $A \cdot B$ | **$\overline{A \cdot B}$** <br> (NAND Gate) | **$\bar{A} + \bar{B}$** <br> (De Morgan) | **$\overline{A + B}$** <br> (NOR Gate) |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **0** | **0** | 1 | 1 | **1** | 0 | **1** | 1 | **1** |
| **0** | **1** | 1 | 0 | **0** ❌ | 0 | **1** ❌ | 1 | **0** |
| **1** | **0** | 0 | 1 | **0** ❌ | 0 | **1** ❌ | 1 | **0** |
| **1** | **1** | 0 | 0 | **0** | 1 | **0** | 0 | **0** |

### ข้อสังเกตความแตกต่าง:
- **แถวที่ 2 ($A=0, B=1$):** $\bar{A} \cdot \bar{B} = \mathbf{0}$ แต่ $\overline{A \cdot B} = \mathbf{1}$
- **แถวที่ 3 ($A=1, B=0$):** $\bar{A} \cdot \bar{B} = \mathbf{0}$ แต่ $\overline{A \cdot B} = \mathbf{1}$
- จะเห็นได้ชัดเจนว่า $\bar{A} \cdot \bar{B}$ มีค่าเท่ากับ **$\overline{A + B}$ (NOR Gate)** ไม่ใช่ $\overline{A \cdot B}$ (NAND Gate)

---

## 💡 2. ความหมายในเชิงตรรกศาสตร์ (Intuitive Meaning)

### 1. $\bar{A} \cdot \bar{B}$ (NOT A AND NOT B)
- **ความหมาย:** *"ต้องไม่ใช่ทั้ง A และไม่ใช่ทั้ง B พร้อมกันทั้งคู่"*
- **เงื่อนไขติดไฟ (เป็น 1):** เกิดขึ้นกรณีเดียวเท่านั้น คือ **$A=0$ และ $B=0$**
- **เปรียบเทียบ:** สวิตช์ A ต้องปิด และ สวิตช์ B ต้องปิด ทั้งสองตัวพร้อมกัน!

### 2. $\overline{A \cdot B}$ (NOT (A AND B) / NAND)
- **ความหมาย:** *"ห้ามเปิดสวิตช์พร้อมกันทั้งคู่ (ห้ามเป็น $A=1$ และ $B=1$ พร้อมกัน)"*
- **เงื่อนไขติดไฟ (เป็น 1):** เกิดขึ้นได้ถึง **3 กรณี** ขอแค่ไม่เปิดสวิตช์คู่กัน!
- **เปรียบเทียบ:** เบรกเกอร์ตัดไฟเมื่อมีการเปิดเครื่องใช้ไฟฟ้า A และ B พร้อมกัน ถ้าเปิดแค่ตัวเดียวหรือปิดทั้งคู่ ไฟจะยังทำงานปกติ!

---

## 📜 3. กฎของ De Morgan (De Morgan's Laws)

เดอมอร์แกน (Augustus De Morgan) ได้สรุปกฎสำคัญ 2 ข้อในการแจกแจงเครื่องหมาย NOT (Bar):

### กฎข้อที่ 1: การแจกแจงนิเสธของผลคูณ (NAND Law)
$$\overline{A \cdot B} = \bar{A} + \bar{B}$$
*(NOT ของ AND เท่ากับ NOT A **OR** NOT B)*

### กฎข้อที่ 2: การแจกแจงนิเสธของผลบวก (NOR Law)
$$\overline{A + B} = \bar{A} \cdot \bar{B}$$
*(NOT ของ OR เท่ากับ NOT A **AND** NOT B)*

---

## 🧠 4. เทคนิคการจำแบบรวดเร็ว (Rule of Thumb)

> **สูตรผ่า Bar ยาว (Break the bar, change the sign):**
> 1. เมื่อต้องการตัด Bar ยาวออกจากกัน ให้ผ่า Bar ตรงกลาง
> 2. **เปลี่ยนเครื่องหมาย:**
>    - จากคูณ ($\cdot$) $\rightarrow$ เปลี่ยนเป็น บวก ($+$)
>    - จากบวก ($+$) $\rightarrow$ เปลี่ยนเป็น คูณ ($\cdot$)
> 3. ใส่ Bar สั้นลงบนตัวแปรแต่ละตัว
>
> **ตัวอย่าง:**
> - $\overline{A \cdot B} \xrightarrow{\text{ผ่า Bar}} \bar{A} + \bar{B}$
> - $\overline{A + B} \xrightarrow{\text{ผ่า Bar}} \bar{A} \cdot \bar{B}$

---

## 🔗 เอกสารที่เกี่ยวข้อง
- 📖 [หน้าหลัก Boolean Algebra](README.md)
- 🔍 [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](why_sop_1_pos_0.md)
