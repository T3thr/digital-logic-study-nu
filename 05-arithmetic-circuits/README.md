# ➕ บทที่ 5 : วงจรเลขคณิต (Arithmetic Circuits)

เอกสารสรุปเนื้อหาทฤษฎี วงจรบวก วงจรลบ วงจรบวก/ลบในตัว วงจรคูณ วงจรเปรียบเทียบ และการออกแบบ ALU ประจำบทที่ 5 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 145 – 175)

🌐 [เปิดหน้าเว็บบทที่ 5](index.html) · [เฉลยละเอียดข้อ 3 ท้ายบท พร้อมห้องทดลอง](exercises/3/solution.html)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **5.1-5.2** | [วงจรบวกเลขฐานสอง](01-adders/) | Binary Adders (Half Adder, Full Adder & 7483/74283) | [`01-adders/`](01-adders/) |
| **5.3-5.4** | [วงจรลบและวงจรบวก/ลบ](02-subtractors/) | Binary Subtractors & Adder/Subtractor Circuits | [`02-subtractors/`](02-subtractors/) |
| **5.5** | [วงจรตรวจจับสภาวะเลขล้น](03-overflow-detection/) | Overflow Detection Circuitry in 2's Complement | [`03-overflow-detection/`](03-overflow-detection/) |
| **5.6** | [วงจรคูณเลขฐานสอง](04-multipliers/) | Binary Multipliers & Array Multipliers | [`04-multipliers/`](04-multipliers/) |
| **5.7** | [วงจรเปรียบเทียบขนาด](05-comparators/) | Magnitude Comparators (7485: A>B, A=B, A<B) | [`05-comparators/`](05-comparators/) |
| **5.8** | [การออกแบบวงจรหลายฟังก์ชัน (ALU)](06-multifunction-alu/) | Arithmetic Logic Unit & Function Generators | [`06-multifunction-alu/`](06-multifunction-alu/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 5](exercises/) | Chapter 5 Solved Exercises | [`exercises/`](exercises/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 5.1-5.2 วงจรบวกเลขฐานสอง (Adders)
* **Half Adder (วงจรกึ่งบวก):** บวกเลข 2 บิต (`A, B`) ได้ผลบวก `Sum` และตัวทด `Carry Out`
  * `Sum = A ⊕ B`
  * `Cout = A · B`
* **Full Adder (วงจรบวกเต็ม):** บวกเลข 3 บิต (`A, B, Cin`)
  * `Sum = A ⊕ B ⊕ Cin`
  * `Cout = A·B + Cin·(A ⊕ B)` (สร้างได้จาก 2 Half Adders + 1 OR Gate)
* **Parallel Binary Adder (IC 7483 / 74283):** วงจรบวกเลขฐานสองขนาด 4 บิตแบบขนาน (มี Fast Carry Look-Ahead)

### 5.3-5.4 วงจรบวก/ลบเลขฐานสอง (Adder / Subtractor)
* ใช้ **XOR Gate** ต่อกับอินพุต `B` เพื่อทำหน้าที่เป็นสวิตช์ Invert แบบควบคุมได้ (Controlled Inverter):
  * เมื่อขาควบคุม `M = 0` : `B ⊕ 0 = B`, `Cin = 0` → วงจรทำหน้าที่เป็น **วงจรบวก (`A + B`)**
  * เมื่อขาควบคุม `M = 1` : `B ⊕ 1 = B'`, `Cin = 1` → วงจรทำหน้าที่เป็น **วงจรลบ (`A + B' + 1 = A - B`)** ด้วย 2's Complement

### 5.5 วงจรตรวจจับภาวะเลขล้น (Overflow Detection)
* ในระบบ 2's Complement สามารถตรวจจับ Overflow ได้ง่ายมากโดยนำตัวทดเข้าบิต MSB (`C_in_MSB`) มา XOR กับตัวทดออกจากบิต MSB (`C_out_MSB`):
  ```text
  Overflow = C_in_MSB ⊕ C_out_MSB
  ```

### 5.7 วงจรเปรียบเทียบขนาด (Magnitude Comparator)
* **IC 7485:** 4-Bit Magnitude Comparator เปรียบเทียบเลขฐานสองขนาด 4 บิต (`A` และ `B`) โดยให้เอาต์พุต 3 สถานะ: `A > B`, `A = B`, `A < B` พร้อมขยายการต่อพ่วงแบบ Cascading ได้

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [04-decoders-encoders/](../04-decoders-encoders/README.md)
- ➡️ ไปยังบทถัดไป: [06-latches-flip-flops/](../06-latches-flip-flops/README.md)
