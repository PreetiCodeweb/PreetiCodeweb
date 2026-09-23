import random
random.seed(3)

W, H = 1269, 190
GRID_AVAIL = W - 995  # width available for the heatmap grid
FONT = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"
BG = "#050813"
BORDER = "#7c3aed"
PINK = "#ff2fb0"
PURPLE = "#8b5cf6"
CYAN = "#38bdf8"
WHITE = "#e6ecff"
DIM = "#8892b0"

parts = []
parts.append(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')
parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="{BG}"/>')
parts.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="12" fill="none" stroke="{BORDER}" stroke-width="2" opacity="0.6"/>')

# left: name + icon-ish label
parts.append(f'<text x="34" y="55" font-family="{FONT}" font-size="20" font-weight="700" fill="{WHITE}">PreetiCodeweb</text>')
parts.append(f'<text x="34" y="78" font-family="{FONT}" font-size="13" fill="{DIM}">GitHub Stats</text>')

stats = [
    ("180+", "Total Commits", PINK),
    ("25+", "Repositories", CYAN),
    ("5+", "Contributors", PURPLE),
    ("1.2k+", "Followers", "#fbbf24"),
]
sx = 250
for val, label, color in stats:
    parts.append(f'<text x="{sx}" y="52" font-family="{FONT}" font-size="21" font-weight="700" fill="{color}">{val}</text>')
    parts.append(f'<text x="{sx}" y="75" font-family="{FONT}" font-size="12.5" fill="{DIM}">{label}</text>')
    sx += 190

# divider
parts.append(f'<line x1="900" y1="25" x2="900" y2="{H-25}" stroke="{DIM}" stroke-width="1" opacity="0.3"/>')

# day labels
for i, d in enumerate(["Mon", "Wed", "Fri"]):
    parts.append(f'<text x="955" y="{55+i*26}" font-family="{FONT}" font-size="11" fill="{DIM}">{d}</text>')

# heatmap grid: 36 weeks x 7 days
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep"]
weeks = 39
gap = 2
cell = max(5, GRID_AVAIL // weeks - gap)
gx0 = 1000
gy0 = 30
colors_low_to_high = ["#141a33", "#2d1a4a", "#5b2a8a", "#a23bd6", "#ff2fb0"]

for w in range(weeks):
    # bias more activity mid-to-late year for a nice gradient look
    week_bias = 0.3 + 0.7 * (w / weeks)
    for d in range(7):
        r = random.random() * week_bias
        if r < 0.35:
            lvl = 0
        elif r < 0.55:
            lvl = 1
        elif r < 0.72:
            lvl = 2
        elif r < 0.88:
            lvl = 3
        else:
            lvl = 4
        x = gx0 + w * (cell + gap)
        y = gy0 + d * (cell + gap)
        color = colors_low_to_high[lvl]
        parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}"/>')

# month labels under grid
for i, m in enumerate(months):
    x = gx0 + i * (weeks * (cell + gap) / len(months))
    parts.append(f'<text x="{x}" y="{gy0 + 7*(cell+gap) + 14}" font-family="{FONT}" font-size="11" fill="{DIM}">{m}</text>')

parts.append('</svg>')

with open("/home/claude/profile-readme/assets/stats-banner.svg", "w") as f:
    f.write("\n".join(parts))

print("wrote stats-banner.svg")
