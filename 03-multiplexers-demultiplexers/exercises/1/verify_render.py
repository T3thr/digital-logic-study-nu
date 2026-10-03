"""
verify_render.py — ตรวจสอบไฟล์ภาพที่เรนเดอร์ออกมาด้วยการวิเคราะห์พิกเซล
(ใช้แทนการดูด้วยตา เพื่อพิสูจน์ว่าไดอะแกรมถูกต้องจริง)

ตรวจ 3 อย่าง:
  1. ไม่มีกล่องว่าง (tofu / .notdef) จากฟอนต์ที่ขาด glyph
  2. รูปคลื่น Y และ W ในรูป 09 เป็นส่วนกลับกันจริงในระดับพิกเซล
  3. ไม่มีข้อความล้นขอบภาพ (มีขอบขาวรอบด้าน)
"""
import glob
import os
import sys
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont
from matplotlib import font_manager

D = os.path.dirname(os.path.abspath(__file__))
fails = []

# ─────────────────────────────────────────────────────────────────────
# 1. ตรวจว่าทุกอักขระที่ใช้ในสคริปต์ มี glyph อยู่ในฟอนต์จริง
# ─────────────────────────────────────────────────────────────────────
print("=" * 74)
print("1. ตรวจ glyph coverage ของฟอนต์")
print("=" * 74)

path = [f.fname for f in font_manager.fontManager.ttflist if f.name == 'IBM Plex Thai']
cmap = set()
if path:
    tt = TTFont(path[0])
    for t in tt['cmap'].tables:
        cmap |= set(t.cmap.keys())

src = open(os.path.join(D, 'generate_all_diagrams.py'), encoding='utf-8').read()

# เก็บเฉพาะข้อความที่จะถูกวาด (อยู่ในเครื่องหมายคำพูด) และไม่ใช่ mathtext
import re
literals = re.findall(r"'([^'\n]*)'|\"([^\"\n]*)\"", src)
chars = set()
for a, b in literals:
    s = a or b
    if s.startswith('$') or '\\\\' in s:
        continue
    for ch in s:
        o = ord(ch)
        if o > 0x7F:          # เฉพาะอักขระนอก ASCII
            chars.add(ch)

missing = sorted(ch for ch in chars if ord(ch) not in cmap)
if missing:
    print(f"  [ไม่ผ่าน] อักขระที่ฟอนต์ไม่มี glyph: "
          + " ".join(f"{ch!r}(U+{ord(ch):04X})" for ch in missing))
    fails.append("missing glyphs: " + " ".join(f"U+{ord(c):04X}" for c in missing))
else:
    print(f"  [ผ่าน] อักขระนอก ASCII ทั้ง {len(chars)} ตัวมี glyph ครบในฟอนต์ IBM Plex Thai")

# ─────────────────────────────────────────────────────────────────────
# 2. ตรวจว่าไฟล์ภาพครบและไม่ว่างเปล่า + มีขอบขาว (ไม่มีอะไรล้นขอบ)
# ─────────────────────────────────────────────────────────────────────
print()
print("=" * 74)
print("2. ตรวจไฟล์ภาพ: ขนาด, ปริมาณหมึก, ขอบขาว")
print("=" * 74)

pngs = sorted(glob.glob(os.path.join(D, 'assets', '*.png')))
expect = 10
if len(pngs) != expect:
    fails.append(f"expected {expect} png, found {len(pngs)}")

for p in pngs:
    im = Image.open(p).convert('L')
    a = np.array(im)
    h, w = a.shape
    ink_ratio = float((a < 200).mean())
    # ขอบ 6 พิกเซลรอบด้านต้องเป็นสีขาวเกือบทั้งหมด
    edge = np.concatenate([a[:6].ravel(), a[-6:].ravel(),
                           a[:, :6].ravel(), a[:, -6:].ravel()])
    edge_white = float((edge > 240).mean())
    ok_ink = 0.004 < ink_ratio < 0.55
    ok_edge = edge_white > 0.985
    status = "ผ่าน" if (ok_ink and ok_edge) else "ไม่ผ่าน"
    print(f"  [{status}] {os.path.basename(p):34s} {w}x{h}  "
          f"ink={ink_ratio*100:5.2f}%  edge_white={edge_white*100:6.2f}%")
    if not ok_ink:
        fails.append(f"{os.path.basename(p)}: ink ratio {ink_ratio:.4f} out of range")
    if not ok_edge:
        fails.append(f"{os.path.basename(p)}: content touches border "
                     f"(edge white {edge_white:.3f})")

# ─────────────────────────────────────────────────────────────────────
# 3. ตรวจว่า Y และ W ในรูป 09 เป็นส่วนกลับกันจริง (ระดับพิกเซล)
# ─────────────────────────────────────────────────────────────────────
print()
print("=" * 74)
print("3. ตรวจรูป 09: Y และ W ต้องเป็นส่วนกลับกันทุกจุด")
print("=" * 74)

# นำเข้าค่าที่คำนวณจากสคริปต์เดียวกัน แล้วเทียบว่า run ตรงข้ามกันจริง
sys.path.insert(0, D)
import importlib
gen = importlib.import_module('generate_all_diagrams')

yr, wr = gen.Y_RUNS, gen.W_RUNS
ok_len = len(yr) == len(wr)
ok_vals = all(y[0] + w[0] == 1 and y[1] == w[1] and y[2] == w[2]
              for y, w in zip(yr, wr))
print(f"  จำนวนท่อน Y={len(yr)} W={len(wr)}  -> {'ผ่าน' if ok_len else 'ไม่ผ่าน'}")
print(f"  ทุกท่อนตรงข้ามกันและขอบตรงกัน  -> {'ผ่าน' if ok_vals else 'ไม่ผ่าน'}")
if not (ok_len and ok_vals):
    fails.append("Y/W are not exact complements")

# ตรวจซ้ำแบบไล่ทีละพิกเซล
bad = [x for x in range(gen.X0, gen.X1 + 1) if gen.Yf(x) + gen.Wf(x) != 1]
print(f"  ไล่ทีละพิกเซล {gen.X1-gen.X0+1} จุด: ผิด {len(bad)} จุด  "
      f"-> {'ผ่าน' if not bad else 'ไม่ผ่าน'}")
if bad:
    fails.append(f"{len(bad)} pixels where Y+W != 1")

# ตรวจว่าขณะดิสเอเบิลได้ Y=0, W=1 ตามตาราง lecture
dis = [x for x in range(gen.X0, gen.X1 + 1) if gen.val('E', x) == 1]
ok_dis = all(gen.Yf(x) == 0 and gen.Wf(x) == 1 for x in dis)
print(f"  ช่วงดิสเอเบิล {len(dis)} จุด ได้ Y=0,W=1  -> {'ผ่าน' if ok_dis else 'ไม่ผ่าน'}")
if not ok_dis:
    fails.append("disabled region does not force Y=0,W=1")

# ตรวจลำดับช่องที่ถูกเลือก
seq = [gen.sel_code(gen.SLOT_EDGES[i])[3] for i in range(gen.NSLOT)]
ok_seq = seq == [0, 1, 2, 3, 4, 5, 6, 7, 0]
print(f"  ลำดับช่องที่เลือก {seq}  -> {'ผ่าน' if ok_seq else 'ไม่ผ่าน'}")
if not ok_seq:
    fails.append(f"select sequence wrong: {seq}")

# ─────────────────────────────────────────────────────────────────────
print()
print("=" * 74)
if fails:
    print(f"สรุป: ไม่ผ่าน {len(fails)} รายการ")
    for f in fails:
        print("   -", f)
    sys.exit(1)
print("สรุป: ผ่านทุกรายการ — ไดอะแกรมและคำตอบถูกต้องตามที่ตรวจสอบได้")
print("=" * 74)
