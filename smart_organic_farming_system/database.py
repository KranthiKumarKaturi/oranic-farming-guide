import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "farming_advisor.db"

CROP_DATA = [
    ("Rice","Clayey, clay-loam or loamy","Kharif / locally suitable irrigated season","High","Warm conditions; reliable water supply is important.",
     "Well-decomposed farmyard manure (FYM), mature compost and locally recommended organic nutrient management.",
     "Monitor for stem borer, leaf folder and planthoppers. Use field sanitation, balanced nutrients, resistant varieties and locally approved biological controls after correct pest identification.",
     "Maintain water according to the rice establishment method. Avoid unnecessary continuous flooding where water-saving methods are appropriate.",
     "Harvest when most grains are mature and golden; confirm grain moisture and local harvest guidance."),
    ("Tomato","Loamy, sandy-loam, well-drained","Season depends on local temperature and variety","Medium","Needs sunlight and moderate temperatures; sensitive to waterlogging.",
     "Mature compost, well-decomposed FYM and soil-test-based organic nutrient inputs.",
     "Scout for fruit borer, whitefly and leaf miner. Remove affected plant parts, use physical traps and seek local advice before applying a botanical product.",
     "Use drip or basin irrigation to maintain even moisture; avoid wetting foliage late in the day.",
     "Pick fruits at the maturity stage required for fresh use or transport; harvest regularly."),
    ("Chilli","Well-drained loamy soil rich in organic matter","Season varies by region and variety","Medium","Warm conditions and good drainage are preferred.",
     "Mature compost, FYM and organic matter based on soil test.",
     "Monitor thrips, mites and fruit borers. Use clean seedlings, field hygiene, barriers/traps and locally recommended biological controls.",
     "Avoid both prolonged dry stress and waterlogging. Prefer measured irrigation.",
     "Harvest green or red depending on market purpose and variety; pick carefully to avoid plant damage."),
    ("Groundnut","Loose, well-drained sandy loam or loam","Often Kharif; also grown in other locally suitable windows","Medium","Warm conditions and friable soil support pod development.",
     "Well-decomposed FYM/compost; use soil-test and local recommendations for calcium and other nutrients.",
     "Monitor leaf miner, tobacco caterpillar and diseases. Rotate crops, remove volunteer plants and use locally recommended biological measures.",
     "Avoid waterlogging; moisture is important at flowering, pegging and pod development.",
     "Harvest when a suitable proportion of pods are mature; dry and cure properly."),
    ("Cotton","Deep, well-drained loam or black soil depending on region","Kharif in many Indian regions; local sowing window varies","Medium","Needs a long warm growing period; drainage is important.",
     "Compost, FYM, green manures and residue recycling guided by soil testing.",
     "Scout for bollworms, whiteflies and sucking pests. Use refuge/resistant varieties where applicable, traps, field sanitation and integrated biological controls.",
     "Avoid waterlogging; schedule irrigation based on soil moisture and crop stage.",
     "Pick fully opened, dry kapas in clean rounds; keep harvested cotton free from soil and trash."),
    ("Leafy vegetables","Fertile loam with good drainage and moisture retention","Cooler season often suits many leafy crops; species vary","Low to medium","Rapid growth needs consistent moisture and suitable temperatures.",
     "Mature compost and well-decomposed FYM; avoid fresh manure on edible leaves.",
     "Use insect netting, crop rotation, hand removal and sanitation; identify pests before selecting any control.",
     "Frequent light irrigation may be needed; avoid waterlogging and overhead watering close to harvest.",
     "Harvest tender leaves at the correct stage; wash and handle hygienically."),
    ("Maize","Well-drained loam or sandy loam","Kharif, Rabi or spring depending on irrigation and region","Medium","Warm growing conditions; sensitive to waterlogging.",
     "Mature FYM, compost, legume rotation and soil-test-based nutrient management.",
     "Scout for fall armyworm and stem borers. Use timely scouting, destruction of egg masses where practical and local integrated pest management advice.",
     "Moisture is especially important around tasseling, silking and grain filling.",
     "Harvest when husks dry and grains reach suitable maturity and moisture."),
    ("Pigeon Pea","Well-drained loam to clay loam","Commonly Kharif; duration and window vary by variety","Low to medium","Warm conditions; avoid poorly drained fields.",
     "Compost/FYM, crop residues and suitable intercrops or rotations.",
     "Monitor pod borers and wilt. Use resistant varieties, crop rotation, timely scouting and locally recommended biological control.",
     "Generally drought tolerant after establishment, but avoid severe moisture stress at flowering and pod filling.",
     "Harvest when most pods turn brown and dry; dry before storage."),
    ("Banana","Deep, fertile, well-drained loam","Can be grown year-round where water and temperature are suitable","High","Warm, humid conditions and protection from strong winds are helpful.",
     "Well-decomposed FYM, compost and mulching; nutrient plan should be based on soil test and growth stage.",
     "Monitor rhizome weevil, aphids and leaf diseases. Use clean planting material, sanitation and locally recommended biological measures.",
     "Needs regular moisture and good drainage; drip irrigation and mulching can improve water use.",
     "Harvest bunches at suitable maturity for the market and handle carefully."),
    ("Onion","Well-drained sandy loam or loam","Rabi and other locally suitable seasons depending on region","Medium","Bulb development needs suitable day length and temperature for the variety.",
     "Mature compost and well-decomposed FYM incorporated before planting.",
     "Monitor thrips and purple blotch. Use clean planting material, crop rotation, field sanitation and local integrated management.",
     "Keep moisture even during bulb development; reduce irrigation near maturity as locally advised.",
     "Harvest after tops fall and bulbs mature; cure thoroughly before storage.")
]

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def initialize_database():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS crops(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL,
            soil TEXT NOT NULL, season TEXT NOT NULL, water TEXT NOT NULL,
            climate TEXT NOT NULL, fertilizer TEXT NOT NULL, pest_control TEXT NOT NULL,
            irrigation TEXT NOT NULL, harvesting TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS analyses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, crop_name TEXT NOT NULL,
            location TEXT NOT NULL, soil TEXT NOT NULL, season TEXT NOT NULL,
            water TEXT NOT NULL, status TEXT NOT NULL, score INTEGER NOT NULL,
            notes TEXT, land_image TEXT, plant_image TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        count = con.execute("SELECT COUNT(*) FROM crops").fetchone()[0]
        if count == 0:
            con.executemany("""INSERT INTO crops(name,soil,season,water,climate,fertilizer,pest_control,irrigation,harvesting)
                VALUES(?,?,?,?,?,?,?,?,?)""", CROP_DATA)

def get_crop_names():
    with connect() as con:
        return [r["name"] for r in con.execute("SELECT name FROM crops ORDER BY name")]

def get_crop(name):
    with connect() as con:
        row = con.execute("SELECT * FROM crops WHERE lower(name)=lower(?)", (name,)).fetchone()
        return dict(row) if row else None

def save_analysis(**data):
    with connect() as con:
        cur = con.execute("""INSERT INTO analyses(crop_name,location,soil,season,water,status,score,notes,land_image,plant_image)
            VALUES(:crop_name,:location,:soil,:season,:water,:status,:score,:notes,:land_image,:plant_image)""", data)
        return cur.lastrowid
