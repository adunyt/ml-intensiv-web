from flask import Flask, render_template, request
from model import Model
from deep_translator import GoogleTranslator
import json

app = Flask(__name__)
model = Model("house_predict.cbm")
translated_dict = {}
translator = GoogleTranslator(source="en", target="ru")
CITY_JSON = "city.json"
DISTRICT_JSON = "district.json"

def load_citys():
    citys = json.load(open(CITY_JSON))
    return list(citys.keys())

def load_districts():
    district = json.load(open(DISTRICT_JSON))
    return list(district.keys())

@app.route("/api/predict", methods=['GET', 'POST'])
def predict():
    value = model.predict(
        request.form["city"],
        request.form["floor"],
        request.form["floors_count"],
        request.form["rooms_count"],
        request.form["total_meters"], 
        request.form["year_of_construction"],
        request.form["living_meters"],
        request.form["kitchen_meters"], 
        request.form["district"])
    return {"price_per_m2": value}

def save_locations():
    citys = load_citys()
    translated_citys = []
    for city in citys:
        translated = translator.translate(city)
        translated_citys.append(translated)
        print(f"city: {city} translated: {translated}")
    translated_citys.sort()
    districts = load_districts()
    translated_districts = []
    for district in districts:
        translated = translator.translate(district)
        translated_districts.append(translated)
        print(f"district: {district} translated: {translated}")
    translated_districts.sort()
    translated_dict["citys"] = citys
    translated_dict["districts"] = districts
    json.dump(translated_dict, open("translated.json", "w"))

@app.route("/api/locations")
def return_locations():
    translated = json.load(open("translated.json", "r"))
    return translated

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/dev")
def dev():
    return render_template("index-dev.html")

# save_locations()
app.run(debug=True)