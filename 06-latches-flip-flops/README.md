# 🔄 บทที่ 6 : แลตช์และฟลิปฟล็อป (Latches and Flip-Flops)

เอกสารสรุปเนื้อหาทฤษฎี วงจรตรรกะแบบลำดับ (Sequential Logic) แลตช์ ฟลิปฟล็อปชนิดต่างๆ สัญญาณ Clock ขอบขาขึ้น/ลง และขาสัญญาณ Asynchronous ประจำบทที่ 6 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 176 – 201)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **6.1-6.5** | [แลตช์](01-latches/) | Latches (S-R Latch, D-Latch, Preset & Clear) | [`01-latches/`](01-latches/) |
| **6.6-6.10** | [ฟลิปฟล็อป](02-flip-flops/) | Flip-Flops (D, S-R, J-K, Master-Slave, 7474, 7476) | [`02-flip-flops/`](02-flip-flops/) |
| **6.11** | [การประยุกต์ใช้งานฟลิปฟล็อป](03-applications/) | Flip-Flop Applications (Storage, Frequency Divider) | [`03-applications/`](03-applications/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 6](exercises/) | Chapter 6 Solved Exercises | [`exercises/`](exercises/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 6.1-6.5 วงจรแลตช์ (Latches)
* **Combinational vs Sequential:**
  * Combinational Logic: เอาต์พุตขึ้นอยู่กับอินพุตปัจจุบันเท่านั้น (ไม่มีความจำ)
  * Sequential Logic: เอาต์พุตขึ้นอยู่กับทั้งอินพุตปัจจุบันและ **สถานะในอดีต (Memory/State)**
* **S-R Latch (Set-Reset Latch):** สร้างจาก NOR หรือ NAND เกตต่อแบบ Cross-Coupled Feedback
  * `S=1, R=0` → Set (`Q=1, Q'=0`)
  * `S=0, R=1` → Reset (`Q=0, Q'=1`)
  * `S=0, R=0` → Hold / No Change (คงสถานะเดิม)
  * `S=1, R=1` → Invalid / Prohibited State (ห้ามใช้)
* **D-Latch (Delay / Transparent Latch):** ป้องกันสภาวะห้ามใช้โดยใช้อินพุต `D` ตัวเดียว ร่วมกับขาเปิดใช้งาน `Enable (E)`

### 6.6-6.10 วงจรฟลิปฟล็อป (Flip-Flops)
* **ความแตกต่างระหว่าง Latch กับ Flip-Flop:**
  * Latch ทำงานตาม **ระดับสัญญาณ (Level-Triggered)**
  * Flip-Flop ทำงานตาม **ขอบสัญญาณนาฬิกา (Edge-Triggered)** เช่น ขอบขาขึ้น (Positive Edge: `↑`) หรือขอบขาลง (Negative Edge: `↓`)
* **ประเภทของ Flip-Flop:**
  1. **D Flip-Flop (Data FF):** ถ่ายโอนค่า `D` ไปยัง `Q` เมื่อเกิดขอบ Clock (`Q_next = D`) ใช้มากที่สุดใน Register
  2. **J-K Flip-Flop:** แก้ปัญหาสภาวะห้ามใช้ของ S-R โดยเมื่อ `J=1, K=1` จะเกิดสถานะ **Toggle (`Q_next = Q'`)** สลับค่าทุกรอบ Clock
  3. **T Flip-Flop (Toggle FF):** นำขา `J` และ `K` ต่อรวมกัน ทำหน้าที่สลับสถานะ (ใช้สร้างวงจรหารความถี่และตัวนับ)
* **ไอซีมาตรฐาน:**
  * **7474:** Dual D-Type Positive-Edge-Triggered Flip-Flops with Preset & Clear
  * **7476:** Dual J-K Flip-Flops with Preset & Clear
* **Asynchronous Inputs (Preset & Clear):**
  * ขา `PRE'` และ `CLR'` ทำงานทันทีโดย **ไม่ต้องรอสัญญาณ Clock (Overriding Inputs)**

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [05-arithmetic-circuits/](../05-arithmetic-circuits/README.md)
- ➡️ ไปยังบทถัดไป: [07-counters/](../07-counters/README.md)
