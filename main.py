from flask import Flask, render_template, request
from model import Model
from location_manager import cache_locations, is_location_cached, get_districts, get_citys

app = Flask(__name__)
model = Model("house_predict.cbm")
translated_citys = {}
translated_districts = {}

@app.route("/api/predict", methods=['GET', 'POST'])
def predict():
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

if not is_location_cached():
    app.logger.warning("No cached locations! Saving...")
    cache_locations()

translated_citys = get_citys()
translated_districts = get_districts()

if __name__ == "__main__":
    app.run(debug=True)