from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    news = None
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        translate_weather(weather)
        news = get_news()
        translate_news(news)
    return render_template('index.html', weather=weather, news=news)

def get_weather(city):
    api_key = 'a8c805717850df507e2c52ddfcea157e'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()

def translate_weather(weather):
    translator = Translator()
    weather['weather'][0]['description'] = translator.translate(weather['weather'][0]['description'], dest='ru').text
    return weather

def get_news():
    api_key = 'b92990dfceb44975827da9419965f9a0'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    return response.json().get('articles', [])

def translate_news(news):
    translator = Translator()
    for article in news:
        article['title'] = translator.translate(article['title'], dest='ru').text
    return news

if __name__ == '__main__':
    app.run(debug=True)
