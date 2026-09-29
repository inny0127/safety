"""중형버스(현대 카운티 계열) 측면도.

좌표는 참고 사진(Juulchin Tourism Corp 10, Wikimedia Commons, 퍼블릭 도메인,
1280x720)의 픽셀 좌표를 그대로 쓴다. 사진 위에 겹쳐 보며 형태를 맞췄다.
버스는 오른쪽을 보고, 보이는 면은 출입문이 있는 오른쪽 옆면이다.
포스터에서는 transform으로 옮기고 키운다.
"""
import math

C = dict(
    white='#F2F2EE', white_sh='#D8D9D4', lower='#3D4042', lower_sh='#2C2F31',
    glass='#1C2227', pane='#262E34', frame='#0E1012', people='#0A0C0D',
    headrest='#C9CAC5', metal='#8B9092', chrome='#CDD0D0', tire='#131414',
    rim='#585D60', hub='#2A2D2F', lamp='#B22A1C', lens='#E6E3D8', belt='#FF5A1F',
)

GROUND = 577
WHEELS = ((408, 508), (998, 508))
R_TIRE = 69


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def pts(*p):
    return ' '.join(f'{f(x)},{f(y)}' for x, y in p)


def body_outline():
    """whole body silhouette with both wheel arches cut out"""
    return ('M112,498 C106,494 104,486 104,470 L104,210 C104,168 112,146 128,133 '
            'C140,124 156,119 180,118 L980,122 C1030,123 1068,129 1094,141 '
            'C1118,152 1136,172 1149,200 C1162,229 1171,268 1176,310 '
            'C1179,340 1180,372 1180,405 L1182,470 C1183,488 1182,498 1178,504 '
            'L1082,506 A84,84 0 0 0 914,506 L840,509 L686,509 L492,506 A84,84 0 0 0 324,506 Z')


def windows():
    g = []
    # passenger window band (rear quarter + two sliding bays), rounded at the rear
    g.append(f'<path d="M686,160 L686,318 L140,318 C128,318 122,311 122,299 L122,184 '
             f'C122,168 131,158 150,158 Z" fill="{C["frame"]}"/>')
    for x1, x2 in ((127, 151), (157, 410), (416, 682)):
        r = 12 if x1 == 127 else 0
        g.append(f'<rect x="{x1}" y="164" width="{x2 - x1}" height="148" rx="{r}" fill="{C["glass"]}"/>')
    # rear quarter louvre
    for i in range(9):
        y = 206 + i * 10
        g.append(f'<rect x="130" y="{y}" width="18" height="4" rx="2" fill="{C["frame"]}"/>')
    # sliding sashes
    for x in (282, 549):
        g.append(f'<rect x="{x - 2}" y="164" width="4" height="148" fill="{C["frame"]}"/>')
    # front side window + windscreen return + black garnish under it
    g.append(f'<path d="M842,172 L1040,174 C1072,176 1094,184 1110,199 C1127,216 1140,245 1149,282 '
             f'C1154,304 1158,330 1161,352 C1163,368 1164,378 1163,387 L1086,388 '
             f'C1058,388 1040,378 1033,358 C1030,346 1028,334 1028,322 L842,322 Z" fill="{C["frame"]}"/>')
    g.append(f'<path d="M848,178 L1038,180 C1068,182 1088,190 1103,204 C1118,220 1130,246 1139,280 '
             f'C1143,295 1146,308 1148,316 L848,316 Z" fill="{C["glass"]}"/>')
    return '\n'.join(g)


def door():
    g = []
    g.append(f'<rect x="686" y="168" width="154" height="341" fill="{C["metal"]}"/>')
    g.append(f'<rect x="690" y="172" width="146" height="26" fill="{C["frame"]}"/>')
    for x1, x2 in ((693, 760), (764, 833)):
        g.append(f'<rect x="{x1}" y="200" width="{x2 - x1}" height="303" fill="{C["white"]}"/>')
        g.append(f'<rect x="{x1}" y="402" width="{x2 - x1}" height="101" fill="{C["lower"]}"/>')
        g.append(f'<rect x="{x1 + 8}" y="204" width="{x2 - x1 - 16}" height="146" rx="6" fill="{C["frame"]}"/>')
        g.append(f'<rect x="{x1 + 11}" y="207" width="{x2 - x1 - 22}" height="140" rx="4" fill="{C["glass"]}"/>')
    g.append(f'<rect x="760" y="200" width="4" height="303" fill="{C["frame"]}"/>')
    for x in (752, 768):
        g.append(f'<rect x="{x}" y="362" width="4" height="36" rx="2" fill="{C["chrome"]}"/>')
    g.append(f'<rect x="686" y="503" width="154" height="6" fill="{C["frame"]}"/>')
    return '\n'.join(g)


def wheel(cx, cy):
    gy = cy + R_TIRE
    g = [f'<path d="M{cx - 78},{gy} C{cx - 50},{gy - 7} {cx - 10},{gy - 6} {cx + 32},{gy} '
         f'C{cx + 4},{gy + 2} {cx - 40},{gy + 2} {cx - 78},{gy} Z" fill="#000" opacity=".55"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{R_TIRE}" fill="{C["tire"]}"/>',
         f'<path d="M{cx - 24},{gy - 4} C{cx - 26},{gy - 1} {cx - 22},{gy} {cx - 16},{gy} L{cx + 16},{gy} '
         f'C{cx + 22},{gy} {cx + 26},{gy - 1} {cx + 24},{gy - 4} Z" fill="{C["tire"]}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{R_TIRE - 9}" fill="none" stroke="#1E2021" stroke-width="3"/>',
         f'<circle cx="{cx}" cy="{cy}" r="42" fill="{C["rim"]}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="42" fill="none" stroke="#6F7477" stroke-width="3"/>',
         f'<circle cx="{cx}" cy="{cy}" r="31" fill="#4A4E51"/>']
    for i in range(6):
        a = math.pi / 3 * i + 0.3
        g.append(f'<circle cx="{f(cx + 22 * math.cos(a))}" cy="{f(cy + 22 * math.sin(a))}" r="3.6" fill="#8C9295"/>')
    for i in range(4):
        a = math.pi / 2 * i + 0.75
        g.append(f'<ellipse cx="{f(cx + 35 * math.cos(a))}" cy="{f(cy + 35 * math.sin(a))}" rx="5" ry="3" '
                 f'transform="rotate({math.degrees(a):.0f} {f(cx + 35 * math.cos(a))} {f(cy + 35 * math.sin(a))})" fill="#2E3234"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{C["hub"]}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#6F7477"/>')
    return '\n'.join(g)


def bus(people=''):
    """return the bus group in reference-photo coordinates; `people` is drawn behind the glass tint"""
    g = []
    # ground shadow
    # cast shadow as in the reference photo: a band under the body, reaching a little past the rear,
    # soft fringe first, then the core, then dark contact patches where the tyres meet the ground
    g.append(f'<path d="M118,{GROUND - 84} L1148,{GROUND - 80} C1158,{GROUND - 60} 1160,{GROUND - 42} 1148,{GROUND - 24} L1086,{GROUND - 16} C1072,{GROUND - 10} 1060,{GROUND - 2} 1040,{GROUND} L930,{GROUND} C906,{GROUND - 10} 892,{GROUND - 18} 872,{GROUND - 20} L508,{GROUND - 22} C490,{GROUND - 26} 478,{GROUND - 8} 460,{GROUND} L350,{GROUND} C326,{GROUND - 10} 312,{GROUND - 16} 292,{GROUND - 22} C220,{GROUND - 26} 150,{GROUND - 28} 84,{GROUND - 28} C76,{GROUND - 40} 74,{GROUND - 44} 78,{GROUND - 50} Z" fill="#000" opacity=".16"/>')
    g.append(f'<path d="M126,{GROUND - 76} L1140,{GROUND - 72} C1150,{GROUND - 60} 1152,{GROUND - 42} 1140,{GROUND - 32} L1078,{GROUND - 24} C1064,{GROUND - 10} 1052,{GROUND - 2} 1032,{GROUND} L930,{GROUND} C914,{GROUND - 10} 900,{GROUND - 26} 880,{GROUND - 28} L500,{GROUND - 30} C482,{GROUND - 26} 470,{GROUND - 8} 452,{GROUND} L350,{GROUND} C334,{GROUND - 10} 320,{GROUND - 24} 300,{GROUND - 30} C220,{GROUND - 34} 150,{GROUND - 36} 92,{GROUND - 36} C84,{GROUND - 40} 82,{GROUND - 44} 86,{GROUND - 50} Z" fill="#000" opacity=".32"/>')
    # wheels behind the body (arches cut the body)
    g.append('<clipPath id="busBody"><path d="' + body_outline() + '"/></clipPath>')
    g.append(f'<path d="M912,506 A86,86 0 0 1 1084,506 Z" fill="{C["frame"]}"/>')
    g.append(f'<path d="M322,506 A86,86 0 0 1 494,506 Z" fill="{C["frame"]}"/>')
    for cx, cy in WHEELS:
        g.append(wheel(cx, cy))
    # body
    g.append(f'<path d="{body_outline()}" fill="{C["white"]}"/>')
    g.append(f'<g clip-path="url(#busBody)">'
             f'<rect x="90" y="403" width="1100" height="120" fill="{C["lower"]}"/>'
             f'<rect x="90" y="403" width="1100" height="3" fill="{C["lower_sh"]}"/>'
             f'<rect x="90" y="118" width="1100" height="9" fill="#FFFFFF" opacity=".55"/>'
             f'<rect x="90" y="318" width="1100" height="6" fill="{C["white_sh"]}"/>'
             f'<path d="M150,437 L322,437 M1086,437 L1170,437" stroke="{C["lower_sh"]}" stroke-width="2"/>'
             f'</g>')
    # volume: shade along the rounded front and rear, clipped to the white body
    g.append(f'<g clip-path="url(#busBody)" opacity=".55">'
             f'<path d="M1096,140 C1126,158 1148,194 1160,240 C1170,284 1175,340 1176,402 L1152,402 '
             f'C1152,342 1147,292 1139,252 C1129,206 1114,172 1088,146 Z" fill="{C["white_sh"]}"/>'
             f'<path d="M152,121 C130,131 113,152 108,190 L106,402 L122,402 L123,196 C125,162 134,140 152,128 Z" fill="{C["white_sh"]}"/>'
             f'</g>')
    for mx in (292, 1104):
        g.append(f'<rect x="{mx}" y="452" width="18" height="8" rx="3" fill="#F2A31B"/>')
    # wheel-arch lips
    for cx in (408, 998):
        g.append(f'<path d="M{cx - 86},506 A86,86 0 0 1 {cx + 86},506" fill="none" stroke="{C["lower_sh"]}" stroke-width="6"/>')
    # roof vent
    g.append(f'<path d="M338,118 L346,109 L412,109 L420,118 Z" fill="{C["white_sh"]}"/>')
    # glass, people, door
    g.append(windows())
    g.append(f'<g clip-path="url(#busGlass)">{people}</g>')
    g.append('<clipPath id="busGlass">'
             '<rect x="157" y="164" width="253" height="148"/><rect x="416" y="164" width="266" height="148"/>'
             '<path d="M848,178 L1038,180 C1068,182 1088,190 1103,204 C1118,220 1130,246 1139,280 '
             'C1143,295 1146,308 1148,316 L848,316 Z"/></clipPath>')
    # glass reflections
    for x in (200, 470, 900):
        g.append(f'<path d="M{x},164 L{x + 40},164 L{x - 34},312 L{x - 74},312 Z" fill="#FFFFFF" opacity=".05" clip-path="url(#busGlass)"/>')
    g.append(door())
    # front: lamp, bumper, mirror
    g.append(f'<path d="M1162,408 L1178,408 C1181,420 1181,440 1179,452 L1162,452 Z" fill="{C["lens"]}"/>')
    g.append(f'<path d="M1150,462 L1181,462 C1184,480 1183,496 1178,504 L1150,506 Z" fill="{C["lower_sh"]}"/>')
    g.append(f'<path d="M1168,320 C1190,318 1206,316 1216,312" fill="none" stroke="{C["frame"]}" stroke-width="5" stroke-linecap="round"/>')
    g.append(f'<rect x="1204" y="250" width="26" height="64" rx="9" fill="{C["frame"]}"/>')
    g.append(f'<rect x="1208" y="256" width="6" height="52" rx="3" fill="#3A4045"/>')
    # rear: tail lamp, flap
    g.append(f'<path d="M104,393 L120,393 C124,393 125,396 125,400 L125,440 C125,444 123,446 119,446 L104,446 Z" fill="{C["lamp"]}"/>')
    # mud flaps: dusty rubber sheet hung from under the skirt behind each tyre; the lower end kicks back
    for x0, top, bot, w in ((322, 497, 568, 19), (910, 505, 552, 15)):
        x1 = x0 + w
        g.append(f'<path d="M{x0},{top} L{x1},{top} L{x1 - 1},{bot - 30} C{x1 - 2},{bot - 12} {x1 - 7},{bot - 2} {x0 + 1},{bot + 1} '
                 f'L{x0 - 7},{bot + 2} C{x0 - 4},{bot - 8} {x0 - 2},{bot - 20} {x0 - 1},{bot - 32} Z" fill="#55595C"/>')
        g.append(f'<path d="M{x1 - 1},{top} L{x1 - 2},{bot - 30} C{x1 - 3},{bot - 12} {x1 - 8},{bot - 3} {x0 + 1},{bot}" fill="none" stroke="#35393C" stroke-width="3"/>')
        g.append(f'<path d="M{x0 + 2},{top + 4} L{x0 + 1},{bot - 32}" stroke="#71767A" stroke-width="2" stroke-linecap="round"/>')
        g.append(f'<rect x="{x0 - 1}" y="{top - 2}" width="{w + 2}" height="5" fill="#1B1E20"/>')
    # fuel / battery hatch
    g.append(f'<rect x="854" y="455" width="36" height="26" rx="4" fill="none" stroke="{C["lower_sh"]}" stroke-width="2"/>')
    return '\n'.join(g)


# ---------------------------------------------------------------- people (photo coordinates)
PASSENGERS = (212, 330, 482, 600)      # head x of the belted passengers
CODRIVER = (1003, 250)                 # near-side front seat (선탑자)
DRIVER = (1062, 236)                   # far side, at the wheel (운전병)


def seated(hx, hy, col=None, belt=True, seat=True, cover=True):
    """seated soldier in profile facing right, patrol cap, 3-point belt over the chest"""
    col = col or C['people']
    g = []
    if seat:
        g.append(f'<path d="M{hx - 34},{hy + 110} L{hx - 32},{hy - 20} C{hx - 31},{hy - 33} {hx - 24},{hy - 38} '
                 f'{hx - 16},{hy - 38} C{hx - 8},{hy - 38} {hx - 3},{hy - 33} {hx - 3},{hy - 22} L{hx - 5},{hy + 110} Z" fill="#11161A"/>')
        if cover:
            g.append(f'<path d="M{hx - 32},{hy - 18} C{hx - 31},{hy - 31} {hx - 24},{hy - 37} {hx - 16},{hy - 37} '
                     f'C{hx - 8},{hy - 37} {hx - 3},{hy - 31} {hx - 3},{hy - 20} L{hx - 4},{hy + 12} L{hx - 31},{hy + 12} Z" '
                     f'fill="{C["headrest"]}" opacity=".9"/>')
    # torso + neck (back leans slightly into the seat)
    g.append(f'<path d="M{hx - 24},{hy + 110} L{hx - 22},{hy + 40} C{hx - 22},{hy + 24} {hx - 14},{hy + 17} {hx - 4},{hy + 15} '
             f'L{hx - 4},{hy + 8} L{hx + 7},{hy + 8} L{hx + 8},{hy + 16} C{hx + 20},{hy + 19} {hx + 25},{hy + 30} {hx + 24},{hy + 46} '
             f'L{hx + 22},{hy + 110} Z" fill="{col}"/>')
    # head
    g.append(f'<path d="M{hx - 13},{hy + 2} C{hx - 14},{hy - 10} {hx - 7},{hy - 15} {hx + 1},{hy - 15} C{hx + 10},{hy - 15} '
             f'{hx + 15},{hy - 9} {hx + 15},{hy - 1} L{hx + 18},{hy + 5} L{hx + 14},{hy + 7} C{hx + 14},{hy + 12} '
             f'{hx + 11},{hy + 15} {hx + 5},{hy + 15} L{hx - 4},{hy + 14} C{hx - 10},{hy + 12} {hx - 13},{hy + 8} {hx - 13},{hy + 2} Z" fill="{col}"/>')
    # patrol cap: flat crown sitting low on the head, short brim at brow level
    g.append(f'<path d="M{hx - 14},{hy - 3} L{hx - 14},{hy - 12} C{hx - 14},{hy - 17} {hx - 10},{hy - 20} {hx - 4},{hy - 20} '
             f'L{hx + 9},{hy - 20} C{hx + 13},{hy - 20} {hx + 15},{hy - 17} {hx + 15},{hy - 13} L{hx + 15},{hy - 8} '
             f'L{hx + 25},{hy - 6} C{hx + 27},{hy - 4} {hx + 25},{hy - 2} {hx + 22},{hy - 2} L{hx - 14},{hy - 1} Z" fill="{col}"/>')
    if belt:
        g.append(f'<path d="M{hx - 19},{hy + 20} L{hx - 11},{hy + 17} L{hx + 22},{hy + 76} L{hx + 14},{hy + 80} Z" fill="{C["belt"]}"/>')
    return '\n'.join(g)


def people():
    g = []
    # driver: far side, slightly smaller and darker, hands on the big flat bus wheel
    dx, dy = DRIVER
    g.append(seated(dx, dy, col='#07090A', seat=False))
    g.append(f'<path d="M{dx + 4},{dy + 36} C{dx + 14},{dy + 48} {dx + 24},{dy + 54} {dx + 36},{dy + 54}" fill="none" '
             f'stroke="#07090A" stroke-width="10" stroke-linecap="round"/>')
    g.append(f'<ellipse cx="{dx + 42}" cy="{dy + 56}" rx="27" ry="5" transform="rotate(-38 {dx + 42} {dy + 56})" '
             f'fill="none" stroke="#07090A" stroke-width="5"/>')
    # co-driver in the near-side front seat
    cx, cy = CODRIVER
    g.append(seated(cx, cy))
    for hx in PASSENGERS:
        g.append(seated(hx, 250))
    return '\n'.join(g)


def guide(x, y, s=1.0, vest='#EDEDE8', stripe='#FF5A1F', baton='#FFFFFF', col='#0D0F10'):
    """ground guide (유도병) standing, facing right, signalling with a raised baton. (x, y) = feet."""
    body = (
        # back leg (trousers bloused into boots)
        'M-23,-122 C-26,-100 -26,-80 -24,-62 C-23,-46 -22,-30 -22,-15 C-22,-12 -3,-12 -2,-15 '
        'C-1,-30 1,-46 2,-62 C4,-82 6,-102 8,-122 Z '
        # front leg, stepped forward
        'M-1,-124 C3,-102 9,-82 13,-62 C16,-46 18,-30 19,-15 C19,-12 39,-12 39,-15 '
        'C37,-30 34,-48 31,-64 C27,-86 24,-106 23,-124 Z '
        # boots
        'M-24,-16 L-1,-16 L0,0 L-26,0 C-27,-8 -26,-13 -24,-16 Z '
        'M18,-16 L37,-16 C44,-12 48,-6 48,0 L17,0 Z '
        # torso
        'M-20,-118 C-22,-146 -22,-170 -18,-190 C-15,-202 -6,-208 4,-208 C14,-208 22,-202 24,-190 '
        'C27,-170 26,-144 23,-118 Z '
        # neck
        'M-3,-212 L9,-212 L9,-202 L-3,-202 Z'
    )
    head = ('M-10,-226 C-10,-236 -4,-242 4,-242 C12,-242 17,-236 17,-228 L19,-222 L16,-220 '
            'C16,-214 13,-210 7,-210 L0,-210 C-6,-211 -10,-216 -10,-222 Z')
    helmet = ('M-15,-224 C-16,-244 -6,-254 5,-254 C17,-254 24,-245 24,-232 L27,-227 L22,-226 '
              'C18,-229 10,-231 2,-231 C-5,-231 -11,-229 -15,-224 Z')
    vest_d = ('M-19,-186 C-17,-198 -9,-205 2,-205 C13,-205 21,-199 23,-188 C25,-170 25,-150 24,-136 '
              'L-21,-136 C-22,-152 -21,-172 -19,-186 Z')
    arm_up = 'M-6,-190 C-2,-200 8,-206 18,-212 C24,-216 28,-224 32,-236 C36,-248 40,-258 43,-266 C47,-270 53,-266 51,-260 C47,-246 43,-232 39,-220 C35,-208 26,-198 16,-190 C8,-184 -2,-180 -6,-190 Z'
    hand_up = 'M40,-262 C39,-272 44,-279 50,-278 C56,-277 57,-269 53,-262 Z'
    arm_fw = 'M8,-192 C20,-186 34,-180 48,-176 C54,-175 55,-167 49,-166 C34,-168 18,-172 6,-178 Z'
    hand_fw = 'M47,-178 C52,-184 60,-184 63,-178 C64,-172 60,-166 52,-166 C49,-168 47,-172 47,-178 Z'
    return (f'<g transform="translate({f(x)},{f(y)}) scale({s})">'
            f'<ellipse cx="10" cy="1" rx="42" ry="6" fill="#000" opacity=".28"/>'
            f'<path d="{arm_fw}" fill="{col}"/><path d="{hand_fw}" fill="{col}"/>'
            f'<path d="{body}" fill="{col}"/>'
            f'<path d="{vest_d}" fill="{vest}"/>'
            f'<rect x="-22" y="-176" width="47" height="7" fill="{stripe}"/>'
            f'<rect x="-22" y="-156" width="47" height="7" fill="{stripe}"/>'
            f'<rect x="-21" y="-136" width="45" height="7" fill="{col}"/>'
            f'<path d="{head}" fill="{col}"/><path d="{helmet}" fill="{col}"/>'
            f'<path d="{arm_up}" fill="{col}"/><path d="{hand_up}" fill="{col}"/>'
            f'<rect x="44" y="-338" width="9" height="66" rx="4.5" fill="{baton}" transform="rotate(14 48 -272)"/>'
            f'</g>')
