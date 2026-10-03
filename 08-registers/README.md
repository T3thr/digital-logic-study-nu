# 💾 บทที่ 8 : รีจิสเตอร์ (Registers)

เอกสารสรุปเนื้อหาทฤษฎี รีจิสเตอร์เลื่อนข้อมูล (Shift Registers) ชนิดต่างๆ การวิเคราะห์สัญญาณเวลา และไอซีมาตรฐาน ประจำบทที่ 8 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 235 – 260)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **8.1-8.2** | [รีจิสเตอร์และการเลื่อนข้อมูล](01-shift-registers/) | Shift Register Operations (SISO, SIPO, PISO, PIPO) | [`01-shift-registers/`](01-shift-registers/) |
| **8.3** | [สัญญาณเวลาและรูปคลื่น](02-timing-waveforms/) | Timing Diagrams & Clock Waveforms Analysis | [`02-timing-waveforms/`](02-timing-waveforms/) |
| **8.4** | [ไอซีรีจิสเตอร์มาตรฐาน](03-ic-shift-registers/) | IC Shift Registers (74164, 74165, 74194) | [`03-ic-shift-registers/`](03-ic-shift-registers/) |
| **8.5** | [การประยุกต์ใช้งานรีจิสเตอร์](04-applications/) | Applications (Ring Counter, Johnson Counter, UART) | [`04-applications/`](04-applications/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 8](exercises/) | Chapter 8 Solved Exercises | [`exercises/`](exercises/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 8.1-8.2 การทำงานและการจำแนกประเภทรีจิสเตอร์ (Shift Register Types)
* **นิยาม:** อุปกรณ์หน่วยความจำชั่วคราวที่สร้างจากฟลิปฟล็อปหลายตัวต่อเรียงกัน ใช้สำหรับเก็บข้อมูลดิจิทัล `n` บิต หรือเลื่อนข้อมูล (Shift Left / Shift Right)
* **4 โหมดหลักของการส่งผ่านข้อมูล:**
  1. **SISO (Serial-In Serial-Out):** ป้อนข้อมูลเข้าทีละบิต และอ่านออกทีละบิต (ใช้หน่วงเวลาข้อมูล)
  2. **SIPO (Serial-In Parallel-Out):** ป้อนข้อมูลเข้าทีละบิต แต่อ่านออกพร้อมกันทุกบิต (แปลง Serial → Parallel)
  3. **PISO (Parallel-In Serial-Out):** โหลดข้อมูลเข้าพร้อมกันทุกบิต แล้วเลื่อนส่งออกทีละบิต (แปลง Parallel → Serial)
  4. **PIPO (Parallel-In Parallel-Out):** โหลดข้อมูลและอ่านข้อมูลพร้อมกันทุกบิต (ทำหน้าที่เป็น Buffer Storage)

### 8.4 ไอซีรีจิสเตอร์มาตรฐาน (Integrated Circuit Shift Registers)
* **74164:** 8-Bit Serial-In Parallel-Out (SIPO) Shift Register
* **74165:** 8-Bit Parallel-In Serial-Out (PISO) Shift Register
* **74194:** 4-Bit **Universal Shift Register** (มีความสามารถรอบด้าน: Hold, Shift Left, Shift Right และ Parallel Load ตามโหมดควบคุม `S₁ S₀`)

### 8.5 วงจรนับพิเศษจากรีจิสเตอร์ (Counter Applications)
* **Ring Counter (ตัวนับแบบวงแหวน):** นำเอาต์พุต `Q` ของบิตสุดท้ายต่อวนกลับมาเข้าอินพุตของบิตแรก (หากมี `n` ฟลิปฟล็อป จะมีสถานะ `MOD = n`)
* **Johnson Counter (Twisted-Ring Counter):** นำเอาต์พุตกลับด้าน `Q'` ของบิตสุดท้ายต่อวนกลับมาเข้าอินพุตของบิตแรก (หากมี `n` ฟลิปฟล็อป จะมีสถานะ `MOD = 2n`)

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [07-counters/](../07-counters/README.md)
- 🏠 กลับสู่หน้าหลัก: [README.md](../README.md)
