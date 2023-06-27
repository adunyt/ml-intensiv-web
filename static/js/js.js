var form = document.querySelector("#form")
var price = "Введите все данные и отправьте запрос"
var price_per_m2_text = document.querySelector("#price-per-m2")
var price_flat_text = document.querySelector("#flat-price")
var city = document.querySelector("#select-city");
var district = document.querySelector("#select-district");

var login_form = document.querySelector("#login-form");
var all_content = document.querySelector(".all-content")
var login_form_from = login_form.querySelector("#login_form_from");

var formData;
var citys;
var districts;
var citys_dict = {};
var jsonData;

login_form_from.addEventListener("submit", function(e) {
    e.preventDefault();
    make_predict_and_show(); 
    return false;
})

form.addEventListener("submit", function (e) {
    e.preventDefault();
    formData = new FormData(form);
    raise_form();
    return false;
})

function raise_form(){
    all_content.classList.add("blur")
    login_form.classList.remove("hidden")
}

function remove_form(){
    all_content.classList.remove("blur")
    login_form.classList.add("hidden")
}

function make_predict_and_show(){
    remove_form()

    const XHR = new XMLHttpRequest();

    // Define what happens in case of an error
    XHR.addEventListener("error", (event) => {
        alert("Упс! Что-то пошло не так.");
    });

    // Set up our request
    XHR.open("POST", "/api/predict");

    // Send our FormData object; HTTP headers are set automatically
    XHR.send(formData);

    XHR.onloadend = () => {
        price = JSON.parse(XHR.responseText);
        update_price(price["price_per_m2"])
        price_flat_text.scrollIntoView()
    }
}

function update_price(price) {
    price_per_m2_text.textContent = parseFloat(price).toFixed(2) + " ₽";
    price_flat_text.textContent = (+form.elements["total_meters"].value * price).toFixed(2) + " ₽";
}

async function get_possible_locations() {
    const XHR = new XMLHttpRequest();

    // Define what happens in case of an error
    XHR.addEventListener("error", (event) => {
        alert("Упс! Что-то пошло не так. При получении локаций");
    });

    // Set up our request
    XHR.open("GET", "/api/locations");

    // Send our FormData object; HTTP headers are set automatically
    XHR.send();
    XHR.onloadend = () => {
        jsonData = JSON.parse(XHR.responseText);
        save_locations()
    }
}

function save_locations() {
    var json = jsonData;
    citys = json["citys"];
    districts = json["district"];
    make_dict()
}

function make_dict() {
    var non_moscow_district;
    var moscow_list = []
    for (let index = 0; index < districts.length; index++) {
        const element = districts[index];
        console.log(element)
        non_moscow_district = citys.find(x => x == element);
        if (non_moscow_district === undefined) {
            moscow_list.push(element);
        } else {
            citys_dict[non_moscow_district] = [element];
        }
        console.log(non_moscow_district);
    }
    citys_dict["москва"] = moscow_list;
    fill_locations()
}

async function fill_locations() {
    city.innerHTML = ''
    for (const [key, value] of Object.entries(citys_dict)) {
        var opt = document.createElement('option');
        var element = key;
        opt.value = element;
        var phrase = element;
        opt.innerHTML = phrase.charAt(0).toUpperCase() + phrase.slice(1);
        city.appendChild(opt);
    }
    update_discrict();
}

function update_discrict() {
    var current_city = city.value
    district.innerHTML = ''
    var district_list = citys_dict[current_city]
    for (let index = 0; index < district_list.length; index++) {
        const element = district_list[index];
        var opt = document.createElement('option');
        opt.value = element;
        var phrase = element;
        opt.innerHTML = phrase.charAt(0).toUpperCase() + phrase.slice(1);
        district.appendChild(opt);
    }
}

city.addEventListener("change", update_discrict)

window.onload = () => {
    get_possible_locations()
}