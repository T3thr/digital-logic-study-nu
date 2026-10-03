# 3.1-3.3 มัลติเพล็กเซอร์ (Multiplexers / Data Selectors)

## 📌 สรุปทฤษฎีและการทำงาน
* **ขนาด:** `2ⁿ` อินพุตข้อมูล, `n` สายควบคุมการเลือก (Select lines), 1 เอาต์พุต
* **ไอซีมาตรฐาน:**
  * **74151:** 8-to-1 Multiplexer (Select: `S₂ S₁ S₀`, Strobe: `G'`, Outputs: `Y, W`)
  * **74150:** 16-to-1 Multiplexer (Active-LOW Inverting Output `W`)
* **การประยุกต์:** Universal Logic Generator, Data Routing, Serial Transmission
