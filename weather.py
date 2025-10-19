import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api = os.getenv("APPID", "")

def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 1)

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {city}: {response.status_code}")
        return None
    return response.json()

def print_daily_summary(city, data):
    print(f"\nWeather forecast for {city} (Daily Summary):")
    seen_dates = set()
    for item in data["list"]:
        dt = item["dt_txt"]
        date, time = dt.split()
        if time == "12:00:00" and date not in seen_dates:
            seen_dates.add(date)
            temp = kelvin_to_celsius(item["main"]["temp"])
            desc = item["weather"][0]["description"].capitalize()
            print(f"{date} | {temp}°C | {desc}")

def main():
    cities = ["Toronto", "Kitchener", "Ottawa"]
    for city in cities:
        data = fetch_weather(city)
        if data:
            print_daily_summary(city, data)

if __name__ == "__main__":
    main()
