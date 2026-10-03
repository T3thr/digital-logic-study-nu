# ⚡ Digital Logic Design & Engineering Problem Hub (305241)

คลังเอกสารสรุปบทเรียน ทฤษฎีพีชคณิตบูลีน สถาปัตยกรรมวงจรดิจิทัล และ **คลังเฉลยโจทย์วิเคราะห์/ลดรูปวงจรตรรกศาสตร์ดิจิทัลฉบับสมบูรณ์** ประจำรายวิชา **305241 Digital Logic Design & Engineering** มหาวิทยาลัยนเรศวร พร้อมภาพวงจรความละเอียดสูง ตารางความจริง แผนผัง Karnaugh Map (K-Map) ทั้งแบบ SOP / POS และการวิเคราะห์สัญญาณเวลาอย่างละเอียด

---

## 🧭 โครงสร้างสารบัญรายวิชา 8 บทเรียน (Course Syllabus Hub)

โครงสร้างโฟลเดอร์ถูกจัดเรียงตามเนื้อหาจริงทั้ง 8 บทของสไลด์บรรยายประจำวิชา [`00-lecture/305241_lecture.pdf`](00-lecture/305241_lecture.pdf):

| บทที่ | โฟลเดอร์เนื้อหา | ชื่อบทเรียนภาษาไทย | รายละเอียดเนื้อหาสำคัญ |
| :---: | :--- | :--- | :--- |
| **00** | [`00-lecture/`](00-lecture/README.md) | **เอกสารประกอบการสอน** | สไลด์บรรยายฉบับเต็ม 260 หน้า และสารบัญหลักสูตร |
| **01** | [`01-number-systems/`](01-number-systems/README.md) | **บทที่ 1: ระบบจำนวน** | ฐานสอง/แปด/สิบหก, การแปลงฐาน, รหัส BCD/Gray, Signed 2's Complement |
| **02** | [`02-logic-functions-combinational/`](02-logic-functions-combinational/README.md) | **บทที่ 2: ฟังก์ชันลอจิกและวงจรลอจิกผสม** | เกตตรรกะ, พีชคณิตบูลีน, กฎเดอมอร์แกน, SOP/POS, K-Map และคลังโจทย์ Ex 01-03 |
| **03** | [`03-multiplexers-demultiplexers/`](03-multiplexers-demultiplexers/README.md) | **บทที่ 3: มัลติเพล็กเซอร์และดีมัลติเพล็กเซอร์** | MUX 74151/74150, DMUX 74138, Universal Logic Gen และคลังข้อสอบ Exam 1 |
| **04** | [`04-decoders-encoders/`](04-decoders-encoders/README.md) | **บทที่ 4: วงจรถอดรหัสและวงจรเข้ารหัส** | Decoder 74138/74154, 7-Segment Driver 7447/7448, Priority Encoder 74147/74148 |
| **05** | [`05-arithmetic-circuits/`](05-arithmetic-circuits/README.md) | **บทที่ 5: วงจรเลขคณิต** | Half/Full Adder, 7483/74283, วงจรบวก/ลบ, Overflow Detection, Comparator 7485, ALU |
| **06** | [`06-latches-flip-flops/`](06-latches-flip-flops/README.md) | **บทที่ 6: แลตช์และฟลิปฟล็อป** | S-R/D Latch, D/J-K/Master-Slave Flip-Flops 7474/7476, Preset/Clear, Edge-Trigger |
| **07** | [`07-counters/`](07-counters/README.md) | **บทที่ 7: วงจรนับ** | Asynchronous Ripple Counters, Synchronous Counters, Modulo-N, 7490/7493/74190/74193 |
| **08** | [`08-registers/`](08-registers/README.md) | **บทที่ 8: รีจิสเตอร์** | Shift Registers (SISO/SIPO/PISO/PIPO), 74164/74165/74194, Ring & Johnson Counters |
| **99** | [`99-textbook/`](99-textbook/) | **ตำราและเอกสารอ้างอิง** | หนังสือตำราวิศวกรรมดิจิทัลและคู่มือดาต้าชีตไอซี |

---

## 🏆 คลังตัวอย่างโจทย์และการเฉลยละเอียด (Featured Solved Sets)

| หมวดบทเรียน | รหัสโจทย์ | สมการ / วงจรโจทย์ | คำตอบลดรูป (Minimal Form) | ลิงก์เฉลยละเอียด |
| :---: | :---: | :--- | :--- | :---: |
| **บทที่ 2** | **Ex 01** | `Y = ((A·B)(A+C))' · ((B)' + D)'` | **SOP:** `Y = A'·B·D'`<br>**POS:** `Y = (A + B' + D)'` | [📖 อ่านเฉลย Ex 01](02-logic-functions-combinational/exercises/01/README.md) |
| **บทที่ 2** | **Ex 02** | `Y = ((A+B)+AC)' ⊕ (A·C·D')` | **SOP:** `Y = A'·B' + A·C·D'`<br>**POS:** `Y = (A+B')(A'+C)(A'+D')` | [📖 อ่านเฉลย Ex 02](02-logic-functions-combinational/exercises/02/README.md) |
| **บทที่ 2** | **Ex 03** | `F = A'·B + A·C' + B'·D·E + C·D'·E'` | **SOP:** `F = A'·B + A·C' + B'·D·E + C·D'·E'` (32 กรณี) | [📖 อ่านเฉลย Ex 03](02-logic-functions-combinational/exercises/03/README.md) |
| **บทที่ 3** | **MUX ข้อ 1** | หารูปคลื่น `Y` และ `W` จากไอซี **74151** (รูปที่ 3.40) | **Y = 11 ช่วง:** `0 1 0 1 0 1 0 1 0 1 0`<br>**W = Y' :** `1 0 1 0 1 0 1 0 1 0 1` | [📖 อ่านเฉลย MUX ข้อ 1](03-multiplexers-demultiplexers/exercises/1/README.md)<br>[🌐 เปิดเว็บแอป Interactive](03-multiplexers-demultiplexers/exercises/1/solution.html) |

---

## 🔍 บทความเจาะลึกเฉพาะทาง (Special Topic Deep Dives)

- 💡 [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](02-logic-functions-combinational/04-standard-forms/why_sop_1_pos_0.md) : วิเคราะห์ระดับฟิสิกส์เกต (AND-OR Detector vs OR-AND Filter)
- 📜 [กฎของ De Morgan และข้อพิสูจน์ (A'·B' ≠ (A·B)')](02-logic-functions-combinational/03-boolean-algebra/demorgan_laws.md) : พิสูจน์ด้วยตารางความจริง และเทคนิคผ่า Bar สลับเครื่องหมาย

---

## 🌲 แผนผังโครงสร้างโฟลเดอร์ทั้งหมด (Directory Tree)

```
digital-logic/
├── README.md                                        # [MAIN HUB] สารบัญหลักภาพรวมวิชา
├── index.html                                       # เว็บแอปพลิเคชันรวมบทเรียน
├── 00-lecture/                                      # สไลด์และเอกสารประกอบการสอน
│   ├── 305241_lecture.pdf                           # สไลด์บรรยายฉบับเต็ม 260 หน้า
│   └── README.md
│
├── 01-number-systems/                               # บทที่ 1: ระบบจำนวน
│   ├── README.md
│   ├── 01-number-representation/
│   ├── 02-base-conversion/
│   ├── 03-binary-codes/
│   ├── 04-binary-arithmetic/
│   ├── 05-signed-numbers/
│   ├── 06-signed-arithmetic/
│   └── exercises/
│
├── 02-logic-functions-combinational/                 # บทที่ 2: ฟังก์ชันลอจิกและวงจรลอจิกผสม
│   ├── README.md
│   ├── 01-logic-gates/
│   ├── 02-combinational-circuits/
│   ├── 03-boolean-algebra/
│   ├── 04-standard-forms/
│   ├── 05-equivalent-circuits/
│   ├── 06-karnaugh-map/
│   └── exercises/                                   # คลังเฉลยตัวอย่างโจทย์ (Ex 01, 02, 03)
│       ├── 01/
│       ├── 02/
│       └── 03/
│
├── 03-multiplexers-demultiplexers/                  # บทที่ 3: มัลติเพล็กเซอร์และดีมัลติเพล็กเซอร์
│   ├── README.md
│   ├── index.html
│   ├── 01-multiplexers/
│   ├── 02-demultiplexers/
│   └── exercises/                                   # คลังข้อสอบเตรียมสอบ (Exam 1)
│       ├── index.html
│       └── 1/
│
├── 04-decoders-encoders/                            # บทที่ 4: วงจรถอดรหัสและวงจรเข้ารหัส
│   ├── README.md
│   ├── 01-decoders/
│   ├── 02-seven-segment-driver/
│   ├── 03-encoders/
│   ├── 04-priority-encoders/
│   └── exercises/
│
├── 05-arithmetic-circuits/                          # บทที่ 5: วงจรเลขคณิต
│   ├── README.md
│   ├── 01-adders/
│   ├── 02-subtractors/
│   ├── 03-overflow-detection/
│   ├── 04-multipliers/
│   ├── 05-comparators/
│   ├── 06-multifunction-alu/
│   └── exercises/
│
├── 06-latches-flip-flops/                           # บทที่ 6: แลตช์และฟลิปฟล็อป
│   ├── README.md
│   ├── 01-latches/
│   ├── 02-flip-flops/
│   ├── 03-applications/
│   └── exercises/
│
├── 07-counters/                                     # บทที่ 7: วงจรนับ
│   ├── README.md
│   ├── 01-asynchronous-counters/
│   ├── 02-synchronous-counters/
│   ├── 03-ic-counters/
│   └── exercises/
│
├── 08-registers/                                    # บทที่ 8: รีจิสเตอร์
│   ├── README.md
│   ├── 01-shift-registers/
│   ├── 02-timing-waveforms/
│   ├── 03-ic-shift-registers/
│   ├── 04-applications/
│   └── exercises/
│
└── 99-textbook/                                     # หนังสือและตำราอ้างอิง
```

---

## 🛠️ เครื่องมือช่วยสร้างไดอะแกรม (Python Asset Generators)

ภายในแต่ละชุดโจทย์มีไฟล์ `generate_all_diagrams.py` สำหรับสร้างรูปภาพวงจรและ K-Map ความละเอียดสูง (300 DPI) โดยอัตโนมัติ:

```bash
# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์บทที่ 2 ข้อที่ 1
python3 02-logic-functions-combinational/exercises/01/generate_all_diagrams.py

# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์บทที่ 2 ข้อที่ 2
python3 02-logic-functions-combinational/exercises/02/generate_all_diagrams.py

# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์บทที่ 2 ข้อที่ 3
python3 02-logic-functions-combinational/exercises/03/generate_all_diagrams.py

# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์บทที่ 3 (MUX 74151)
python3 03-multiplexers-demultiplexers/exercises/1/generate_all_diagrams.py
```
