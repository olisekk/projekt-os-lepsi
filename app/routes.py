from flask import Blueprint, render_template
from .forms import CityForm
from .models import Query
from . import db
import requests
import os

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    form = CityForm()
    weather = None
    city = None

    if form.validate_on_submit():
        city = form.city.data

        # ulozeni do DB
        q = Query(city=city)
        db.session.add(q)
        db.session.commit()

        # Geocoding - ziskani souradnic mesta
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=cs"
        geo_response = requests.get(geocoding_url)
        
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            if "results" in geo_data and len(geo_data["results"]) > 0:
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                
                # Ziskani pocasi pro souradnice
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = requests.get(weather_url)
                
                if weather_response.status_code == 200:
                    data = weather_response.json()
                    current = data["current_weather"]
                    # Prevod do formatu kompatibilniho s puvodnim kodem
                    weather = {
                        "temp": current["temperature"],
                        "humidity": None,  # Open-Meteo nezahrrnuje vlhkost v current_weather
                        "pressure": None
                    }

    return render_template(
        "index.html",
        form=form,
        weather=weather,
        city=city
    )
