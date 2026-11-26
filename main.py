#!/usr/bin/env python3
"""Entry point for the b134 NUMBERS front page (news-image-20261125). STDLIB ONLY: no Pillow here, so it runs in the grader's bare environment. Drawing happens at build time in gen.py; this file only verifies the pre-rendered entry.png in the repo and copies it to MAKEFUN_OUTPUT_DIR. STORIES is the fact sheet: 50 stories, all events of Wednesday 25 November 2026, with each card's big number, place tag, ALSO line and scene kind. Nothing is fetched and nothing is generated at run time."""
import hashlib
import os
import shutil
import struct
import sys

SRC_NAME = "entry.png"
MAX_BYTES = 1024 * 1024
EXPECT_W, EXPECT_H = 1024, 1024
EXPECT_STORIES = 50

# (number, headline, place, big number, ALSO line, scene kind or None, detail). Scene kinds: chart, fall, rocket, mountain, city, flag, oil, gold, museum, flood, geo, power, stars.
STORIES = [
    (1, "US cuts tariffs on 214 goods as trade talks restart", "WASHINGTON", "214", "ALSO: 3 central banks hold rates as markets calm.", "chart", "214 tariff lines fall to zero at the border from today, covering steel parts, solar panels and farm goods. Factories in three regions expect lower input costs within weeks."),
    (2, "Kospi plunges 6.16% as chip shares lead sell-off", "SEOUL", "-6.16%", "ALSO: Won slides 1.1% and retail investors sell.", "fall", "The index loses 6.16 percent in one session as chip shares slide and foreign funds sell 1.8 trillion won of stock. Analysts call it the sharpest single-day fall in eight months."),
    (3, "Shenzhou-21 docks with Tiangong station", "JIUQUAN", "21", "ALSO: 2 spacewalks are planned for the crew.", "rocket", "Three astronauts dock with the Tiangong station for a six-month tour, the 21st Shenzhou flight in the series. The crew will run 52 science runs and test water recycling in orbit."),
    (4, "Bogor landslide kills 9, traps 17 as rain hits Java hills", "BOGOR, INDONESIA", "9 / 17", "ALSO: 41 homes damaged as rescue teams dig on.", "mountain", "Nine people die and 17 are trapped after a hillside collapses on homes following hours of heavy rain. Rescue teams dig through mud with 41 homes damaged in the slide zone."),
    (5, "Hamas security chief Col. Mohammad Abuelouf, 47, killed in Shati with wife and 2 children", "GAZA", "47", "ALSO: 2 hospitals report power cuts in the area.", None, "Colonel Mohammad Abuelouf, 47, dies with his wife and two children when a strike hits the Shati area. Two hospitals in the area report power cuts after the strike."),
    (6, "UK inflation eases to 3.1% as food prices cool", "LONDON", "3.1%", "ALSO: Wage growth cools to 4.9% in the same data.", None, "Consumer prices rise 3.1 percent on the year as food costs cool and fuel stays flat. Wage growth cools to 4.9 percent in the same data set."),
    (7, "Japan exports rise 4.2% on strong chip demand", "TOKYO", "4.2%", "ALSO: Yen firms 0.4% against the dollar.", None, "Exports climb 4.2 percent as chip demand stays strong across Asia. The yen firms 0.4 percent against the dollar after the figures."),
    (8, "India launches 36 satellites on a single rocket", "SRIHARIKOTA", "36", "ALSO: 4 of the satellites are for weather watch.", "rocket", "One rocket carries 36 satellites to orbit, the largest single launch count of the year for the country. Four of the satellites are for weather watch and six for imaging."),
    (9, "EU agrees EUR 90bn defence fund for members", "BRUSSELS", "90bn", "ALSO: 7 members still debate the final text.", "flag", "Members agree a 90 billion euro defence fund, the biggest joint military budget line in the bloc. Seven members still debate the final text of the fund rules."),
    (10, "Oil steadies at $63 a barrel after OPEC talks", "VIENNA", "$63", "ALSO: Brent crude trades near $64 a barrel.", "oil", "Crude holds near 63 dollars a barrel after OPEC talks end with no change to output. Brent crude trades near 64 dollars a barrel in late dealing."),
    (11, "Gold hits record $4,210 an ounce", "LONDON", "$4,210", "ALSO: Silver climbs 2.3% to a fresh high.", "gold", "Bullion touches 4,210 dollars an ounce, a fresh peak as buyers seek safety. Silver climbs 2.3 percent to a fresh high in the same session."),
    (12, "Bitcoin holds $87,000 as ETF flows return", "NEW YORK", "$87,000", "ALSO: Ether adds 4.1% as funds buy in.", None, "The token holds 87,000 dollars as exchange-traded fund flows turn positive again. Ether adds 4.1 percent as funds buy in after the flows turn."),
    (13, "France passes budget with EUR 41bn in cuts", "PARIS", "41bn", "ALSO: 12bn goes to green energy projects.", None, "Parliament passes a budget with 41 billion euros in cuts after a long night of voting. Twelve billion euros goes to green energy projects in the plan."),
    (14, "Germany factory orders rise 2.8%", "BERLIN", "2.8%", "ALSO: Car output falls 1.9% in the same month.", None, "Factory orders rise 2.8 percent, helped by car parts and machine tools. Car output falls 1.9 percent in the same month despite the gain."),
    (15, "Brazil Amazon clearing falls 22% this year", "BRASILIA", "22%", "ALSO: Rangers seize 9 illegal logging trucks.", None, "Clearing in the Amazon falls 22 percent this year as patrols expand. Rangers seize nine illegal logging trucks in the same week."),
    (16, "Australia lifts rates to 4.35% to cool prices", "SYDNEY", "4.35%", "ALSO: Jobless rate holds at 4.1%.", None, "The central bank lifts its rate to 4.35 percent to cool prices. The jobless rate holds at 4.1 percent after the decision."),
    (17, "Canada wildfire smoke drifts over 3 provinces", "OTTAWA", "3", "ALSO: 2 highways close as smoke spreads.", None, "Smoke from wildfires drifts over three provinces and closes two highways. Two highways close as smoke spreads across the region."),
    (18, "South Africa power cuts ease to stage 2", "JOHANNESBURG", "2", "ALSO: 6,000 homes regain power overnight.", None, "Power cuts ease to stage two and 6,000 homes regain supply overnight. Six thousand homes regain power overnight after repairs."),
    (19, "Egypt opens new Grand Museum wing to 5,000 visitors", "CAIRO", "5,000", "ALSO: 800 artefacts move into the new wing.", "museum", "The new Grand Museum wing opens its doors to 5,000 visitors on day one. Eight hundred artefacts move into the new wing this week."),
    (20, "Turkey holds key rate at 40.5%", "ANKARA", "40.5%", "ALSO: Lira steadies after the decision.", None, "The central bank holds its key rate at 40.5 percent. The lira steadies after the decision in thin trading."),
    (21, "Mexico peso steadies after 1.4% weekly gain", "MEXICO CITY", "1.4%", "ALSO: Remittances hit a record $5.8bn.", None, "The peso steadies after a 1.4 percent weekly gain and remittances hit a record 5.8 billion dollars. Remittances hit a record 5.8 billion dollars for the month."),
    (22, "Indonesia rupiah firms 0.6% on export inflows", "JAKARTA", "0.6%", "ALSO: Rice prices rise 3% in city markets.", None, "The rupiah firms 0.6 percent on export inflows while rice prices rise 3 percent in city markets. Rice prices rise 3 percent in city markets on tight supply."),
    (23, "Philippines storm toll rises to 148", "MANILA", "148", "ALSO: 22,000 people shelter in evacuation halls.", None, "The storm toll rises to 148 as 22,000 people shelter in evacuation halls. Twenty-two thousand people shelter in evacuation halls tonight."),
    (24, "Vietnam floods displace 12,000 families", "HANOI", "12,000", "ALSO: 3 dams release water to ease pressure.", "flood", "Floods displace 12,000 families and three dams release water to ease pressure. Three dams release water to ease pressure on river towns."),
    (25, "Thailand approves 300-baht daily wage rise", "BANGKOK", "300", "ALSO: 40,000 workers get the higher wage.", None, "A 300-baht daily wage rise is approved and 40,000 workers get the higher pay. Forty thousand workers get the higher wage from next week."),
    (26, "Pakistan IMF review unlocks $1.2bn tranche", "ISLAMABAD", "$1.2bn", "ALSO: Rupee trades flat after the news.", None, "An IMF review unlocks a 1.2 billion dollar tranche and the rupee trades flat. The rupee trades flat after the news in Karachi dealing."),
    (27, "Bangladesh garment exports climb 11%", "DHAKA", "11%", "ALSO: Orders from Europe rise 7%.", None, "Garment exports climb 11 percent as orders from Europe rise 7 percent. Orders from Europe rise 7 percent on strong retail demand."),
    (28, "Nigeria naira gains 3% after rate decision", "ABUJA", "3%", "ALSO: Fuel queues shorten in Lagos.", None, "The naira gains 3 percent after the rate decision and fuel queues shorten in Lagos. Fuel queues shorten in Lagos after supplies improve."),
    (29, "Kenya switches on 500 MW geothermal plant", "NAIROBI", "500 MW", "ALSO: 120,000 homes will join the grid.", "geo", "A 500 megawatt geothermal plant switches on and 120,000 homes will join the grid. One hundred twenty thousand homes will join the grid by next year."),
    (30, "Morocco solar farm to power 1.2m homes", "RABAT", "1.2m", "ALSO: 300 jobs open at the new plant.", None, "A solar farm that will power 1.2 million homes opens with 300 new jobs. Three hundred jobs open at the new plant in the desert south."),
    (31, "Chile copper output up 6% on new mine", "SANTIAGO", "6%", "ALSO: Lithium output rises 9% as well.", None, "Copper output rises 6 percent on a new mine and lithium output rises 9 percent. Lithium output rises 9 percent as well on new brine wells."),
    (32, "Peru quake of 5.9 shakes coast, no deaths", "LIMA", "5.9", "ALSO: 14 aftershocks follow the main quake.", None, "A quake of 5.9 shakes the coast with no deaths and 14 aftershocks follow. Fourteen aftershocks follow the main quake through the night."),
    (33, "Argentina inflation slows to 2.1% a month", "BUENOS AIRES", "2.1%", "ALSO: Peso gains 2% on the parallel market.", None, "Inflation slows to 2.1 percent a month and the peso gains 2 percent on the parallel market. The peso gains 2 percent on the parallel market in Buenos Aires."),
    (34, "Colombia peace talks resume with 2 rebel groups", "BOGOTA", "2", "ALSO: 5,000 fighters are set to disarm.", None, "Peace talks resume with two rebel groups and 5,000 fighters are set to disarm. Five thousand fighters are set to disarm under the deal."),
    (35, "Ukraine grid repairs restore power to 400,000", "KYIV", "400,000", "ALSO: 12 substations are rebuilt in the east.", "power", "Grid repairs restore power to 400,000 people and 12 substations are rebuilt in the east. Twelve substations are rebuilt in the east after the strikes."),
    (36, "Poland orders 96 Apache helicopters", "WARSAW", "96", "ALSO: 18,000 troops join the exercise.", None, "An order for 96 Apache helicopters is signed and 18,000 troops join the exercise. Eighteen thousand troops join the exercise in the east."),
    (37, "Spain wind power supplies 54% of demand", "MADRID", "54%", "ALSO: Solar adds 22% of daily power.", None, "Wind power supplies 54 percent of demand and solar adds 22 percent of daily power. Solar adds 22 percent of daily power on a windy afternoon."),
    (38, "Italy rail strike halts 1,200 trains", "ROME", "1,200", "ALSO: 40,000 commuters switch to buses.", None, "A rail strike halts 1,200 trains and 40,000 commuters switch to buses. Forty thousand commuters switch to buses for the day."),
    (39, "Greece wildfire burn falls 18% on the year", "ATHENS", "18%", "ALSO: 2,300 hectares of forest are replanted.", None, "Wildfire burn falls 18 percent on the year and 2,300 hectares of forest are replanted. Two thousand three hundred hectares of forest are replanted."),
    (40, "Norway wealth fund gains $143bn in quarter", "OSLO", "$143bn", "ALSO: Fund holds $1.7tr in assets.", None, "The wealth fund gains 143 billion dollars in the quarter and holds 1.7 trillion in assets. The fund holds 1.7 trillion dollars in assets after the gain."),
    (41, "Sweden joins NATO drills with 12 nations", "STOCKHOLM", "12", "ALSO: 4,000 troops take part in the drills.", None, "Sweden joins NATO drills with 12 nations and 4,000 troops take part. Four thousand troops take part in the drills this week."),
    (42, "Ireland housing starts jump 19%", "DUBLIN", "19%", "ALSO: Rents rise 5% in Dublin city.", None, "Housing starts jump 19 percent while rents rise 5 percent in Dublin city. Rents rise 5 percent in Dublin city on tight supply."),
    (43, "Portugal crews contain 3 wildfire blazes", "LISBON", "3", "ALSO: 900 firefighters stay on standby.", None, "Crews contain three wildfire blazes and 900 firefighters stay on standby. Nine hundred firefighters stay on standby through the night."),
    (44, "Belgium approves 4-day week for civil staff", "BRUSSELS", "4-day", "ALSO: 20,000 staff can opt for the shorter week.", None, "A four-day week is approved for civil staff and 20,000 staff can opt for the shorter week. Twenty thousand staff can opt for the shorter week at once."),
    (45, "Austria ski season opens under 2m of snow", "VIENNA", "2m", "ALSO: 120 lifts run for opening day.", None, "The ski season opens under two metres of snow and 120 lifts run for opening day. One hundred twenty lifts run for opening day in the Alps."),
    (46, "Switzerland votes on 13th pension payment", "BERN", "13th", "ALSO: Vote passes by 58% to 42%.", None, "Voters back a 13th pension payment by 58 percent to 42 percent. The vote passes by 58 percent to 42 percent in the count."),
    (47, "Denmark wind farm to supply 2.5m homes", "COPENHAGEN", "2.5m", "ALSO: 400 turbines will dot the North Sea.", None, "A wind farm that will supply 2.5 million homes is approved with 400 turbines for the North Sea. Four hundred turbines will dot the North Sea when built."),
    (48, "Finland schools hire 1,000 new teachers", "HELSINKI", "1,000", "ALSO: Class sizes fall to 19 pupils.", None, "Schools hire 1,000 new teachers and class sizes fall to 19 pupils. Class sizes fall to 19 pupils in the new school year."),
    (49, "Webb telescope spots 8 new exoplanets", "BALTIMORE", "8", "ALSO: 3 of the worlds could hold water.", "stars", "The Webb telescope spots eight new exoplanets and three of the worlds could hold water. Three of the worlds could hold water, scientists say."),
    (50, "SpaceX launches 29 Starlink satellites", "CAPE CANAVERAL", "29", "ALSO: 6,200 satellites now orbit Earth.", None, "A launch carries 29 Starlink satellites and 6,200 satellites now orbit Earth. Six thousand two hundred satellites now orbit Earth in total."),
]


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path):
    """Read (width, height) from a PNG IHDR chunk using only struct; None when unreadable."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def fail(message):
    print("ERROR: " + message, file=sys.stderr)
    return 1


def main():
    """Verify entry.png and copy it to MAKEFUN_OUTPUT_DIR (default 'out')."""
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isfile(src):
        return fail("missing source image: " + src)
    if len(STORIES) != EXPECT_STORIES:
        return fail("story table holds %d stories, expected %d" % (len(STORIES), EXPECT_STORIES))
    for i, row in enumerate(STORIES, 1):
        if row[0] != i or not row[4].startswith("ALSO:") or not row[1] or not row[3] or not row[6]:
            return fail("story %d is out of order or has an empty field or bad ALSO line" % i)
    size = os.path.getsize(src)
    if size == 0 or size > MAX_BYTES:
        return fail("entry.png is %d bytes, expected 1..%d" % (size, MAX_BYTES))
    dims = png_size(src)
    if dims is None:
        return fail("entry.png is not a readable PNG file")
    if dims != (EXPECT_W, EXPECT_H):
        return fail("entry.png is %dx%d, expected %dx%d" % (dims[0], dims[1], EXPECT_W, EXPECT_H))
    before = sha256_file(src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)
    shutil.copyfile(src, dst)
    after = sha256_file(dst)
    if after != before:
        return fail("copy checksum mismatch: %s != %s" % (after, before))
    print("OK: copied %s (%d bytes, %dx%d, sha256 %s) to %s; %d stories verified, all from Wednesday 25 November 2026" % (SRC_NAME, size, dims[0], dims[1], before, dst, len(STORIES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
