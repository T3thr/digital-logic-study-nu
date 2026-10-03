"""Generate vector teaching diagrams using only the Python standard library."""
from pathlib import Path
from html import escape

ASSETS = Path(__file__).parent / "assets"
ASSETS.mkdir(exist_ok=True)
BLUE = "#1E40AF"
GREEN = "#047857"
PURPLE = "#6D28D9"
AMBER = "#B45309"
INK = "#22292F"


def start(height, title, description):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10Z" fill="context-stroke"/></marker></defs>
<style>text{{font-family:Thonburi,"Noto Sans Thai",sans-serif;fill:{INK};font-size:20px}}.small{{font-size:16px}}.label{{font-size:18px;font-weight:700}}.mono{{font-family:Consolas,monospace}}</style>
<rect width="1120" height="{height}" fill="#fff"/>''']


def text(parts, x, y, content, color=INK, size=20, anchor="start", weight=400):
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="fill:{color};font-size:{size}px;font-weight:{weight}">{escape(content)}</text>')


def wire(parts, points, color=INK, width=3, arrow=False):
    parts.append(f'<path d="{points}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{chr(32)+"marker-end="+chr(34)+"url(#arrow)"+chr(34) if arrow else ""}/>')


def box(parts, x, y, w, h, color, fill, label, subtitle):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="2.5"/>')
    text(parts, x+w/2, y+h/2-3, label, color, 23, "middle", 700)
    text(parts, x+w/2, y+h/2+24, subtitle, color, 16, "middle")


def bus(parts, x, y, color=INK):
    wire(parts, f'M{x-4},{y+8} L{x+4},{y-8}', color, 2)
    text(parts, x, y-16, "4", color, 15, "middle")


def full():
    p = start(610, "วงจรหลายฟังก์ชัน 4 บิตด้วย 74283", "สองฝั่ง XOR กับ J แล้ว AND เลือกด้วย K; เข้า 74283 โดย C0 เท่ากับ 0; ผลบวก OR กับ G ทั้ง 4 บิต")
    text(p, 32, 42, "วงจรสมบูรณ์ · 4 บิต", INK, 25, weight=700)
    text(p, 32, 74, "A₁ / B₁ = LSB    ·    A₄ / B₄ = MSB    ·    บล็อก ×4 = เกตแยก 4 ตัว", "#4B5563", 18)
    for x, number, label in [(165,"01","กลับบิต"),(380,"02","เลือกฝั่ง"),(670,"03","บวกกับศูนย์"),(938,"04","บังคับค่า 1")]:
        text(p, x, 118, number + " · " + label, AMBER, 18, weight=700)
    for y, letter, color, fill in [(225,"A",BLUE,"#EFF6FF"),(385,"B",GREEN,"#ECFDF5")]:
        text(p, 22, y+7, letter+"[4:1]", color, 20, weight=700)
        wire(p, f'M104,{y} H150', color, 4, True)
        bus(p, 122, y, color)
        box(p, 150, y-45, 155, 90, color, fill, "XOR ×4", letter+"ᵢ ⊕ J")
        wire(p, f'M305,{y} H365', color, 4, True)
        bus(p, 329, y, color)
        box(p, 365, y-45, 150, 90, color, fill, "AND ×4", "กับ K̅" if letter=="A" else "กับ K")
        wire(p, f'M515,{y} H650', color, 4, True)
        bus(p, 591, y, color)
        text(p, 572, y-30, "X[4:1]" if letter=="A" else "Y[4:1]", color, 19, "middle", 700)
        text(p, 227, y-76, "J", PURPLE, 22, "middle", 700)
        wire(p, f'M227,{y-65} V{y-45}', PURPLE, 2.5, True)
        text(p, 440, y-76, "K̅ = NOT K" if letter=="A" else "K", PURPLE, 19, "middle", 700)
        wire(p, f'M440,{y-65} V{y-45}', PURPLE, 2.5, True)
    p.append('<rect x="650" y="195" width="200" height="220" rx="8" fill="#F5F0E4" stroke="#22292F" stroke-width="3"/>')
    text(p, 664, 231, "A[4:1]", BLUE, 17, weight=700)
    text(p, 664, 390, "B[4:1]", GREEN, 17, weight=700)
    text(p, 750, 295, "74283", INK, 32, "middle", 700)
    text(p, 750, 328, "4-bit adder", INK, 18, "middle")
    wire(p, 'M750,467 V415', INK, 2.5, True)
    text(p, 750, 493, "C₀ = 0", INK, 20, "middle", 700)
    wire(p, 'M815,415 V460', "#64748B", 2.5)
    text(p, 826, 455, "C₄ = 0", "#4B5563", 17)
    wire(p, 'M850,285 H945', INK, 4, True)
    bus(p, 900, 285)
    text(p, 895, 253, "Σ[4:1]", INK, 18, "middle", 700)
    box(p, 945, 240, 110, 100, AMBER, "#FFFBEB", "OR ×4", "Σᵢ ∨ G")
    text(p, 1000, 179, "G", PURPLE, 22, "middle", 700)
    wire(p, 'M1000,190 V240', PURPLE, 2.5, True)
    wire(p, 'M1055,285 H1096', AMBER, 4, True)
    text(p, 1091, 372, "S[4:1]", AMBER, 18, "end", 700)
    text(p, 1091, 402, "ผลลัพธ์", AMBER, 17, "end")
    p.append('<rect x="32" y="527" width="1056" height="57" rx="6" fill="#F8FAFC" stroke="#D8CFBC"/>')
    text(p, 54, 563, "Xᵢ = K̅·(Aᵢ ⊕ J)", BLUE, 21)
    text(p, 345, 563, "Yᵢ = K·(Bᵢ ⊕ J)", GREEN, 21)
    text(p, 635, 563, "Sᵢ = Σᵢ ∨ G", AMBER, 21)
    text(p, 890, 563, "i = 1, 2, 3, 4", INK, 20)
    p.append('</svg>')
    (ASSETS / "full-circuit.svg").write_text('\n'.join(p), encoding="utf-8")


def xor_gate(p, x, y, color):
    wire(p, f'M{x+5},{y-35} Q{x+27},{y} {x+5},{y+35} Q{x+56},{y+33} {x+77},{y} Q{x+56},{y-33} {x+5},{y-35}', color, 2.5)
    wire(p, f'M{x-4},{y-35} Q{x+18},{y} {x-4},{y+35}', color, 2.5)


def and_gate(p, x, y, color):
    wire(p, f'M{x},{y-32} H{x+31} C{x+79},{y-32} {x+79},{y+32} {x+31},{y+32} H{x} Z', color, 2.5)


def bit_slice():
    p = start(500, "วงจรย่อยหนึ่งบิต", "Ai และ Bi ผ่าน XOR และ AND ก่อนเข้าเซลล์บวกหนึ่งบิต; ผลบวก OR กับ G; ตัวทดเข้าศูนย์และตัวทดออกศูนย์")
    text(p, 32, 42, "วงจรย่อย 1 บิต · ทำซ้ำ i = 1, 2, 3, 4", INK, 25, weight=700)
    text(p, 32, 75, "รูปนี้อธิบายลอจิกทีละบิตภายในวงจร ใช้ไอซี 74283 เพียง 1 ตัวในผังเต็ม", "#4B5563", 18)
    for y, letter, color in [(170,"A",BLUE),(325,"B",GREEN)]:
        text(p, 32, y-8, letter+"ᵢ", color, 22, weight=700)
        wire(p, f'M80,{y-15} H195', color, 3)
        text(p, 110, y+33, "J", PURPLE, 20, weight=700)
        wire(p, f'M132,{y+25} H165 V{y+15} H195', PURPLE, 2.5)
        xor_gate(p, 180, y, color)
        wire(p, f'M257,{y} H325 V{y-15} H355', color, 3)
        text(p, 283, y-40, letter+"ᵢ ⊕ J", color, 18, "middle")
        and_gate(p, 355, y, color)
        text(p, 284, y+47, "K̅" if letter=="A" else "K", PURPLE, 20, weight=700)
        wire(p, f'M305,{y+40} H335 V{y+15} H355', PURPLE, 2.5)
        wire(p, f'M423,{y} H575', color, 3, True)
        text(p, 500, y-14, "Xᵢ" if letter=="A" else "Yᵢ", color, 21, "middle", 700)
    p.append('<rect x="575" y="130" width="175" height="235" rx="8" fill="#F5F0E4" stroke="#22292F" stroke-width="2.5"/>')
    text(p, 662, 215, "FULL", INK, 24, "middle", 700)
    text(p, 662, 248, "ADDER", INK, 24, "middle", 700)
    text(p, 662, 282, "บิต i", INK, 19, "middle")
    text(p, 662, 104, "Cᵢ₋₁ = 0", INK, 19, "middle")
    wire(p, 'M662,113 V130', INK, 2.5, True)
    wire(p, 'M662,365 V397', INK, 2.5, True)
    text(p, 662, 422, "Cᵢ = 0", INK, 19, "middle")
    wire(p, 'M750,235 H904', INK, 3)
    text(p, 807, 219, "Σᵢ", INK, 22, "middle", 700)
    wire(p, 'M892,218 Q917,250 892,282 Q944,282 973,250 Q944,218 892,218', AMBER, 2.5)
    text(p, 832, 319, "G", PURPLE, 22, weight=700)
    wire(p, 'M855,310 H875 V265 H904', PURPLE, 2.5)
    wire(p, 'M973,250 H1050', AMBER, 3, True)
    text(p, 1062, 257, "Sᵢ", AMBER, 22, weight=700)
    p.append('<rect x="32" y="449" width="1056" height="36" rx="5" fill="#EFF6FF"/>')
    text(p, 54, 473, "Xᵢ และ Yᵢ ไม่เป็น 1 พร้อมกัน เพราะ K·K̅ = 0; เมื่อ C₀ = 0 ตัวทดทุกบิตจึงเป็น 0", BLUE, 18)
    p.append('</svg>')
    (ASSETS / "bit-slice.svg").write_text('\n'.join(p), encoding="utf-8")


if __name__ == "__main__":
    full()
    bit_slice()
    print("Generated full-circuit.svg and bit-slice.svg")
