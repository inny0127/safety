#!/usr/bin/env python3
"""Builds poster.html: '한 대의 차량, 네 명의 안전관' (A2, 420x594mm).

Everything is vector: the landscape, truck and figures are generated SVG,
text is live Pretendard / Big Shoulders Stencil, icons are Tabler (MIT).
"""
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
W, H = 1587.4, 2245.04          # 420mm x 594mm in CSS px
HERO_H = 1420                   # height of the illustrated scene
M = 96                          # outer margin

# ---------------------------------------------------------------- palette
INK = '#12160F'
PAPER = '#F2EEE1'
MUTED = '#A7A48C'
YEL = '#FFC421'
YEL_SOFT = '#FFE08A'
GROUND = '#1B2216'

SKY = ['#0F140C', '#161D11', '#48523A', '#66704B']
RIDGE = ['#434E36', '#313B28', GROUND]

BODY = '#6D7747'       # olive drab, lit side
BODY_HI = '#8E9A62'
BODY_SH = '#57613A'
BODY_DK = '#3E452D'
CHASSIS = '#23271D'
TARP = '#74764F'
TARP_SH = '#63654A'
TARP_ROLL = '#8A8B62'
INTERIOR = '#1D2419'
FARWALL = '#29311F'
TIRE = '#15171200'
UNI = '#5E6842'        # uniform
UNI_SH = '#4B5434'
UNI_FAR = '#434B30'
SKIN = '#C8966B'
SKIN_SH = '#A77B55'
SKIN_FAR = '#9A7253'
HELM = '#4F5836'
HELM_HI = '#646E45'
HELM_FAR = '#3B4229'


def f(v):
    """compact number formatting for SVG paths"""
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


# ---------------------------------------------------------------- landscape
def ridge_y(x, base, comps):
    return base + sum(a * math.sin(2 * math.pi * x / lam + ph) for a, lam, ph in comps)


def ridge_path(base, comps, bottom=HERO_H, step=5):
    pts = [(x, ridge_y(x, base, comps)) for x in range(-10, int(W) + 16, step)]
    d = 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in pts)
    crest = d
    d += f' L{f(W + 10)},{bottom} L-10,{bottom} Z'
    return d, crest


R1 = (868, [(22, 540, 0.4), (11, 230, 1.3), (4, 95, 2.2)])
R2 = (948, [(24, 700, 2.4), (12, 270, 0.2), (4, 120, 1.1)])
R3 = (1030, [(20, 860, 3.6), (9, 330, 2.9), (3, 140, 0.7)])


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def receding_road():
    """Road leaving the foreground band and winding over the near hill."""
    end_x = 1318
    end_y = ridge_y(end_x, *R3) + 1
    p0, p1, p2, p3 = (1395, 1226), (1560, 1150), (1215, 1080), (end_x, end_y)
    left, right, centre = [], [], []
    n = 60
    for i in range(n + 1):
        t = i / n
        x, y = bezier(p0, p1, p2, p3, t)
        x2, y2 = bezier(p0, p1, p2, p3, min(1, t + 0.001))
        x1, y1 = bezier(p0, p1, p2, p3, max(0, t - 0.001))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        wdt = 118 * (1 - t) ** 1.7 + 5          # half width, perspective taper
        left.append((x + nx * wdt, y + ny * wdt))
        right.append((x - nx * wdt, y - ny * wdt))
        centre.append((x, y, wdt, nx, ny))
    poly = left + right[::-1]
    d = 'M' + ' L'.join(f'{f(x)},{f(y)}' for x, y in poly) + ' Z'
    return d, left, right, centre


# ---------------------------------------------------------------- figures
def seated_front(cx):
    """Passenger on the far bench, facing the viewer, visible from the waist up."""
    return f'''
    <g>
      <path d="M{cx-31},-210 L{cx-31},-257 Q{cx-31},-277 {cx-13},-279 L{cx+13},-279 Q{cx+31},-277 {cx+31},-257 L{cx+31},-210 Z" fill="{UNI}"/>
      <path d="M{cx-31},-210 L{cx-31},-257 Q{cx-31},-272 {cx-21},-277 L{cx-21},-210 Z" fill="{UNI_SH}"/>
      <path d="M{cx+31},-210 L{cx+31},-257 Q{cx+31},-272 {cx+21},-277 L{cx+21},-210 Z" fill="{UNI_SH}"/>
      <path d="M{cx},-277 L{cx},-212" stroke="{UNI_SH}" stroke-width="2"/>
      <rect x="{cx-7}" y="-290" width="14" height="14" fill="{SKIN_SH}"/>
      <path d="M{cx-9},-279 L{cx},-270 L{cx+9},-279" fill="none" stroke="{UNI_SH}" stroke-width="3" stroke-linejoin="round"/>
      <circle cx="{cx}" cy="-295" r="15" fill="{SKIN}"/>
      <path d="M{cx-21},-296 A21,21 0 0 1 {cx+21},-296 L{cx+23},-291 L{cx-23},-291 Z" fill="{HELM}"/>
      <path d="M{cx-13},-308 A15,15 0 0 1 {cx+3},-313" fill="none" stroke="{HELM_HI}" stroke-width="3" stroke-linecap="round"/>
      <path d="M{cx-16},-291 L{cx-9},-281 M{cx+16},-291 L{cx+9},-281" stroke="{CHASSIS}" stroke-width="2" opacity=".7"/>
    </g>'''


def profile_head(hx, hy, skin, helm, helm_hi=None):
    """Head + helmet in profile, facing right."""
    hi = f'<path d="M{hx-12},{hy-17} Q{hx-2},{hy-22} {hx+8},{hy-18}" fill="none" stroke="{helm_hi}" stroke-width="3" stroke-linecap="round"/>' if helm_hi else ''
    return f'''
      <circle cx="{hx}" cy="{hy}" r="15" fill="{skin}"/>
      <path d="M{hx-21},{hy+3} C{hx-22},{hy-24} {hx+12},{hy-30} {hx+18},{hy-5} L{hx+24},{hy-2} L{hx+24},{hy+1} L{hx-21},{hy+5} Z" fill="{helm}"/>
      {hi}
      <path d="M{hx-3},{hy+2} L{hx+5},{hy+15}" stroke="{CHASSIS}" stroke-width="2" opacity=".6"/>'''


def cab_occupants():
    # driver: far seat (left side of the vehicle), in shadow, slightly ahead
    dx, dy = 704, -342
    driver = f'''
      <rect x="{dx-20}" y="{dy+18}" width="36" height="80" rx="12" fill="{UNI_FAR}"/>
      <rect x="{dx-6}" y="{dy+8}" width="11" height="14" fill="{SKIN_FAR}"/>
      {profile_head(dx, dy, SKIN_FAR, HELM_FAR)}
      <path d="M{dx+2},{dy+30} L{dx+20},{dy+50} L{dx+36},{dy+36}" fill="none" stroke="{UNI_FAR}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="{dx+37}" cy="{dy+35}" r="5.5" fill="{SKIN_FAR}"/>
      <ellipse cx="{dx+40}" cy="{dy+36}" rx="5" ry="21" transform="rotate(-24 {dx+40} {dy+36})" fill="none" stroke="#0E110B" stroke-width="5"/>
      <path d="M{dx+18},{dy+18} L{dx+23},{dy+29}" stroke="{YEL}" stroke-width="5" opacity=".55"/>'''
    # co-driver (선탑자): near seat, belted, pointing ahead (지적확인)
    px, py = 670, -337
    seat = f'<rect x="{px-40}" y="{py-24}" width="16" height="110" rx="6" fill="#262D20"/>'
    codriver = f'''
      {seat}
      <rect x="{px-22}" y="{py+18}" width="40" height="80" rx="13" fill="{UNI}"/>
      <rect x="{px-6}" y="{py+8}" width="11" height="14" fill="{SKIN_SH}"/>
      {profile_head(px, py, SKIN, HELM, HELM_HI)}
      <path d="M{px-18},{py+20} L{px+14},{py+62}" stroke="{YEL}" stroke-width="8"/>
      <path d="M{px+2},{py+30} L{px+34},{py+40} L{px+62},{py+22}" fill="none" stroke="{UNI}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="{px+64}" cy="{py+21}" r="6" fill="{SKIN}"/>
      <path d="M{px+66},{py+19} L{px+76},{py+14}" stroke="{SKIN}" stroke-width="4" stroke-linecap="round"/>'''
    return driver + codriver


def truck():
    """6x6 cargo truck, side view, facing right. Local origin: rear end, ground line."""
    win = 'M616,-372 L738,-372 L758,-282 L616,-282 Z'
    wheels = ''
    for wx in (205, 345, 818):
        lugs = ''.join(
            f'<circle cx="{f(wx + 24 * math.cos(a))}" cy="{f(-64 + 24 * math.sin(a))}" r="3.2" fill="{CHASSIS}"/>'
            for a in [i * math.pi / 4 for i in range(8)])
        tread = ''.join(
            f'<rect x="{f(wx - 5)}" y="-131" width="10" height="9" rx="2" fill="#0B0D09" transform="rotate({i * 360 / 20:.1f} {wx} -64)"/>'
            for i in range(20))
        wheels += f'''
      <g>
        <circle cx="{wx}" cy="-64" r="66" fill="#0B0D09"/>
        {tread}
        <circle cx="{wx}" cy="-64" r="58" fill="#1A1D16"/>
        <circle cx="{wx}" cy="-64" r="47" fill="#23271D"/>
        <circle cx="{wx}" cy="-64" r="37" fill="{BODY_SH}"/>
        <circle cx="{wx}" cy="-64" r="37" fill="none" stroke="{BODY_HI}" stroke-width="2" opacity=".35"/>
        <circle cx="{wx}" cy="-64" r="29" fill="{BODY_DK}"/>
        {lugs}
        <circle cx="{wx}" cy="-64" r="13" fill="{BODY_SH}"/>
        <circle cx="{wx}" cy="-64" r="5" fill="{CHASSIS}"/>
      </g>'''

    bows = ''.join(f'<rect x="{bx}" y="-372" width="9" height="162" fill="#4A5234"/>'
                   for bx in (12, 152, 293, 434, 564))
    far_bows = ''.join(f'<rect x="{bx + 2}" y="-372" width="6" height="162" fill="#222A1A"/>'
                       for bx in (152, 293, 434))
    straps = ''.join(f'<rect x="{sx}" y="-392" width="7" height="30" rx="2" fill="{TARP_SH}"/>'
                     for sx in (82, 222, 363, 503))
    stakes = ''.join(f'<rect x="{sx}" y="-212" width="10" height="72" fill="{BODY_SH}"/>'
                     for sx in (12, 152, 293, 434, 564))
    passengers = ''.join(seated_front(cx) for cx in (82, 222, 364, 504))

    return f'''
    <g id="truck" transform="translate(360,1292)">
      <ellipse cx="500" cy="2" rx="560" ry="15" fill="#000" opacity=".38"/>
      <!-- chassis, tank, box -->
      <rect x="30" y="-130" width="910" height="30" fill="{CHASSIS}"/>
      <rect x="436" y="-132" width="130" height="44" rx="4" fill="{BODY_DK}"/>
      <rect x="436" y="-132" width="130" height="6" fill="{BODY_SH}"/>
      <rect x="604" y="-132" width="112" height="46" rx="12" fill="{BODY_SH}"/>
      <rect x="612" y="-126" width="96" height="5" rx="2.5" fill="{BODY_HI}" opacity=".4"/>
      <rect x="626" y="-132" width="7" height="46" fill="{CHASSIS}"/>
      <rect x="687" y="-132" width="7" height="46" fill="{CHASSIS}"/>
      <!-- cargo bed -->
      <rect x="0" y="-212" width="585" height="84" fill="{BODY_SH}"/>
      <rect x="0" y="-212" width="585" height="64" fill="#65703F"/>
      {stakes}
      <rect x="0" y="-212" width="585" height="7" fill="{BODY_HI}" opacity=".5"/>
      <rect x="0" y="-150" width="585" height="4" fill="{BODY_DK}"/>
      <rect x="-4" y="-200" width="8" height="16" rx="2" fill="#E0A526"/>
      <!-- canvas cover, near side rolled up -->
      <path d="M0,-212 L0,-384 Q0,-420 36,-420 L566,-420 Q585,-420 585,-401 L585,-212 Z" fill="{TARP}"/>
      <rect x="12" y="-372" width="561" height="162" fill="{FARWALL}"/>
      <rect x="12" y="-372" width="561" height="162" fill="url(#interiorShade)"/>
      {far_bows}
      <rect x="12" y="-262" width="561" height="5" fill="#222A1A"/>
      {passengers}
      {bows}
      <rect x="0" y="-212" width="585" height="7" fill="{BODY_HI}" opacity=".5"/>
      <rect x="0" y="-384" width="12" height="174" fill="{TARP_SH}"/>
      <rect x="573" y="-384" width="12" height="174" fill="{TARP_SH}"/>
      <path d="M4,-386 Q4,-414 34,-414 L564,-414 Q580,-414 580,-400 L580,-386 Z" fill="{TARP}"/>
      <path d="M36,-419 L566,-419" stroke="{BODY_HI}" stroke-width="2" opacity=".55"/>
      <rect x="2" y="-392" width="581" height="26" rx="13" fill="{TARP_ROLL}"/>
      <path d="M14,-379 L571,-379" stroke="{TARP_SH}" stroke-width="2" opacity=".7"/>
      {straps}
      <!-- cab -->
      <path d="M600,-140 L600,-370 Q600,-388 618,-388 L744,-388 Q754,-388 756,-378 L784,-262 L784,-140 Z" fill="{BODY}"/>
      <path d="M618,-387 L744,-387" stroke="{BODY_HI}" stroke-width="3" stroke-linecap="round"/>
      <path d="{win}" fill="{INTERIOR}"/>
      <g clip-path="url(#cabWin)">
        {cab_occupants()}
        <path d="M660,-372 L684,-372 L640,-282 L616,-282 Z" fill="#fff" opacity=".06"/>
        <path d="M694,-372 L702,-372 L658,-282 L650,-282 Z" fill="#fff" opacity=".05"/>
      </g>
      <path d="{win}" fill="none" stroke="{BODY_DK}" stroke-width="3"/>
      <path d="M610,-150 L610,-376 Q610,-380 614,-380" fill="none" stroke="{BODY_SH}" stroke-width="3"/>
      <path d="M770,-266 L770,-150" stroke="{BODY_SH}" stroke-width="3"/>
      <rect x="628" y="-268" width="30" height="7" rx="3" fill="{BODY_DK}"/>
      <rect x="614" y="-150" width="170" height="10" fill="{BODY_SH}"/>
      <rect x="628" y="-140" width="96" height="10" rx="2" fill="{CHASSIS}"/>
      <!-- mirror -->
      <path d="M770,-320 L794,-334" stroke="{CHASSIS}" stroke-width="4"/>
      <rect x="790" y="-378" width="15" height="54" rx="4" fill="{CHASSIS}"/>
      <rect x="792" y="-374" width="4" height="46" rx="2" fill="{BODY_HI}" opacity=".35"/>
      <!-- hood / engine -->
      <path d="M782,-262 L944,-254 Q962,-252 962,-234 L962,-150 L782,-150 Z" fill="{BODY}"/>
      <path d="M784,-261 L944,-253" stroke="{BODY_HI}" stroke-width="3" stroke-linecap="round"/>
      <path d="M836,-226 L906,-223 M836,-214 L906,-211 M836,-202 L906,-199" stroke="{BODY_DK}" stroke-width="4" stroke-linecap="round"/>
      <rect x="950" y="-248" width="12" height="98" fill="{BODY_DK}"/>
      <!-- front fender with wheel arch -->
      <path d="M740,-150 L740,-168 Q818,-190 898,-168 L906,-150 Z" fill="{BODY_SH}"/>
      <rect x="782" y="-150" width="180" height="26" fill="{BODY_SH}"/>
      <circle cx="818" cy="-64" r="78" fill="#161A12" clip-path="url(#archClip)"/>
      <!-- headlight + bumper -->
      <rect x="956" y="-214" width="18" height="26" rx="5" fill="{BODY_DK}"/>
      <rect x="968" y="-211" width="7" height="20" rx="3" fill="#F3EDD2"/>
      <rect x="938" y="-150" width="52" height="32" rx="3" fill="{CHASSIS}"/>
      <rect x="938" y="-150" width="52" height="4" fill="{BODY_SH}"/>
      {wheels}
    </g>'''


def guide(gx, gy):
    """유도병: ground guide in a reflective vest, signalling with a baton."""
    return f'''
    <g id="guide" transform="translate({gx},{gy})">
      <ellipse cx="10" cy="1" rx="52" ry="8" fill="#000" opacity=".4"/>
      <!-- far arm, stretched toward the truck -->
      <path d="M2,-178 L40,-168 L64,-176" fill="none" stroke="{UNI_FAR}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="62" y="-186" width="10" height="20" rx="5" fill="{SKIN_FAR}"/>
      <!-- legs -->
      <path d="M-4,-112 L-12,-12" stroke="{UNI_SH}" stroke-width="22" stroke-linecap="round"/>
      <path d="M8,-112 L22,-12" stroke="{UNI}" stroke-width="22" stroke-linecap="round"/>
      <path d="M-26,-12 Q-26,-22 -14,-22 L-2,-22 L0,0 L-26,0 Z" fill="#0E110B"/>
      <path d="M12,-22 L28,-22 Q42,-20 42,-8 L42,0 L12,0 Z" fill="#0E110B"/>
      <!-- torso + vest -->
      <rect x="-19" y="-192" width="40" height="92" rx="14" fill="{UNI}"/>
      <path d="M-20,-186 Q-20,-192 -12,-192 L14,-192 Q22,-192 22,-184 L22,-116 L-20,-116 Z" fill="{YEL}"/>
      <rect x="-20" y="-162" width="42" height="7" fill="#FFF6D6"/>
      <rect x="-20" y="-138" width="42" height="7" fill="#FFF6D6"/>
      <path d="M-20,-116 L22,-116" stroke="#C8971A" stroke-width="3"/>
      <!-- head -->
      <rect x="-5" y="-204" width="11" height="14" fill="{SKIN_SH}"/>
      {profile_head(2, -214, SKIN, HELM, HELM_HI)}
      <!-- near arm raised forward with baton -->
      <circle cx="50" cy="-330" r="30" fill="{YEL}" opacity=".16"/>
      <circle cx="50" cy="-330" r="16" fill="{YEL}" opacity=".22"/>
      <path d="M-2,-182 L34,-206 L44,-262" fill="none" stroke="{UNI}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="38" y="-276" width="12" height="16" rx="6" fill="{SKIN}"/>
      <rect x="42" y="-350" width="8" height="76" rx="4" fill="{YEL}" transform="rotate(6 46 -274)"/>
      <rect x="42" y="-350" width="8" height="30" rx="4" fill="{YEL_SOFT}" transform="rotate(6 46 -274)"/>
    </g>'''


def curve_sign(x, base_y):
    return f'''
    <g id="sign">
      <rect x="{x-4}" y="{base_y-128}" width="8" height="128" fill="#40463A"/>
      <rect x="{x-4}" y="{base_y-128}" width="3" height="128" fill="#5C6352"/>
      <g transform="translate({x},{base_y-150}) rotate(45)">
        <rect x="-40" y="-40" width="80" height="80" rx="9" fill="{YEL}"/>
        <rect x="-34" y="-34" width="68" height="68" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>
      </g>
      <g transform="translate({x},{base_y-150})" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M-9,26 L-9,4 Q-9,-12 7,-12 L10,-12"/>
        <path d="M2,-22 L12,-12 L2,-2"/>
      </g>
    </g>'''


def marker(n, x, y, tx, ty, label, side='right'):
    dx, dy = tx - x, ty - y
    ln = math.hypot(dx, dy)
    sx, sy = x + dx / ln * 36, y + dy / ln * 36
    if side == 'right':
        lab = f'<text x="{x+48}" y="{y+11}" class="mk-label">{label}</text>'
    else:
        lab = f'<text x="{x-48}" y="{y+11}" class="mk-label" text-anchor="end">{label}</text>'
    return f'''
    <g class="marker">
      <line x1="{f(sx)}" y1="{f(sy)}" x2="{tx}" y2="{ty}" stroke="{YEL}" stroke-width="2.5"/>
      <circle cx="{tx}" cy="{ty}" r="6" fill="{YEL}" stroke="{INK}" stroke-width="2.5"/>
      <circle cx="{x}" cy="{y}" r="36" fill="none" stroke="{YEL}" stroke-width="2" opacity=".35"/>
      <circle cx="{x}" cy="{y}" r="29" fill="{YEL}"/>
      <text x="{x}" y="{y+14}" class="mk-num" text-anchor="middle">{n}</text>
      {lab}
    </g>'''


def hero_svg():
    r1, c1 = ridge_path(*R1)
    r2, c2 = ridge_path(*R2)
    r3, c3 = ridge_path(*R3)
    road_d, left, right, centre = receding_road()
    # dashed centre line on the receding road
    dash = ''
    for i in range(2, 50, 5):
        x0, y0, w0, *_ = centre[i]
        x1, y1, w1, *_ = centre[i + 2]
        dash += f'<line x1="{f(x0)}" y1="{f(y0)}" x2="{f(x1)}" y2="{f(y1)}" stroke="#D9D2B8" stroke-width="{f(max(1.2, w0 / 22))}" opacity=".32"/>'
    # delineator posts on the outer (right-hand) edge
    posts = ''
    for i in (6, 14, 22, 30, 38):
        x, y = right[i]
        w = max(2.5, centre[i][2] / 14)
        h = w * 6
        posts += f'<rect x="{f(x - w / 2 + 6)}" y="{f(y - h)}" width="{f(w)}" height="{f(h)}" fill="#D8D2BE" opacity=".8"/>'
        posts += f'<rect x="{f(x - w / 2 + 6)}" y="{f(y - h)}" width="{f(w)}" height="{f(h / 3)}" fill="{YEL}"/>'

    markers = (
        marker(1, 1150, 800, 1064, 930, '운전병', 'right') +
        marker(2, 972, 800, 1030, 935, '선탑자', 'left') +
        marker(3, 138, 918, 186, 1090, '유도병', 'right') +
        marker(4, 520, 800, 582, 978, '탑승자', 'right')
    )

    return f'''
  <svg class="hero" viewBox="0 0 {W} {HERO_H}" width="{W}" height="{HERO_H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="sky" x1="0" y1="0" x2="0" y2="{HERO_H}" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="{SKY[0]}"/>
        <stop offset=".42" stop-color="{SKY[1]}"/>
        <stop offset=".63" stop-color="{SKY[2]}"/>
        <stop offset=".72" stop-color="{SKY[3]}"/>
        <stop offset="1" stop-color="{SKY[3]}"/>
      </linearGradient>
      <radialGradient id="glow" cx="1230" cy="900" r="620" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#B3A874" stop-opacity=".55"/>
        <stop offset="1" stop-color="#8C865A" stop-opacity="0"/>
      </radialGradient>
      <linearGradient id="mist" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#C9C3A2" stop-opacity="0"/>
        <stop offset="1" stop-color="#C9C3A2" stop-opacity=".10"/>
      </linearGradient>
      <linearGradient id="interiorShade" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0C0F09" stop-opacity=".75"/>
        <stop offset=".55" stop-color="#0C0F09" stop-opacity=".15"/>
        <stop offset="1" stop-color="#0C0F09" stop-opacity=".35"/>
      </linearGradient>
      <linearGradient id="beam" x1="1335" y1="0" x2="1587" y2="0" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#FFF1C2" stop-opacity=".34"/>
        <stop offset="1" stop-color="#FFF1C2" stop-opacity="0"/>
      </linearGradient>
      <clipPath id="cabWin"><path d="M616,-372 L738,-372 L758,-282 L616,-282 Z"/></clipPath>
      <clipPath id="archClip"><rect x="700" y="-160" width="240" height="36"/></clipPath>
    </defs>

    <rect width="{W}" height="{HERO_H}" fill="url(#sky)"/>
    <rect width="{W}" height="{HERO_H}" fill="url(#glow)"/>

    <path d="{r1}" fill="{RIDGE[0]}"/>
    <path d="{c1}" fill="none" stroke="#CFC7A0" stroke-opacity=".10" stroke-width="1.5"/>
    <rect x="0" y="880" width="{W}" height="90" fill="url(#mist)"/>
    <path d="{r2}" fill="{RIDGE[1]}"/>
    <path d="{c2}" fill="none" stroke="#CFC7A0" stroke-opacity=".08" stroke-width="1.5"/>
    <rect x="0" y="960" width="{W}" height="80" fill="url(#mist)"/>
    <path d="{r3}" fill="{RIDGE[2]}"/>
    <path d="{c3}" fill="none" stroke="#CFC7A0" stroke-opacity=".07" stroke-width="1.5"/>

    <!-- road -->
    <rect x="0" y="1222" width="{W}" height="150" fill="#2B3126"/>
    <rect x="0" y="1222" width="{W}" height="3" fill="#3F4636"/>
    <line x1="0" y1="1298" x2="{W}" y2="1298" stroke="#D9D2B8" stroke-width="5" stroke-dasharray="64 52" opacity=".28"/>
    <rect x="0" y="1360" width="{W}" height="4" fill="#D9D2B8" opacity=".22"/>

    {curve_sign(1496, 1218)}

    <!-- headlight beam -->
    <path d="M1334,1092 L1587,1016 L1587,1196 Z" fill="url(#beam)"/>

    {truck()}
    {guide(186, 1300)}
    {markers}
  </svg>'''


# ---------------------------------------------------------------- icons
def icon(name, size=46, color=YEL, sw=1.8):
    if name == 'seatbelt':
        body = ('<circle cx="12" cy="5" r="2.6"/>'
                '<path d="M6.5 21v-6.2a5.5 5.5 0 0 1 11 0v6.2"/>'
                '<path d="M8.6 10.9l7.6 10.1"/>'
                '<path d="M11.4 16.9l2.6 -2"/>')
    else:
        src = (ROOT / 'icons' / f'{name}.svg').read_text()
        inner = src[src.index('>', src.index('<svg')) + 1: src.rindex('</svg>')]
        body = re.sub(r'<path stroke="none"[^>]*/>', '', inner).strip()
    return (f'<svg class="ico" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


ROLES = [
    ('운전병', '핸들을 잡은 안전관', [
        ('clipboard-check', '운행 전', '일일점검표 확인'),
        ('zzz', '졸리면', '즉시 보고하고 휴식'),
        ('clock-pause', '장거리 운행은', '2시간마다 15분 휴식'),
    ]),
    ('선탑자', '승객이 아닌 안전 책임자', [
        ('seatbelt', '출발 전', '전원 안전벨트 확인'),
        ('hand-stop', '과속·졸음이 보이면', '즉시 제지'),
        ('eye-check', '운행 중 수시로', '운전병 상태 확인'),
    ]),
    ('유도병', '운전병의 눈', [
        ('arrow-back-up', '후진은', '반드시 유도병과'),
        ('alert-triangle', '차량 뒤 사각지대', '절대 서지 않기'),
        ('eye', '운전병과', '눈을 맞춘 뒤 신호'),
    ]),
    ('탑승자', '적재함의 안전관', [
        ('armchair', '적재함에서', '서 있지 않기'),
        ('hand-off', '이동 중', '몸 내밀지 않기'),
        ('speakerphone', '이상 발견 시', '즉시 알리기'),
    ]),
]


def rules_html():
    cols = []
    for i, (role, tag, items) in enumerate(ROLES, 1):
        lis = ''.join(f'<li>{icon(ic)}<span>{ctx}<b>{act}</b></span></li>' for ic, ctx, act in items)
        cols.append(f'''
      <div class="col">
        <div class="role"><span class="num">{i}</span><h2>{role}</h2></div>
        <p class="tag">{tag}</p>
        <ul>{lis}</ul>
      </div>''')
    return '\n'.join(cols)


CAUSES = [('차량사고', 34), ('추락·충격', 15), ('항공·함정', 11), ('익사', 11), ('총기', 3)]


def causes_html():
    maxw = 176
    rows = ''
    for i, (name, v) in enumerate(CAUSES):
        on = ' class="on"' if i == 0 else ''
        rows += (f'<dt{on}>{name}</dt><dd><i{on} style="width:{maxw * v / CAUSES[0][1]:.0f}px"></i>'
                 f'<em{on}>{v}%</em></dd>')
    return f'<dl class="causes">{rows}</dl>'


# ---------------------------------------------------------------- page
def page():
    fonts = ''.join(
        f"@font-face{{font-family:'Pretendard';src:url('fonts/Pretendard-{n}.otf');font-weight:{w};}}\n"
        for n, w in [('Regular', 400), ('Medium', 500), ('SemiBold', 600),
                     ('ExtraBold', 800), ('Black', 900)])
    fonts += ''.join(
        f"@font-face{{font-family:'BSS';src:url('fonts/BigShouldersStencilDisplay-{w}.woff2');font-weight:{w};}}\n"
        for w in (900,))
    fonts += ''.join(
        f"@font-face{{font-family:'Barlow Condensed';src:url('fonts/BarlowCondensed-{w}.woff2');font-weight:{w};}}\n"
        for w in (600, 700))

    css = f'''
{fonts}
@page {{ size: 420mm 594mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 420mm; height: 594mm; background: {GROUND}; }}
body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.poster {{ position: relative; width: 420mm; height: 594mm; overflow: hidden; background: {GROUND};
  font-family: 'Pretendard', sans-serif; color: {PAPER}; word-break: keep-all; }}
.hero {{ position: absolute; left: 0; top: 0; display: block; }}
.mk-num {{ font-family: 'BSS'; font-weight: 900; font-size: 40px; fill: {INK}; }}
.mk-label {{ font-family: 'Pretendard'; font-weight: 800; font-size: 32px; fill: {PAPER}; letter-spacing: -0.02em; }}

.head {{ position: absolute; left: {M}px; top: 104px; width: 1000px; }}
.eyebrow {{ display: flex; align-items: center; gap: 18px; font-size: 27px; font-weight: 600;
  letter-spacing: 0.18em; color: #CFC9B2; }}
.eyebrow .bar {{ width: 46px; height: 6px; background: {YEL}; }}
h1 {{ margin-top: 38px; font-weight: 900; font-size: 150px; line-height: 1.08; letter-spacing: -0.045em; color: {PAPER}; }}
h1 .y {{ color: {YEL}; }}
.sub {{ margin-top: 40px; font-size: 34px; line-height: 1.5; font-weight: 500; color: #C4BFA8; letter-spacing: -0.01em; }}
.sub b {{ font-weight: 800; color: {PAPER}; }}
.sub .dot {{ color: {YEL}; padding: 0 6px; }}

.stat {{ position: absolute; right: {M}px; top: 128px; width: 372px; padding-left: 34px; border-left: 1.5px solid rgba(242,238,225,.16); }}
.stat .n {{ font-family: 'Barlow Condensed'; font-weight: 700; font-size: 232px; line-height: .8; color: {YEL}; letter-spacing: -0.01em; }}
.stat .n small {{ font-size: 120px; margin-left: 6px; vertical-align: 78px; }}
.causes {{ margin-top: 28px; display: grid; grid-template-columns: 104px 1fr; row-gap: 10px; align-items: center; text-align: left; }}
.causes dt {{ font-size: 21px; font-weight: 600; color: #BDB8A1; white-space: nowrap; }}
.causes dt.on {{ color: {PAPER}; font-weight: 800; }}
.causes dd {{ display: flex; align-items: center; gap: 10px; }}
.causes i {{ display: block; height: 16px; border-radius: 0 4px 4px 0; background: #5E6450; }}
.causes i.on {{ background: {YEL}; }}
.causes em {{ font-style: normal; font-family: 'Barlow Condensed'; font-weight: 600; font-size: 24px; color: #BDB8A1; }}
.causes em.on {{ color: {PAPER}; font-weight: 700; }}
.stat .cap {{ margin-top: 22px; font-size: 27px; line-height: 1.45; font-weight: 500; color: #D6D0B9; }}
.stat .cap b {{ font-weight: 800; color: {PAPER}; }}
.stat .src {{ margin-top: 18px; font-size: 18px; color: #8F8C74; letter-spacing: 0.01em; }}

.rules {{ position: absolute; left: {M}px; right: {M}px; top: 1452px; display: grid;
  grid-template-columns: repeat(4, 1fr); column-gap: 0; }}
.col {{ padding: 0 24px; border-left: 1.5px solid rgba(242,238,225,.13); }}
.col:first-child {{ padding-left: 0; border-left: 0; }}
.col:last-child {{ padding-right: 0; }}
.role {{ display: flex; align-items: center; gap: 18px; }}
.role .num {{ width: 56px; height: 56px; border-radius: 50%; background: {YEL}; color: {INK};
  font-family: 'BSS'; font-weight: 900; font-size: 38px; display: flex; align-items: center; justify-content: center; padding-top: 2px; }}
.role h2 {{ font-weight: 900; font-size: 52px; letter-spacing: -0.03em; }}
.tag {{ margin-top: 16px; font-size: 26px; font-weight: 600; color: {MUTED}; letter-spacing: -0.01em; }}
ul {{ list-style: none; margin-top: 30px; padding-top: 34px; border-top: 1.5px solid rgba(242,238,225,.13); }}
li {{ display: flex; gap: 14px; align-items: flex-start; margin-bottom: 36px; }}
li .ico {{ flex: none; margin-top: -2px; }}
li span {{ font-size: 26px; line-height: 1.3; font-weight: 500; color: #BDB8A1; letter-spacing: -0.02em; white-space: nowrap; }}
li b {{ display: block; margin-top: 3px; font-size: 31px; font-weight: 800; color: {PAPER}; }}

.band {{ position: absolute; left: 0; right: 0; bottom: 0; height: 214px; background: {YEL};
  display: flex; align-items: center; justify-content: center; }}
.band p {{ font-weight: 900; font-size: 78px; letter-spacing: -0.04em; color: {INK}; }}
.band p em {{ font-style: normal; background: {INK}; color: {YEL}; padding: 0 14px 4px; margin: 0 4px; border-radius: 6px; }}
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
  {hero_svg()}
  <header class="head">
    <div class="eyebrow"><span class="bar"></span>육군 차량 안전사고 예방</div>
    <h1>한 대의 차량,<br>네 명의 <span class="y">안전관</span></h1>
    <p class="sub">운전병<span class="dot">·</span>선탑자<span class="dot">·</span>유도병<span class="dot">·</span>탑승자<br>각자의 자리에서 지키는 <b>12가지 안전 수칙</b></p>
  </header>
  <aside class="stat">
    <div class="n">34<small>%</small></div>
    <p class="cap">군 안전사고 사망자<br><b>3명 중 1명은 차량사고</b></p>
    {causes_html()}
    <p class="src">2010~2019년 군 안전사고 사망자 기준</p>
  </aside>
  <section class="rules">{rules_html()}
  </section>
  <footer class="band"><p>선탑자는 승객이 아니라 <em>안전관</em>입니다</p></footer>
</div>
</body>
</html>
'''


if __name__ == '__main__':
    (ROOT / 'poster.html').write_text(page(), encoding='utf-8')
    print('wrote', ROOT / 'poster.html')
