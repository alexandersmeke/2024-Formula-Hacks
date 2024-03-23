from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

TIRE_IMAGES = {
    "Soft": "static/images/red-parentesi-soft-tyres.png",
    "Medium": "static/images/yellow-parentesi-medium.png",
    "Medium/Hard": "static/images/white-parentesi-hard.png",
    "Hard": "static/images/white-parentesi-hard.png"
}

BACKGROUND_IMAGE ={
    "background": "static/images/background.png"
}



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "Austin"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    temp = weather_data['main']['temp']
    tire_type = None
    background = None

    if temp < 20:
        tire_type = "Soft"
    elif temp >= 20 and temp < 30:
        tire_type = "Medium"
    elif temp >= 30 and temp < 40:
        tire_type = "Medium/Hard"
    elif temp >= 40:
        tire_type = "Hard"

    tire_image = TIRE_IMAGES.get(tire_type, "")

    background_image = BACKGROUND_IMAGE.get(background)

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{temp:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        tire_type=tire_type,
        tire_image=tire_image,
        background_image=background_image
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)