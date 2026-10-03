# 🔀 บทที่ 3 : มัลติเพล็กเซอร์และดีมัลติเพล็กเซอร์ (Multiplexers and Demultiplexers)

เอกสารสรุปเนื้อหาทฤษฎี วงจรสมมูล ไอซีมาตรฐาน การประยุกต์ใช้งาน และคลังข้อสอบวิเคราะห์สัญญาณเวลา ประจำบทที่ 3 ของรายวิชา **305241 Digital Logic Design & Engineering** อ้างอิงตามสไลด์บรรยาย [`305241_lecture.pdf`](../00-lecture/305241_lecture.pdf) (หน้า 79 – 112)

---

## 🧭 สารบัญเนื้อหาภายในบท (Table of Contents)

| ลำดับหัวข้อ | ชื่อหัวข้อภาษาไทย | ชื่อหัวข้อภาษาอังกฤษ | โฟลเดอร์เนื้อหา |
| :---: | :--- | :--- | :--- |
| **3.1-3.3** | [มัลติเพล็กเซอร์และการประยุกต์](01-multiplexers/) | Multiplexers (Data Selectors), Equivalents & ICs | [`01-multiplexers/`](01-multiplexers/) |
| **3.4-3.6** | [ดีมัลติเพล็กเซอร์และการประยุกต์](02-demultiplexers/) | Demultiplexers (Data Distributors), Equivalents & ICs | [`02-demultiplexers/`](02-demultiplexers/) |
| **Ex** | [คลังข้อสอบและแบบฝึกหัดท้ายบทที่ 3](exercises/) | Solved Waveform & Design Problems | [`exercises/`](exercises/) |

---

## 🏆 ไฮไลต์ข้อสอบและแบบฝึกหัดสำคัญ (Solved Exam Sets)

| รหัสโจทย์ | ภาพโจทย์ต้นฉบับ | หัวข้อการวิเคราะห์ | ผลลัพธ์เอาต์พุต | ลิงก์เฉลยละเอียด |
| :---: | :---: | :--- | :--- | :---: |
| **Exam ข้อ 1** | [`example01.jpeg`](exercises/1/example01.jpeg) | การวิเคราะห์รูปคลื่นเอาต์พุต `Y` และ `W` จากวงจร **74151** (รูปที่ 3.40) | **Y = 11 ช่วง:** `0 1 0 1 0 1 0 1 0 1 0`<br>**W = Y' :** `1 0 1 0 1 0 1 0 1 0 1` | [📖 อ่านเฉลยละเอียด MUX ข้อ 1](exercises/1/README.md)<br>[🌐 เปิดเว็บแอป Interactive](exercises/1/solution.html) |
| **Exam ข้อ 2** | [`03_tdm_system_circuit.png`](exercises/2/assets/03_tdm_system_circuit.png) | การวิเคราะห์วงจรดีมัลติเพล็กเซอร์ **74138** ในระบบรับส่ง TDM และเกต NAND `F` | **Ȳ₀..Ȳ₇ (Active-LOW):** เกิดพัลส์ 0 ที่ช่องถูกเลือก<br>**F :** ลอจิก 1 เฉพาะช่วง 1c, 4a, 7 | [📖 อ่านเฉลยละเอียด DMUX ข้อ 2](exercises/2/README.md)<br>[🌐 เปิดเว็บแอป Interactive](exercises/2/solution.html) |

---

## 💡 สรุปใจความสำคัญของแต่ละหัวข้อ (Key Takeaways)

### 3.1-3.3 มัลติเพล็กเซอร์ (Multiplexer / MUX)
* **นิยาม:** อุปกรณ์เลือกส่งสัญญาณข้อมูล (Data Selector) รับสัญญาณข้อมูลเข้าหลายช่องทาง (`2ⁿ` อินพุต) แล้วเลือกส่งออกไปยังเอาต์พุตเพียง **1 ช่องทาง** โดยอาศัยสายสัญญาณควบคุมการเลือก (Select Lines) จำนวน `n` เส้น
* **ไอซี MUX มาตรฐาน:**
  * **74151:** 8-to-1 Data Selector/Multiplexer (Select 3 เส้น: `S₂ S₁ S₀`, ขา Enable/Strobe `G'` แบบ Active-LOW, เอาต์พุตมีทั้ง `Y` และ `W = Y'`)
  * **74150:** 16-to-1 Data Selector/Multiplexer (Select 4 เส้น, เอาต์พุตเป็น Inverted `W`)
  * **74157:** Quad 2-to-1 Multiplexer (สวิตช์เลือกชุดข้อมูล 4 บิตพร้อมกัน)
* **การประยุกต์ใช้งาน:**
  1. การส่งข้อมูลแบบแบ่งเวลา (Time-Division Multiplexing)
  2. **การสร้างฟังก์ชันลอจิกโดยไม่ต้องใช้เกต (Universal Logic Generator):** นำตัวแปร `n` ตัวต่อเข้าขา Select และนำค่าตารางความจริง (0, 1 หรือตัวแปรที่เหลือ) ต่อเข้าขาข้อมูล `D₀..D₇`

### 3.4-3.6 ดีมัลติเพล็กเซอร์ (Demultiplexer / DMUX)
* **นิยาม:** อุปกรณ์กระจายสัญญาณข้อมูล (Data Distributor) รับสัญญาณข้อมูลเข้า **1 ช่องทาง** แล้วกระจายส่งออกไปยังเอาต์พุตปลายทางช่องใดช่องหนึ่งจาก `2ⁿ` ช่องทาง ตามรหัสที่เลือกในสาย Select
* **ความสัมพันธ์ระหว่าง DMUX และ Decoder:**
  * วงจรถอดรหัส (Decoder) ที่มีขา Enable สามารถทำหน้าที่เป็น Demultiplexer ได้ทันที โดยป้อนข้อมูลเข้าที่ขา Enable และใช้ขาแอดเดรสเป็นขา Select
* **ไอซี DMUX มาตรฐาน:**
  * **74138:** 3-to-8 Line Decoder / Demultiplexer (Active-LOW Outputs)
  * **74154:** 4-to-16 Line Decoder / Demultiplexer (Active-LOW Outputs)

---

## 🔗 ลิงก์เชื่อมโยง
- ⬅️ กลับไปยังบทก่อนหน้า: [02-logic-functions-combinational/](../02-logic-functions-combinational/README.md)
- ➡️ ไปยังบทถัดไป: [04-decoders-encoders/](../04-decoders-encoders/README.md)
