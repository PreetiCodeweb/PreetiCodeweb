from PIL import Image, ImageEnhance
import html as htmlmod

SRC = "/home/claude/ascii-portrait/source.png"
OUT = "/home/claude/profile-readme/assets/terminal-banner.svg"
FONT = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

BG = "#050813"
BORDER = "#7c3aed"
PINK = "#ff2fb0"
PURPLE = "#8b5cf6"
CYAN = "#38bdf8"
WHITE = "#e6ecff"
DIM = "#3a4468"

# ---------------- portrait grid (true photo data) ----------------
PORTRAIT_H = 620.0
FONT_ASPECT = 0.55
COLS = 148

im = Image.open(SRC).convert("RGB")
im = ImageEnhance.Contrast(im).enhance(1.15)
im = ImageEnhance.Color(im).enhance(1.2)
im = ImageEnhance.Sharpness(im).enhance(1.4)
PW, PH = im.size
ROWS = max(1, int(COLS * (PH / PW) * FONT_ASPECT))

small = im.resize((COLS, ROWS), Image.Resampling.BOX)
px = small.load()

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
N = len(RAMP)

def luminance(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b

grid = []
for y in range(ROWS):
    row = []
    for x in range(COLS):
        r, g, b = px[x, y]
        lum = luminance(r, g, b) / 255.0
        idx = int(lum * (N - 1))
        idx = max(0, min(N - 1, idx))
        row.append((RAMP[idx], r, g, b))
    grid.append(row)

cell_w = PORTRAIT_W = COLS and (PORTRAIT_H / ROWS) * FONT_ASPECT
cell_h = PORTRAIT_H / ROWS
PORTRAIT_W = COLS * cell_w

PAD = 34
RIGHT_W = 650.0
W = PAD + PORTRAIT_W + 46 + RIGHT_W + PAD
H = PORTRAIT_H + PAD * 2

svg = []
svg.append(f'<svg width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg">')
svg.append(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" rx="14" fill="{BG}"/>')
svg.append(f'<rect x="3" y="3" width="{W-6:.0f}" height="{H-6:.0f}" rx="12" fill="none" stroke="{BORDER}" stroke-width="2" opacity="0.55"/>')

# portrait
svg.append(f'<g font-family="{FONT}" font-size="{cell_h*0.92:.2f}">')
ox, oy = PAD, PAD
for y, row in enumerate(grid):
    ty = oy + y * cell_h + cell_h * 0.82
    spans = []
    for x, (ch, r, g, b) in enumerate(row):
        if ch == " ":
            continue
        cx = ox + x * cell_w
        esc = htmlmod.escape(ch)
        spans.append(f'<tspan x="{cx:.2f}" y="{ty:.2f}" fill="rgb({r},{g},{b})">{esc}</tspan>')
    if spans:
        svg.append("<text>" + "".join(spans) + "</text>")
svg.append("</g>")

# stray accent marks like the reference
for (ax, ay) in [(ox+40, oy+70), (ox+PORTRAIT_W-30, oy+PORTRAIT_H-20)]:
    svg.append(f'<text x="{ax:.0f}" y="{ay:.0f}" font-family="{FONT}" font-size="15" fill="{PINK}" opacity="0.7">+</text>')

# divider
div_x = ox + PORTRAIT_W + 23
svg.append(f'<line x1="{div_x:.0f}" y1="18" x2="{div_x:.0f}" y2="{H-18:.0f}" stroke="{BORDER}" stroke-width="1" opacity="0.35"/>')

# ---------------- right info panel ----------------
rx = div_x + 46
y = PAD + 12

def line(text, dy=26, size=16, color=WHITE, weight="normal"):
    global y
    svg.append(f'<text x="{rx}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" font-weight="{weight}">{text}</text>')
    y += dy

def kv(label, value, dy=25):
    global y
    svg.append(f'<text x="{rx}" y="{y}" font-family="{FONT}" font-size="15" fill="{CYAN}">{label}:</text>')
    svg.append(f'<text x="{rx+150}" y="{y}" font-family="{FONT}" font-size="15" fill="{WHITE}">{value}</text>')
    y += dy

def section(label, dy=27):
    global y
    svg.append(f'<text x="{rx}" y="{y}" font-family="{FONT}" font-size="15.5" fill="{PINK}" font-weight="700">{label}</text>')
    y += dy

svg.append(f'<text x="{rx}" y="{y}" font-family="{FONT}" font-size="24" font-weight="700" fill="{PINK}">preeti<tspan fill="{PURPLE}">@</tspan><tspan fill="{CYAN}">devbox</tspan></text>')
y += 18
svg.append(f'<line x1="{rx}" y1="{y}" x2="{W-PAD:.0f}" y2="{y}" stroke="{DIM}" stroke-width="1" stroke-dasharray="4,3"/>')
y += 30

kv("OS", "AI/ML x CS x Art")
kv("Host", "Kolkata, West Bengal, IN")
kv("Kernel", "Python 3.x, Node/Express")
kv("Role", "AI Engineer / Builder")
kv("Status", "1st-yr CS (AI &#38; ML) &#183; Grad 2030")
y += 12
svg.append(f'<line x1="{rx}" y1="{y-6}" x2="{W-PAD:.0f}" y2="{y-6}" stroke="{DIM}" stroke-width="1" stroke-dasharray="4,3"/>')

section("Languages.Programming:")
line("  Python, JS/TS, C++", dy=30)

section("Languages.ML/AI:")
line("  RAG, LangChain, LlamaIndex,", dy=24)
line("  PyTorch, TensorFlow, Vector DBs", dy=30)

section("Stacks:")
line("  FastAPI, Node/Express, React,", dy=24)
line("  MongoDB, SQLite", dy=30)

section("Hobbies.Craft:")
line("  Digital art, cinematic portfolio design", dy=30)

section("Currently.Building:")
line("  OmniMind &#183; MedSync &#183; VITALIS", dy=32)

section("Contact::", dy=24)
line("  github.com/PreetiCodeweb", dy=20, color=CYAN)

svg.append('</svg>')

with open(OUT, "w") as f:
    f.write("\n".join(svg))

print(f"grid {COLS}x{ROWS}, portrait {PORTRAIT_W:.0f}x{PORTRAIT_H:.0f}, canvas {W:.0f}x{H:.0f}")
