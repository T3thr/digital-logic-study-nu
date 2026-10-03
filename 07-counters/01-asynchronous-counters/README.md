# 7.1-7.3 วงจรนับแบบอะซิงโครนัส (Ripple Counters)

## 📌 หลักการทำงาน
* สัญญาณ Clock ป้อนเข้าเฉพาะ Flip-Flop บิตแรก บิตถัดไปรับ Clock จาก `Q` ตัวก่อนหน้า
* เกิด Propagation Delay สะสม
* การตัดรอบนับเป็น Modulo-N (Truncated Modulo)
