# Smart Organic Farming Advisor

A new Flask + SQLite project built from scratch. It helps a farmer check whether a selected crop is broadly compatible with the stated soil type, sowing season and water availability, then displays crop-specific organic fertilizer, pest-management, irrigation and harvesting guidance.

## Main workflow
1. Farmer selects crop and enters village/town/district.
2. Farmer selects soil type, season and water availability.
3. Farmer may attach a land/soil photo and/or crop photo.
4. App calculates a transparent, rule-based suitability score.
5. For suitable or potentially suitable results, app displays crop-specific organic guidance.
6. If the crop is not recommended, app lists possible alternatives based on the same filters.

## Tech stack
- Python, Flask
- SQLite
- HTML, CSS, JavaScript
- Werkzeug secure filename utility (included with Flask)

## Run on Windows
1. Extract the ZIP.
2. Open the folder in VS Code.
3. In terminal:
   ```bash
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
4. Open `http://127.0.0.1:5000`.

## Run on macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Database
The app automatically creates `farming_advisor.db` and inserts 10 starter crop profiles on first run. The database stores crop profiles and submitted assessments. Delete the database file only if you want to reset the sample data and assessment history.

## Important current limitations
- Suitability is a transparent rule-based screening based on crop profile, soil category, season and water availability. It is not a trained AI model, scientific prediction or yield guarantee.
- Location is recorded as context but live weather, GPS, geospatial soil and rainfall data are not yet connected.
- Uploaded photos are saved and displayed with the assessment. The app does not yet use computer vision to identify crops, soil texture, pests or diseases from the photos.
- Crop guidance is general educational content. Verify variety, sowing dates, soil test, pest diagnosis and input choices with local agricultural extension experts.

## Suggested next upgrades
- Integrate location geocoding and live weather / rainfall API.
- Add a soil-test input module (pH, EC, N-P-K, organic carbon).
- Add a vision model to analyze uploaded images, with user consent and clear confidence/limitations.
- Add admin CRUD screens for crop profiles and guidance.
- Add user accounts and saved assessment history.
