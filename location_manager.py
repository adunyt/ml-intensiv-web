from deep_translator import GoogleTranslator
import json
import os.path

translator = GoogleTranslator(source="en", target="ru")
CITY_JSON = "city.json"
DISTRICT_JSON = "district.json"

T_CITY_JSON = "translated_citys.json"
T_DISTRICT_JSON = "translated_districts.json"

def __load_citys():
    citys = json.load(open(CITY_JSON))
    return list(citys.keys())

def __load_districts():
    district = json.load(open(DISTRICT_JSON))
    return list(district.keys())

def get_districts():
    translated_districts = json.load(open("translated_districts.json", "r"))
    return translated_districts

def get_citys():
    translated_citys = json.load(open("translated_citys.json", "r"))
    return translated_citys

def is_location_cached():
    return os.path.exists(T_CITY_JSON) and os.path.exists(T_DISTRICT_JSON)
    
def cache_locations():
    translated_citys = {}
    translated_districts = {}
    citys = __load_citys()
    for city in citys:
        translated = translator.translate(city).lower()
        translated_citys[translated] = city
        print(f"city: {city} translated: {translated}")
    districts = __load_districts()
    for district in districts:
        translated = translator.translate(district).lower()
        translated_districts[translated] = district
        print(f"district: {district} translated: {translated}")
    json.dump(translated_citys, open("translated_citys.json", "w"))
    json.dump(translated_districts, open("translated_districts.json", "w"))
