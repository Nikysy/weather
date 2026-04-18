from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "af85d70fc8b88ff77e69de17117db148"
URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/")
def home():
    return """
    <h2>Weather API</h2>
    <p>Пример запроса:</p>
    <p>/weather?city=Moscow</p>
    <p>/weather?city=Berlin</p>
    """


@app.route("/weather")
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "Нужно указать город",
            "example": "/weather?city=Moscow"
        }), 400

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return jsonify({
            "error": "Город не найден или ошибка API",
            "details": data
        }), response.status_code

    result = {
        "version": "v2",
        "Город": data["name"],
        "Температура (°C)": data["main"]["temp"],
        "Описание": data["weather"][0]["description"]
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)