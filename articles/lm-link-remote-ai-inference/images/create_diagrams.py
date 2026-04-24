#!/usr/bin/env python3
"""Create article diagrams with Pillow for LM Link article."""
from PIL import Image, ImageDraw, ImageFont
import math, os

def get_font(size, bold=False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else \
           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size) if os.path.exists(name) else ImageFont.load_default()

def get_mono_font(size):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    return ImageFont.truetype(name, size) if os.path.exists(name) else ImageFont.load_default()

def rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    r = radius
    if fill:
        draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
        draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
        draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
        draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
        draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
        draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)
    if outline:
        draw.arc([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)

def draw_arrow(draw, x1, y1, x2, y2, color, width=2, head_size=12):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = angle + math.pi * 0.8, angle - math.pi * 0.8
    draw.polygon([(x2, y2),
                  (x2 + head_size * math.cos(a1), y2 + head_size * math.sin(a1)),
                  (x2 + head_size * math.cos(a2), y2 + head_size * math.sin(a2))], fill=color)

def text_center(draw, x, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((x - w // 2, y), text, fill=fill, font=font, anchor="lm")

# ============================================================
# DIAGRAM 1: LM Link Architecture
# ============================================================
W, H = 1440, 700
img = Image.new("RGB", (W, H), "#0f172a")
draw = ImageDraw.Draw(img)

# Title
font_title = get_font(32, bold=True)
text_center(draw, W // 2, 40, "LM Link Architecture", font_title, "#e5e5e5")

# Subtitle
font_sub = get_font(18)
text_center(draw, W // 2, 80, "End-to-end encrypted P2P mesh network — powered by Tailscale", font_sub, "#94a3b8")

# Device boxes
devices = [
    {"name": "MacBook Pro M4", "model": "Qwen 3.6 27B", "icon": "💻", "x": 140, "y": 220, "w": 280, "h": 160, "fill": "#1e3a5f", "outline": "#4a9eed"},
    {"name": "Cloud VPS", "model": "llmster (headless)", "icon": "🖥️", "x": 580, "y": 220, "w": 280, "h": 160, "fill": "#2d1b69", "outline": "#8b5cf6"},
    {"name": "GPU Rig", "model": "Llama 3 70B", "icon": "⚡", "x": 1020, "y": 220, "w": 280, "h": 160, "fill": "#1a4d2e", "outline": "#22c55e"},
]

for d in devices:
    cx, cy = d["x"], d["y"]
    w, h = d["w"], d["h"]
    rounded_rect(draw, [cx, cy, cx + w, cy + h], 12, fill=d["fill"], outline=d["outline"], width=2)
    
    # Device name
    font_dev = get_font(20, bold=True)
    text_center(draw, cx + w // 2, cy + 35, d["name"], font_dev, "#ffffff")
    
    # Model label
    font_model = get_font(16)
    text_center(draw, cx + w // 2, cy + 70, d["model"], font_model, "#cbd5e1")
    
    # Status dot
    draw.ellipse([cx + w // 2 - 6, cy + 100, cx + w // 2 + 6, cy + 112], fill="#22c55e")
    font_status = get_font(13)
    text_center(draw, cx + w // 2, cy + 130, "Connected", font_status, "#22c55e")

# Draw mesh connections (dashed lines between all pairs)
def draw_dashed_line(draw, x1, y1, x2, y2, color, dash_len=12, gap_len=8, width=2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance == 0:
        return
    dx, dy = (x2 - x1) / distance, (y2 - y1) / distance
    pos = 0
    while pos < distance:
        end = min(pos + dash_len, distance)
        draw.line([(x1 + dx * pos, y1 + dy * pos), (x1 + dx * end, y1 + dy * end)], fill=color, width=width)
        pos += dash_len + gap_len

# MacBook to VPS
draw_dashed_line(draw, 420, 300, 580, 300, "#4a9eed")
# VPS to GPU Rig
draw_dashed_line(draw, 860, 300, 1020, 300, "#22c55e")
# MacBook to GPU Rig (curved - via bottom)
draw_dashed_line(draw, 280, 380, 1160, 380, "#94a3b8")

# Encryption label
font_enc = get_font(14)
text_center(draw, 500, 290, "E2E Encrypted", font_enc, "#60a5fa")
text_center(draw, 940, 290, "E2E Encrypted", font_enc, "#60a5fa")
text_center(draw, 720, 370, "E2E Encrypted (Tailscale Mesh)", font_enc, "#94a3b8")

# Bottom section - OpenAI compatible
y_bottom = 460
rounded_rect(draw, [200, y_bottom, 1240, y_bottom + 120], 12, fill="#111827", outline="#334155", width=2)

font_api = get_font(18, bold=True)
text_center(draw, 720, y_bottom + 30, "OpenAI-Compatible API on Every Device", font_api, "#e5e5e5")

font_code = get_mono_font(15)
code_lines = [
    "curl http://localhost:1234/v1/chat/completions",
    "curl http://localhost:1234/v1/models          # Lists ALL linked models",
]
for i, line in enumerate(code_lines):
    text_center(draw, 720, y_bottom + 60 + i * 25, line, font_code, "#f472b6")

# Works with tools section
y_tools = 610
font_tools = get_font(14)
tools_text = "Works with: Codex  ·  Claude Code  ·  OpenCode  ·  Any OpenAI SDK  ·  curl"
text_center(draw, W // 2, y_tools, tools_text, font_tools, "#94a3b8")

# Tailscale badge
y_badge = 645
font_badge = get_font(13)
text_center(draw, W // 2, y_badge, "🔒 No ports exposed  ·  No public internet  ·  Zero-config NAT traversal", font_badge, "#6b7280")

img.save("/tmp/blog-repo/articles/lm-link-remote-ai-inference/images/architecture.png", "PNG", optimize=True)
sz = os.path.getsize("/tmp/blog-repo/articles/lm-link-remote-ai-inference/images/architecture.png")
print(f"architecture.png: {img.size[0]}x{img.size[1]}, {sz} bytes")

# ============================================================
# DIAGRAM 2: Setup Flow
# ============================================================
W2, H2 = 1440, 500
img2 = Image.new("RGB", (W2, H2), "#0f172a")
draw2 = ImageDraw.Draw(img2)

# Title
text_center(draw2, W2 // 2, 40, "Setup in 4 Steps", font_title, "#e5e5e5")

steps = [
    {"num": "1", "title": "Install llmster", "code": "curl -fsSL \\\n  lmstudio.ai/install.sh \\\n  | bash", "x": 50},
    {"num": "2", "title": "Login", "code": "lms login", "x": 390},
    {"num": "3", "title": "Enable Link", "code": "lms link enable", "x": 730},
    {"num": "4", "title": "Use Models", "code": "curl localhost:1234 \\\n  /v1/chat/completions", "x": 1070},
]

box_w = 280
box_h = 260
box_y = 110

for i, step in enumerate(steps):
    sx = step["x"]
    
    # Step number circle
    cx = sx + box_w // 2
    draw2.ellipse([cx - 22, box_y - 10, cx + 22, box_y + 34], fill="#3b82f6")
    font_num = get_font(22, bold=True)
    text_center(draw2, cx, box_y + 12, step["num"], font_num, "#ffffff")
    
    # Box
    rounded_rect(draw2, [sx, box_y + 40, sx + box_w, box_y + 40 + box_h - 40], 12, fill="#1e293b", outline="#334155", width=2)
    
    # Title
    font_step_title = get_font(18, bold=True)
    text_center(draw2, cx, box_y + 80, step["title"], font_step_title, "#f1f5f9")
    
    # Code block background
    code_y = box_y + 105
    code_h = 85
    rounded_rect(draw2, [sx + 15, code_y, sx + box_w - 15, code_y + code_h], 8, fill="#0f172a", outline="#1f2937", width=1)
    
    # Code text
    lines = step["code"].split("\n")
    font_code2 = get_mono_font(14)
    for j, line in enumerate(lines):
        draw2.text((sx + 25, code_y + 12 + j * 22), line, fill="#f472b6", font=font_code2)
    
    # Arrow between steps
    if i < len(steps) - 1:
        arrow_x1 = sx + box_w + 5
        arrow_x2 = steps[i + 1]["x"] - 5
        arrow_y = box_y + 12
        draw_arrow(draw2, arrow_x1, arrow_y, arrow_x2, arrow_y, "#4a9eed", width=3, head_size=14)

# Bottom result
y_result = box_y + box_h + 30
rounded_rect(draw2, [200, y_result, 1240, y_result + 70], 12, fill="#1a4d2e", outline="#22c55e", width=2)
font_result = get_font(18, bold=True)
text_center(draw2, W2 // 2, y_result + 25, "✅ Done! Your devices find each other automatically.", font_result, "#22c55e")
font_result_sub = get_font(14)
text_center(draw2, W2 // 2, y_result + 50, "Free for up to 2 users, 5 devices each (10 total) · No ports to configure · Zero-config", font_result_sub, "#94a3b8")

img2.save("/tmp/blog-repo/articles/lm-link-remote-ai-inference/images/setup-flow.png", "PNG", optimize=True)
sz2 = os.path.getsize("/tmp/blog-repo/articles/lm-link-remote-ai-inference/images/setup-flow.png")
print(f"setup-flow.png: {img2.size[0]}x{img2.size[1]}, {sz2} bytes")
