import os
from pathlib import Path
from uuid import uuid4
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import database
from suitability import evaluate_crop, find_alternatives, get_crop_profile

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "development-key-change-before-deployment")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_optional_image(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        raise ValueError("Upload JPG, JPEG, PNG or WEBP images only.")
    extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    name = f"{uuid4().hex}.{extension}"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file.save(UPLOAD_DIR / name)
    return name

@app.route("/")
def home():
    return render_template("index.html", crop_names=database.get_crop_names())

@app.route("/analyze", methods=["POST"])
def analyze():
    crop_name = request.form.get("crop_name", "").strip()
    location = request.form.get("location", "").strip()
    soil = request.form.get("soil", "").strip().lower()
    season = request.form.get("season", "").strip().lower()
    water = request.form.get("water", "").strip().lower()
    notes = request.form.get("notes", "").strip()

    if not crop_name or not location or not soil or not season or not water:
        flash("Please complete the crop, location, soil, season and water fields.", "error")
        return redirect(url_for("home"))

    profile = get_crop_profile(crop_name)
    if not profile:
        flash("We do not have a crop profile for that crop yet. Choose a crop from the list.", "error")
        return redirect(url_for("home"))

    try:
        land_image = save_optional_image(request.files.get("land_image"))
        plant_image = save_optional_image(request.files.get("plant_image"))
    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("home"))

    result = evaluate_crop(profile, soil, season, water, location, notes)
    alternatives = find_alternatives(soil, season, water, exclude=profile["name"]) if result["status"] != "Suitable" else []

    analysis_id = database.save_analysis(
        crop_name=profile["name"], location=location, soil=soil, season=season,
        water=water, status=result["status"], score=result["score"],
        notes=notes, land_image=land_image, plant_image=plant_image
    )
    return render_template(
        "result.html", profile=profile, result=result, alternatives=alternatives,
        crop_name=profile["name"], location=location, soil=soil, season=season,
        water=water, land_image=land_image, plant_image=plant_image,
        analysis_id=analysis_id
    )

@app.route("/guide/<crop_name>")
def crop_guide(crop_name):
    profile = get_crop_profile(crop_name)
    if not profile:
        flash("Crop guide not found.", "error")
        return redirect(url_for("home"))
    return render_template("guide.html", profile=profile)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/health")
def health():
    return {"status": "ok", "database": "connected"}

@app.errorhandler(413)
def too_large(_error):
    flash("Each image must be smaller than 8 MB.", "error")
    return redirect(url_for("home"))

if __name__ == "__main__":
    database.initialize_database()
    app.run(debug=True)
