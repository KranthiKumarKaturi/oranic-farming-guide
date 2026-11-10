import database

def get_crop_profile(name):
    return database.get_crop(name)

def evaluate_crop(profile, soil, season, water, location, notes=""):
    score = 0
    reasons = []
    warnings = []
    soil_text = profile["soil"].lower()
    soil_match = {
        "clayey": "clay" in soil_text,
        "loamy": "loam" in soil_text,
        "sandy": "sandy" in soil_text,
        "black": "black" in soil_text or "clay" in soil_text,
        "red": "loam" in soil_text or "sandy" in soil_text,
        "other": False
    }.get(soil, False)

    if soil == "unknown":
        reasons.append("Soil type was not confirmed; a soil test is recommended.")
    elif soil_match:
        score += 35
        reasons.append("The selected soil category is broadly compatible with the crop profile.")
    else:
        score += 8
        warnings.append("The selected soil category does not clearly match the crop's commonly suitable soil. Check drainage, pH and soil test results.")

    season_text = profile["season"].lower()
    if season == "unknown":
        reasons.append("Season was not confirmed; local sowing calendars should be checked.")
    elif season in season_text or "varies" in season_text or "locally suitable" in season_text or "year-round" in season_text:
        score += 30
        reasons.append("The selected season may fit the crop's broad growing window; confirm the local variety calendar.")
    else:
        score += 8
        warnings.append("The selected season may not match the crop's common growing window. Confirm local sowing dates and variety.")

    water_need = profile["water"].lower()
    if water == "adequate":
        score += 25 if "high" not in water_need else 22
        reasons.append("You reported adequate water availability.")
    elif water == "limited":
        if "high" in water_need:
            score += 2
            warnings.append("This crop has relatively high water needs, but you selected limited water availability.")
        elif "low" in water_need:
            score += 22
            reasons.append("The crop profile indicates comparatively lower water demand.")
        else:
            score += 12
            warnings.append("Water may be a limiting factor; consider water-saving irrigation and local advice.")
    else:
        reasons.append("Water availability is unknown; verify irrigation or rainfall before planting.")

    if water == "limited" and "high" in water_need:
        status = "Not recommended with current water availability"
    elif score >= 70:
        status = "Suitable based on the details provided"
    elif score >= 42:
        status = "Potentially suitable – verify locally"
    else:
        status = "Not recommended without changing conditions"

    if status.startswith("Suitable"):
        level = "success"
    elif status.startswith("Potentially"):
        level = "warning"
    else:
        level = "danger"

    return {
        "score": min(score, 100), "status": status, "level": level,
        "reasons": reasons, "warnings": warnings,
        "disclaimer": "This is a preliminary rule-based screening, not a guarantee of yield or an agronomic diagnosis. Confirm with a soil test and your local agricultural extension officer."
    }

def find_alternatives(soil, season, water, exclude=None):
    matches = []
    for name in database.get_crop_names():
        if name == exclude:
            continue
        profile = database.get_crop(name)
        result = evaluate_crop(profile, soil, season, water, "", "")
        if result["score"] >= 42 and not result["status"].startswith("Not recommended"):
            matches.append({"name": name, "score": result["score"], "status": result["status"]})
    return sorted(matches, key=lambda x: x["score"], reverse=True)[:4]
