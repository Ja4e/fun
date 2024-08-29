# weather: get the weather on the CLI
#
# Copyright (C) ja4e, Eason Qin, 2024.
#
# This source code form is licensed under the MIT/expat license. This program is provided
# on an AS IS BASIS with NO implications or expression of warranty. Please visit the
# OSI website for a full text of the license. 
#

import asyncio
import python_weather
import time
import json
import pycountry
import os

from rapidfuzz import process, fuzz

user_entries = {}

CACHE_FILE = "weather_cache.json"
CACHE_TIMEOUT = 2000

country_dict = {
    country.name.upper(): country.alpha_2 for country in pycountry.countries
}


def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            # Remove expired cache entries
            data["matches"] = {
                loc: match
                for loc, match in data.get("matches", {}).items()
                if time.time() - data["timestamp"] < CACHE_TIMEOUT
            }
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"timestamp": time.time(), "matches": {}}


def save_cache(data):
    data["timestamp"] = time.time()
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("Cache cleared.")
    else:
        print("Cache file does not exist.")


def get_country_flag(country_code):
    try:
        flag = "".join([chr(0x1F1E6 + ord(c) - ord("A")) for c in country_code.upper()])
        return flag
    except Exception as e:
        print(f"Error retrieving flag for {country_code}: {e}")
        return ":question:"


def get_country_code(location_name):
    location_name = location_name.upper()
    matches = process.extract(
        location_name, country_dict.keys(), scorer=fuzz.ratio, limit=15
    )
    exact_match = [match for match in matches if match[0] == location_name]
    if exact_match:
        matches = exact_match
    else:
        # Sort matches based on score (highest first)
        matches = sorted(matches, key=lambda x: x[1], reverse=True)

    cache = load_cache()
    cache["matches"][location_name] = matches
    save_cache(cache)
    return matches


def exit_program():
    print("Exiting the program.")
    exit()


USER_ENTRIES_FILE = "user_entries.json"


def load_user_entries():
    try:
        with open(USER_ENTRIES_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_user_entries():
    with open(USER_ENTRIES_FILE, "w") as f:
        json.dump(user_entries, f, indent=4)


def clear_user_entries():
    global user_entries

    user_entries.clear()
    print("User entries have been cleared.")


def get_location_choice(matches, location_name):
    while True:
        try:
            choice = int(input(f"Please select the correct option (1-{len(matches) + 6}): "))

            if 1 <= choice <= len(matches):
                # The user has selected a valid match
                selected_location = matches[choice - 1][0]
                return selected_location

            choice -= len(matches)

            match choice:
                case 1:
                    manual_entry = input("Please enter the correct location manually: ").upper()
                    country = input(f"Enter the country for {manual_entry}: ").upper()
                    if input(f"Do you want to save {manual_entry} as {country}? (y/n): ").lower() == "y":
                        user_entries[manual_entry] = country
                    return manual_entry
                case 2:
                    manual_entry = input("Please enter the correct location manually: ").upper()
                    return manual_entry
                case 3:
                    clear_cache()
                    return prompt_for_location(location_name)
                case 4:
                    clear_user_entries()
                    return prompt_for_location(location_name)
                case 5:
                    clear_cache()
                    clear_user_entries()
                    return prompt_for_location(location_name)
                case 6:
                    exit_program()
                case _:
                    print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def prompt_for_location(location_name):
    cache = load_cache()
    matches = cache.get("matches", {}).get(location_name)

    if not matches:
        matches = get_country_code(location_name)

    if not matches:
        print("No matches found.")
        return location_name

    if len(matches) == 1:
        return matches[0][0]

    print("\nAmbiguous location. Here are some possible matches:")
    for i, item in enumerate(matches):
        if len(item) == 3:
            match, score, _ = item
            print(f"{i + 1}. {match} (Score: {score:.2f})")
        else:
            print(f"Unexpected item structure: {item}")

    print(f"{len(matches) + 1}. Manual Correction")
    print(f"{len(matches) + 2}. Full Manual (not saved in dictionary)")
    print(f"{len(matches) + 3}. Clear Cache")
    print(f"{len(matches) + 4}. Clear User Entries")
    print(f"{len(matches) + 5}. Clear All Cache")
    print(f"{len(matches) + 6}. Exit")

    try:
        return get_location_choice(matches, location_name)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return prompt_for_location(location_name)  # Recursively call if invalid input



def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8


def print_daily_forecast(daily):
    high_temp_celsius = fahrenheit_to_celsius(daily.highest_temperature)
    low_temp_celsius = fahrenheit_to_celsius(daily.lowest_temperature)

    print(f"  Date: {daily.date}")

    print(
        f"  Highest Temperature: {daily.highest_temperature}°F ({high_temp_celsius:.1f}°C)"
    )

    print(
        f"  Lowest Temperature: {daily.lowest_temperature}°F ({low_temp_celsius:.1f}°C)"
    )

    print(f"  Sunrise: {daily.sunrise}, Sunset: {daily.sunset}")
    print(f"  Moon Phase: {daily.moon_phase.emoji} ({daily.moon_phase.name})")
    print(f"  Snowfall: {daily.snowfall} inches")
    print("  Hourly Forecast:")

    for hourly in daily.hourly_forecasts:
        time_formatted = hourly.time.strftime("%H:%M")
        hourly_temp_celsius = fahrenheit_to_celsius(hourly.temperature)

        print(
            f"    → {time_formatted}: {hourly.temperature}°F ({hourly_temp_celsius:.1f}°C), {hourly.description}"
        )

        print(
            f"      Wind Speed: {hourly.wind_speed} mph, {hourly.wind_direction.emoji} ({hourly.wind_direction.name})"
        )

        print(
            f"      Humidity: {hourly.humidity}%, UV Index: {hourly.ultraviolet.index} ({hourly.ultraviolet.name})"
        )
    print("-" * 40)


async def print_overview(location_name, weather):

    current_temp_fahrenheit = weather.temperature
    current_temp_celsius = fahrenheit_to_celsius(current_temp_fahrenheit)
    country_code = country_dict.get(location_name.upper())
    country_flag = (
        get_country_flag(country_code) if country_code else "No flag available"
    )

    print(f"\n🌡️ Current Weather in {location_name}: {country_flag}")
    print(f"  Temperature: {current_temp_fahrenheit}°F ({current_temp_celsius:.1f}°C)")
    print(f"  Humidity: {weather.humidity}%")
    print(
        f"  Wind Speed: {weather.wind_speed} mph, {weather.wind_direction.emoji} ({weather.wind_direction.name})"
    )
    print(f"  UV Index: {weather.ultraviolet.index} ({weather.ultraviolet.name})\n")


async def get_weather_forecast(location_name):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        print("📅 Daily Forecast:")

        weather = await client.get(location_name)
        await print_overview(location_name, weather)

        daily_forecasts = list(weather.daily_forecasts)
        for daily in daily_forecasts[:3]:  # Get the first 3 days of forecasts
            print_daily_forecast(daily)

def input_request():
    location = input("Please enter the location for which you want the weather forecast: ").upper()
    
while True:    
	if __name__ == "__main__":
		user_entries.update(load_user_entries())
		print("clear cache input: 1")
		print("clear user entries input: 2")
		print("clear all cache input: 3")
		print("Exit: 4")
		location = input(
			"Please enter the location for which you want the weather forecast: "
		).upper()
		if location== "1":
			clear_cache()
			input_request()
		elif location== "2":
			clear_user_entries()
			input_request()
		elif location== "3":
			clear_cache()
			clear_user_entries()
			input_request()
		elif location== "4":
			exit_program()
		else:
			location = prompt_for_location(location)

			if os.name == "nt":
				asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

			asyncio.run(get_weather_forecast(location))

			save_user_entries()
	else:
		exit_program()
