import asyncio
import python_weather
import time
import json
import pycountry
from fuzzywuzzy import process
import os

CACHE_FILE = 'weather_cache.json'
CACHE_TIMEOUT = 600

country_dict = {country.name.upper(): country.alpha_2 for country in pycountry.countries}

def load_cache():
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            # Remove expired cache entries
            data['matches'] = {
                loc: match for loc, match in data.get('matches', {}).items()
                if time.time() - data['timestamp'] < CACHE_TIMEOUT
            }
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {'timestamp': time.time(), 'matches': {}}

def save_cache(data):
    data['timestamp'] = time.time()
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_country_flag(country_code):
    try:
        flag = ''.join([chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper()])
        return flag
    except Exception as e:
        print(f"Error retrieving flag for {country_code}: {e}")
        return ':question:'

def get_country_code(location_name):
    location_name = location_name.upper()
    matches = process.extract(location_name, country_dict.keys(), limit=5)
    cache = load_cache()
    cache['matches'][location_name] = matches
    save_cache(cache)
    return matches

def exit_program():
    print("Exiting the program.")
    exit()

def prompt_for_location(location_name):
    cache = load_cache()
    matches = cache.get('matches', {}).get(location_name)
    
    if not matches:
        matches = get_country_code(location_name)
    
    if not matches:
        print("No matches found.")
        return location_name

    if len(matches) == 1:
        return matches[0][0]

    print("\nAmbiguous location. Here are some possible matches:")
    for i, (match, score) in enumerate(matches):
        print(f"{i + 1}. {match} (Score: {score})")
    print(f"{len(matches) + 1}. Enter manually")
    print(f"{len(matches) + 2}. Exit")

    while True:
        try:
            choice = int(input(f"Please select the correct option (1-{len(matches) + 2}): "))
            if choice == len(matches) + 1:
                return input("Please enter the correct location manually: ").upper()
            elif choice == len(matches) + 2:
                exit_program()
            elif 1 <= choice <= len(matches):
                return matches[choice - 1][0]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

async def get_weather_forecast(location_name):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(location_name)

        current_temp_fahrenheit = weather.temperature
        current_temp_celsius = fahrenheit_to_celsius(current_temp_fahrenheit)
        country_code = country_dict.get(location_name.upper())
        country_flag = get_country_flag(country_code) if country_code else 'No flag available'
        
        print(f"\n🌡️ Current Weather in {location_name}: {country_flag}")
        print(f"  Temperature: {current_temp_fahrenheit}°F ({current_temp_celsius:.1f}°C)")
        print(f"  Humidity: {weather.humidity}%")
        print(f"  Wind Speed: {weather.wind_speed} mph, {weather.wind_direction.emoji} ({weather.wind_direction.name})")
        print(f"  UV Index: {weather.ultraviolet.index} ({weather.ultraviolet.name})\n")

        print("📅 Daily Forecast:")
        daily_forecasts = list(weather.daily_forecasts)
        for daily in daily_forecasts[:3]:  # Get the first 3 days of forecasts
            high_temp_celsius = fahrenheit_to_celsius(daily.highest_temperature)
            low_temp_celsius = fahrenheit_to_celsius(daily.lowest_temperature)
            
            print(f"  Date: {daily.date}")
            print(f"  Highest Temperature: {daily.highest_temperature}°F ({high_temp_celsius:.1f}°C)")
            print(f"  Lowest Temperature: {daily.lowest_temperature}°F ({low_temp_celsius:.1f}°C)")
            print(f"  Sunrise: {daily.sunrise}, Sunset: {daily.sunset}")
            print(f"  Moon Phase: {daily.moon_phase.emoji} ({daily.moon_phase.name})")
            print(f"  Snowfall: {daily.snowfall} inches")
            print("  Hourly Forecast:")
            for hourly in daily.hourly_forecasts:
                time_formatted = hourly.time.strftime("%H:%M")
                hourly_temp_celsius = fahrenheit_to_celsius(hourly.temperature)
                print(f"    → {time_formatted}: {hourly.temperature}°F ({hourly_temp_celsius:.1f}°C), {hourly.description}")
                print(f"      Wind Speed: {hourly.wind_speed} mph, {hourly.wind_direction.emoji} ({hourly.wind_direction.name})")
                print(f"      Humidity: {hourly.humidity}%, UV Index: {hourly.ultraviolet.index} ({hourly.ultraviolet.name})")
            print("-" * 40)

async def get_weather(location):
    await get_weather_forecast(location)

if __name__ == '__main__':
    location = input("Please enter the location for which you want the weather forecast: ").upper()
    location = prompt_for_location(location)

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(get_weather(location))
