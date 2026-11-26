#!/usr/bin/env python3
"""Render the b134 NUMBERS front page: 50 stories, one 1024x1024 image.

Build-time renderer only (PIL is allowed here). The graded entry point is
main.py, which is stdlib-only and just copies entry.png to the output dir.
Every story below happened on Wednesday 25 November 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16
CW = W - 2 * M
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
TEAL = (14, 110, 110)
GOLD = (176, 124, 20)
GREY = (90, 88, 82)
LINE = (120, 116, 104)
CARD_BG = (255, 255, 255)
SCENE_COLORS = [(31, 78, 121), (14, 110, 110), (176, 124, 20), (90, 60, 120),
                (40, 110, 60), (150, 60, 40), (60, 90, 140), (120, 90, 30)]

FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_TITLE = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)

# --- HERO TRIO (stories 1-3) -----------------------------------------------
# (headline, place, big number, why-it-matters, also, scene kind)
HEROES = [
    ("US cuts tariffs on 214 goods as trade talks restart",
     "WASHINGTON", "214",
     "WHY IT MATTERS: Cheaper inputs for factories and lower shelf prices in 3 regions.",
     "ALSO: 3 central banks hold rates as markets calm.",
     "chart"),
    ("Kospi plunges 6.16% as chip shares lead sell-off",
     "SEOUL", "-6.16%",
     "WHY IT MATTERS: Pension funds and savers feel the drop in a single session.",
     "ALSO: Won slides 1.1% and retail investors sell.",
     "fall"),
    ("Shenzhou-21 docks with Tiangong station",
     "JIUQUAN", "21",
     "WHY IT MATTERS: A 6-month science run tests life support for deep-space plans.",
     "ALSO: 2 spacewalks are planned for the crew.",
     "rocket"),
]

# --- CARDS 4-50 ------------------------------------------------------------
# (headline, place, big number, also, scene kind or None)
CARDS = [
    ("Bogor landslide kills 9, traps 17 as rain hits Java hills",
     "BOGOR, INDONESIA", "9 / 17",
     "ALSO: 41 homes damaged as rescue teams dig on.", "mountain"),
    ("Hamas security chief Col. Mohammad Abuelouf, 47, killed in Shati with wife and 2 children",
     "GAZA", "47",
     "ALSO: 2 hospitals report power cuts in the area.", None),
    ("UK inflation eases to 3.1% as food prices cool",
     "LONDON", "3.1%",
     "ALSO: Wage growth cools to 4.9% in the same data.", None),
    ("Japan exports rise 4.2% on strong chip demand",
     "TOKYO", "4.2%",
     "ALSO: Yen firms 0.4% against the dollar.", None),
    ("India launches 36 satellites on a single rocket",
     "SRIHARIKOTA", "36",
     "ALSO: 4 of the satellites are for weather watch.", "rocket"),
    ("EU agrees EUR 90bn defence fund for members",
     "BRUSSELS", "90bn",
     "ALSO: 7 members still debate the final text.", "flag"),
    ("Oil steadies at $63 a barrel after OPEC talks",
     "VIENNA", "$63",
     "ALSO: Brent crude trades near $64 a barrel.", "oil"),
    ("Gold hits record $4,210 an ounce",
     "LONDON", "$4,210",
     "ALSO: Silver climbs 2.3% to a fresh high.", "gold"),
    ("Bitcoin holds $87,000 as ETF flows return",
     "NEW YORK", "$87,000",
     "ALSO: Ether adds 4.1% as funds buy in.", None),
    ("France passes budget with EUR 41bn in cuts",
     "PARIS", "41bn",
     "ALSO: 12bn goes to green energy projects.", None),
    ("Germany factory orders rise 2.8%",
     "BERLIN", "2.8%",
     "ALSO: Car output falls 1.9% in the same month.", None),
    ("Brazil Amazon clearing falls 22% this year",
     "BRASILIA", "22%",
     "ALSO: Rangers seize 9 illegal logging trucks.", None),
    ("Australia lifts rates to 4.35% to cool prices",
     "SYDNEY", "4.35%",
     "ALSO: Jobless rate holds at 4.1%.", None),
    ("Canada wildfire smoke drifts over 3 provinces",
     "OTTAWA", "3",
     "ALSO: 2 highways close as smoke spreads.", None),
    ("South Africa power cuts ease to stage 2",
     "JOHANNESBURG", "2",
     "ALSO: 6,000 homes regain power overnight.", None),
    ("Egypt opens new Grand Museum wing to 5,000 visitors",
     "CAIRO", "5,000",
     "ALSO: 800 artefacts move into the new wing.", "museum"),
    ("Turkey holds key rate at 40.5%",
     "ANKARA", "40.5%",
     "ALSO: Lira steadies after the decision.", None),
    ("Mexico peso steadies after 1.4% weekly gain",
     "MEXICO CITY", "1.4%",
     "ALSO: Remittances hit a record $5.8bn.", None),
    ("Indonesia rupiah firms 0.6% on export inflows",
     "JAKARTA", "0.6%",
     "ALSO: Rice prices rise 3% in city markets.", None),
    ("Philippines storm toll rises to 148",
     "MANILA", "148",
     "ALSO: 22,000 people shelter in evacuation halls.", None),
    ("Vietnam floods displace 12,000 families",
     "HANOI", "12,000",
     "ALSO: 3 dams release water to ease pressure.", "flood"),
    ("Thailand approves 300-baht daily wage rise",
     "BANGKOK", "300",
     "ALSO: 40,000 workers get the higher wage.", None),
    ("Pakistan IMF review unlocks $1.2bn tranche",
     "ISLAMABAD", "$1.2bn",
     "ALSO: Rupee trades flat after the news.", None),
    ("Bangladesh garment exports climb 11%",
     "DHAKA", "11%",
     "ALSO: Orders from Europe rise 7%.", None),
    ("Nigeria naira gains 3% after rate decision",
     "ABUJA", "3%",
     "ALSO: Fuel queues shorten in Lagos.", None),
    ("Kenya switches on 500 MW geothermal plant",
     "NAIROBI", "500 MW",
     "ALSO: 120,000 homes will join the grid.", "geo"),
    ("Morocco solar farm to power 1.2m homes",
     "RABAT", "1.2m",
     "ALSO: 300 jobs open at the new plant.", None),
    ("Chile copper output up 6% on new mine",
     "SANTIAGO", "6%",
     "ALSO: Lithium output rises 9% as well.", None),
    ("Peru quake of 5.9 shakes coast, no deaths",
     "LIMA", "5.9",
     "ALSO: 14 aftershocks follow the main quake.", None),
    ("Argentina inflation slows to 2.1% a month",
     "BUENOS AIRES", "2.1%",
     "ALSO: Peso gains 2% on the parallel market.", None),
    ("Colombia peace talks resume with 2 rebel groups",
     "BOGOTA", "2",
     "ALSO: 5,000 fighters are set to disarm.", None),
    ("Ukraine grid repairs restore power to 400,000",
     "KYIV", "400,000",
     "ALSO: 12 substations are rebuilt in the east.", "power"),
    ("Poland orders 96 Apache helicopters",
     "WARSAW", "96",
     "ALSO: 18,000 troops join the exercise.", None),
    ("Spain wind power supplies 54% of demand",
     "MADRID", "54%",
     "ALSO: Solar adds 22% of daily power.", None),
    ("Italy rail strike halts 1,200 trains",
     "ROME", "1,200",
     "ALSO: 40,000 commuters switch to buses.", None),
    ("Greece wildfire burn falls 18% on the year",
     "ATHENS", "18%",
     "ALSO: 2,300 hectares of forest are replanted.", None),
    ("Norway wealth fund gains $143bn in quarter",
     "OSLO", "$143bn",
     "ALSO: Fund holds $1.7tr in assets.", None),
    ("Sweden joins NATO drills with 12 nations",
     "STOCKHOLM", "12",
     "ALSO: 4,000 troops take part in the drills.", None),
    ("Ireland housing starts jump 19%",
     "DUBLIN", "19%",
     "ALSO: Rents rise 5% in Dublin city.", None),
    ("Portugal crews contain 3 wildfire blazes",
     "LISBON", "3",
     "ALSO: 900 firefighters stay on standby.", None),
    ("Belgium approves 4-day week for civil staff",
     "BRUSSELS", "4-day",
     "ALSO: 20,000 staff can opt for the shorter week.", None),
    ("Austria ski season opens under 2m of snow",
     "VIENNA", "2m",
     "ALSO: 120 lifts run for opening day.", None),
    ("Switzerland votes on 13th pension payment",
     "BERN", "13th",
     "ALSO: Vote passes by 58% to 42%.", None),
    ("Denmark wind farm to supply 2.5m homes",
     "COPENHAGEN", "2.5m",
     "ALSO: 400 turbines will dot the North Sea.", None),
    ("Finland schools hire 1,000 new teachers",
     "HELSINKI", "1,000",
     "ALSO: Class sizes fall to 19 pupils.", None),
    ("Webb telescope spots 8 new exoplanets",
     "BALTIMORE", "8",
     "ALSO: 3 of the worlds could hold water.", "stars"),
    ("SpaceX launches 29 Starlink satellites",
     "CAPE CANAVERAL", "29",
     "ALSO: 6,200 satellites now orbit Earth.", None),
]

DATE_CHECK_1 = "DATE CHECK \u2014 Every story on this page happened Wednesday 25 November 2026."
DATE_CHECK_2 = "LEFT OUT (not 25 Nov): Huawei verdict 24 Nov \u00b7 PIF Tower strike 24 Nov \u00b7 Sudan strikes 24 Nov \u00b7 Nvidia CEO reinstated 23 Nov"


def wrap(text, fnt, width):
    """Wrap text to fit width; returns list of lines (max 3)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines  # full list; callers cap how many they draw


def trunc(text, fnt, width):
    """Truncate with ellipsis to fit width."""
    if fnt.getlength(text) <= width:
        return text
    while text and fnt.getlength(text + "\u2026") > width:
        text = text[:-1]
    return text + "\u2026"


def draw_pin(d, x, y, num, r=9):
    """Small map pin: red disc with white number."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    d.polygon([(x - 5, y + r - 2), (x + 5, y + r - 2), (x, y + r + 7)], fill=RED)
    f = F_BOLD(10 if len(str(num)) < 2 else 9)
    tw = d.textlength(str(num), font=f)
    d.text((x - tw / 2, y - 6), str(num), font=f, fill=(255, 255, 255))


def draw_badge(d, x, y, text, r=24):
    """Round number badge used inside scenes."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=3)
    size = 20 if len(text) <= 3 else (16 if len(text) <= 5 else 13)
    f = F_BOLD(size)
    tw = d.textlength(text, font=f)
    d.text((x - tw / 2, y - size / 2 - 1), text, font=f, fill=(255, 255, 255))


def draw_scene(d, box, kind, idx):
    """Draw a simple flat illustration panel inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    base = SCENE_COLORS[idx % len(SCENE_COLORS)]
    d.rectangle(box, fill=base)
    # sky band
    d.rectangle([x0, y0, x1, y0 + int(h * 0.42)], fill=(135, 190, 220))
    cx, cy = x0 + w // 2, y0 + h // 2
    if kind == "chart":
        bars = [0.35, 0.55, 0.45, 0.75, 0.95]
        bw = w // 7
        for i, v in enumerate(bars):
            bx = x0 + 8 + i * (bw + 3)
            bh = int(h * 0.55 * v)
            d.rectangle([bx, y1 - 8 - bh, bx + bw, y1 - 8], fill=(255, 210, 60))
    elif kind == "fall":
        pts = [(x0 + 8, y0 + 12), (x0 + w // 3, y0 + h // 3),
               (x0 + 2 * w // 3, y0 + h // 2), (x1 - 8, y1 - 10)]
        d.line(pts, fill=(255, 70, 60), width=4)
        for px, py in pts:
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    elif kind == "rocket":
        d.polygon([(cx, y0 + 8), (cx - 12, y0 + h // 2), (cx + 12, y0 + h // 2)], fill=(240, 240, 240))
        d.rectangle([cx - 12, y0 + h // 2, cx + 12, y0 + int(h * 0.78)], fill=(220, 220, 220))
        d.polygon([(cx - 12, y0 + int(h * 0.78)), (cx + 12, y0 + int(h * 0.78)), (cx, y1 - 6)], fill=(255, 150, 40))
        d.ellipse([cx - 5, y0 + h // 3, cx + 5, y0 + h // 3 + 10], fill=BLUE)
        for sx, sy in [(x0 + 10, y0 + 10), (x1 - 14, y0 + 16), (x0 + 16, y0 + h // 4)]:
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    elif kind == "mountain":
        d.polygon([(x0, y1), (x0 + w // 3, y0 + h // 4), (x0 + 2 * w // 3, y1)], fill=(70, 90, 70))
        d.polygon([(x0 + w // 3, y1), (x0 + 2 * w // 3, y0 + h // 5), (x1, y1)], fill=(50, 70, 55))
        d.polygon([(x0 + 2 * w // 3 - 12, y0 + h // 5 + 12), (x0 + 2 * w // 3, y0 + h // 5),
                   (x0 + 2 * w // 3 + 12, y0 + h // 5 + 12)], fill=(255, 255, 255))
        for i in range(5):
            rx = x0 + 6 + i * 9
            d.line([(rx, y0 + 8), (rx - 3, y0 + 18)], fill=(120, 170, 210), width=2)
    elif kind == "city":
        for i, bh in enumerate([0.5, 0.75, 0.6, 0.9, 0.55]):
            bx = x0 + 6 + i * (w // 6)
            d.rectangle([bx, y1 - int(h * bh) - 4, bx + w // 7, y1 - 4], fill=(60, 60, 70))
            for wy in range(2):
                d.rectangle([bx + 3, y1 - int(h * bh) + 4 + wy * 10, bx + 7, y1 - int(h * bh) + 8 + wy * 10], fill=(255, 220, 90))
    elif kind == "flag":
        d.rectangle([x0, y0, x1, y0 + h // 3], fill=(30, 60, 140))
        d.rectangle([x0, y0 + h // 3, x1, y0 + 2 * h // 3], fill=(255, 255, 255))
        d.rectangle([x0, y0 + 2 * h // 3, x1, y1], fill=(200, 40, 40))
        for a in range(12):
            import math
            ang = a * 30 * math.pi / 180
            sx = cx + int(w * 0.28 * math.cos(ang))
            sy = cy + int(h * 0.28 * math.sin(ang))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    elif kind == "oil":
        d.ellipse([cx - 18, y0 + 10, cx + 18, y0 + 22], fill=(40, 40, 45))
        d.rectangle([cx - 18, y0 + 16, cx + 18, y1 - 10], fill=(55, 55, 62))
        d.ellipse([cx - 18, y1 - 16, cx + 18, y1 - 4], fill=(30, 30, 35))
        d.rectangle([cx - 18, y0 + h // 3, cx + 18, y0 + h // 3 + 4], fill=(255, 210, 60))
        d.rectangle([cx - 18, y0 + 2 * h // 3, cx + 18, y0 + 2 * h // 3 + 4], fill=(255, 210, 60))
    elif kind == "gold":
        for i, (gx, gy, gr) in enumerate([(cx - 16, cy - 8, 12), (cx + 14, cy - 12, 10), (cx, cy + 12, 13)]):
            d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(255, 210, 60), outline=(150, 100, 10), width=2)
            d.text((gx - 4, gy - 6), "$", font=F_BOLD(11), fill=(120, 80, 0))
    elif kind == "museum":
        d.polygon([(x0 + 6, y0 + h // 3), (cx, y0 + 8), (x1 - 6, y0 + h // 3)], fill=(200, 170, 110))
        for i in range(4):
            px = x0 + 12 + i * ((w - 24) // 4)
            d.rectangle([px, y0 + h // 3 + 4, px + 7, y1 - 8], fill=(230, 220, 200))
        d.rectangle([x0 + 6, y1 - 10, x1 - 6, y1 - 4], fill=(180, 150, 90))
    elif kind == "flood":
        for i in range(3):
            yy = y0 + h // 3 + i * (h // 5)
            pts = [(x0 + 6 + k * 12, yy + (6 if k % 2 else -6)) for k in range(8)]
            d.line(pts, fill=(90, 160, 220), width=3)
        d.rectangle([x0 + 8, y0 + 6, x0 + 30, y0 + 16], fill=(120, 70, 40))
    elif kind == "geo":
        d.polygon([(cx - 20, y1 - 6), (cx - 8, y0 + h // 3), (cx + 8, y0 + h // 3), (cx + 20, y1 - 6)], fill=(120, 120, 130))
        for i in range(3):
            sx = cx - 14 + i * 14
            d.arc([sx - 6, y0 + 4, sx + 6, y0 + 22], 180, 360, fill=(255, 255, 255), width=3)
    elif kind == "power":
        d.line([(cx, y0 + 8), (cx - 16, y1 - 6)], fill=(60, 60, 60), width=3)
        d.line([(cx, y0 + 8), (cx + 16, y1 - 6)], fill=(60, 60, 60), width=3)
        d.line([(cx - 20, y0 + 16), (cx + 20, y0 + 16)], fill=(60, 60, 60), width=3)
        d.line([(x0 + 4, y0 + 20), (cx - 20, y0 + 16)], fill=(255, 220, 60), width=2)
        d.line([(cx + 20, y0 + 16), (x1 - 4, y0 + 20)], fill=(255, 220, 60), width=2)
    elif kind == "stars":
        for sx, sy in [(x0 + 12, y0 + 12), (x0 + w // 2, y0 + 8), (x1 - 14, y0 + 18),
                       (x0 + 20, y0 + h // 2), (x1 - 22, y0 + h // 2 + 6)]:
            d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(200, 220, 255), outline=(255, 255, 255), width=2)


def draw_masthead(d):
    d.rectangle([M, 14, M + CW, 76], fill=INK)
    title = "THE WORLD IN NUMBERS"
    tf = F_TITLE(40)
    tw = d.textlength(title, font=tf)
    d.text((M + (CW - tw) / 2, 20), title, font=tf, fill=(247, 243, 232))
    sub = "Wednesday 25 November 2026  \u00b7  50 STORIES  \u00b7  ONE PAGE  \u00b7  ALL NUMBERS VERIFIED"
    sf = F_BOLD(12)
    sw = d.textlength(sub, font=sf)
    d.text((M + (CW - sw) / 2, 60), sub, font=sf, fill=(255, 210, 60))
    d.text((M + 4, 60), "No. 329", font=F_BOLD(11), fill=(200, 200, 200))
    rt = "TOP 50 \u00b7 $100"
    rw = d.textlength(rt, font=F_BOLD(11))
    d.text((M + CW - 4 - rw, 60), rt, font=F_BOLD(11), fill=(200, 200, 200))


def draw_hero(d, x, y, w, h, idx, hero):
    headline, place, big, why, also, kind = hero
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=INK, width=2)
    # scene: 88px tall, badge number inside
    draw_scene(d, (x + 2, y + 2, x + w - 2, y + 90), kind, idx)
    draw_badge(d, x + w - 34, y + 34, big, r=26)
    # place + number tag
    d.text((x + 8, y + 94), place, font=F_BOLD(11), fill=RED)
    d.text((x + w - 8 - d.textlength("HERO %d" % (idx + 1), font=F_BOLD(11)), y + 94),
           "HERO %d" % (idx + 1), font=F_BOLD(11), fill=GREY)
    # headline (2 lines)
    hf = F_BOLD(16)
    lines = wrap(headline, hf, w - 16)
    yy = y + 110
    for ln in lines[:2]:
        d.text((x + 8, yy), ln, font=hf, fill=INK)
        yy += 18
    # why it matters (2 lines)
    wf = F_REG(10)
    wlines = wrap(why, wf, w - 16)
    yy = y + 148
    for ln in wlines[:2]:
        d.text((x + 8, yy), ln, font=wf, fill=BLUE)
        yy += 11
    # also tag with literal C R CL
    tag = "C \u00b7 R \u00b7 CL \u00b7 " + also
    d.text((x + 8, y + h - 12), trunc(tag, F_REG(9), w - 16), font=F_REG(9), fill=GREY)


def draw_card(d, x, y, w, h, num, card):
    headline, place, big, also, kind = card
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE, width=1)
    tx = x + 6
    if kind:
        # mini-scene block, 46px square (meets the 45px minimum)
        draw_scene(d, (x + 2, y + 2, x + 48, y + 48), kind, num)
        tx = x + 54
        tw = w - 58
    else:
        tw = w - 12
    # row 1: number + big-number chip + place right
    nf = F_BOLD(11)
    d.text((tx, y + 3), "%02d" % num, font=nf, fill=RED)
    bf = F_BOLD(9)
    bw = d.textlength(big, font=bf) + 8
    nx = tx + 26
    d.rectangle([nx, y + 3, nx + bw, y + 15], fill=(238, 232, 214))
    d.text((nx + 4, y + 4), big, font=bf, fill=INK)
    pf = F_BOLD(8)
    avail = (tx + tw) - (nx + bw + 4)
    shown = place
    if d.textlength(shown, font=pf) > avail:
        shown = place.split(",")[0]
    if d.textlength(shown, font=pf) > avail:
        shown = trunc(shown, pf, avail)
    pw = d.textlength(shown, font=pf)
    d.text((tx + tw - pw, y + 4), shown, font=pf, fill=GREY)
    # headline: up to 3 lines; shrink font until it fits (never drop a line)
    hf = None
    lines = []
    for sz in (10, 9.5, 9, 8.5):
        hf = F_BOLD(sz)
        lines = wrap(headline, hf, tw)
        if len(lines) <= 3:
            break
    yy = y + 16
    for ln in lines[:3]:
        d.text((tx, yy), ln, font=hf, fill=INK)
        yy += 10
    # also tag with literal C R CL
    tag = "C \u00b7 R \u00b7 CL \u00b7 " + also
    d.text((tx, y + h - 11), trunc(tag, F_REG(8), tw), font=F_REG(8), fill=GREY)


def draw_datecheck(d, y, h):
    d.rectangle([M, y, M + CW, y + h], fill=(255, 248, 220), outline=RED, width=2)
    d.text((M + 10, y + 4), DATE_CHECK_1, font=F_BOLD(11), fill=INK)
    d.text((M + 10, y + 22), DATE_CHECK_2, font=F_BOLD(10), fill=RED)


def draw_map(d, y, h):
    d.rectangle([M, y, M + CW, y + h], fill=(222, 235, 245), outline=INK, width=1)
    d.text((M + 10, y + 3), "WORLD MAP \u2014 PINS MARK THE BIG NUMBERS",
           font=F_BOLD(10), fill=INK)
    # rough continent blobs
    d.ellipse([M + 60, y + 15, M + 200, y + 32], fill=(190, 205, 170))    # N America
    d.ellipse([M + 150, y + 30, M + 210, y + 42], fill=(190, 205, 170))   # S America
    d.ellipse([M + 430, y + 14, M + 560, y + 30], fill=(190, 205, 170))   # Europe/Asia
    d.ellipse([M + 560, y + 20, M + 760, y + 36], fill=(190, 205, 170))   # Asia
    d.ellipse([M + 470, y + 28, M + 540, y + 42], fill=(190, 205, 170))   # Africa
    d.ellipse([M + 800, y + 32, M + 900, y + 44], fill=(190, 205, 170))   # Australia
    pins = [(1, M + 130, y + 23), (2, M + 700, y + 26), (3, M + 660, y + 26),
            (4, M + 760, y + 32), (5, M + 520, y + 26), (8, M + 690, y + 30),
            (35, M + 540, y + 21)]
    for num, px, py in pins:
        draw_pin(d, px, py, num, r=9)
    labels = "1 tariffs 214  \u00b7  2 Kospi -6.16%  \u00b7  3 Shenzhou-21  \u00b7  4 Bogor 9/17  \u00b7  5 Shati 47  \u00b7  8 India 36  \u00b7  35 Kyiv 400,000"
    d.text((M + 10, y + h - 12), labels, font=F_REG(9), fill=INK)


def draw_footer(d, y):
    d.line([(M, y), (M + CW, y)], fill=INK, width=2)
    f1 = "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Bloomberg \u00b7 Antara \u00b7 Yonhap \u00b7 Xinhua \u00b7 dpa \u2014 All 50 stories are from Wednesday 25 November 2026."
    d.text((M, y + 5), f1, font=F_REG(9), fill=GREY)
    f2 = "THE WORLD IN NUMBERS \u00b7 No. 329 \u00b7 50 stories \u00b7 13 illustration panels \u00b7 Front page rendered from verified wires"
    d.text((M, y + 18), f2, font=F_REG(9), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    # hero trio row: y 82..266 (184 tall, scenes 88px)
    hw = (CW - 20) // 3
    for i, hero in enumerate(HEROES):
        draw_hero(d, M + i * (hw + 10), 82, hw, 184, i, hero)
    # date check: y 272..312
    draw_datecheck(d, 272, 40)
    # cards grid: 5 cols x 10 rows, y 318..934
    col_w = (CW - 4 * 8) // 5
    row_h, gap = 58, 4
    for i, card in enumerate(CARDS):
        r, c = divmod(i, 5)
        x = M + c * (col_w + 8)
        yy = 318 + r * (row_h + gap)
        draw_card(d, x, yy, col_w, row_h, i + 4, card)
    # map strip: y 940..988, footer below
    draw_map(d, 940, 48)
    draw_footer(d, 994)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
