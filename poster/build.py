#!/usr/bin/env python3
"""차량 안전사고 예방 포스터 (A2) — 회색 바탕 + 시그널 오렌지, Black Han Sans.

트럭 평면도는 실제 치수(m)로 그린다. 로컬 좌표는 앞범퍼 중앙이 원점이고
차량 뒤쪽이 +y, 차량 오른쪽이 +x. 이것을 -90도 돌려 왼쪽을 보고 서 있는
트럭으로 배치한다(뒤쪽 = 포스터 오른쪽).
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).parent
W, H = 1587.4, 2245.04            # 420 x 594 mm (CSS px)
M = 84

INK = '#111210'
WHITE = '#F1F1EC'
LIGHT = '#DDDDD8'
MID = '#A3A49F'
BODY = '#2B2C29'

PALETTES = {
    # bg: 바탕 / acc: 사각지대·하단 띠·유도봉 / on: acc 위의 글자·선 / hl: 강조 글자
    'gray':   dict(BG='#C4C5C0', ACC='#FF4D1A', ON=INK, HL='#FF4D1A'),
    'orange': dict(BG='#FF5A1F', ACC=INK, ON='#FF5A1F', HL='#FFFFFF'),
}
BG = ACC = ON = HL = None


def use(name):
    global BG, ACC, ON, HL
    pal = PALETTES[name]
    BG, ACC, ON, HL = pal['BG'], pal['ACC'], pal['ON'], pal['HL']

# ---------------------------------------------------------------- diagram placement
S = 140.0      # px per metre
XF = 128       # front bumper (global x)
CY = 1150      # vehicle centre line (global y)
Y_COLS = 1540
Y_BAND = 1994


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def G(xm, ym):
    """local metres -> global px"""
    return XF + ym * S, CY - xm * S


def L(m):
    return m * S


def attrs(a):
    return ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items())


def rect(x1, y1, x2, y2, **a):
    a1, a2 = min(x1, x2), max(x1, x2)
    return f'<rect x="{f(L(a1))}" y="{f(L(y1))}" width="{f(L(a2 - a1))}" height="{f(L(y2 - y1))}" {attrs(a)}/>'


def line(x1, y1, x2, y2, **a):
    return f'<line x1="{f(L(x1))}" y1="{f(L(y1))}" x2="{f(L(x2))}" y2="{f(L(y2))}" {attrs(a)}/>'


def poly(pts, close=True, **a):
    d = 'M' + ' L'.join(f'{f(L(x))},{f(L(y))}' for x, y in pts) + (' Z' if close else '')
    return f'<path d="{d}" {attrs(a)}/>'


LW_OUT, LW_MID, LW_FINE = 2.6, 1.4, 0.9
DASH_HIDDEN = {'stroke-dasharray': '7 5'}
DASH_PHANTOM = {'stroke-dasharray': '22 5 3 5'}

DRIVER = (-0.52, 2.47)
CODRIVER = (0.52, 2.47)
MIRROR_L = (-1.49, 1.74)
GUIDE = (-1.95, 8.10)
BENCH_Y = (3.62, 4.32, 5.02, 5.72)
Y_END = (W + 30 - XF) / S          # zone runs off the right edge
ZONE = [(-1.22, 6.74), (1.22, 6.74), (1.62, Y_END), (-1.62, Y_END)]


def person(xm, ym, ang, arms='lap'):
    x, y = L(xm), L(ym)
    p = []
    if arms == 'lap':
        p += [f'<rect x="-25" y="-26" width="11" height="30" rx="5.5" fill="{BODY}"/>',
              f'<rect x="14" y="-26" width="11" height="30" rx="5.5" fill="{BODY}"/>']
    elif arms == 'wheel':
        p += [f'<rect x="-25" y="-34" width="11" height="38" rx="5.5" fill="{BODY}" transform="rotate(8 -19 0)"/>',
              f'<rect x="14" y="-34" width="11" height="38" rx="5.5" fill="{BODY}" transform="rotate(-8 19 0)"/>']
    elif arms == 'signal':
        p += [f'<rect x="14" y="-46" width="11" height="50" rx="5.5" fill="{BODY}" transform="rotate(-14 19 0)"/>',
              f'<rect x="-25" y="-30" width="11" height="34" rx="5.5" fill="{BODY}" transform="rotate(26 -19 0)"/>',
              f'<rect x="27" y="-94" width="8" height="46" rx="4" fill="{HL if ACC == INK else ACC}" stroke="{INK}" stroke-width="1.5" transform="rotate(-14 19 0)"/>']
    p += [f'<rect x="-28" y="-12" width="56" height="25" rx="12.5" fill="{BODY}"/>',
          f'<circle cx="0" cy="-2" r="17" fill="{INK}" stroke="{WHITE}" stroke-width="3"/>']
    return f'<g transform="translate({f(x)},{f(y)}) rotate({ang})">{"".join(p)}</g>'


def truck():
    g = []
    # bumper + tow hooks
    g.append(rect(-1.19, 0.0, 1.19, 0.19, fill=BODY, stroke=INK, stroke_width=LW_OUT))
    for s in (-1, 1):
        g.append(poly([(s * 0.47, 0.0), (s * 0.47, -0.10), (s * 0.63, -0.10), (s * 0.63, 0.0)], close=False,
                      fill='none', stroke=INK, stroke_width=LW_MID))
    # fenders with headlamps, hidden front wheels
    for s in (-1, 1):
        a, b = sorted((s * 1.18, s * 0.60))
        g.append(f'<rect x="{f(L(a))}" y="{f(L(0.21))}" width="{f(L(b - a))}" height="{f(L(1.36))}" rx="14" '
                 f'fill="{WHITE}" stroke="{INK}" stroke-width="{LW_OUT}"/>')
        g.append(rect(s * 0.80, 0.25, s * 1.02, 0.37, fill=LIGHT, stroke=INK, stroke_width=LW_MID))
        g.append(line(s * 0.80, 0.31, s * 1.02, 0.31, stroke=INK, stroke_width=LW_FINE))
    # hood
    g.append(rect(-0.60, 0.19, 0.60, 1.60, fill=LIGHT, stroke=INK, stroke_width=LW_OUT))
    g.append(line(0, 0.30, 0, 1.52, stroke=INK, stroke_width=LW_FINE))
    for s in (-1, 1):
        for i in range(6):
            yy = 0.46 + i * 0.09
            g.append(line(s * 0.20, yy, s * 0.46, yy, stroke=INK, stroke_width=1.2))
        g.append(line(s * 0.56, 0.30, s * 0.56, 1.52, stroke=INK, stroke_width=LW_FINE))
    g.append(rect(-0.56, 0.19, 0.56, 0.27, fill=INK))
    # windshield
    g.append(rect(-1.09, 1.60, 1.09, 1.76, fill=WHITE, stroke=INK, stroke_width=LW_MID))
    g.append(line(0, 1.60, 0, 1.76, stroke=INK, stroke_width=3))
    for s in (-1, 1):
        for dx in (0.30, 0.38):
            g.append(line(s * (dx + 0.02), 1.73, s * (dx + 0.12), 1.63, stroke=INK, stroke_width=LW_FINE))
    # mirrors
    for s in (-1, 1):
        g.append(line(s * 1.15, 1.66, s * 1.46, 1.70, stroke=INK, stroke_width=2.2))
        g.append(line(s * 1.15, 1.86, s * 1.46, 1.78, stroke=INK, stroke_width=1.3))
        g.append(rect(s * 1.45, 1.58, s * 1.54, 1.92, fill=INK))
    # cab walls in section, roof removed
    g.append(rect(-1.16, 1.76, 1.16, 2.98, fill=INK))
    g.append(rect(-1.10, 1.80, 1.10, 2.92, fill=WHITE))
    for s in (-1, 1):
        for yy in (1.92, 2.80):
            g.append(rect(s * 1.17, yy, s * 1.09, yy + 0.025, fill=BG))
    g.append(rect(-1.10, 1.80, 1.10, 1.92, fill=MID, stroke=INK, stroke_width=LW_FINE))
    for s in (-1, 1):
        a, b = sorted((s * 0.80, s * 0.24))
        g.append(f'<rect x="{f(L(a))}" y="{f(L(2.18))}" width="{f(L(b - a))}" height="{f(L(0.54))}" rx="7" '
                 f'fill="{LIGHT}" stroke="{INK}" stroke-width="{LW_MID}"/>')
        g.append(f'<rect x="{f(L(a))}" y="{f(L(2.72))}" width="{f(L(b - a))}" height="{f(L(0.14))}" rx="5" '
                 f'fill="{MID}" stroke="{INK}" stroke-width="{LW_MID}"/>')
        # door steps
        g.append(rect(s * 1.16, 2.12, s * 1.27, 2.62, fill=MID, stroke=INK, stroke_width=LW_MID))
        for yy in (2.22, 2.32, 2.42, 2.52):
            g.append(line(s * 1.18, yy, s * 1.25, yy, stroke=INK, stroke_width=LW_FINE))
    g.append(f'<circle cx="{f(L(0.98))}" cy="{f(L(3.02))}" r="{f(L(0.075))}" fill="{WHITE}" stroke="{INK}" stroke-width="{LW_MID}"/>')
    g.append(f'<circle cx="{f(L(0.98))}" cy="{f(L(3.02))}" r="{f(L(0.035))}" fill="{INK}"/>')
    g.append(f'<circle cx="0" cy="{f(L(2.20))}" r="5" fill="{INK}"/>')
    g.append(f'<circle cx="{f(L(0.07))}" cy="{f(L(2.36))}" r="3.5" fill="{INK}"/>')
    g.append(f'<ellipse cx="{f(L(-0.52))}" cy="{f(L(2.02))}" rx="{f(L(0.21))}" ry="{f(L(0.075))}" fill="none" stroke="{INK}" stroke-width="3.2"/>')
    g.append(line(-0.52, 1.92, -0.52, 2.02, stroke=INK, stroke_width=3.2))
    # cargo bed
    g.append(rect(-1.23, 3.06, 1.23, 6.72, fill=INK))
    g.append(rect(-1.17, 3.12, 1.17, 6.66, fill=WHITE))
    for i in range(1, 12):
        xx = -1.17 + i * (2.34 / 12)
        g.append(line(xx, 3.12, xx, 6.66, stroke=INK, stroke_width=LW_FINE, opacity=.28))
    for s in (-1, 1):
        a, b = sorted((s * 1.17, s * 0.77))
        g.append(rect(a, 3.28, b, 6.44, fill=LIGHT, stroke=INK, stroke_width=LW_MID))
        for yy in (3.97, 4.67, 5.37, 6.07):
            g.append(line(a, yy, b, yy, stroke=INK, stroke_width=LW_FINE))
    for yy in (3.18, 4.08, 4.98, 5.88, 6.60):
        g.append(line(-1.23, yy, 1.23, yy, stroke=INK, stroke_width=1, opacity=.55, **DASH_PHANTOM))
    for s in (-1, 1):
        g.append(rect(s * 0.70, 6.72, s * 0.82, 6.80, fill=INK))
        g.append(rect(s * 1.05, 6.72, s * 1.20, 6.78, fill=HL if ACC == INK else ACC, stroke=INK, stroke_width=LW_MID))
    # hidden wheels
    for yc in (0.95, 4.82, 6.07):
        for s in (-1, 1):
            g.append(rect(s * 0.86, yc - 0.55, s * 1.16, yc + 0.55, fill='none', stroke=INK, stroke_width=1.2,
                          opacity=.65, **DASH_HIDDEN))
    # people
    g.append(person(*DRIVER, 0, 'wheel'))
    g.append(person(*CODRIVER, 0, 'lap'))
    for yy in BENCH_Y:
        g.append(person(-0.97, yy, 90, 'lap'))
        g.append(person(0.97, yy, -90, 'lap'))
    return '\n'.join(g)


def zone():
    g = [poly(ZONE, fill=ACC)]
    # fine hazard hatch across the zone (local coords, clipped)
    pts = ' '.join(f'{f(L(x))},{f(L(y))}' for x, y in ZONE)
    hatch = []
    y0, y1 = L(6.74), L(Y_END)
    t = -600
    while t < 1200:
        hatch.append(f'<line x1="{f(-300 + t)}" y1="{f(y1)}" x2="{f(-300 + t + (y1 - y0))}" y2="{f(y0)}" '
                     f'stroke="{ON}" stroke-width="1.4" opacity=".16"/>')
        t += 15
    g.append(f'<clipPath id="zc"><polygon points="{pts}"/></clipPath><g clip-path="url(#zc)">{"".join(hatch)}</g>')
    return '\n'.join(g)


def sightline():
    p = [DRIVER, MIRROR_L, (GUIDE[0], GUIDE[1] - 0.30)]
    d = poly(p, close=False, fill='none', stroke=INK, stroke_width=2, **{'stroke-dasharray': '10 7'})
    (x1, y1), (x2, y2) = p[1], p[2]
    ang = math.degrees(math.atan2(L(y2) - L(y1), L(x2) - L(x1)))
    head = (f'<path d="M-15,-7 L0,0 L-15,7" transform="translate({f(L(x2))},{f(L(y2))}) rotate({ang:.1f})" '
            f'fill="none" stroke="{INK}" stroke-width="2.2"/>')
    return d + head


def flag(label, target, up=True, y_label=None):
    """vertical leader from the target to a label that sits beside the top (or bottom) of the leader"""
    tx, ty = G(*target)
    if up:
        top = y_label - 34
        return (f'<line x1="{f(tx)}" y1="{f(top)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{INK}" stroke-width="2.2"/>'
                f'<circle cx="{f(tx)}" cy="{f(ty)}" r="6" fill="{INK}" stroke="{WHITE}" stroke-width="2.5"/>'
                f'<text x="{f(tx + 12)}" y="{f(y_label)}" class="flag">{label}</text>')
    bot = y_label + 6
    return (f'<line x1="{f(tx)}" y1="{f(ty)}" x2="{f(tx)}" y2="{f(bot)}" stroke="{INK}" stroke-width="2.2"/>'
            f'<circle cx="{f(tx)}" cy="{f(ty)}" r="6" fill="{INK}" stroke="{WHITE}" stroke-width="2.5"/>'
            f'<text x="{f(tx + 12)}" y="{f(y_label)}" class="flag">{label}</text>')


def diagram_svg():
    zx, zy = G(0, 8.95)
    ax1, _ = G(0, 7.55)
    ax2, _ = G(0, 10.05)
    ay = CY + 58
    return f'''
  <svg class="fig" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate({XF},{CY}) rotate(-90)">
      {zone()}
      {truck()}
      {sightline()}
      {person(*GUIDE, 0, 'signal')}
    </g>
    <text x="{f(zx)}" y="{f(zy - 8)}" class="zl" text-anchor="middle">후방 사각지대</text>
    <path d="M{f(ax1)},{f(ay)} L{f(ax2 - 30)},{f(ay)}" stroke="{ON}" stroke-width="9"/>
    <path d="M{f(ax2 - 52)},{f(ay - 26)} L{f(ax2)},{f(ay)} L{f(ax2 - 52)},{f(ay + 26)} Z" fill="{ON}"/>
    {flag('선탑자', CODRIVER, True, 916)}
    {flag('탑승자', (0.97, BENCH_Y[1]), True, 916)}
    {flag('운전병', DRIVER, False, 1452)}
    {flag('유도병', GUIDE, False, 1498)}
  </svg>'''


ROLES = [
    ('운전병', '차량을 몰고, 차량 상태를 책임진다.', [
        '운행 전 일일점검표로 차량을 점검한다.',
        '졸음이 오면 즉시 선탑자에게 알리고 쉰다.',
        '장거리 운행은 2시간마다 15분씩 쉰다.',
    ]),
    ('선탑자', '차량에 탄 모두의 안전을 책임진다.', [
        '출발 전 전원의 안전벨트를 확인한다.',
        '과속이나 졸음운전은 즉시 제지한다.',
        '운행 중 수시로 운전병의 상태를 살핀다.',
    ]),
    ('유도병', '후진하는 차량의 눈이 된다.', [
        '차량이 후진할 때는 반드시 유도한다.',
        '차량 바로 뒤, 사각지대에 서지 않는다.',
        '운전병과 눈을 맞춘 뒤 신호한다.',
    ]),
    ('탑승자', '적재함에서도 스스로를 지킨다.', [
        '이동 중에는 적재함에서 일어서지 않는다.',
        '차량 밖으로 몸을 내밀지 않는다.',
        '이상한 점을 보면 즉시 알린다.',
    ]),
]


def page():
    ff = [('BH', 'BlackHanSans-Regular.ttf', 400),
          ('GA', 'GothicA1-Bold.ttf', 700), ('GA', 'GothicA1-ExtraBold.ttf', 800), ('GA', 'GothicA1-Black.ttf', 900)]
    fonts = ''.join(f"@font-face{{font-family:'{n}';src:url('fonts/{p}');font-weight:{w};}}\n" for n, p, w in ff)
    cols = ''.join(
        f'<section class="col"><h2>{name}</h2><p class="d">{desc}</p><ul>{"".join(f"<li>{r}</li>" for r in rules)}</ul></section>'
        for name, desc, rules in ROLES)
    css = f'''
{fonts}
@page {{ size: 420mm 594mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 420mm; height: 594mm; background: {BG}; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.poster {{ position: relative; width: 420mm; height: 594mm; overflow: hidden; background: {BG}; color: {INK};
  font-family: 'GA', sans-serif; word-break: keep-all; }}
.fig {{ position: absolute; left: 0; top: 0; }}
.fig .flag {{ font: 400 40px 'BH'; fill: {INK}; }}
.fig .zl {{ font: 400 54px 'BH'; fill: {ON}; }}
.fig .zs {{ font: 400 30px 'BH'; fill: {INK}; }}

h1 {{ position: absolute; left: {M - 10}px; top: 64px; font: 400 236px/1.0 'BH'; letter-spacing: -0.015em; word-spacing: -0.12em; }}
h1 em {{ font-style: normal; color: {HL}; }}

.stat {{ position: absolute; left: {M}px; top: 596px; }}
.stat b {{ display: block; font: 400 214px/0.9 'BH'; color: {HL}; letter-spacing: -0.02em; }}
.stat b small {{ font-size: 128px; margin-left: 6px; }}
.stat span {{ display: block; margin-top: 16px; font: 700 22px/1.45 'GA'; }}
.lede {{ position: absolute; left: 808.7px; top: 606px; width: 700px; font: 700 33px/1.5 'GA'; letter-spacing: -0.03em; }}
.lede strong {{ font-weight: 900; color: {HL}; }}

.cols {{ position: absolute; left: {M}px; right: {M}px; top: {Y_COLS}px; display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 30px; }}
.col {{ border-top: 5px solid {INK}; padding-top: 16px; }}
.col h2 {{ font: 400 60px/1 'BH'; }}
.col .d {{ margin-top: 12px; font: 800 21px/1.4 'GA'; letter-spacing: -0.02em; }}
.col ul {{ list-style: none; margin-top: 18px; }}
.col li {{ border-top: 1.5px solid rgba(17,18,16,.35); padding: 12px 0 13px; font: 700 25px/1.38 'GA'; letter-spacing: -0.04em; text-wrap: balance; }}

.band {{ position: absolute; left: 0; right: 0; top: {Y_BAND}px; bottom: 0; background: {ACC}; color: {ON}; }}
.band p {{ position: absolute; left: {M - 4}px; right: {M}px; top: 50%; transform: translateY(-54%); font: 400 88px/1 'BH'; letter-spacing: -0.02em; word-spacing: -0.1em; white-space: nowrap; }}
'''
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>한 대의 차량, 네 명의 안전관</title>
<style>{css}</style>
</head>
<body>
<div class="poster">
  <h1>한 대의 차량,<br>네 명의 <em>안전관</em>.</h1>
  <div class="stat"><b>34<small>%</small></b><span>군 안전사고 사망자 중 차량사고 비율<br>2010~2019년, 사망 원인 1위</span></div>
  <p class="lede">안전사고로 숨진 장병 <strong>세 명 중 한 명</strong>은<br>차량사고로 목숨을 잃었습니다.<br>차량 한 대에는 네 개의 자리가 있고,<br>자리마다 지켜야 할 임무가 있습니다.</p>
  {diagram_svg()}
  <div class="cols">{cols}</div>
  <div class="band"><p>선탑자는 승객이 아니라 안전관입니다.</p></div>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    for name in PALETTES:
        use(name)
        out = ROOT / ('poster.html' if name == 'gray' else f'poster-{name}.html')
        out.write_text(page(), encoding='utf-8')
        print('wrote', out.name)
