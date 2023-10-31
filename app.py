from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv
import os

# Import OpenAI API - Use your OpenAI API credentials here
import openai

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv('OPENAI_KEY')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# Function to interact with GPT-3 for general conversation
def chat_with_gpt3(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function to fetch weather information based on the location
def get_weather(location):
    # Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key from OpenWeatherMap
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            weather_data = response.json()
            if weather_data:
                temperature = weather_data['main']['temp']
                weather_description = weather_data['weather'][0]['description']
                city_name = weather_data['name']
                country_code = weather_data['sys']['country']
                weather_info = f"Current weather in {city_name}, {country_code}: Temperature: {temperature}K, Description: {weather_description}"
                return weather_info
            else:
                return "Weather information not available for this location."
        else:
            return f"Failed to fetch weather data. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Request to weather API failed: {str(e)}"
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    if "current location" in user_message.lower():
        response = get_weather("New York")  # You can replace "New York" with the user's detected location
    else:
        response = chat_with_gpt3(user_message)
    return {'message': response}


if __name__ == '__main__':
    app.run(debug=True)
