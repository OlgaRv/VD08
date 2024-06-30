from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        translate_weather(weather)
    return render_template('index.html', weather=weather)

def get_weather(city):
    api_key = 'a8c805717850df507e2c52ddfcea157e'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

def translate_weather(weather):
    translator = Translator()
    weather['weather'][0]['description'] = translator.translate(weather['weather'][0]['description'], dest='ru').text
    return weather

if __name__ == '__main__':
    app.run(debug=True)
