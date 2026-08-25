import os
from html import escape
import urllib.request

FONT = "'Fira Code', 'JetBrains Mono', 'Cascadia Mono', 'Courier New', monospace"

def esc(value):
    return escape(str(value), quote=True)

# ============================================================
# SVG FILTERS
# ============================================================
retro_filters = """
<!-- RETRO PHOSPHOR GLOW -->
<filter id="glowCyan" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.4" result="blur1"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur2"/>
    <feFlood flood-color="#20DFFF" flood-opacity="0.38" result="cyanGlow"/>
    <feComposite in="cyanGlow" in2="blur2" operator="in" result="cyanComposite"/>
    <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="cyanComposite"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>

<filter id="glowMint" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.3" result="blur1"/>
    <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur2"/>
    <feFlood flood-color="#36E3A3" flood-opacity="0.42" result="mintGlow"/>
    <feComposite in="mintGlow" in2="blur2" operator="in" result="mintComposite"/>
    <feMerge>
        <feMergeNode in="blur1"/>
        <feMergeNode in="mintComposite"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>

<filter id="glowWhite" x="-40%" y="-40%" width="180%" height="180%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceGraphic" stdDeviation="1.1" result="blur"/>
    <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
    </feMerge>
</filter>
"""

# ============================================================
# FIXED-COLUMN HELPERS
# ============================================================
def text(x, y, value, cls):
    return f'<text x="{x}" y="{y}" class="{cls}">{esc(value)}</text>'

def leader(x1, x2, y, opacity=0.52):
    return (
        f'<line x1="{x1}" y1="{y - 5}" x2="{x2}" y2="{y - 5}" '
        f'stroke="#475569" stroke-width="1" stroke-linecap="round" '
        f'stroke-dasharray="1 7" opacity="{opacity}"/>'
    )

def reveal_clip(cid, y, start, duration="0.35s"):
    return (
        f'<clipPath id="{cid}">'
        f'    <rect x="30" y="{y - 20}" width="0" height="28">'
        f'        <animate attributeName="width" from="0" to="940" dur="{duration}" begin="{start}s" fill="freeze"/>'
        f'    </rect>'
        f'</clipPath>'
    )

def command_line(y, command, delay, index):
    cid = f"cmd_clip_{index}"
    clip = reveal_clip(cid, y, delay)
    body = (
        f'<g clip-path="url(#{cid})">'
        f'    <g filter="url(#glowWhite)">'
        f'        {text(36, y, "praneeth@devbox", "prompt-user")}'
        f'        {text(173, y, ":", "prompt-sep")}'
        f'        {text(184, y, "~$", "prompt-path")}'
        f'        {text(214, y, command, "command")}'
        f'    </g>'
        f'</g>'
    )
    return clip, body

def data_row(y, pieces, delay, index):
    cid = f"row_clip_{index}"
    clip = reveal_clip(cid, y, delay)
    body = (
        f'<g clip-path="url(#{cid})">'
        f'    <g filter="url(#glowCyan)">'
        f'        {"".join(pieces)}'
        f'    </g>'
        f'</g>'
    )
    return clip, body

def build_retro_terminal_content():
    clips = []
    content = []
    VALUE_X = 470

    # COMMAND 1: WHOAMI
    clip, body = command_line(78, "whoami", 0.35, 1)
    clips.append(clip)
    content.append(body)

    # IDENTITY
    pieces = [
        text(48, 102, "PRANEETH REDDY", "name"),
        leader(238, 448, 102),
        text(VALUE_X, 102, "Software Developer | Cyber Security | DevOps Engineer", "value"),
    ]
    clip, body = data_row(102, pieces, 0.72, 10)
    clips.append(clip)
    content.append(body)

    # COMMAND 2: EDUCATION
    clip, body = command_line(138, "cat ~/.education", 1.15, 2)
    clips.append(clip)
    content.append(body)

    # EDUCATION
    education = [
        (162, "┌─", "DEGREE", "B.Tech in Computer Science & Engineering", 1.48),
        (186, "└─", "INST.",  "Amrita Vishwa Vidyapeetham (2021 – 2025)", 1.78),
    ]
    for i, (y, branch, key, value, delay) in enumerate(education):
        pieces = [
            text(48, y, branch, "branch"),
            text(82, y, key, "key"),
            leader(155, 448, y),
            text(VALUE_X, y, value, "value"),
        ]
        clip, body = data_row(y, pieces, delay, 20 + i)
        clips.append(clip)
        content.append(body)

    # COMMAND 3: SKILLS
    clip, body = command_line(222, "./skills.sh --summary", 2.38, 3)
    clips.append(clip)
    content.append(body)

    # SKILLS
    skills = [
        (246, "Core Tech",   "Python, Go, C++, TypeScript, Rust, Linux, GCP",    2.68),
        (270, "Security",    "Cryptography, ZK-Proofs, QKD, PenTesting, NetSec", 2.98),
        (294, "DevOps/Cloud","Docker, Kubernetes, Terraform, CI/CD, Microservices", 3.28),
        (318, "Hardware",    "LoRa Mesh, ESP32 Microcontrollers, Raspberry Pi",  3.58),
    ]
    for i, (y, key, value, delay) in enumerate(skills):
        pieces = [
            text(48, y, "[+]", "tag"),
            text(92, y, key, "key"),
            leader(205, 448, y),
            text(VALUE_X, y, value, "value"),
        ]
        clip, body = data_row(y, pieces, delay, 40 + i)
        clips.append(clip)
        content.append(body)

    # COMMAND 4: PROJECTS
    clip, body = command_line(354, "cat ~/.projects", 4.05, 4)
    clips.append(clip)
    content.append(body)

    # FEATURED PROJECTS
    projects = [
        (378, "[01]", "Ternix    ", "Cross-Platform SSH & Remote Session Manager",   4.35),
        (402, "[02]", "Bloom     ", "Floating Desktop Widget & Voice Dictation",       4.65),
        (426, "[03]", "DevFlow   ", "Interactive Visual Developer Workflow Platform", 4.95),
        (450, "[04]", "CloudShare", "Passwordless Zero-Knowledge File Storage",        5.25),
    ]
    for i, (y, number, proj, desc, delay) in enumerate(projects):
        pieces = [
            text(48, y, number, "muted-bold"),
            text(95, y, proj, "venue"),
            leader(210, 448, y),
            text(VALUE_X, y, desc, "value"),
        ]
        clip, body = data_row(y, pieces, delay, 60 + i)
        clips.append(clip)
        content.append(body)

    # COMMAND 5: CONTACT
    clip, body = command_line(486, "./contact.sh", 5.75, 5)
    clips.append(clip)
    content.append(body)

    contacts = [
        (510, "Email",    "connectwithpraneeth@gmail.com",       6.05),
        (534, "LinkedIn", "linkedin.com/in/connectwithpraneeth", 6.35),
        (558, "GitHub",   "github.com/PraneethReddy-github",     6.65),
    ]
    for i, (y, key, value, delay) in enumerate(contacts):
        pieces = [
            text(48, y, key, "key"),
            text(125, y, "›", "arrow"),
            leader(150, 448, y),
            text(VALUE_X, y, value, "value"),
        ]
        clip, body = data_row(y, pieces, delay, 80 + i)
        clips.append(clip)
        content.append(body)

    # FINAL PROMPT
    final_y = 596
    final_clip_id = "final_prompt_clip"
    final_clip = reveal_clip(final_clip_id, final_y, 7.10)
    clips.append(final_clip)

    final_prompt = (
        f'<g clip-path="url(#{final_clip_id})">'
        f'    <g filter="url(#glowMint)">'
        f'        {text(36, final_y, "praneeth@devbox", "prompt-user")}'
        f'        {text(173, final_y, ":", "prompt-sep")}'
        f'        {text(184, final_y, "~$", "prompt-path")}'
        f'    </g>'
        f'</g>'
    )
    content.append(final_prompt)

    # CURSOR
    cursor = f"""
<g filter="url(#glowMint)">
    <rect x="214" y="{final_y - 15}" width="9" height="17" rx="1" class="cursor" opacity="0">
        <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.01;0.05;0.45;0.5;1" dur="1.15s" begin="7.50s" repeatCount="indefinite"/>
    </rect>
</g>
"""
    return "\n".join(clips), "\n".join(content), cursor

# MULTI-LINE SYNCHRONIZED HIGH-INTENSITY GLITCH SYSTEM
retro_glitch_defs = """
<clipPath id="glitchA"><rect x="0" y="60" width="1000" height="24"/></clipPath>
<clipPath id="glitchB"><rect x="0" y="126" width="1000" height="35"/></clipPath>
<clipPath id="glitchC"><rect x="0" y="196" width="1000" height="40"/></clipPath>
<clipPath id="glitchD"><rect x="0" y="263" width="1000" height="35"/></clipPath>
<clipPath id="glitchE"><rect x="0" y="334" width="1000" height="45"/></clipPath>
<clipPath id="glitchF"><rect x="0" y="414" width="1000" height="50"/></clipPath>
<clipPath id="glitchG"><rect x="0" y="474" width="1000" height="40"/></clipPath>
<clipPath id="glitchH"><rect x="0" y="548" width="1000" height="45"/></clipPath>

<clipPath id="frag1"><rect x="50" y="90" width="320" height="12"/></clipPath>
<clipPath id="frag2"><rect x="450" y="240" width="400" height="14"/></clipPath>
<clipPath id="frag3"><rect x="120" y="370" width="500" height="16"/></clipPath>
<clipPath id="frag4"><rect x="40" y="505" width="420" height="14"/></clipPath>
"""

def build_glitch(master_id="terminalContent"):
    return f"""
<!-- HIGH INTENSITY MULTI-LINE SYNCHRONIZED CYBER GLITCH SYSTEM (STRICTLY CLIPPED TO BODY AREA y >= 40) -->
<g id="terminalGlitch" clip-path="url(#bodyArea)" pointer-events="none">

    <!-- WAVE 1: MULTI-LINE BURST ON SLICES A, C, E, G (Fires together at t = 1.8s) -->
    <g clip-path="url(#glitchA)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.4;1;0;0" keyTimes="0;0.36;0.375;0.395;0.41;0.44;1" dur="4.8s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;-55 0;75 0;-25 1;0 0" keyTimes="0;0.375;0.395;0.41;0.44" dur="4.8s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(-8 0)" opacity="0.95" style="color:#00E5FF"/>
            <use href="#{master_id}" transform="translate(10 0)" opacity="0.8" style="color:#FF00A8"/>
        </g>
    </g>

    <g clip-path="url(#glitchC)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.3;1;0;0" keyTimes="0;0.36;0.375;0.395;0.41;0.44;1" dur="4.8s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;68 0;-45 0;30 -1;0 0" keyTimes="0;0.375;0.395;0.41;0.44" dur="4.8s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(9 0)" opacity="0.9" style="color:#FF0055"/>
            <use href="#{master_id}" transform="translate(-11 0)" opacity="0.85" style="color:#00E5FF"/>
        </g>
    </g>

    <g clip-path="url(#glitchE)" opacity="0">
        <animate attributeName="opacity" values="0;0;0.95;0.2;1;0;0" keyTimes="0;0.36;0.375;0.395;0.41;0.44;1" dur="4.8s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;-80 0;60 0;-30 0;0 0" keyTimes="0;0.375;0.395;0.41;0.44" dur="4.8s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(-12 0)" opacity="0.9"/>
        </g>
    </g>

    <g clip-path="url(#glitchG)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.3;0.9;0;0" keyTimes="0;0.36;0.375;0.395;0.41;0.44;1" dur="4.8s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;72 0;-50 0;22 0;0 0" keyTimes="0;0.375;0.395;0.41;0.44" dur="4.8s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(14 0)" opacity="0.85" style="color:#FF00A8"/>
        </g>
    </g>

    <!-- WAVE 2: MULTI-LINE BURST ON SLICES B, D, F, H (Fires together at t = 3.2s) -->
    <g clip-path="url(#glitchB)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.25;1;0;0" keyTimes="0;0.62;0.635;0.655;0.67;0.70;1" dur="5.2s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;65 0;-70 1;35 -1;0 0" keyTimes="0;0.635;0.655;0.67;0.70" dur="5.2s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(10 0)" opacity="0.9" style="color:#FF00A8"/>
            <use href="#{master_id}" transform="translate(-8 0)" opacity="0.8" style="color:#00E5FF"/>
        </g>
    </g>

    <g clip-path="url(#glitchD)" opacity="0">
        <animate attributeName="opacity" values="0;0;0.95;0.2;1;0;0" keyTimes="0;0.62;0.635;0.655;0.67;0.70;1" dur="5.2s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;-75 0;55 0;-30 0;0 0" keyTimes="0;0.635;0.655;0.67;0.70" dur="5.2s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(-11 0)" opacity="0.9" style="color:#00E5FF"/>
        </g>
    </g>

    <g clip-path="url(#glitchF)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.35;0.9;0;0" keyTimes="0;0.62;0.635;0.655;0.67;0.70;1" dur="5.2s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;82 0;-60 0;28 0;0 0" keyTimes="0;0.565;0.59;0.61;0.65" dur="7.1s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(12 0)" opacity="0.85" style="color:#FF0055"/>
        </g>
    </g>

    <g clip-path="url(#glitchH)" opacity="0">
        <animate attributeName="opacity" values="0;0;1;0.15;0.95;0;0" keyTimes="0;0.62;0.635;0.655;0.67;0.70;1" dur="5.2s" repeatCount="indefinite"/>
        <g>
            <animateTransform attributeName="transform" type="translate" values="0 0;-68 0;48 0;-20 0;0 0" keyTimes="0;0.325;0.35;0.365;0.40" dur="5.9s" repeatCount="indefinite"/>
            <use href="#{master_id}" transform="translate(-9 0)" opacity="0.9"/>
        </g>
    </g>

    <!-- INTENSE DIGITAL FRAGMENT TEARING BARS -->
    <g opacity="0">
        <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.36;0.38;0.43" dur="4.8s" repeatCount="indefinite"/>
        <rect x="50" y="90" width="320" height="12" fill="#00E5FF" opacity="0.85">
            <animateTransform attributeName="transform" type="translate" values="0 0;75 0;-35 0;0 0" dur="4.8s" repeatCount="indefinite"/>
        </rect>
    </g>

    <g opacity="0">
        <animate attributeName="opacity" values="0;0;1;0" keyTimes="0;0.62;0.64;0.69" dur="5.2s" repeatCount="indefinite"/>
        <rect x="450" y="240" width="400" height="14" fill="#FF0055" opacity="0.9">
            <animateTransform attributeName="transform" type="translate" values="0 0;-80 0;45 0;0 0" dur="5.2s" repeatCount="indefinite"/>
        </rect>
    </g>

    <!-- HIGH-ENERGY DIGITAL FULL FLASH BARS (CLIPPED TO BODY y >= 40) -->
    <rect x="0" y="42" width="1000" height="3" fill="#FFFFFF" opacity="0">
        <animate attributeName="opacity" values="0;0;0.85;0;0" keyTimes="0;0.37;0.375;0.395;1" dur="4.8s" repeatCount="indefinite"/>
    </rect>
    <rect x="0" y="42" width="1000" height="3" fill="#00E5FF" opacity="0">
        <animate attributeName="opacity" values="0;0;0.85;0;0" keyTimes="0;0.63;0.635;0.655;1" dur="5.2s" repeatCount="indefinite"/>
    </rect>

</g>
"""

def generate_svg(is_dark=True):
    width = 1000
    height = 660
    
    if is_dark:
        bg_start = "#0C0F17"
        bg_end = "#020305"
        border_color = "#1E293B"
        divider_color = "#1E293B"
        titlebar_bg = "#080B10"
        scanline_op = "0.025"
    else:
        bg_start = "#F8FAFC"
        bg_end = "#F1F5F9"
        border_color = "#CBD5E1"
        divider_color = "#CBD5E1"
        titlebar_bg = "#E2E8F0"
        scanline_op = "0.012"

    clips, content, cursor = build_retro_terminal_content()

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <radialGradient id="bgGlow" cx="50%" cy="15%" r="85%">
    <stop offset="0%" stop-color="{bg_start}"/>
    <stop offset="100%" stop-color="{bg_end}"/>
  </radialGradient>

  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#FFFFFF" opacity="{scanline_op}"/>
  </pattern>

  <clipPath id="bodyArea"><rect x="0" y="40" width="{width}" height="620"/></clipPath>

{retro_filters}

  <style>
    text, tspan {{
        font-family: 'Fira Code', 'JetBrains Mono', 'Cascadia Mono', 'Courier New', monospace;
        white-space: pre;
        dominant-baseline: auto;
    }}
    .prompt-user {{ fill: #36E3A3; font-size: 16px; font-weight: 700; letter-spacing: 0.05px; }}
    .prompt-sep  {{ fill: #64748B; font-size: 16px; font-weight: 500; }}
    .prompt-path {{ fill: #38BDF8; font-size: 16px; font-weight: 700; }}
    .command     {{ fill: #F8FAFC; font-size: 16.5px; font-weight: 700; letter-spacing: 0.03px; }}
    .name        {{ fill: #38BDF8; font-size: 17px; font-weight: 800; letter-spacing: 0.6px; }}
    .key         {{ fill: #34D399; font-size: 15px; font-weight: 700; letter-spacing: 0.05px; }}
    .branch      {{ fill: #64748B; font-size: 15px; font-weight: 700; }}
    .tag         {{ fill: #38BDF8; font-size: 15px; font-weight: 700; }}
    .arrow       {{ fill: #34D399; font-size: 19px; font-weight: 800; }}
    .muted-bold  {{ fill: #64748B; font-size: 14.5px; font-weight: 700; }}
    .venue       {{ fill: #38BDF8; font-size: 14.5px; font-weight: 700; }}
    .value       {{ fill: #D7DEE8; font-size: 16px; font-weight: 450; letter-spacing: 0; }}
    .cursor      {{ fill: #34E6A5; }}
    .term-title  {{ font-family: 'Fira Code', 'JetBrains Mono', 'Courier New', Consolas, monospace; font-size: 13.5px; fill: #64748B; letter-spacing: 0.5px; font-weight: bold; }}
  </style>

{retro_glitch_defs}

{clips}
</defs>

<!-- BASE CONTAINER & BACKGROUND -->
<rect width="{width}" height="{height}" rx="14" fill="url(#bgGlow)"/>

<!-- TERMINAL BODY BACKGROUND SCANLINES -->
<g clip-path="url(#bodyArea)">
  <rect x="0" y="40" width="{width}" height="620" fill="url(#scanlines)"/>
</g>

<!-- STABLE ANCHORED DARK TITLEBAR HEADER -->
<g id="titlebar">
  <path d="M 1,14 Q 1,1 14,1 L {width-14},1 Q {width-1},1 {width-1},14 L {width-1},40 L 1,40 Z" fill="{titlebar_bg}"/>
  <line x1="0" y1="40" x2="{width}" y2="40" stroke="{divider_color}" stroke-width="1.2"/>
  <circle cx="22" cy="20" r="5" fill="#EF4444">
    <animate attributeName="opacity" values="1;0.7;1" dur="4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="38" cy="20" r="5" fill="#F59E0B">
    <animate attributeName="opacity" values="1;0.7;1" dur="4s" begin="0.3s" repeatCount="indefinite"/>
  </circle>
  <circle cx="54" cy="20" r="5" fill="#10B981">
    <animate attributeName="opacity" values="1;0.7;1" dur="4s" begin="0.6s" repeatCount="indefinite"/>
  </circle>
  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">praneeth@devbox:~</text>
</g>

<!-- STABLE OUTER BORDER STROKE -->
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="{border_color}" stroke-width="1.2">
  <animate attributeName="stroke-opacity" values="0.5;0.9;0.5" dur="4s" repeatCount="indefinite"/>
</rect>

<!-- MAIN TERMINAL CONTENT WITH RETRO PHOSPHOR GLOW -->
<g id="terminalContent">
{content}
</g>

<!-- FINAL CURSOR -->
{cursor}

<!-- RETRO CYBER GLITCH OVERLAY (STRICTLY ISOLATED TO y >= 40 BODY AREA) -->
{build_glitch("terminalContent")}

</svg>
"""
    return svg_content

# ============================================================
# RETRO TERMINAL THEMED GITHUB STATS FRAME SVG
# ============================================================
def fetch_svg(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching SVG from {url}: {e}")
        return ""

def generate_github_stats_svg():
    width = 1000
    height = 475
    
    print("Fetching live stats for embedded SVG generation...")
    stats_url = "https://github-stats-extended.vercel.app/api?username=PraneethReddy-github&show_icons=true&theme=tokyonight&hide_border=true&title_color=38BDF8&icon_color=34D399&text_color=E2E8F0&bg_color=00000000"
    langs_url = "https://github-stats-extended.vercel.app/api/top-langs/?username=PraneethReddy-github&layout=compact&theme=tokyonight&hide_border=true&title_color=38BDF8&text_color=E2E8F0&bg_color=00000000"
    streak_url = "https://github-readme-streak-stats.herokuapp.com/?user=PraneethReddy-github&theme=tokyonight&hide_border=true&background=00000000&ring=38BDF8&fire=38BDF8&currStreakLabel=38BDF8"
    
    stats_svg = fetch_svg(stats_url)
    langs_svg = fetch_svg(langs_url)
    streak_svg = fetch_svg(streak_url)
    print("Successfully fetched stats!")
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <radialGradient id="statsBgGlow" cx="50%" cy="15%" r="85%">
    <stop offset="0%" stop-color="#0C0F17"/>
    <stop offset="100%" stop-color="#020305"/>
  </radialGradient>

  <pattern id="statsScanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#FFFFFF" opacity="0.025"/>
  </pattern>

  {retro_filters}

  <style>
    .term-title  {{ font-family: 'Fira Code', 'JetBrains Mono', 'Courier New', monospace; font-size: 12.5px; fill: #64748B; letter-spacing: 0.5px; font-weight: bold; }}
  </style>
</defs>

<!-- BASE CONTAINER & BACKGROUND -->
<rect width="{width}" height="{height}" rx="14" fill="url(#statsBgGlow)"/>
<rect x="0" y="36" width="{width}" height="{height-36}" fill="url(#statsScanlines)"/>

<!-- ANCHORED TITLEBAR HEADER -->
<g id="statsTitlebar">
  <path d="M 1,14 Q 1,1 14,1 L {width-14},1 Q {width-1},1 {width-1},14 L {width-1},36 L 1,36 Z" fill="#080B10"/>
  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#1E293B" stroke-width="1.2"/>
  <circle cx="22" cy="18" r="4.5" fill="#EF4444"/>
  <circle cx="38" cy="18" r="4.5" fill="#F59E0B"/>
  <circle cx="54" cy="18" r="4.5" fill="#10B981"/>
  <text x="{width/2}" y="22" text-anchor="middle" class="term-title">praneeth@devbox:~/stats --live</text>
</g>

<!-- STABLE OUTER BORDER STROKE -->
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#1E293B" stroke-width="1.2"/>

<!-- EMBEDDED LIVE GITHUB STATS & TOP LANGUAGES CARDS -->
<g transform="translate(0, 42)" filter="url(#glowCyan)">
  <g transform="translate(101.5, 0)">
    {stats_svg}
  </g>
  <g transform="translate(598.5, 15)">
    {langs_svg}
  </g>
  <g transform="translate(252.5, 235)">
    {streak_svg}
  </g>
</g>
</svg>
"""

# ============================================================
# FULL-WIDTH VISITOR COUNTER SVG (CONSISTENT BACKGROUND, NO TOP TAB)
# ============================================================
def generate_visitor_counter_svg():
    width = 1000
    height = 110
    
    print("Fetching live visitor count for embedded SVG generation...")
    vis_url = "https://komarev.com/ghpvc/?username=PraneethReddy-github&style=for-the-badge&color=38BDF8&label=PROFILE+VISITORS&label_color=00000000"
    vis_svg = fetch_svg(vis_url)
    
    import re
    matches = re.findall(r'<text[^>]*>([^<]+)</text>', vis_svg)
    count = matches[-1] if matches else "0"
    print(f"Successfully fetched visitor count: {count}")
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <radialGradient id="visBgGlow" cx="50%" cy="15%" r="85%">
    <stop offset="0%" stop-color="#0C0F17"/>
    <stop offset="100%" stop-color="#020305"/>
  </radialGradient>

  <pattern id="visScanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#FFFFFF" opacity="0.025"/>
  </pattern>

  {retro_filters}

  <clipPath id="vGlitchA"><rect x="0" y="0" width="{width}" height="55"/></clipPath>
  <clipPath id="vGlitchB"><rect x="0" y="55" width="{width}" height="55"/></clipPath>
</defs>

<!-- BASE CONTAINER & BACKGROUND (CONSISTENT WITH TERMINAL, NO TITLEBAR TAB) -->
<rect width="{width}" height="{height}" rx="14" fill="url(#visBgGlow)"/>
<rect width="{width}" height="{height}" rx="14" fill="url(#visScanlines)"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#1E293B" stroke-width="1.2"/>

<g id="visitorBody" filter="url(#glowCyan)">
  <text x="{width/2}" y="38" text-anchor="middle" fill="#38BDF8" font-family="'Fira Code', 'JetBrains Mono', monospace" font-size="14.5" font-weight="bold" letter-spacing="1.8">👁️ PROFILE VISITORS</text>
  <text x="{width/2}" y="80" text-anchor="middle" fill="#F8FAFC" font-family="'Fira Code', 'JetBrains Mono', Consolas, monospace" font-size="36" font-weight="900" letter-spacing="5">{count}</text>
</g>

<!-- RETRO GLITCH OVERLAY ACROSS FULL WIDTH -->
<g pointer-events="none">
  <g clip-path="url(#vGlitchA)" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0.35;1;0;0" keyTimes="0;0.4;0.42;0.44;0.46;0.48;1" dur="3.5s" repeatCount="indefinite"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;-25 0;35 0;-8 0;0 0" keyTimes="0;0.42;0.44;0.46;0.48" dur="3.5s" repeatCount="indefinite"/>
      <use href="#visitorBody" opacity="0.85" style="color:#00E5FF" transform="translate(-6 0)"/>
    </g>
  </g>
  <g clip-path="url(#vGlitchB)" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0.25;1;0;0" keyTimes="0;0.7;0.72;0.74;0.76;0.78;1" dur="4.2s" repeatCount="indefinite"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;30 0;-20 0;10 0;0 0" keyTimes="0;0.72;0.74;0.76;0.78" dur="4.2s" repeatCount="indefinite"/>
      <use href="#visitorBody" opacity="0.85" style="color:#FF0055" transform="translate(7 0)"/>
    </g>
  </g>
</g>
</svg>
"""

if __name__ == '__main__':
    dark_svg = generate_svg(is_dark=True)
    light_svg = generate_svg(is_dark=False)
    github_stats_svg = generate_github_stats_svg()
    visitor_svg = generate_visitor_counter_svg()
    
    with open('dark.svg', 'w', encoding='utf-8') as f:
        f.write(dark_svg)
    with open('light.svg', 'w', encoding='utf-8') as f:
        f.write(light_svg)
    with open('github_stats.svg', 'w', encoding='utf-8') as f:
        f.write(github_stats_svg)
    with open('visitor_counter.svg', 'w', encoding='utf-8') as f:
        f.write(visitor_svg)
        
    print("Successfully built dark.svg, light.svg, github_stats.svg, and consistent visitor_counter.svg!")
