# 🔢 บทที่ 1 : ระบบจำนวน (Number Systems)

เอกสารสรุปเนื้อหาทฤษฎี หลักการคำนวณ และแบบฝึกหัดประจำบทที่ 1 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 1 – 25)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **1.1** | [ระบบจำนวน](01-number-representation/) | Number Systems & Positional Notation | [`01-number-representation/`](01-number-representation/) |
| **1.2** | [การแปลงผันระบบจำนวน](02-base-conversion/) | Number Base Conversions | [`02-base-conversion/`](02-base-conversion/) |
| **1.3** | [รหัสฐานสอง](03-binary-codes/) | Binary Codes (BCD, Gray, Excess-3, ASCII) | [`03-binary-codes/`](03-binary-codes/) |
| **1.4** | [กระบวนการคำนวณทางคณิตศาสตร์](04-binary-arithmetic/) | Binary Arithmetic Operations (+, -, ×, ÷) | [`04-binary-arithmetic/`](04-binary-arithmetic/) |
| **1.5** | [จำนวนฐานสองแบบมีเครื่องหมาย](05-signed-numbers/) | Signed Binary Numbers (Sign-Mag, 1's & 2's Comp) | [`05-signed-numbers/`](05-signed-numbers/) |
| **1.6** | [การบวกและการลบจำนวนแบบมีเครื่องหมาย](06-signed-arithmetic/) | Signed Addition, Subtraction & Overflow | [`06-signed-arithmetic/`](06-signed-arithmetic/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 1](exercises/) | Chapter 1 Solved Exercises | [`exercises/`](exercises/) |
| **Exam v1** | [ข้อสอบลูกโซ่ 12 ขั้นตอน](exam/version1/) | 12-Step Chained Multi-Step Exam | [`exam/version1/`](exam/version1/) |
| **Exam v2** | [แบบทดสอบและคู่มือติวเข้ม 15 ข้อ](exam/version2/) | 15 Core Direct Questions & Study Guide | [`exam/version2/`](exam/version2/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 1.1 ระบบจำนวน (Number Systems)
* ระบบจำนวนในวงจรดิจิทัลเป็นระบบตัวเลขแบบ **ตำแหน่งและค่าน้ำหนัก (Positional Weighting System)**:
  * ฐานสิบ (Decimal, Base-10): เลขโดด 0 ถึง 9, น้ำหนักคือ `10ⁱ`
  * ฐานสอง (Binary, Base-2): เลขโดด 0 และ 1, น้ำหนักคือ `2ⁱ`
  * ฐานแปด (Octal, Base-8): เลขโดด 0 ถึง 7, น้ำหนักคือ `8ⁱ`
  * ฐานสิบหก (Hexadecimal, Base-16): เลขโดด 0 ถึง 9 และตัวอักษร A ถึง F (`A=10, B=11, C=12, D=13, E=14, F=15`), น้ำหนักคือ `16ⁱ`
* คำศัพท์บิตที่สำคัญ:
  * **MSB (Most Significant Bit)**: บิตที่มีค่าน้ำหนักสูงสุด (ซ้ายสุด)
  * **LSB (Least Significant Bit)**: บิตที่มีค่าน้ำหนักต่ำสุด (ขวาสุด)

### 1.2 การแปลงผันระบบจำนวน (Base Conversions)
* **ฐานใดๆ → ฐานสิบ:** กระจายผลรวมของ `(เลขโดด × ฐานⁱ)`
* **ฐานสิบ → ฐานใดๆ:**
  * ส่วนจำนวนเต็ม: ใช้วิธีหารสั้นด้วยฐานปลายทาง เก็บเศษเรียงจากล่างขึ้นบน (LSB → MSB)
  * ส่วนทศนิยม: ใช้วิธีคูณด้วยฐานปลายทาง ดึงจำนวนเต็มหน้าจุดเรียงจากบนลงล่าง
* **การแปลงระหว่าง ฐานสอง ↔ ฐานแปด ↔ ฐานสิบหก:**
  * ฐาน 2 ↔ ฐาน 8 : จัดกลุ่มบิตละ **3 บิต** (เพราะ 2³ = 8)
  * ฐาน 2 ↔ ฐาน 16 : จัดกลุ่มบิตละ **4 บิต** (เพราะ 2⁴ = 16)

### 1.3 รหัสฐานสอง (Binary Codes)
* **BCD (Binary-Coded Decimal / 8421 Code):** แทนเลขฐานสิบแต่ละหลักด้วยเลขฐานสอง 4 บิต (0000 ถึง 1001) ค่าตั้งแต่ 1010 ถึง 1111 เป็น Invalid BCD
* **Gray Code (รหัสเกรย์ / Unit-Distance Code):** แต่ละค่าที่เรียงติดกันจะเปลี่ยนสถานะบิตเพียง **1 บิตเท่านั้น** ช่วยลด Glitch ในการเปลี่ยนสถานะของเซนเซอร์และตัวนับ
  * Binary → Gray: `G[n] = B[n]`, `G[i] = B[i+1] ⊕ B[i]`
  * Gray → Binary: `B[n] = G[n]`, `B[i] = B[i+1] ⊕ G[i]`
* **Excess-3 Code:** BCD + 3 (บวก 0011₂ เข้าไปในแต่ละหลักของ BCD) มีคุณสมบัติ Self-Complementing
* **ASCII Code:** รหัสมาตรฐาน 7 บิต (หรือ 8 บิต Extended) สำหรับแทนตัวอักษร อักขระพิเศษ และคำสั่งควบคุม

### 1.4 กระบวนการคำนวณทางคณิตศาสตร์ (Binary Arithmetic)
* **การบวกฐานสอง:**
  ```text
  0 + 0 = 0
  0 + 1 = 1
  1 + 0 = 1
  1 + 1 = 0  (ตัวทด Carry = 1)
  1 + 1 + 1 = 1 (ตัวทด Carry = 1)
  ```
* **การคูณฐานสอง:** ใช้หลักการ Shift and Add เหมือนการคูณเลขฐานสิบ

### 1.5 จำนวนฐานสองแบบมีเครื่องหมาย (Signed Numbers)
* ในระบบคอมพิวเตอร์และดิจิทัล มี 3 รูปแบบหลัก (บิตซ้ายสุดเป็น Sign bit: `0 = บวก`, `1 = ลบ`):
  1. **Sign-Magnitude:** บิตแรกบอกเครื่องหมาย บิตที่เหลือบอกขนาด (มี 0 สองค่าคือ +0 และ -0)
  2. **1's Complement (ส่วนเติมเต็มหนึ่ง):** จำนวนลบเกิดจากการกลับบิตทุกบิต (Invert: 0 ↔ 1)
  3. **2's Complement (ส่วนเติมเต็มสอง):** นำ 1's Complement มาบวกด้วย 1
     ```text
     2's Complement = (1's Complement) + 1
     ```
  * เทคนิคเร็วในการหา 2's Complement: ไล่บิตจากขวาสุดไปซ้ายสุด คงบิตไว้จนกระทั่งเจอ `1` ตัวแรก หลังจากนั้นให้สลับบิตทั้งหมด (Invert)

### 1.6 การบวกและการลบจำนวนแบบมีเครื่องหมาย (Signed Arithmetic & Overflow)
* การลบเลข `A - B` ในระบบดิจิทัล ทำได้โดยการบวก `A + (2's complement of B)`
* หากมีตัวทดล้นออกจากบิต MSB ในระบบ 2's Complement ให้ **ตัดทิ้ง (Discard carry)**
* **สภาวะเลขล้น (Overflow):** เกิดขึ้นเมื่อบวกจำนวนเครื่องหมายเดียวกัน 2 จำนวนแล้วได้ผลลัพธ์เครื่องหมายตรงกันข้าม (เช่น บวก + บวก ได้ ลบ หรือ ลบ + ลบ ได้ บวก) ซึ่งทำให้คำตอบผิดพลาดเนื่องจากจำนวนบิตไม่เพียงพอ

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังหน้าหลัก: [README.md](../README.md)
- ➡️ ไปยังบทถัดไป: [02-logic-functions-combinational/](../02-logic-functions-combinational/README.md)
