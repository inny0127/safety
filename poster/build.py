#!/usr/bin/env python3
"""차량 안전사고 예방 포스터 (A2) — 중형버스 측면 일러스트 + Black Han Sans.

버스 그림은 bus.py에 있다(참고 사진 좌표계). 이 파일은 그 그림을 포스터에
배치하고, 도로·후방 사각지대·역할 라벨·본문을 얹어 두 가지 색 조합으로 출력한다.
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
    'orange': dict(BG='#FF5A1F', ACC=INK, ON='#FF5A1F', HL='#FFFFFF', ROADC='#EF5118', GUIDE_STRIPE='#FF5A1F'),
}
BG = ACC = ON = HL = ROADC = GUIDE_STRIPE = None


def use(name):
    global BG, ACC, ON, HL, ROADC, GUIDE_STRIPE
    pal = PALETTES[name]
    BG, ACC, ON, HL, ROADC, GUIDE_STRIPE = (pal[k] for k in ('BG', 'ACC', 'ON', 'HL', 'ROADC', 'GUIDE_STRIPE'))

# ---------------------------------------------------------------- illustration placement
import bus as B

K = 1.0                 # reference-photo px -> poster px
TX, TY = 268, 879       # bus origin on the poster
Y_COLS = 1540
Y_BAND = 1994


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def P(x, y):
    """reference-photo coordinates -> poster coordinates"""
    return TX + x * K, TY + y * K


Y_GROUND = P(0, B.GROUND)[1]          # near-side wheels touch here
ROAD = (Y_GROUND - 100, Y_GROUND + 44)  # far / near edge of the road band
X_REAR = P(104, 0)[0]
GUIDE_AT = (150, ROAD[0] + 6)         # feet: far side of the road, off the bus's rear-left corner
GUIDE_S = 0.95


def flag(label, tx, ty, y_label, side='right'):
    """vertical leader from a label down to its target"""
    top = y_label - 34
    if side == 'right':
        text = f'<text x="{f(tx + 12)}" y="{f(y_label)}" class="flag">{label}</text>'
    else:
        text = f'<text x="{f(tx - 12)}" y="{f(y_label)}" class="flag" text-anchor="end">{label}</text>'
    return (f'<line x1="{f(tx)}" y1="{f(top)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{INK}" stroke-width="2.2"/>'
            f'<circle cx="{f(tx)}" cy="{f(ty)}" r="6" fill="{INK}" stroke="{WHITE}" stroke-width="2.5"/>' + text)


def illustration_svg():
    y_far, y_near = ROAD
    # road band (a little perspective) and the blind zone directly behind the bus
    road = (f'<rect x="-10" y="{f(y_far)}" width="{W + 20}" height="{f(y_near - y_far)}" fill="{ROADC}"/>'
            f'<rect x="-10" y="{f(y_far)}" width="{W + 20}" height="2" fill="{INK}" opacity=".18"/>')
    zx2 = X_REAR + 2
    # blind zone: trapezoid that starts at the bus footprint and widens toward the left edge
    yg = Y_GROUND
    zpts = [(zx2, yg - 52), (zx2, yg + 30), (-10, yg + 74), (-10, yg - 100)]
    zp = ' '.join(f'{f(x)},{f(y)}' for x, y in zpts)
    zone = f'<polygon points="{zp}" fill="{ACC}"/>'
    hatch = ''.join(f'<line x1="{f(x)}" y1="{f(yg + 60)}" x2="{f(x + 150)}" y2="{f(yg - 90)}" '
                    f'stroke="{ON}" stroke-width="1.5" opacity=".18"/>' for x in range(-180, int(zx2), 15))
    zone += f'<clipPath id="zc"><polygon points="{zp}"/></clipPath><g clip-path="url(#zc)">{hatch}</g>'
    # reversing arrow and label, set where the zone is widest
    ay = yg - 44
    zone += (f'<path d="M{f(zx2 - 34)},{f(ay)} L{f(58)},{f(ay)}" stroke="{ON}" stroke-width="6"/>'
             f'<path d="M{f(64)},{f(ay - 15)} L{f(34)},{f(ay)} L{f(64)},{f(ay + 15)} Z" fill="{ON}"/>')
    zone += f'<text x="30" y="{f(yg + 28)}" class="zl">후방 사각지대</text>'

    bus_g = f'<g transform="translate({TX},{TY}) scale({K})">{B.bus(people=B.people())}</g>'
    gx, gy = GUIDE_AT
    guide = B.guide(gx, gy, GUIDE_S, stripe=GUIDE_STRIPE)

    # labels
    px, py = P(B.PASSENGERS[2], 250 - 8)
    cx_, cy_ = P(*B.CODRIVER)
    dx, dy = P(*B.DRIVER)
    labels = (flag('탑승자', px, py - 6, 938) +
              flag('선탑자', cx_, cy_ - 14, 938, 'left') +
              flag('운전병', dx, dy - 14, 938) +
              flag('유도병', gx + 4 * GUIDE_S, gy - 228 * GUIDE_S, 1016))
    return f'''
  <svg class="fig" viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
    {road}
    {zone}
    {guide}
    {bus_g}
    {labels}
  </svg>'''


ROLES = [
    ('운전병', '차량을 몰고, 차량 상태를 책임진다.', [
        '운행 전 반드시 검차 실시하기',
        '졸음이 오면 즉시 선탑자에게 알리고 쉬기',
        '장거리 운행은 2시간마다 15분씩 쉬기',
    ]),
    ('선탑자', '차량에 탄 모두의 안전을 책임진다.', [
        '출발 전 전원의 안전벨트 확인하기',
        '과속이나 졸음운전은 즉시 제지하기',
        '운행 중 수시로 운전병의 상태 살피기',
    ]),
    ('유도병', '후진하는 차량의 눈이 된다.', [
        '차량이 후진할 때는 반드시 유도하기',
        '차량 바로 뒤, 사각지대에 서지 않기',
        '운전병과 눈을 맞춘 뒤 신호하기',
    ]),
    ('탑승자', '좌석에서도 스스로를 지킨다.', [
        '출발부터 도착까지 안전벨트 매기',
        '차량 밖으로 몸을 내밀지 않기',
        '이상한 점을 보면 즉시 알리기',
    ]),
]


def page():
    ff = [('BH', 'BlackHanSans-Regular.ttf', 400), ('GS', 'GasoekOne-Regular.ttf', 400), ('DH', 'DoHyeon-Regular.ttf', 400),
          ('GA', 'GothicA1-Bold.ttf', 700), ('GA', 'GothicA1-ExtraBold.ttf', 800), ('GA', 'GothicA1-Black.ttf', 900)]
    fonts = ''.join(f"@font-face{{font-family:'{n}';src:url('fonts/{p}');font-weight:{w};}}\n" for n, p, w in ff)
    cols = ''.join(
        f'<section class="col"><h2>{name}</h2><p class="d">{desc}</p><ul>{"".join(f"<li>{r}</li>" for r in rules)}</ul></section>'
        for name, desc, rules in ROLES)
    css = f'''
{fonts}
@page {{ size: 297mm 420mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 297mm; height: 420mm; overflow: hidden; background: {BG}; }}
.page {{ width: 297mm; height: 420mm; overflow: hidden; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.poster {{ transform: scale(0.707142857); transform-origin: 0 0; position: relative; width: 420mm; height: 594mm; overflow: hidden; background: {BG}; color: {INK};
  font-family: 'GA', sans-serif; word-break: keep-all; }}
.fig {{ position: absolute; left: 0; top: 0; }}
.fig .flag {{ font: 400 44px 'DH'; fill: {INK}; }}
.fig .zl {{ font: 400 46px 'BH'; fill: {ON}; }}

h1 {{ position: absolute; left: {M - 10}px; top: 64px; font: 400 236px/1.0 'BH'; letter-spacing: -0.015em; word-spacing: -0.12em; }}
h1 em {{ font-style: normal; color: {HL}; }}

.stat {{ position: absolute; left: {M}px; top: 596px; }}
.stat b {{ display: block; font: 400 196px/0.9 'GS'; color: {HL}; letter-spacing: -0.02em; }}
.stat b small {{ font-size: 128px; margin-left: 6px; }}
.stat span {{ display: block; margin-top: 16px; font: 700 22px/1.45 'GA'; }}
.lede {{ position: absolute; left: 808.7px; top: 606px; width: 700px; font: 700 33px/1.5 'GA'; letter-spacing: -0.03em; }}
.lede strong {{ font-weight: 900; color: {HL}; }}

.cols {{ position: absolute; left: {M}px; right: {M}px; top: {Y_COLS}px; display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 30px; }}
.col {{ border-top: 5px solid {INK}; padding-top: 16px; }}
.col h2 {{ font: 400 68px/1 'DH'; letter-spacing: -0.01em; }}
.col .d {{ margin-top: 12px; font: 800 21px/1.4 'GA'; letter-spacing: -0.02em; }}
.col ul {{ list-style: none; margin-top: 18px; }}
.col li {{ border-top: 1.5px solid rgba(17,18,16,.35); padding: 12px 0 13px; font: 700 25px/1.38 'GA'; letter-spacing: -0.04em; text-wrap: balance; }}

.band {{ position: absolute; left: 0; right: 0; top: {Y_BAND}px; bottom: 0; background: {ACC}; color: {ON}; }}
.band p {{ position: absolute; left: {M - 4}px; right: {M}px; top: 50%; transform: translateY(-54%); font: 400 70px/1 'GS'; letter-spacing: 0.01em; word-spacing: 0.05em; white-space: nowrap; }}
'''
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>한 대의 차량, 네 명의 안전관</title>
<style>{css}</style>
</head>
<body>
<div class="page"><div class="poster">
  <h1>한 대의 차량,<br>네 명의 <em>안전관</em>.</h1>
  <div class="stat"><b>34<small>%</small></b><span>군 안전사고 사망자 중 차량사고 비율<br>2010~2019년, 사망 원인 1위</span></div>
  <p class="lede">안전사고로 숨진 장병 <strong>세 명 중 한 명</strong>은<br>차량사고로 목숨을 잃었습니다.<br>차량 한 대에는 네 개의 자리가 있고,<br>자리마다 지켜야 할 임무가 있습니다.</p>
  {illustration_svg()}
  <div class="cols">{cols}</div>
  <div class="band"><p>선탑자는 승객이 아니라 안전관입니다.</p></div>
</div></div>
</body>
</html>
'''


if __name__ == '__main__':
    for name in PALETTES:
        use(name)
        out = ROOT / 'poster.html'
        out.write_text(page(), encoding='utf-8')
        print('wrote', out.name)
