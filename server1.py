from flask import Flask, render_template, request, jsonify
import datetime
import pywhatkit
import pyttsx3
import webbrowser
import pyjokes
import requests

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# OpenWeatherMap API configuration
WEATHER_API_KEY = 'd8a22dfed073dc543d2f5dd3f99ddbb3'  # Replace with your OpenWeatherMap API key
WEATHER_CITY = 'Bengaluru'  # Replace with your city

# Dictionary of Indian states and their capitals
states_and_capitals = {
    "andhra pradesh": "amaravati",
    "arunachal pradesh": "itanagar",
    "assam": "dispur",
    "bihar": "patna",
    "chhattisgarh": "raipur",
    "goa": "panaji",
    "gujarat": "gandhinagar",
    "haryana": "chandigarh",
    "himachal pradesh": "shimla",
    "jharkhand": "ranchi",
    "karnataka": "bengaluru",
    "kerala": "thiruvananthapuram",
    "madhya pradesh": "bhopal",
    "maharashtra": "mumbai",
    "manipur": "imphal",
    "meghalaya": "shillong",
    "mizoram": "aizawl",
    "nagaland": "kohima",
    "odisha": "bhubaneswar",
    "punjab": "chandigarh",
    "rajasthan": "jaipur",
    "sikkim": "gangtok",
    "tamil nadu": "chennai",
    "telangana": "hyderabad",
    "tripura": "agartala",
    "uttar pradesh": "lucknow",
    "uttarakhand": "dehradun",
    "west bengal": "kolkata"
}

@app.route('/')
def home():
    return render_template('indexx.html')

@app.route('/process', methods=['POST'])

def process():
    command = request.form['command'].lower()
    response = ""

    if 'chrome' in command:
        open_chrome()
        response = "Opening Chrome..."
    elif 'time' in command:
        response = get_current_time()
    elif 'play' in command:
        play_on_youtube(command)
        response = "Playing on YouTube..."
    elif 'news' in command:
        response = get_news()
    elif 'maps' in command:
        destination = command.replace('maps', '').replace('search', '').strip()
        response = search_google_maps(destination)
    elif 'weather' in command:
        response = get_weather()
    elif 'joke' in command:
        response = tell_joke()
    elif 'whatsapp' in command:
        open_whatsapp_web()
        response = "Opening WhatsApp Web..."
    elif 'papers' in command:
        open_IEEE()
        response = "Opening IEEE website..."
    elif 'netflix' in command:
        command_without_netflix = command.replace('netflix', '').strip()
        play_on_netflix(command_without_netflix)
        response = "Playing on Netflix..."
    elif 'amazon' in command:
        search_on_amazon(command)
        response = "Searching on Amazon..."
    elif 'capital' in command:
        response = get_state_capital(command)
    elif 'hello' in command:
        response = "hello, how are you"
    else:
        response = "Sorry, I didn't understand that."

    speak(response)  # Read the response aloud
    return jsonify(response=response)

def open_chrome():
    webbrowser.open("https://www.google.com/")

def open_IEEE():
    webbrowser.open("https://ieeexplore.ieee.org/browse/periodicals/title")

def get_current_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return f"Current time is {current_time}"

def play_on_youtube(command):
    query = command.replace('play', '').strip()
    pywhatkit.playonyt(query)

def get_news():
    NEWS_API_KEY = 'cb3fee6182db4fe7b179f2a22c2db8c6'  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'ok' and data['articles']:
        top_articles = data['articles'][:3]  # Get top 3 news articles
        news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(top_articles)]
        response_text = "Here are the top news headlines: " + " | ".join(news_list)
    else:
        response_text = "Sorry, I couldn't retrieve the news information."
        
    return response_text


def search_google_maps(destination):
    webbrowser.open(f"https://www.google.com/maps/search/{destination}")

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        response_text = f"The current weather in {WEATHER_CITY} is {weather_description} with a temperature of {temperature}°C."
    else:
        response_text = "Sorry, I couldn't retrieve the weather information."
    return response_text

def tell_joke():
    joke = pyjokes.get_joke()
    return f"Here's a joke: {joke}"


def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")

def play_on_netflix(command):
    query = command.replace('play', '').replace('on netflix', '').strip()
    webbrowser.open(f"https://www.netflix.com/search?q={query}")

def search_on_amazon(command):
    query = command.replace('search for', '').replace('on amazon', '').strip()
    webbrowser.open(f"https://www.amazon.com/s?k={query}")

def get_state_capital(command):
    for state in states_and_capitals:
        if state in command:
            capital = states_and_capitals[state]
            return f"The capital of {state} is {capital}."
    return "Sorry, I didn't understand that."

def speak(text):
    if not engine._inLoop:
        engine.say(text)
        engine.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)
