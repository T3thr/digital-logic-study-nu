# ⏱️ บทที่ 7 : วงจรนับ (Counters)

เอกสารสรุปเนื้อหาทฤษฎี วงจรนับแบบอะซิงโครนัส วงจรนับแบบซิงโครนัส วงจรนับขึ้น/ลง วงจรนับมอดุโล-N และไอซีวงจรนับมาตรฐาน ประจำบทที่ 7 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 202 – 234)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **7.1-7.3** | [วงจรนับแบบอะซิงโครนัส](01-asynchronous-counters/) | Asynchronous Counters (Ripple Counters & Modulo-N) | [`01-asynchronous-counters/`](01-asynchronous-counters/) |
| **7.4** | [วงจรนับแบบซิงโครนัส](02-synchronous-counters/) | Synchronous Counters (Up/Down & Design with K-Map) | [`02-synchronous-counters/`](02-synchronous-counters/) |
| **7.5** | [ไอซีวงจรนับและการประยุกต์](03-ic-counters/) | IC Counters (7490, 7493, 74190, 74193) & Applications | [`03-ic-counters/`](03-ic-counters/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 7](exercises/) | Chapter 7 Solved Exercises | [`exercises/`](exercises/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 7.1-7.3 วงจรนับแบบอะซิงโครนัส (Asynchronous / Ripple Counters)
* **การทำงาน:** เอาต์พุต `Q` ของฟลิปฟล็อปตัวก่อนหน้า จะถูกต่อเป็น **สัญญาณ Clock** ให้กับฟลิปฟล็อปตัวถัดไป
* **ข้อดี:** วงจรง่าย ไม่ซับซ้อน ใช้จำนวนเกตน้อย
* **ข้อเสีย:** เกิดเวลาหน่วงสะสม (Propagation Delay Accumulation) สัญญาณกระเพื่อม (Ripple) ทำให้ความถี่สูงสุดในการทำงานจำกัด และอาจเกิด Glitch ในช่วงเปลี่ยนผ่าน
* **Modulo (MOD):** จำนวนสถานะทั้งหมดที่ตัวนับสามารถนับได้ เช่น Flip-Flop `n` ตัว สามารถนับได้สูงสุด `MOD = 2ⁿ`
  * การตัดทอนรอบนับ (Truncated Sequence): ใช้วงจรตรวจจับค่าสูงสุด (เช่น NAND Gate) แล้วป้อนกลับไปยังขา `CLR'` ของทุก Flip-Flop

### 7.4 วงจรนับแบบซิงโครนัส (Synchronous Counters)
* **การทำงาน:** ฟลิปฟล็อปทุกตัวได้รับสัญญาณ **Clock จากแหล่งเดียวกันพร้อมกัน (Common Clock)**
* **ข้อดี:** ไม่มีปัญหาเวลาหน่วงสะสม สามารถทำงานที่ความถี่สูงได้แม่นยำมาก
* **ขั้นตอนการออกแบบวงจรนับซิงโครนัส:**
  1. กำหนดไดอะแกรมแสดงสถานะ (State Diagram) และตารางสถานะ (State Table)
  2. ใช้ตารางกระตุ้น (Excitation Table) ของ Flip-Flop ที่เลือกใช้ (J-K, D หรือ T)
  3. ลดรูปฟังก์ชันอินพุตของแต่ละ Flip-Flop โดยใช้ K-Map
  4. วาดวงจรลอจิกจริง

### 7.5 ไอซีวงจรนับมาตรฐาน (Integrated Circuit Counters)
* **7490:** Asynchronous Decade Counter (นับ 0 ถึง 9 แบบ BCD / MOD-10)
* **7493:** 4-Bit Binary Ripple Counter (MOD-16)
* **74190:** Synchronous Up/Down Decade Counter
* **74193:** Synchronous Up/Down 4-Bit Binary Counter (มีขา Clock แยกนับขึ้น `CP_U` และนับลง `CP_D`)

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [06-latches-flip-flops/](../06-latches-flip-flops/README.md)
- ➡️ ไปยังบทถัดไป: [08-registers/](../08-registers/README.md)
