# 📟 บทที่ 4 : วงจรถอดรหัสและวงจรเข้ารหัส (Decoders and Encoders)

เอกสารสรุปเนื้อหาทฤษฎี วงจรสมมูล ไอซีมาตรฐาน วงจรขับตัวแสดงผล 7-Segment และวงจรเข้ารหัสแบบเรียงลำดับความสำคัญ ประจำบทที่ 4 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 113 – 144)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **4.1-4.3** | [วงจรถอดรหัสและการประยุกต์](01-decoders/) | Decoders, Equivalent Circuits & Address Decoding | [`01-decoders/`](01-decoders/) |
| **4.4** | [วงจรขับตัวแสดงผล 7-Segment](02-seven-segment-driver/) | 7-Segment LED Display Drivers (7447, 7448) | [`02-seven-segment-driver/`](02-seven-segment-driver/) |
| **4.5** | [วงจรเข้ารหัส](03-encoders/) | Encoders (Octal-to-Binary, Decimal-to-BCD) | [`03-encoders/`](03-encoders/) |
| **4.6-4.8** | [วงจรเข้ารหัสแบบเรียงลำดับความสำคัญ](04-priority-encoders/) | Priority Encoders (74147, 74148) & Applications | [`04-priority-encoders/`](04-priority-encoders/) |
| **Ex** | [แบบฝึกหัดท้ายบทที่ 4](exercises/) | Chapter 4 Solved Exercises | [`exercises/`](exercises/) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 4.1-4.3 วงจรถอดรหัส (Decoders)
* **นิยาม:** วงจรที่แปลงรหัสฐานสองขนาด `n` บิตให้เป็นเอาต์พุต `2ⁿ` ช่องทาง (โดยจะมีเอาต์พุตทำงานเพียง 1 ช่องตามรหัสที่ป้อนเข้ามา)
* **ไอซีมาตรฐาน:**
  * **74138 (3-to-8 Decoder):** Active-LOW outputs (`Y₀'..Y₇'`), มีขา Enable 3 ขา (`G₁`, `G₂A'`, `G₂B'`) เหมาะกับการต่อขยายแอดเดรสหน่วยความจำ (Address Decoding)
  * **74154 (4-to-16 Decoder):** ถอดรหัส 4 บิตเป็น 16 เอาต์พุต
  * **7442 (BCD-to-Decimal Decoder):** ถอดรหัส BCD 4 บิตเป็นเลขฐานสิบ 10 ช่องทาง (0 ถึง 9)

### 4.4 วงจรขับตัวแสดงผลเจ็ดส่วน (7-Segment LED Display Drivers)
* **โครงสร้าง 7-Segment:** หลอด LED 7 ท่อน (`a, b, c, d, e, f, g`) มี 2 ชนิด:
  1. **Common Anode (ขั้วแอโนดร่วม):** ขั้วบวกรวมกัน จ่ายลอจิก `0` (Active-LOW) เพื่อให้ติด ใช้คู่กับ **IC 7447**
  2. **Common Cathode (ขั้วแคโทดร่วม):** ขั้วลบรวมกัน จ่ายลอจิก `1` (Active-HIGH) เพื่อให้ติด ใช้คู่กับ **IC 7448**
* **ขาสัญญาณควบคุมพิเศษ:**
  * `LT'` (Lamp Test): ทดสอบหลอดไฟทุกท่อนให้ติดสว่างพร้อมกัน
  * `BI'/RBO'` (Blanking Input / Ripple Blanking Output): ดับหลอดไฟทั้งหมด หรือดับเลขศูนย์นำหน้า (Zero Suppression)
  * `RBI'` (Ripple Blanking Input): อินพุตสำหรับตัดเลขศูนย์ที่ไม่จำเป็น

### 4.5-4.8 วงจรเข้ารหัสและตัวเข้ารหัสความสำคัญ (Priority Encoders)
* **วงจรเข้ารหัส (Encoder):** ทำงานตรงข้ามกับ Decoder รับอินพุต `2ⁿ` ช่อง แล้วแปลงเป็นรหัสฐานสอง `n` บิต
* **Priority Encoder:** หากมีอินพุตเข้ามาพร้อมกันหลายช่อง จะเข้ารหัสเฉพาะช่องที่มี **ลำดับความสำคัญสูงสุด (Highest Priority)** เสมอ
* **ไอซีมาตรฐาน:**
  * **74147:** 10-Line to 4-Line Priority Encoder (Decimal-to-BCD, Active-LOW) ช่อง `9` มีความสำคัญสูงสุด
  * **74148:** 8-Line to 3-Line Octal Priority Encoder (Active-LOW) มีขา `EO` (Enable Output) และ `GS` (Group Select) สำหรับต่อขยายเป็น 16 หรือ 32 ช่อง

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [03-multiplexers-demultiplexers/](../03-multiplexers-demultiplexers/README.md)
- ➡️ ไปยังบทถัดไป: [05-arithmetic-circuits/](../05-arithmetic-circuits/README.md)
