from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import api_token

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    background_image = 'default.jpg'

    if request.method == 'POST':
        zipcode = request.form['zipcode']
        api_key = api_token
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={zipcode}")
        if response.status_code == 200:
            weather_data = response.json()
            if 'current' in weather_data and 'location' in weather_data:
                weather = {
                    'current': weather_data['current'],
                    'location': weather_data['location']
                }
                condition = weather['current']['condition']['text']
                background_image = get_background(condition)
                
            else:
                error = "Weather data not found."

        else:
            error = "Unable to get weather for that ZIP code."
    
    print("Background image: ", background_image)
    return render_template('index.html', weather=weather, background_image=background_image, error=error)

def get_background(condition):
    background_images = {
        'Clear': '/static/images/clear.jpg',
    }
    return background_images.get(condition, 'default.jpg')

if __name__ == '__main__':
    app.run(debug=True)