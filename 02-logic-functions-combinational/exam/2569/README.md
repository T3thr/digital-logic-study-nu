# 🏆 คลังข้อสอบและแบบฝึกหัด บทที่ 2 (Exam Archive 2569)

**วิชา:** 305241 การออกแบบวงจรดิจิตอล (Digital Logic Circuit Design)  
**ภาควิชา:** วิศวกรรมไฟฟ้าและคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยนเรศวร  
**บทที่ 2:** ฟังก์ชันตรรกศาสตร์และเกตเชิงผสม (Logic Functions & Combinational Circuits)

---

## 📑 สารบัญข้อสอบ (Exam Index)

| รหัสข้อสอบ | หัวข้อและเนื้อหาสำคัญ | เทคนิคเด่น | สื่อประกอบ | ลิงก์เฉลยละเอียด |
| :---: | :--- | :--- | :---: | :---: |
| **EXAM 01** | **การวิเคราะห์ วาดวงจร และลดรูปวงจรตรรกศาสตร์ 5 ตัวแปรด้วย K-Map 8×4**<br>• วงจร 5 อินพุต (A, B, C, D, E) ประกอบด้วย 7404, 7408, 7411, OR5<br>• ตารางความจริง 32 กรณี (23 Minterms, 9 Maxterms) | • ผัง K-Map 8 แถว × 4 คอลัมน์ (ABC / DE)<br>• การจับกลุ่มวนขอบ (Wraparound)<br>• การเปรียบเทียบ Minimal SOP vs POS<br>• การสังเคราะห์วงจรและคำนวณทรานซิสเตอร์ CMOS | 6 ไดอะแกรม (300 DPI) | [📖 เฉลยละเอียดข้อ 01](1/README.md)<br>[🌐 Web UI เฉลยข้อ 01](1/solution.html) |
| **EXAM 02** | **การวิเคราะห์ วาดวงจรเกตผสมแบบ 2 อินพุต และลดรูปด้วย K-Map 8×4**<br>• วงจรเกตจำกัดไม่เกิน 2 อินพุต (74HC04, 74HC86 XOR, 74HC00 NAND, 74HC02 NOR, 74HC08, 74HC32)<br>• ตารางความจริง 32 กรณี (23 Minterms, 9 Maxterms) | • การวิเคราะห์จุดทดสอบ W₁..W₉ แบบ 4 สเตจ<br>• ผัง K-Map 8×4 แสดงกลุ่ม Octet, Quad, Pair<br>• การลดรูป Minimal SOP และ Minimal POS<br>• การเปรียบเทียบเชิงวิศวกรรมฮาร์ดแวร์จริง | 6 ไดอะแกรม (300 DPI) | [📖 เฉลยละเอียดข้อ 02](2/README.md)<br>[🌐 Web UI เฉลยข้อ 02](2/solution.html) |
| **EXAM 03** | **วงจรลอจิกผสมครบ 7 ชนิดเกตมาตรฐาน (All 7 Standard Gate Types · Max 2-Input)**<br>• วงจร 4 ระดับใช้เกตครบ 7 ชนิด (NOT, XOR, XNOR, NAND, NOR, AND, OR)<br>• ตารางความจริง 32 กรณี (18 Minterms, 14 Maxterms) | • การพิสูจน์เอกลักษณ์ XNOR Absorption และ De Morgan on NAND<br>• ผัง K-Map 8×4 (4 SOP Groups / 6 POS Groups)<br>• Two-Level Logic Synthesis (AND-OR vs OR-AND)<br>• Hardware IC Benchmark ตระกูล 74HC Series | 6 ไดอะแกรม (300 DPI) | [📖 เฉลยละเอียดข้อ 03](3/README.md)<br>[🌐 Web UI เฉลยข้อ 03](3/solution.html) |

---

## 🌐 การเปิดใช้งานเว็บแอปพลิเคชัน (Web UI Access)
สามารถเปิดดูหน้าศูนย์กลางคลังข้อสอบได้ที่ [`index.html`](index.html) หรือเปิดดูเฉลยละเอียดแต่ละข้อได้ทันที:
- [`1/solution.html`](1/solution.html) — ข้อสอบข้อที่ 1 (Exam 01)
- [`2/solution.html`](2/solution.html) — ข้อสอบข้อที่ 2 (Exam 02)
- [`3/solution.html`](3/solution.html) — ข้อสอบข้อที่ 3 (Exam 03)
