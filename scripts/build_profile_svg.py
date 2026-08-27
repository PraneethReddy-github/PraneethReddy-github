import os
import json
import re
import time
from html import escape
import urllib.request

# This script lives in scripts/, but every path it touches is relative to the
# repository root, so it behaves the same whether CI runs it from the root or
# you run it from inside scripts/.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, 'assets', 'svg')

# ------------------------------------------------------------------
# Identity. Defined once here and threaded through every panel and URL.
# GITHUB_REPOSITORY_OWNER is supplied automatically by GitHub Actions, so a CI
# build follows whichever account it runs under instead of a baked-in name; the
# literals are only the local fallback. Each can be overridden by environment.
# ------------------------------------------------------------------
USERNAME = os.environ.get('GITHUB_REPOSITORY_OWNER') or 'PraneethReddy-github'
SHELL_USER = os.environ.get('PROFILE_SHELL_USER') or 'praneeth'
SHELL_HOST = os.environ.get('PROFILE_SHELL_HOST') or 'devbox'
PROMPT = f'{SHELL_USER}@{SHELL_HOST}'
CONTACT_EMAIL = os.environ.get('PROFILE_EMAIL') or 'connectwithpraneeth@gmail.com'
CONTACT_LINKEDIN = os.environ.get('PROFILE_LINKEDIN') or 'linkedin.com/in/connectwithpraneeth'

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
        f'        {text(36, y, PROMPT, "prompt-user")}'
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
        (510, "Email",    CONTACT_EMAIL,                         6.05),
        (534, "LinkedIn", CONTACT_LINKEDIN,                      6.35),
        (558, "GitHub",   f"github.com/{USERNAME}",              6.65),
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
        f'        {text(36, final_y, PROMPT, "prompt-user")}'
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
  <text x="{width/2}" y="24" text-anchor="middle" class="term-title">{PROMPT}:~</text>
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
CACHE_DIR = os.path.join(ROOT, 'assets', 'cache')

# Upstream generators answer with a valid-but-useless "sad face" card when their
# own GitHub API call fails. Those must be treated as failures, not as content,
# or a bad upstream minute gets committed onto the profile until the next run.
UPSTREAM_ERROR_MARKERS = (
    'Failed to retrieve',
    'This is likely a GitHub API issue',
    'Something went wrong',
    'Maximum retries exceeded',
    'Error lable',
    'Error label',
    'Could not fetch',
    'No contributions found',
)


def _looks_like_a_real_card(svg):
    if not svg or len(svg) < 400:
        return False
    if '<svg' not in svg:
        return False
    return not any(marker in svg for marker in UPSTREAM_ERROR_MARKERS)


def fetch_svg(url, attempts=3):
    """Fetch an SVG, retrying transient failures. Returns '' if all tries fail."""
    delay = 2
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            body = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
        except Exception as e:
            print(f"  attempt {attempt}/{attempts} failed for {url}: {e}")
        else:
            if _looks_like_a_real_card(body):
                return body
            print(f"  attempt {attempt}/{attempts}: {url} returned an error/empty card")
        if attempt < attempts:
            time.sleep(delay)
            delay *= 2
    return ""


def _placeholder_card(label):
    """Themed stand-in used only when a card has never been fetched successfully."""
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 495 195' "
        "width='495px' height='195px'>"
        "<text x='247.5' y='100' text-anchor='middle' fill='#64748B' "
        "font-family=\"'Fira Code','JetBrains Mono',monospace\" font-size='13'>"
        f"{esc(label)} :: awaiting next sync</text></svg>"
    )


def fetch_card(name, url, label):
    """Fetch a stats card, falling back to the last good copy on disk.

    The cached copy is committed alongside the SVGs, so an upstream outage
    leaves the previous card in place instead of replacing it with an error.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f'{name}.svg')

    svg = fetch_svg(url)
    if svg:
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f"  [ok] {name}: fetched live")
        return svg

    if os.path.exists(cache_path):
        with open(cache_path, encoding='utf-8') as f:
            cached = f.read()
        if _looks_like_a_real_card(cached):
            print(f"  [stale] {name}: upstream unavailable, reusing last good card")
            return cached

    print(f"  [missing] {name}: no live data and no cache, using placeholder")
    return _placeholder_card(label)

def generate_github_stats_svg():
    width = 1000
    height = 475
    
    print("Fetching live stats for embedded SVG generation...")
    stats_url = (f"https://github-stats-extended.vercel.app/api?username={USERNAME}&show_icons=true&theme=tokyonight&hide_border=true&title_color=38BDF8&icon_color=34D399&text_color=E2E8F0&bg_color=00000000")
    langs_url = (f"https://github-stats-extended.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&theme=tokyonight&hide_border=true&title_color=38BDF8&text_color=E2E8F0&bg_color=00000000")
    # NOTE: the old *.herokuapp.com host for streak-stats is dead (Heroku retired
    # free dynos); demolab.com is the maintained instance.
    streak_url = (f"https://streak-stats.demolab.com/?user={USERNAME}&theme=tokyonight&hide_border=true&background=00000000&ring=38BDF8&fire=38BDF8&currStreakLabel=38BDF8")

    stats_svg = fetch_card('stats', stats_url, 'STATS')
    langs_svg = fetch_card('langs', langs_url, 'LANGUAGES')
    streak_svg = fetch_card('streak', streak_url, 'STREAK')
    
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
  <text x="{width/2}" y="22" text-anchor="middle" class="term-title">{PROMPT}:~/stats --live</text>
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
VISITOR_CACHE = os.path.join(CACHE_DIR, 'visitor_count.txt')

# komarev only *increments* for requests coming through GitHub's camo image
# proxy, i.e. an actual profile view. A plain request like this one reads the
# true total without inflating it -- so this build never counts itself.
VISITOR_URL = (f"https://komarev.com/ghpvc/?username={USERNAME}"
               "&style=for-the-badge&color=38BDF8&label=PROFILE+VISITORS"
               "&label_color=00000000")


def _last_known_count():
    try:
        with open(VISITOR_CACHE, encoding='utf-8') as f:
            return int(f.read().strip())
    except Exception:
        return None


def read_visitor_count():
    """Read the live visitor total, never regressing to 0 on a failed fetch."""
    print("Reading live visitor count (read-only, does not inflate the counter)...")
    previous = _last_known_count()
    badge = fetch_svg(VISITOR_URL, attempts=3)

    count = None
    if badge:
        # "<title>PROFILE VISITORS: 1234</title>" is the authoritative value;
        # the <text> nodes are a fallback for other badge styles.
        m = re.search(r'<title>[^<]*?:\s*([\d,]+)\s*</title>', badge)
        if not m:
            texts = re.findall(r'<text[^>]*>([^<]+)</text>', badge)
            for candidate in reversed(texts):
                if re.fullmatch(r'[\d,]+', candidate.strip()):
                    m = re.match(r'([\d,]+)', candidate.strip())
                    break
        if m:
            count = int(m.group(1).replace(',', ''))

    if count is None:
        if previous is not None:
            print(f"  [stale] could not read the badge, keeping last known count: {previous}")
            return previous
        print("  [missing] could not read the badge and no cache exists, showing 0")
        return 0

    # The counter is monotonic; a lower value means a bad read, not lost views.
    if previous is not None and count < previous:
        print(f"  [guard] read {count} but cache holds {previous}; keeping {previous}")
        return previous

    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(VISITOR_CACHE, 'w', encoding='utf-8') as f:
        f.write(str(count))
    print(f"  [ok] visitor count: {count}")
    return count


def generate_visitor_counter_svg():
    width = 1000
    height = 110
    
    count = read_visitor_count()
    
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

# ============================================================
# REPOSITORY SHOWCASE PANEL (built in-house from the GitHub API)
# ============================================================
REPOS_CACHE = os.path.join(CACHE_DIR, 'repos.json')
REPOS_SHOWN = 6

# Language accent colours, roughly matching GitHub's own linguist palette.
LANG_COLORS = {
    'Python': '#3572A5',
    'Jupyter Notebook': '#DA5B0B',
    'JavaScript': '#F1E05A',
    'TypeScript': '#3178C6',
    'HTML': '#E34C26',
    'CSS': '#563D7C',
    'Java': '#B07219',
    'C': '#555555',
    'C++': '#F34B7D',
    'C#': '#178600',
    'Shell': '#89E051',
    'Go': '#00ADD8',
    'Rust': '#DEA584',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Dart': '#00B4AB',
    'Kotlin': '#A97BFF',
    'Swift': '#F05138',
    'R': '#198CE7',
}


def _fetch_repos_from_api():
    """List the user's public, non-fork repositories, most recently pushed first."""
    url = (f'https://api.github.com/users/{USERNAME}/repos'
           '?per_page=100&sort=pushed&direction=desc&type=owner')
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/vnd.github+json',
    }
    # In CI the workflow token lifts the 60/hour anonymous rate limit.
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    delay = 2
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=headers)
            body = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
            data = json.loads(body)
        except Exception as e:
            print(f"  attempt {attempt}/3 failed for the repo list: {e}")
        else:
            if isinstance(data, list):
                return data
            print(f"  attempt {attempt}/3: unexpected repo payload: {str(data)[:120]}")
        if attempt < 3:
            time.sleep(delay)
            delay *= 2
    return None


def load_repos():
    """Return the repos to showcase, falling back to the cached list on failure."""
    print("Fetching repository list...")
    raw = _fetch_repos_from_api()

    if raw is not None:
        picked = [
            {
                'name': r.get('name') or '',
                'description': r.get('description') or '',
                'language': r.get('language') or '',
                'stars': r.get('stargazers_count') or 0,
                'forks': r.get('forks_count') or 0,
            }
            for r in raw
            if not r.get('fork') and not r.get('archived') and r.get('name') != USERNAME
        ][:REPOS_SHOWN]

        if picked:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(REPOS_CACHE, 'w', encoding='utf-8') as f:
                json.dump(picked, f, indent=2)
            # Total public repo count feeds the snake panel's arcade HUD.
            owned = [r for r in raw if not r.get('fork')]
            with open(os.path.join(CACHE_DIR, 'repo_count.txt'), 'w', encoding='utf-8') as f:
                f.write(str(len(owned)))
            print(f"  [ok] repos: fetched {len(picked)} live")
            return picked
        print("  [warn] repo list came back empty after filtering")

    if os.path.exists(REPOS_CACHE):
        try:
            with open(REPOS_CACHE, encoding='utf-8') as f:
                cached = json.load(f)
            if cached:
                print(f"  [stale] repos: API unavailable, reusing {len(cached)} cached")
                return cached
        except Exception as e:
            print(f"  [warn] repo cache unreadable: {e}")

    print("  [missing] repos: no live data and no cache")
    return []


def _truncate(value, limit):
    value = ' '.join(str(value).split())
    return value if len(value) <= limit else value[:limit - 1].rstrip() + '…'


def generate_repos_svg():
    repos = load_repos()

    width = 1000
    row_h = 54
    top = 62
    height = top + max(len(repos), 1) * row_h + 20

    rows = []
    for i, repo in enumerate(repos):
        y = top + i * row_h
        delay = 0.15 + i * 0.12
        lang = repo.get('language') or ''
        lang_color = LANG_COLORS.get(lang, '#64748B')

        meta = []
        if lang:
            meta.append(lang)
        if repo.get('stars'):
            meta.append(f"★ {repo['stars']}")
        if repo.get('forks'):
            meta.append(f"⑂ {repo['forks']}")
        meta_text = '  │  '.join(meta)

        desc = _truncate(repo.get('description') or 'no description provided', 78)

        rows.append(
            f'\n  <g style="opacity:0; animation: repoIn 0.45s ease-out forwards {delay:.2f}s">'
            f'\n    <text x="40" y="{y}" class="repo-arrow">▸</text>'
            f'\n    <text x="64" y="{y}" class="repo-name">{esc(repo.get("name", ""))}</text>'
            f'\n    <circle cx="{width - 250}" cy="{y - 5}" r="4.5" fill="{lang_color}"/>'
            f'\n    <text x="{width - 236}" y="{y}" class="repo-meta">{esc(meta_text)}</text>'
            f'\n    <text x="64" y="{y + 20}" class="repo-desc">{esc(desc)}</text>'
            f'\n  </g>'
        )

    if not repos:
        rows.append(
            f'\n  <text x="{width/2}" y="{top + 20}" text-anchor="middle" class="repo-desc">'
            'repository list unavailable :: awaiting next sync</text>'
        )

    rows_svg = ''.join(rows)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <radialGradient id="repoBgGlow" cx="50%" cy="12%" r="88%">
    <stop offset="0%" stop-color="#0C0F17"/>
    <stop offset="100%" stop-color="#020305"/>
  </radialGradient>

  <pattern id="repoScanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#FFFFFF" opacity="0.025"/>
  </pattern>

  {retro_filters}

  <style>
    @keyframes repoIn {{
      0%   {{ opacity: 0; transform: translateX(-14px); }}
      100% {{ opacity: 1; transform: translateX(0); }}
    }}
    .term-title {{ font-family: {FONT}; font-size: 12.5px; fill: #64748B; letter-spacing: 0.5px; font-weight: bold; }}
    .repo-arrow {{ font-family: {FONT}; font-size: 13px; fill: #34D399; }}
    .repo-name  {{ font-family: {FONT}; font-size: 15px; fill: #38BDF8; font-weight: bold; letter-spacing: 0.4px; }}
    .repo-meta  {{ font-family: {FONT}; font-size: 11.5px; fill: #94A3B8; }}
    .repo-desc  {{ font-family: {FONT}; font-size: 11.5px; fill: #64748B; }}
  </style>
</defs>

<rect width="{width}" height="{height}" rx="14" fill="url(#repoBgGlow)"/>
<rect x="0" y="36" width="{width}" height="{height-36}" fill="url(#repoScanlines)"/>

<g id="repoTitlebar">
  <path d="M 1,14 Q 1,1 14,1 L {width-14},1 Q {width-1},1 {width-1},14 L {width-1},36 L 1,36 Z" fill="#080B10"/>
  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#1E293B" stroke-width="1.2"/>
  <circle cx="22" cy="18" r="4.5" fill="#EF4444"/>
  <circle cx="38" cy="18" r="4.5" fill="#F59E0B"/>
  <circle cx="54" cy="18" r="4.5" fill="#10B981"/>
  <text x="{width/2}" y="22" text-anchor="middle" class="term-title">{PROMPT}:~/repos --recent</text>
</g>

<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#1E293B" stroke-width="1.2"/>

<g filter="url(#glowCyan)">{rows_svg}
</g>
</svg>
"""


# ============================================================
# RETRO-FRAMED CONTRIBUTION SNAKE
# ============================================================
# Platane/snk emits a bare contribution grid. Two things happen here:
#   1. the progress bar it draws underneath the grid is stripped out, and
#   2. the grid is wrapped in the same terminal chrome as the other panels,
#      with the RGB-split glitch used on the visitor counter.
# The raw snake is cached under assets/cache/ so an snk outage leaves the
# previous frame in place instead of blanking the panel.
# One grid only. The frame below is always dark, exactly like the stats, repo
# and visitor panels, so a pale "light" grid would sit wrongly inside it.


def _strip_css_rule(css, marker):
    """Delete a CSS rule (brace-matched, so nested @keyframes survive intact)."""
    while True:
        start = css.find(marker)
        if start == -1:
            return css
        open_brace = css.find('{', start)
        if open_brace == -1:
            return css
        depth = 0
        end = None
        for i in range(open_brace, len(css)):
            if css[i] == '{':
                depth += 1
            elif css[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is None:
            return css
        css = css[:start] + css[end + 1:]


def strip_snake_progress_bar(svg):
    """Remove the progress bar snk draws below the grid (class 'u' rects)."""
    without_rects = re.sub(r'<rect class="u u\d+"[^>]*/>', '', svg)
    removed = len(re.findall(r'<rect class="u u\d+"[^>]*/>', svg))

    match = re.search(r'<style>(.*?)</style>', without_rects, re.S)
    if match:
        css = match.group(1)
        for marker in ['.u{'] + [f'.u.u{i}' for i in range(10)] + [f'@keyframes u{i}' for i in range(10)]:
            css = _strip_css_rule(css, marker)
        without_rects = without_rects[:match.start(1)] + css + without_rects[match.end(1):]

    return without_rects, removed


def _streak_number(label):
    """Pull one figure out of the cached streak card, or None if unavailable."""
    path = os.path.join(CACHE_DIR, 'streak.svg')
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding='utf-8') as f:
            card = f.read()
    except Exception:
        return None
    match = re.search(re.escape(f'<!-- {label} -->') + r'.*?<text[^>]*>\s*([\d,]+)\s*</text>',
                      card, re.S)
    return match.group(1).replace(',', '') if match else None


def read_arcade_stats(raw_grid):
    """Assemble the HUD figures. Everything here is already on disk, so the
    panel needs no extra API call and inherits the existing cache fallbacks."""
    dots = len(re.findall(r'<rect class="c c[0-9a-z]+"', raw_grid))

    repo_count = None
    count_path = os.path.join(CACHE_DIR, 'repo_count.txt')
    if os.path.exists(count_path):
        try:
            with open(count_path, encoding='utf-8') as f:
                repo_count = str(int(f.read().strip()))
        except Exception:
            repo_count = None

    return {
        'high_score': _streak_number('Total Contributions big number') or '--',
        'combo': _streak_number('Current Streak big number') or '--',
        'max_combo': _streak_number('Longest Streak big number') or '--',
        'dots': str(dots),
        'repos': repo_count or '--',
    }


def generate_snake_svg():
    """Wrap the cached snake grid in the retro terminal frame with an arcade HUD."""
    raw_path = os.path.join(CACHE_DIR, 'snake-raw.svg')
    out_path = os.path.join(SVG_DIR, 'snake.svg')

    if not os.path.exists(raw_path):
        if os.path.exists(out_path):
            print("  [stale] snake: no raw grid, keeping the existing frame")
            with open(out_path, encoding='utf-8') as f:
                return f.read()
        print("  [missing] snake: no raw grid and no previous frame")
        return None

    with open(raw_path, encoding='utf-8') as f:
        raw = f.read()

    stats = read_arcade_stats(raw)

    # The grid declares its own palette as CSS variables (--cs is the snake,
    # --c4 the brightest contribution level). Reading them back means the glow
    # always matches whatever colours the workflow asked snk for, instead of
    # duplicating the hex codes here and drifting when one side changes.
    palette = dict(re.findall(r'--(c[a-z0-9]):(#[0-9A-Fa-f]{3,8})', raw))
    snake_color = palette.get('cs', '#34D399')
    peak_color = palette.get('c4', '#38BDF8')

    raw, removed = strip_snake_progress_bar(raw)
    print(f"  [ok] snake: framed, {removed} progress-bar segments removed, "
          f"HUD {stats['high_score']}/{stats['combo']}/{stats['max_combo']}/{stats['dots']}")

    dims = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*width="(\d+)"[^>]*height="(\d+)"', raw)
    view_box = dims.group(1) if dims else '-16 -32 880 192'
    grid_w = int(dims.group(2)) if dims else 880
    grid_h = int(dims.group(3)) if dims else 192

    # snk sizes its viewBox to include the progress bar. With the bar stripped
    # that leaves ~50px of dead space under the grid, so crop to the real
    # content instead of hardcoding a height.
    try:
        min_x, min_y, box_w, box_h = (float(v) for v in view_box.split())
        # Grid cells take their 12px size from CSS and carry no height
        # attribute, so fall back to that when a rect does not declare one.
        bottoms = []
        for tag in re.findall(r'<rect class="[cs][^"]*"[^>]*/>', raw):
            y = re.search(r'\by="(-?[\d.]+)"', tag)
            h = re.search(r'\bheight="([\d.]+)"', tag)
            if y:
                bottoms.append(float(y.group(1)) + (float(h.group(1)) if h else 12.0))
        if bottoms:
            cropped = max(bottoms) + 6 - min_y
            if 0 < cropped < box_h:
                view_box = f'{min_x:g} {min_y:g} {box_w:g} {cropped:g}'
                grid_h = int(round(cropped))
    except Exception as e:
        print(f"  [warn] could not crop the snake viewBox: {e}")

    inner = re.sub(r'^.*?<svg[^>]*>', '', raw, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
    inner = re.sub(r'<desc>.*?</desc>', '', inner, flags=re.S)

    # Glow only the snake and the cells that actually hold contributions.
    # Filtering all 369 rects (as a group filter does) turns the grid into haze.
    #
    # The cell glow has to be driven by the same keyframes as the fill. A static
    # filter would survive the cell being eaten, leaving a glowing empty box that
    # no longer matches its neighbours. Each stop that paints a contribution
    # colour gets the glow; each stop that returns the cell to --ce drops it.
    lit = sorted(set(re.findall(r'<rect class="c (c[0-9a-z]+)"', inner)))
    lit_selector = ','.join(f'.c.{cls}' for cls in lit)

    eaten_stops = inner.count('fill:var(--ce)}')
    inner = inner.replace('fill:var(--ce)}', 'fill:var(--ce);filter:none}')
    lit_stops = len(re.findall(r'fill:var\(--c\d\)\}', inner))
    inner = re.sub(r'fill:var\(--c(\d)\)\}',
                   r'fill:var(--c\1);filter:url(#snakeGlowCyan)}', inner)
    print(f"  [glow] {lit_stops} lit stops glow, {eaten_stops} eaten stops clear it")

    glow_css = '.s{filter:url(#snakeGlowMint)}'
    if lit_selector:
        glow_css += lit_selector + '{filter:url(#snakeGlowCyan)}'
    inner = inner.replace('</style>', glow_css + '</style>', 1)

    width = 1000
    hud_top = 60
    grid_top = 84
    grid_bottom = grid_top + grid_h
    hud_bottom = grid_bottom + 34
    height = hud_bottom + 44  # room under the HUD values, not flush to the edge
    x_off = (width - grid_w) / 2

    cells = [
        ('COMBO', stats['combo']),
        ('MAX COMBO', stats['max_combo']),
        ('DOTS EATEN', stats['dots']),
        ('REPOS', stats['repos']),
    ]
    span = (width - 120) / len(cells)
    hud_cells = []
    for i, (label, value) in enumerate(cells):
        cx = 60 + span * i + span / 2
        hud_cells.append(
            f'\n    <text x="{cx:.1f}" y="{hud_bottom}" text-anchor="middle" class="hud-label">{esc(label)}</text>'
            f'\n    <text x="{cx:.1f}" y="{hud_bottom + 18}" text-anchor="middle" class="hud-value">{esc(value)}</text>'
        )
        if i:
            dx = 60 + span * i
            hud_cells.append(
                f'\n    <line x1="{dx:.1f}" y1="{hud_bottom - 12}" x2="{dx:.1f}" y2="{hud_bottom + 22}" '
                'stroke="#1E293B" stroke-width="1"/>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs>
  <radialGradient id="snakeBgGlow" cx="50%" cy="12%" r="88%">
    <stop offset="0%" stop-color="#0C0F17"/>
    <stop offset="100%" stop-color="#020305"/>
  </radialGradient>

  <pattern id="snakeScanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#FFFFFF" opacity="0.025"/>
  </pattern>

  {retro_filters}

  <!-- Per-cell glows. Generous regions because each cell is only 12px wide. -->
  <filter id="snakeGlowMint" x="-150%" y="-150%" width="400%" height="400%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceGraphic" stdDeviation="2.6" result="b"/>
    <feFlood flood-color="{snake_color}" flood-opacity="0.85" result="f"/>
    <feComposite in="f" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <filter id="snakeGlowCyan" x="-150%" y="-150%" width="400%" height="400%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceGraphic" stdDeviation="2.2" result="b"/>
    <feFlood flood-color="{peak_color}" flood-opacity="0.75" result="f"/>
    <feComposite in="f" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <clipPath id="snGlitchA"><rect x="0" y="{grid_top + 12}" width="{width}" height="26"/></clipPath>
  <clipPath id="snGlitchB"><rect x="0" y="{grid_top + 74}" width="{width}" height="22"/></clipPath>
  <clipPath id="snGlitchC"><rect x="0" y="{grid_top + 132}" width="{width}" height="18"/></clipPath>

  <style>
    .term-title {{ font-family: {FONT}; font-size: 12.5px; fill: #64748B; letter-spacing: 0.5px; font-weight: bold; }}
    .hud-label  {{ font-family: {FONT}; font-size: 9.5px; fill: #475569; letter-spacing: 1.6px; font-weight: bold; }}
    .hud-value  {{ font-family: {FONT}; font-size: 17px; fill: #38BDF8; letter-spacing: 1px; font-weight: bold; }}
    .hud-key    {{ font-family: {FONT}; font-size: 10px; fill: #475569; letter-spacing: 1.6px; font-weight: bold; }}
    .hud-player {{ font-family: {FONT}; font-size: 12px; fill: #34D399; letter-spacing: 0.8px; font-weight: bold; }}
    .hud-score  {{ font-family: {FONT}; font-size: 15px; fill: #F8FAFC; letter-spacing: 1.2px; font-weight: bold; }}
  </style>
</defs>

<!-- BASE CONTAINER & BACKGROUND -->
<rect width="{width}" height="{height}" rx="14" fill="url(#snakeBgGlow)"/>
<rect x="0" y="36" width="{width}" height="{height-36}" fill="url(#snakeScanlines)"/>

<!-- ANCHORED TITLEBAR HEADER -->
<g id="snakeTitlebar">
  <path d="M 1,14 Q 1,1 14,1 L {width-14},1 Q {width-1},1 {width-1},14 L {width-1},36 L 1,36 Z" fill="#080B10"/>
  <line x1="0" y1="36" x2="{width}" y2="36" stroke="#1E293B" stroke-width="1.2"/>
  <circle cx="22" cy="18" r="4.5" fill="#EF4444"/>
  <circle cx="38" cy="18" r="4.5" fill="#F59E0B"/>
  <circle cx="54" cy="18" r="4.5" fill="#10B981"/>
  <text x="{width/2}" y="22" text-anchor="middle" class="term-title">{PROMPT}:~/snake --contributions</text>
</g>

<!-- ARCADE HUD :: TOP ROW -->
<g filter="url(#glowMint)">
  <text x="40" y="{hud_top}" class="hud-key">PLAYER</text>
  <text x="103" y="{hud_top}" class="hud-player">{esc(USERNAME)}</text>
</g>
<g filter="url(#glowWhite)">
  <text x="{width-40}" y="{hud_top}" text-anchor="end" class="hud-score">{esc(stats['high_score'])}</text>
  <text x="{width-40-(len(stats['high_score'])*10)-14}" y="{hud_top}" text-anchor="end" class="hud-key">HIGH SCORE</text>
</g>

<!-- THE CONTRIBUTION GRID (glow applied per cell, not to the whole group) -->
<g id="snakeBody">
  <g transform="translate({x_off}, {grid_top})">
    <svg viewBox="{view_box}" width="{grid_w}" height="{grid_h}">{inner}</svg>
  </g>
</g>

<!-- ARCADE HUD :: BOTTOM SCOREBOARD -->
<line x1="40" y1="{grid_bottom + 8}" x2="{width-40}" y2="{grid_bottom + 8}" stroke="#1E293B" stroke-width="1"/>
<g filter="url(#glowCyan)">{''.join(hud_cells)}
</g>

<!-- STABLE OUTER BORDER STROKE -->
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="13" fill="none" stroke="#1E293B" stroke-width="1.2"/>

<!-- RGB-SPLIT GLITCH, MATCHING THE VISITOR COUNTER -->
<g pointer-events="none">
  <g clip-path="url(#snGlitchA)" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0.3;1;0;0" keyTimes="0;0.40;0.42;0.44;0.46;0.48;1" dur="3.9s" repeatCount="indefinite"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;-22 0;30 0;-7 0;0 0" keyTimes="0;0.42;0.44;0.46;0.48" dur="3.9s" repeatCount="indefinite"/>
      <use href="#snakeBody" opacity="0.8" transform="translate(-6 0)" style="color:#00E5FF"/>
    </g>
  </g>
  <g clip-path="url(#snGlitchB)" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0.25;1;0;0" keyTimes="0;0.68;0.70;0.72;0.74;0.76;1" dur="4.6s" repeatCount="indefinite"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;26 0;-18 0;9 0;0 0" keyTimes="0;0.70;0.72;0.74;0.76" dur="4.6s" repeatCount="indefinite"/>
      <use href="#snakeBody" opacity="0.8" transform="translate(7 0)" style="color:#FF0055"/>
    </g>
  </g>
  <g clip-path="url(#snGlitchC)" opacity="0">
    <animate attributeName="opacity" values="0;0;1;0.2;0;0" keyTimes="0;0.86;0.88;0.90;0.92;1" dur="5.3s" repeatCount="indefinite"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;-14 0;18 0;0 0" keyTimes="0;0.88;0.90;0.92" dur="5.3s" repeatCount="indefinite"/>
      <use href="#snakeBody" opacity="0.7" transform="translate(-4 0)" style="color:#00E5FF"/>
    </g>
  </g>
</g>
</svg>
"""


# The shared retro_filters / retro_glitch_defs blocks are injected wholesale into
# every panel, but no single panel uses all of them. Stripping the ones a panel
# never references keeps the committed SVGs (and every profile view) smaller.
# Only ids this script generates are considered; ids inside embedded upstream
# cards are left untouched.
OWN_DEF_PREFIXES = ('glow', 'glitch', 'snakeGlow', 'snGlitch', 'vGlitch', 'bodyArea')


def prune_unused_defs(svg):
    """Drop filter/clipPath definitions this script emits but never references."""
    referenced = set(re.findall(r'url\(#([^)]+)\)', svg)) | set(re.findall(r'href="#([^"]+)"', svg))
    removed = 0

    def drop(match):
        nonlocal removed
        el_id = match.group(2)
        if el_id.startswith(OWN_DEF_PREFIXES) and el_id not in referenced:
            removed += 1
            return ''
        return match.group(0)

    svg = re.sub(r'<(filter|clipPath)[^>]*id="([^"]+)"[^>]*>.*?</\1>', drop, svg, flags=re.S)
    return svg, removed


if __name__ == '__main__':
    dark_svg = generate_svg(is_dark=True)
    light_svg = generate_svg(is_dark=False)
    github_stats_svg = generate_github_stats_svg()
    visitor_svg = generate_visitor_counter_svg()
    repos_svg = generate_repos_svg()

    print("Framing the contribution snake...")
    snake_svg = generate_snake_svg()
    
    os.makedirs(SVG_DIR, exist_ok=True)
    for filename, content in (
        ('dark.svg', dark_svg),
        ('light.svg', light_svg),
        ('github_stats.svg', github_stats_svg),
        ('visitor_counter.svg', visitor_svg),
        ('repos.svg', repos_svg),
        *([('snake.svg', snake_svg)] if snake_svg else []),
    ):
        content, pruned = prune_unused_defs(content)
        if pruned:
            print(f"  [prune] {filename}: dropped {pruned} unused definitions")
        with open(os.path.join(SVG_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        
    print(f"Successfully built dark.svg, light.svg, github_stats.svg, visitor_counter.svg and repos.svg into {SVG_DIR}")
