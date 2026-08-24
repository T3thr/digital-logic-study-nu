# ⚡ Digital Logic Design & Engineering Problem Hub (305241)

คลังเอกสารสรุปบทเรียน ทฤษฎีพีชคณิตบูลีน และ **คลังเฉลยโจทย์วิเคราะห์/ลดรูปวงจรตรรกศาสตร์ดิจิทัลฉบับสมบูรณ์** พร้อมภาพวงจรวาดใหม่ความละเอียดสูง ตารางความจริง แผนผัง Karnaugh Map (K-Map) ทั้งแบบ SOP / POS และการวิเคราะห์เปรียบเทียบฮาร์ดแวร์

---

## 🧭 โครงสร้างสารบัญหมวดหมู่ (Course Modules)

| หมวดหมู่ | โฟลเดอร์ | รายละเอียดเนื้อหา |
| :--- | :--- | :--- |
| **00. Lecture Materials** | [`00-lecture/`](00-lecture/README.md) | สไลด์บรรยายฉบับเต็มของวิชา 305241 Digital Logic |
| **01. Boolean Algebra** | [`01-boolean-algebra/`](01-boolean-algebra/README.md) | ทฤษฎีพีชคณิตบูลีน, กฎเดอมอร์แกน, SOP vs POS, และหลักการ K-Map |
| **02. Logic Gate Problems** | [`02-logic-gates/`](02-logic-gates/README.md) | คลังตัวอย่างโจทย์และการลดรูปวงจรเกตลอจิก (Examples 01, 02, 03) |
| **03. MSI Logic (MUX/DMUX)** | [`03-mux-dmux/`](03-mux-dmux/README.md) | ทฤษฎีและการออกแบบวงจรด้วย Multiplexer / Demultiplexer |

---

## 🏆 คลังตัวอย่างโจทย์และการลดรูปวงจร (Solved Problem Sets)

| รหัสโจทย์ | ภาพโจทย์ต้นฉบับ | สมการโจทย์ต้นฉบับ | สมการลดรูป (Minimal Form) | เทคนิคเด่น | ลิงก์เฉลยละเอียด |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Ex 01** | [`image.png`](02-logic-gates/examples/01/image.png) | $Y = \overline{(A\cdot B)(A+C)} \cdot \overline{\bar{B}+D}$ | **SOP:** $Y = \bar{A}B\bar{D}$<br>**POS:** $Y = \overline{A+\bar{B}+D}$ | • $C$ เป็น Don't-care input<br>• ลดจาก 6 Gates เหลือ 2-3 Gates | [📖 อ่านเฉลย Ex 01](02-logic-gates/examples/01/README.md) |
| **Ex 02** | [`image.png`](02-logic-gates/examples/02/image.png) | $Y = \overline{(A+B)+AC} \oplus (AC\bar{D})$ | **SOP:** $Y = \bar{A}\bar{B} + AC\bar{D}$<br>**POS:** $Y = (A+\bar{B})(\bar{A}+C)(\bar{A}+\bar{D})$ | • การกระจาย XOR ร่วมกับ Absorption<br>• K-Map 4x4 จับกลุ่ม Quad & Pair | [📖 อ่านเฉลย Ex 02](02-logic-gates/examples/02/README.md) |
| **Ex 03** | - | $F = \bar{A}B + A\bar{C} + \bar{B}DE + C\bar{D}\bar{E}$ | **SOP:** $F = \bar{A}B + A\bar{C} + \bar{B}DE + C\bar{D}\bar{E}$<br>**POS:** 5 Maxterm factors | • K-Map 5 ตัวแปร (8 แถว x 4 คอลัมน์)<br>• ตารางความจริง 32 กรณี | [📖 อ่านเฉลย Ex 03](02-logic-gates/examples/03/README.md) |
| **MUX ข้อ 1** | [`example01.jpeg`](03-mux-dmux/exam/1/example01.jpeg) | หารูปคลื่นเอาต์พุต $Y$ และ $W$ จากวงจร **74151** (รูปที่ 3.40) | **$Y$ = 11 ท่อน:** `0 1 0 1 0 1 0 1 0 1 0`<br>**$W = \overline{Y}$:** `1 0 1 0 1 0 1 0 1 0 1` | • ขา $\overline{G}$ active LOW<br>• ตัวนับ 3 บิตไล่ช่อง $D_0 \to D_7$<br>• $E$ เปลี่ยนค่ากลางช่วง<br>• เฉลยทีละช่วงพร้อมสื่อ 10 รูป | [📖 อ่านเฉลย MUX ข้อ 1](03-mux-dmux/exam/1/README.md) |

---

## 🔍 บทความเจาะลึกเฉพาะทาง (Special Topic Deep Dives)

- 💡 [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](01-boolean-algebra/why_sop_1_pos_0.md) : ทำความเข้าใจระดับฟิสิกส์เกต (AND-OR Detector vs OR-AND Filter)
- 📜 [กฎของ De Morgan และข้อพิสูจน์ $\bar{A} \cdot \bar{B} \neq \overline{A \cdot B}$](01-boolean-algebra/demorgan_laws.md) : พิสูจน์ด้วยตารางความจริง และเทคนิคผ่า Bar สลับเครื่องหมาย

---

## 🌲 แผนผังโครงสร้างโฟลเดอร์ทั้งหมด (Directory Tree)

```
digital-logic/
├── README.md                                  # [MAIN HUB] เอกสารสารบัญภาพรวมหน้านี้
│
├── 00-lecture/                                # สไลด์และเอกสารประกอบการสอน
│   ├── README.md                              # สารบัญสไลด์
│   └── 305241_lecture.pdf                     # สไลด์บรรยายวิชา Digital Logic
│
├── 01-boolean-algebra/                        # บทที่ 1: พีชคณิตบูลีนและ K-Map
│   ├── README.md                              # สรุปกฎบูลีนและแนวคิด SOP / POS
│   ├── why_sop_1_pos_0.md                     # เจาะลึกทำไม SOP ดู 1 / POS วง 0
│   ├── demorgan_laws.md                       # เจาะลึกกฎของเดอมอร์แกน
│   ├── scripts/
│   │   └── generate_boolean_diagrams.py       # สคริปต์วาดไดอะแกรม K-Map
│   └── assets/                                # รูปภาพไดอะแกรมประกอบบทเรียน
│       ├── kmap_sop_diagram.png
│       ├── kmap_pos_diagram.png
│       ├── sop_circuit_diagram.png
│       ├── pos_circuit_diagram.png
│       └── sop_pos_comparison.png
│
├── 02-logic-gates/                            # บทที่ 2: เกตตรรกะและคลังโจทย์
│   ├── README.md                              # สารบัญเกตตรรกะและภาพรวมโจทย์
│   └── examples/                              # คลังตัวอย่างโจทย์และการลดรูป
│       ├── 01/                                # ตัวอย่างที่ 1: วงจร NAND-NOR-AND 4 ตัวแปร
│       │   ├── README.md                      # เฉลยละเอียด
│       │   ├── image.png                      # ภาพถ่ายโจทย์ต้นฉบับ
│       │   ├── generate_all_diagrams.py       # สคริปต์เรนเดอร์รูป
│       │   └── *.png                          # ไดอะแกรมวงจรและ K-Map
│       ├── 02/                                # ตัวอย่างที่ 2: วงจร XOR 4 ตัวแปร
│       │   ├── README.md                      # เฉลยละเอียด
│       │   ├── image.png                      # ภาพถ่ายโจทย์ต้นฉบับ
│       │   ├── generate_all_diagrams.py       # สคริปต์เรนเดอร์รูป
│       │   └── *.png                          # ไดอะแกรมวงจรและ K-Map
│       └── 03/                                # ตัวอย่างที่ 3: วงจร 5 ตัวแปร K-Map 8x4
│           ├── README.md                      # เฉลยละเอียด
│           ├── generate_all_diagrams.py       # สคริปต์เรนเดอร์รูป
│           └── *.png                          # ไดอะแกรมวงจรและ K-Map
│
└── 03-mux-dmux/                               # บทที่ 3: Multiplexer & Demultiplexer
    ├── README.md                              # สรุปทฤษฎี MUX/DMUX + ตาราง 74151
    └── exam/                                  # โฟลเดอร์เตรียมสอบและแบบฝึกหัด
        ├── README.md                          # รายการโจทย์และมาตรฐานการเฉลย
        └── 1/                                 # ข้อที่ 1: หารูปคลื่น Y, W จากวงจร 74151 (รูปที่ 3.40)
            ├── README.md                      # เฉลยละเอียดทุกขั้นตอนพร้อมสอนทฤษฎี
            ├── VERIFICATION.md                # หลักฐานการตรวจสอบข้อมูลต้นฉบับ (พิกเซล forensics)
            ├── example01.jpeg                 # ภาพโจทย์ต้นฉบับ
            ├── generate_all_diagrams.py       # สคริปต์สร้างไดอะแกรมทั้งหมด (matplotlib)
            ├── verify_render.py               # สคริปต์ตรวจสอบภาพและคำตอบอัตโนมัติ
            └── *.png                          # ไดอะแกรม 10 รูป (300 DPI) เรียงตามลำดับการอ่าน
```

---

## 🛠️ เครื่องมือช่วยสร้างไดอะแกรม (Python Asset Generators)

ภายในแต่ละชุดโจทย์มีไฟล์ `generate_all_diagrams.py` ที่ใช้ไลบรารี `matplotlib` และ `schemdraw` / `PIL` สำหรับ Generate ภาพวงจรและ K-Map ความละเอียดสูง (300 DPI) โดยอัตโนมัติ

วิธีเรียกใช้งาน:
```bash
# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์ข้อที่ 1
python3 02-logic-gates/examples/01/generate_all_diagrams.py

# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์ข้อที่ 2
python3 02-logic-gates/examples/02/generate_all_diagrams.py

# ตัวอย่าง: สร้างไดอะแกรมสำหรับโจทย์ข้อที่ 3
python3 02-logic-gates/examples/03/generate_all_diagrams.py
```
