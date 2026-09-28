#!/usr/bin/env python3
"""차량 안전사고 예방 포스터 (A2) — 편집 디자인 + 교범식 평면 도해.

종이·먹·별색(빨강) 3색. 도해는 실제 치수(m)로 그린 뒤 축척 S(px/m)로 옮긴다.
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).parent
W, H = 1587.4, 2245.04            # 420 x 594 mm (CSS px)
M = 88                             # margin
GUT = 24
COL = (W - 2 * M - 11 * GUT) / 12  # 12-column grid


def cx(i):
    return M + i * (COL + GUT)


def span(n):
    return n * COL + (n - 1) * GUT


PAPER = '#ECE9E1'
INK = '#1B1B19'
RED = '#D23A1E'


def tint(t):
    """ink laid over paper at opacity t, as a flat colour"""
    p = [int(PAPER[i:i + 2], 16) for i in (1, 3, 5)]
    k = [int(INK[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a + (b - a) * t):02X}' for a, b in zip(p, k))


# ---------------------------------------------------------------- layout (y)
Y_RULE_TOP = 132
Y_H1 = 168
Y_LEDE = 566
Y_RULE_MID = 790
Y_FIG = 824            # figure caption / legend row
Y_BLOCK_A = 1128       # callouts 1, 2
Y_BLOCK_B = 1520       # callouts 3, 4
Y_RULE_BOT = 1904

# ---------------------------------------------------------------- drawing scale
S = 112.0              # px per metre
X0 = W / 2             # truck centreline
Y0 = 872               # front of bumper


def X(m):
    return X0 + m * S


def Y(m):
    return Y0 + m * S


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def rect_m(x1, y1, x2, y2, **a):
    attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<rect x="{f(X(x1))}" y="{f(Y(y1))}" width="{f((x2 - x1) * S)}" height="{f((y2 - y1) * S)}" {attrs}/>'


def line_m(x1, y1, x2, y2, **a):
    attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    return f'<line x1="{f(X(x1))}" y1="{f(Y(y1))}" x2="{f(X(x2))}" y2="{f(Y(y2))}" {attrs}/>'


def path_m(pts, close=True, **a):
    attrs = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())
    d = 'M' + ' L'.join(f'{f(X(x))},{f(Y(y))}' for x, y in pts) + (' Z' if close else '')
    return f'<path d="{d}" {attrs}/>'


# line weights (drafting hierarchy)
LW_OUT = 2.4    # visible outline
LW_MID = 1.3    # interior edges
LW_FINE = 0.8   # textures, seams
HIDDEN = 'stroke-dasharray="7 5"'
PHANTOM = 'stroke-dasharray="22 5 3 5"'
CENTRE = 'stroke-dasharray="30 6 6 6"'


def person(xm, ym, ang, arms='lap', hl=False):
    """Plan-view person: shoulders + helmet, facing `ang` degrees (0 = up/forward)."""
    x, y = X(xm), Y(ym)
    body = tint(.78)
    parts = []
    if arms == 'lap':
        parts += [f'<rect x="-25" y="-26" width="11" height="30" rx="5.5" fill="{body}"/>',
                  f'<rect x="14" y="-26" width="11" height="30" rx="5.5" fill="{body}"/>']
    elif arms == 'wheel':
        parts += [f'<rect x="-25" y="-34" width="11" height="38" rx="5.5" fill="{body}" transform="rotate(8 -19 0)"/>',
                  f'<rect x="14" y="-34" width="11" height="38" rx="5.5" fill="{body}" transform="rotate(-8 19 0)"/>']
    elif arms == 'signal':
        parts += [f'<rect x="14" y="-46" width="11" height="50" rx="5.5" fill="{body}" transform="rotate(-14 19 0)"/>',
                  f'<rect x="-25" y="-30" width="11" height="34" rx="5.5" fill="{body}" transform="rotate(26 -19 0)"/>',
                  f'<rect x="27" y="-92" width="7" height="44" rx="3.5" fill="{RED}" transform="rotate(-14 19 0)"/>']
    parts += [f'<rect x="-28" y="-12" width="56" height="25" rx="12.5" fill="{body}"/>',
              f'<circle cx="0" cy="-2" r="17" fill="{INK}" stroke="{PAPER}" stroke-width="3"/>',
              f'<path d="M-11,-13 A14,14 0 0 1 11,-13" fill="none" stroke="{PAPER}" stroke-width="1.6" opacity=".55"/>']
    return f'<g transform="translate({f(x)},{f(y)}) rotate({ang})">{"".join(parts)}</g>'


def hatch(clip_id, x1, y1, x2, y2, gap, color, sw, angle=45):
    """explicit hatch lines inside a clip path (kept vector in PDF)"""
    out = []
    L = (x2 - x1) + (y2 - y1)
    k = 0
    t = -L
    while t < L * 2:
        out.append(f'<line x1="{f(x1 + t)}" y1="{f(y2)}" x2="{f(x1 + t + (y2 - y1))}" y2="{f(y1)}" stroke="{color}" stroke-width="{sw}"/>')
        t += gap
        k += 1
    return f'<g clip-path="url(#{clip_id})">{"".join(out)}</g>'


# key positions (metres; x from centreline, y from front bumper)
DRIVER = (-0.52, 2.47)
CODRIVER = (0.52, 2.47)
MIRROR_L = (-1.49, 1.74)
GUIDE = (-1.95, 8.10)
BENCH_Y = (3.62, 4.32, 5.02, 5.72)
ZONE = [(-1.22, 6.74), (1.22, 6.74), (1.42, 8.98), (-1.42, 8.98)]


def truck_plan():
    g = []
    # --- centre line (drafting) extends past the vehicle
    g.append(line_m(0, -0.45, 0, 7.05, stroke=INK, stroke_width=0.7, **{'stroke-dasharray': '30 6 6 6'}))

    # --- front bumper + tow hooks
    g.append(rect_m(-1.19, 0.0, 1.19, 0.19, fill=tint(.78), stroke=INK, stroke_width=LW_OUT))
    for s in (-1, 1):
        g.append(path_m([(s * 0.47, 0.0), (s * 0.47, -0.10), (s * 0.63, -0.10), (s * 0.63, 0.0)], close=False,
                        fill='none', stroke=INK, stroke_width=LW_MID))
    # --- fenders
    for s in (-1, 1):
        xo, xi = s * 1.18, s * 0.60
        a, b = min(xo, xi), max(xo, xi)
        g.append(f'<rect x="{f(X(a))}" y="{f(Y(0.21))}" width="{f((b - a) * S)}" height="{f(1.36 * S)}" rx="14" '
                 f'fill="{tint(.10)}" stroke="{INK}" stroke-width="{LW_OUT}"/>')
        # headlamp + blackout lamp
        g.append(rect_m(min(s * 0.80, s * 1.02), 0.25, max(s * 0.80, s * 1.02), 0.37, fill=PAPER, stroke=INK, stroke_width=LW_MID))
        g.append(line_m(s * 0.80, 0.31, s * 1.02, 0.31, stroke=INK, stroke_width=LW_FINE))
    # --- hood
    g.append(rect_m(-0.60, 0.19, 0.60, 1.60, fill=tint(.14), stroke=INK, stroke_width=LW_OUT))
    g.append(line_m(0, 0.30, 0, 1.52, stroke=INK, stroke_width=LW_FINE))
    for s in (-1, 1):
        for i in range(6):
            yy = 0.46 + i * 0.09
            g.append(line_m(s * 0.20, yy, s * 0.46, yy, stroke=INK, stroke_width=1.1))
        g.append(line_m(s * 0.56, 0.30, s * 0.56, 1.52, stroke=INK, stroke_width=LW_FINE))
    # grille edge
    g.append(rect_m(-0.56, 0.19, 0.56, 0.27, fill=INK))

    # --- windshield (two panes, glass convention)
    g.append(rect_m(-1.09, 1.60, 1.09, 1.76, fill=PAPER, stroke=INK, stroke_width=LW_MID))
    g.append(line_m(0, 1.60, 0, 1.76, stroke=INK, stroke_width=3))
    for s in (-1, 1):
        for dx in (0.30, 0.38):
            g.append(line_m(s * (dx + 0.02), 1.73, s * (dx + 0.12), 1.63, stroke=INK, stroke_width=LW_FINE))

    # --- mirrors
    for s in (-1, 1):
        g.append(line_m(s * 1.15, 1.66, s * 1.46, 1.70, stroke=INK, stroke_width=2))
        g.append(line_m(s * 1.15, 1.86, s * 1.46, 1.78, stroke=INK, stroke_width=1.2))
        g.append(rect_m(min(s * 1.45, s * 1.54), 1.58, max(s * 1.45, s * 1.54), 1.92, fill=INK))

    # --- cab: walls cut at waist height (poché), roof removed
    g.append(rect_m(-1.16, 1.76, 1.16, 2.98, fill=INK))
    g.append(rect_m(-1.10, 1.80, 1.10, 2.92, fill=tint(.04)))
    # door gaps
    for s in (-1, 1):
        for yy in (1.92, 2.80):
            g.append(rect_m(min(s * 1.17, s * 1.09), yy, max(s * 1.17, s * 1.09), yy + 0.025, fill=PAPER))
    # dashboard
    g.append(rect_m(-1.10, 1.80, 1.10, 1.92, fill=tint(.30), stroke=INK, stroke_width=LW_FINE))
    # seats
    for s in (-1, 1):
        a, b = min(s * 0.80, s * 0.24), max(s * 0.80, s * 0.24)
        g.append(f'<rect x="{f(X(a))}" y="{f(Y(2.18))}" width="{f((b - a) * S)}" height="{f(0.54 * S)}" rx="7" '
                 f'fill="{tint(.13)}" stroke="{INK}" stroke-width="{LW_MID}"/>')
        g.append(f'<rect x="{f(X(a))}" y="{f(Y(2.72))}" width="{f((b - a) * S)}" height="{f(0.14 * S)}" rx="5" '
                 f'fill="{tint(.30)}" stroke="{INK}" stroke-width="{LW_MID}"/>')
    # door steps (outside the cab) and exhaust stack
    for s_ in (-1, 1):
        g.append(rect_m(min(s_ * 1.16, s_ * 1.27), 2.12, max(s_ * 1.16, s_ * 1.27), 2.62, fill=tint(.22), stroke=INK, stroke_width=LW_MID))
        for yy in (2.22, 2.32, 2.42, 2.52):
            g.append(line_m(s_ * 1.18, yy, s_ * 1.25, yy, stroke=INK, stroke_width=LW_FINE))
    g.append(f'<circle cx="{f(X(0.98))}" cy="{f(Y(3.02))}" r="{f(0.075 * S)}" fill="{PAPER}" stroke="{INK}" stroke-width="{LW_MID}"/>')
    g.append(f'<circle cx="{f(X(0.98))}" cy="{f(Y(3.02))}" r="{f(0.035 * S)}" fill="{INK}"/>')
    # gear levers
    g.append(f'<circle cx="{f(X(0))}" cy="{f(Y(2.20))}" r="5" fill="{INK}"/>')
    g.append(f'<circle cx="{f(X(0.07))}" cy="{f(Y(2.36))}" r="3.5" fill="{INK}"/>')
    # steering wheel + column
    g.append(f'<ellipse cx="{f(X(-0.52))}" cy="{f(Y(2.02))}" rx="{f(0.21 * S)}" ry="{f(0.075 * S)}" fill="none" stroke="{INK}" stroke-width="3"/>')
    g.append(line_m(-0.52, 1.92, -0.52, 2.02, stroke=INK, stroke_width=3))

    # --- cargo bed: walls in section, floor boards, benches
    g.append(rect_m(-1.23, 3.06, 1.23, 6.72, fill=INK))
    g.append(rect_m(-1.17, 3.12, 1.17, 6.66, fill=tint(.06)))
    for i in range(1, 12):
        xx = -1.17 + i * (2.34 / 12)
        g.append(line_m(xx, 3.12, xx, 6.66, stroke=INK, stroke_width=LW_FINE, opacity=.35))
    for s in (-1, 1):
        a, b = min(s * 1.17, s * 0.77), max(s * 1.17, s * 0.77)
        g.append(rect_m(a, 3.28, b, 6.44, fill=tint(.16), stroke=INK, stroke_width=LW_MID))
        for yy in (3.97, 4.67, 5.37, 6.07):
            g.append(line_m(a, yy, b, yy, stroke=INK, stroke_width=LW_FINE))
    # canvas bows (removed) — phantom lines
    for yy in (3.18, 4.08, 4.98, 5.88, 6.60):
        g.append(line_m(-1.23, yy, 1.23, yy, stroke=INK, stroke_width=0.9, **{'stroke-dasharray': '22 5 3 5'}))
    # tailgate hinges / rear lamps
    for s in (-1, 1):
        g.append(rect_m(min(s * 0.70, s * 0.82), 6.72, max(s * 0.70, s * 0.82), 6.80, fill=INK))
        g.append(rect_m(min(s * 1.05, s * 1.20), 6.72, max(s * 1.05, s * 1.20), 6.78, fill=PAPER, stroke=INK, stroke_width=LW_MID))

    # --- wheels: hidden under fenders and bed
    for (yc, xin, xout) in ((0.95, 0.86, 1.16), (4.82, 0.86, 1.16), (6.07, 0.86, 1.16)):
        for s in (-1, 1):
            a, b = min(s * xin, s * xout), max(s * xin, s * xout)
            g.append(rect_m(a, yc - 0.55, b, yc + 0.55, fill='none', stroke=INK, stroke_width=1.1, **{'stroke-dasharray': '7 5'}))
        g.append(line_m(-1.30, yc, 1.30, yc, stroke=INK, stroke_width=0.6, **{'stroke-dasharray': '30 6 6 6'}))

    # --- people
    g.append(person(*DRIVER, 0, 'wheel'))
    g.append(person(*CODRIVER, 0, 'lap'))
    for yy in BENCH_Y:
        g.append(person(-0.97, yy, 90, 'lap'))
        g.append(person(0.97, yy, -90, 'lap'))
    return '\n'.join(g)


def zone_and_guide():
    g = []
    zx1, zy1 = X(ZONE[3][0]), Y(ZONE[0][1])
    zx2, zy2 = X(ZONE[2][0]), Y(ZONE[2][1])
    g.append(hatch('zoneClip', zx1, zy1, zx2, zy2, 13, RED, 1.5))
    g.append(path_m(ZONE, fill='none', stroke=RED, stroke_width=2))
    # knock-out label
    lx, ly = X(0), Y(7.72)
    g.append(f'<rect x="{f(lx - 118)}" y="{f(ly - 40)}" width="236" height="96" fill="{PAPER}"/>')
    g.append(f'<text x="{f(lx)}" y="{f(ly)}" class="z1" text-anchor="middle">후방 사각지대</text>')
    g.append(f'<text x="{f(lx)}" y="{f(ly + 30)}" class="z2" text-anchor="middle">운전석에서 보이지 않는 구역</text>')
    g.append(f'<text x="{f(lx)}" y="{f(ly + 50)}" class="z2" text-anchor="middle">사람이 들어가지 않는다</text>')

    # sight line: driver -> left mirror -> guide
    p = [DRIVER, MIRROR_L, (GUIDE[0], GUIDE[1] - 0.30)]
    g.append(path_m(p, close=False, fill='none', stroke=INK, stroke_width=1.4, **{'stroke-dasharray': '9 6'}))
    ex, ey = X(p[2][0]), Y(p[2][1])
    ang = math.degrees(math.atan2(Y(p[2][1]) - Y(p[1][1]), X(p[2][0]) - X(p[1][0])))
    g.append(f'<path d="M-13,-6 L0,0 L-13,6" transform="translate({f(ex)},{f(ey)}) rotate({ang:.1f})" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    # label along the long leg
    mx, my = (X(p[1][0]) + ex) / 2, (Y(p[1][1]) + ey) / 2
    g.append(f'<text transform="translate({f(mx - 12)},{f(my)}) rotate({ang:.1f})" class="lbl" text-anchor="middle">사이드미러 시야선</text>')

    # reversing arrow on the centre line, inside the zone
    ax, ay = X(0), Y(8.84)
    g.append(f'<path d="M{f(ax)},{f(ay - 60)} L{f(ax)},{f(ay)}" stroke="{RED}" stroke-width="3"/>')
    g.append(f'<path d="M{f(ax - 10)},{f(ay - 14)} L{f(ax)},{f(ay)} L{f(ax + 10)},{f(ay - 14)}" fill="none" stroke="{RED}" stroke-width="3"/>')

    g.append(person(*GUIDE, 0, 'signal'))
    return '\n'.join(g)


def leader(x_start, y, tx, ty, side, bend=None):
    """shoulder from the text column, then straight to the target; dot on target"""
    sx = bend if bend is not None else x_start + (26 if side == 'L' else -26)
    return (f'<path d="M{f(x_start)},{f(y)} L{f(sx)},{f(y)} L{f(tx)},{f(ty)}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="{f(tx)}" cy="{f(ty)}" r="4.5" fill="{INK}" stroke="{PAPER}" stroke-width="2"/>')


def figure_svg():
    zone_poly = ' '.join(f'{f(X(x))},{f(Y(y))}' for x, y in ZONE)
    leaders = (
        leader(cx(4) - GUT + 4, Y_BLOCK_A, X(DRIVER[0]) - 12, Y(DRIVER[1]) + 14, 'L', bend=X(-0.98)) +
        leader(cx(8) - 4, Y_BLOCK_A, X(CODRIVER[0]) + 12, Y(CODRIVER[1]) + 14, 'R', bend=X(0.98)) +
        leader(cx(4) - GUT + 4, Y_BLOCK_B, X(GUIDE[0]) - 22, Y(GUIDE[1]) + 8, 'L', bend=X(GUIDE[0]) - 22) +
        leader(cx(8) - 4, Y_BLOCK_B, X(0.97) + 18, Y(BENCH_Y[3]) + 16, 'R', bend=X(1.40))
    )
    # scale bar 0-3 m
    sb_x, sb_y = cx(0), Y_FIG + 196
    sb = ''
    for i in range(3):
        sb += f'<rect x="{f(sb_x + i * S)}" y="{sb_y}" width="{f(S)}" height="9" fill="{INK if i % 2 == 0 else PAPER}" stroke="{INK}" stroke-width="1.2"/>'
        sb += f'<text x="{f(sb_x + i * S)}" y="{sb_y + 32}" class="mono" text-anchor="middle">{i}</text>'
    sb += f'<text x="{f(sb_x + 3 * S)}" y="{sb_y + 32}" class="mono" text-anchor="middle">3 m</text>'
    # legend (right)
    lg_x, lg_y = cx(8), Y_FIG + 6
    lg = ''
    rows = [
        (f'<line x1="0" y1="0" x2="44" y2="0" stroke="{INK}" stroke-width="1.4" stroke-dasharray="9 6"/>', '시야선'),
        (f'<line x1="0" y1="0" x2="44" y2="0" stroke="{INK}" stroke-width="1.1" stroke-dasharray="7 5"/>', '가려진 부분 (바퀴)'),
        (f'<line x1="0" y1="0" x2="44" y2="0" stroke="{INK}" stroke-width="0.9" stroke-dasharray="22 5 3 5"/>', '덮개 골조 (표시 생략)'),
        (f'<g><clipPath id="lgc"><rect x="0" y="-9" width="44" height="18"/></clipPath>'
         + ''.join(f'<line x1="{i}" y1="9" x2="{i + 18}" y2="-9" stroke="{RED}" stroke-width="1.5" clip-path="url(#lgc)"/>' for i in range(-18, 50, 9))
         + f'<rect x="0" y="-9" width="44" height="18" fill="none" stroke="{RED}" stroke-width="1.5"/></g>', '사각지대'),
    ]
    for i, (sym, txt) in enumerate(rows):
        yy = lg_y + 22 + i * 34
        lg += f'<g transform="translate({f(lg_x)},{yy})">{sym}</g><text x="{f(lg_x + 62)}" y="{yy + 7}" class="lbl">{txt}</text>'

    return f'''
  <svg class="fig" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
    <defs><clipPath id="zoneClip"><polygon points="{zone_poly}"/></clipPath></defs>
    {zone_and_guide()}
    {truck_plan()}
    {leaders}
    {sb}
    {lg}
  </svg>'''


ROLES = [
    ('1', '운전병', '차량을 몰고, 차량 상태를 책임진다.', [
        ('1-1', '운행 전 일일점검표로 차량을 점검한다.'),
        ('1-2', '졸음이 오면 즉시 선탑자에게 알리고 쉰다.'),
        ('1-3', '장거리 운행은 2시간마다 15분씩 쉰다.'),
    ]),
    ('2', '선탑자', '차량에 탄 모두의 안전을 책임진다.', [
        ('2-1', '출발 전 전원의 안전벨트를 확인한다.'),
        ('2-2', '과속이나 졸음운전은 즉시 제지한다.'),
        ('2-3', '운행 중 수시로 운전병의 상태를 살핀다.'),
    ]),
    ('3', '유도병', '후진하는 차량의 눈이 된다.', [
        ('3-1', '차량이 후진할 때는 반드시 유도한다.'),
        ('3-2', '차량 바로 뒤, 사각지대에 서지 않는다.'),
        ('3-3', '운전병과 눈을 맞춘 뒤 신호한다.'),
    ]),
    ('4', '탑승자', '적재함에서도 스스로를 지킨다.', [
        ('4-1', '이동 중에는 적재함에서 일어서지 않는다.'),
        ('4-2', '차량 밖으로 몸을 내밀지 않는다.'),
        ('4-3', '이상한 점을 보면 즉시 알린다.'),
    ]),
]


def block(role, x, y):
    n, name, desc, rules = role
    lis = ''.join(f'<li><span class="rn">{rn}</span><span>{t}</span></li>' for rn, t in rules)
    return f'''
  <section class="blk" style="left:{f(x)}px;top:{y}px;width:{f(span(4))}px">
    <div class="bh"><span class="bn">{n}</span><h2>{name}</h2></div>
    <p class="bd">{desc}</p>
    <ol>{lis}</ol>
  </section>'''


def page():
    ff = [
        ('KSerif', 'NotoSerifKR-400.ttf', 400), ('KSerif', 'NotoSerifKR-600.ttf', 600), ('KSerif', 'NotoSerifKR-900.ttf', 900),
        ('KSans', 'IBMPlexSansKR-Regular.ttf', 400), ('KSans', 'IBMPlexSansKR-Medium.ttf', 500),
        ('KSans', 'IBMPlexSansKR-SemiBold.ttf', 600), ('KSans', 'IBMPlexSansKR-Bold.ttf', 700),
        ('KMono', 'IBMPlexMono-Regular.ttf', 400), ('KMono', 'IBMPlexMono-Medium.ttf', 500),
    ]
    fonts = ''.join(f"@font-face{{font-family:'{n}';src:url('fonts/{p}');font-weight:{w};}}\n" for n, p, w in ff)
    css = f'''
{fonts}
@page {{ size: 420mm 594mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 420mm; height: 594mm; background: {PAPER}; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.poster {{ position: relative; width: 420mm; height: 594mm; overflow: hidden; background: {PAPER}; color: {INK};
  font-family: 'KSans', sans-serif; word-break: keep-all; font-kerning: normal; }}
.fig {{ position: absolute; left: 0; top: 0; }}
.fig .lbl {{ font: 500 17px 'KSans'; fill: {INK}; letter-spacing: -0.01em; }}
.fig .mono {{ font: 400 15px 'KMono', 'KSans'; fill: {INK}; }}
.fig .z1 {{ font: 700 25px 'KSans'; fill: {RED}; letter-spacing: -0.01em; }}
.fig .z2 {{ font: 500 16px 'KSans'; fill: {RED}; }}
.rule {{ position: absolute; left: {M}px; right: {M}px; height: 0; border-top: 1.5px solid {INK}; }}

.meta {{ position: absolute; left: {M}px; right: {M}px; top: 96px; display: flex; justify-content: space-between;
  font: 500 19px 'KSans'; letter-spacing: 0.02em; }}
h1 {{ position: absolute; left: {M - 6}px; top: {Y_H1}px; font: 900 158px/1.1 'KSerif'; letter-spacing: -0.05em; }}
h1 i {{ font-style: normal; color: {RED}; }}

.stat {{ position: absolute; left: {M}px; top: {Y_LEDE - 14}px; width: {f(span(4))}px; }}
.stat b {{ display: block; font: 900 138px/1 'KSerif'; color: {RED}; letter-spacing: -0.04em; }}
.stat b small {{ font-size: 84px; margin-left: 4px; }}
.stat span {{ display: block; margin-top: 14px; font: 500 19px/1.5 'KSans'; }}
.lede {{ position: absolute; left: {f(cx(4))}px; top: {Y_LEDE}px; width: {f(span(8))}px;
  font: 400 31px/1.6 'KSerif'; letter-spacing: -0.025em; }}
.lede strong {{ font-weight: 900; }}

.figcap {{ position: absolute; left: {M}px; top: {Y_FIG}px; width: {f(span(4))}px; }}
.figcap .k {{ font: 500 15px 'KMono', 'KSans'; letter-spacing: 0.06em; }}
.figcap h3 {{ margin-top: 10px; font: 600 25px/1.35 'KSerif'; letter-spacing: -0.02em; }}
.figcap p {{ margin-top: 8px; font: 400 16px/1.5 'KSans'; color: {tint(.72)}; }}

.blk {{ position: absolute; border-top: 2px solid {INK}; padding-top: 18px; }}
.bh {{ display: flex; align-items: baseline; gap: 18px; }}
.bn {{ font: 500 26px 'KMono', 'KSans'; }}
.blk h2 {{ font: 900 54px/1.05 'KSerif'; letter-spacing: -0.04em; }}
.bd {{ margin: 12px 0 0 38px; font: 600 23px/1.45 'KSerif'; letter-spacing: -0.02em; color: {tint(.80)}; }}
.blk ol {{ list-style: none; margin-top: 22px; border-top: 1px solid {tint(.35)}; }}
.blk li {{ display: grid; grid-template-columns: 38px 1fr; column-gap: 0; padding: 13px 0 13px; border-bottom: 1px solid {tint(.35)};
  font: 500 25px/1.42 'KSans'; letter-spacing: -0.025em; }}
.blk li .rn {{ font: 500 16px/2.2 'KMono', 'KSans'; color: {tint(.75)}; }}

.foot {{ position: absolute; left: {M}px; top: {Y_RULE_BOT + 34}px; width: {f(span(8))}px; font: 900 70px/1.18 'KSerif'; letter-spacing: -0.05em; }}
.sign {{ position: absolute; left: {f(cx(8))}px; top: {Y_RULE_BOT + 40}px; width: {f(span(4))}px; }}
.sign .t {{ font: 600 17px 'KSans'; display: flex; justify-content: space-between; }}
.sign table {{ margin-top: 10px; width: 100%; border-collapse: collapse; table-layout: fixed; }}
.sign th {{ font: 500 16px 'KSans'; border: 1.5px solid {INK}; padding: 6px 0; background: {tint(.08)}; }}
.sign td {{ border: 1.5px solid {INK}; height: 74px; }}
.small {{ position: absolute; left: {M}px; right: {M}px; top: {H - M - 4}px; font: 400 14px/1.5 'KSans'; color: {tint(.72)};
  display: flex; justify-content: space-between; }}
'''
    blocks = (block(ROLES[0], cx(0), Y_BLOCK_A) + block(ROLES[1], cx(8), Y_BLOCK_A) +
              block(ROLES[2], cx(0), Y_BLOCK_B) + block(ROLES[3], cx(8), Y_BLOCK_B))
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>한 대의 차량, 네 명의 안전관</title>
<style>{css}</style>
</head>
<body>
<div class="poster">
  <div class="meta"><span>육군 차량 안전사고 예방</span><span>운전병 · 선탑자 · 유도병 · 탑승자</span></div>
  <div class="rule" style="top:{Y_RULE_TOP}px"></div>
  <h1>한 대의 차량,<br>네 명의 안전관<i>.</i></h1>
  <div class="stat"><b>34<small>%</small></b><span>군 안전사고 사망자 중 차량사고 비율<br>2010~2019년, 사망 원인 1위</span></div>
  <p class="lede">안전사고로 숨진 장병 <strong>세 명 중 한 명</strong>은<br>차량사고로 목숨을 잃었습니다.<br>차량 한 대에는 네 개의 자리가 있고,<br>자리마다 지켜야 할 임무가 있습니다.</p>
  <div class="rule" style="top:{Y_RULE_MID}px"></div>
  <div class="figcap"><div class="k">그림 1</div><h3>2½톤 카고트럭이 후진할 때<br>네 사람의 위치</h3><p>평면도. 운전실 지붕과 적재함 덮개는 그리지 않았다.</p></div>
  {figure_svg()}
  {blocks}
  <div class="rule" style="top:{Y_RULE_BOT}px"></div>
  <p class="foot">선탑자는 승객이 아니라<br>안전관입니다.</p>
  <div class="sign"><div class="t"><span>출발 전 확인</span><span>네 사람 모두 확인한 뒤 출발한다</span></div>
    <table><tr><th>운전병</th><th>선탑자</th><th>유도병</th><th>탑승자</th></tr><tr><td></td><td></td><td></td><td></td></tr></table></div>
  <div class="small"><span>자료: 군 안전사고 사망자 원인별 현황(2010~2019). 차량 34%, 추락·충격 15%, 항공·함정 11%, 익사 11%, 총기 3%.</span><span>1-3의 휴식 기준은 민간 권고이며, 부대 운행 규정을 우선한다.</span></div>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    (ROOT / 'poster.html').write_text(page(), encoding='utf-8')
    print('wrote poster.html')
