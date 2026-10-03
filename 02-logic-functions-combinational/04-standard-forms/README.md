# 2.5 รูปแบบมาตรฐานของการเขียนสมการลอจิก (Standard Forms of Logic Expressions)

## 📌 SOP vs POS
1. **SOP (Sum of Products):** ผลบวกของผลคูณ (สร้างจาก Minterms `mᵢ` โดยพิจารณาสถานะที่ฟังก์ชันให้ผลลัพธ์เป็น `1`)
   * วงจรสร้างด้วยโครงสร้าง **AND-OR** หรือ **NAND-NAND**
2. **POS (Product of Sums):** ผลคูณของผลบวก (สร้างจาก Maxterms `Mᵢ` โดยพิจารณาสถานะที่ฟังก์ชันให้ผลลัพธ์เป็น `0`)
   * วงจรสร้างด้วยโครงสร้าง **OR-AND** หรือ **NOR-NOR**

---

## 💡 บทความเจาะลึกเฉพาะทาง
- [ทำไม SOP ต้องดู 1 และ POS ต้องวง 0 ใน K-Map?](why_sop_1_pos_0.md) : วิเคราะห์ระดับฟิสิกส์เกต (AND-OR Detector vs OR-AND Filter)
