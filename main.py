from flask import Flask, render_template, request
from model import Model
from deep_translator import GoogleTranslator
import json

app = Flask(__name__)
model = Model("house_predict.cbm")
translated_dict = {}
translated_citys = {}
translated_districts = {}
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
    print(translated_citys)
    print(translated_districts)
    value = model.predict(
        translated_citys[request.form["city"].lower()],
        request.form["floor"],
        request.form["floors_count"],
        request.form["rooms_count"],
        request.form["total_meters"], 
        request.form["year_of_construction"],
        request.form["living_meters"],
        request.form["kitchen_meters"], 
        translated_districts[request.form["district"].lower()])
    return {"price_per_m2": value}

def load_locations():
    global translated_citys, translated_districts
    translated_citys = json.load(open("translated_citys.json", "r"))
    translated_districts = json.load(open("translated_districts.json", "r"))

def save_locations():
    citys = load_citys()
    for city in citys:
        translated = translator.translate(city)
        translated_citys[translated.lower()] = city
        print(f"city: {city} translated: {translated}")
    districts = load_districts()
    for district in districts:
        translated = translator.translate(district)
        translated_districts[translated.lower()] = district
        print(f"district: {district} translated: {translated}")
    json.dump(translated_citys, open("translated_citys.json", "w"))
    json.dump(translated_districts, open("translated_districts.json", "w"))

@app.route("/api/locations")
def return_locations():
    all_dict = {}
    all_dict["citys"] = list(translated_citys.keys())
    all_dict["district"] = list(translated_districts.keys())
    return all_dict

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/dev")
def dev():
    return render_template("index-dev.html")

# save_locations()
load_locations()
app.run(debug=True)