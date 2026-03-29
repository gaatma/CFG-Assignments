
# CFG Data Science & ML — Assignment 2: Using APIs in Python
# -------------------------------------------------------------
# Author:      Gifty Acquah
# Date:        March 2026
# Description: EV Charging Station Environment Monitor
#              A console application that monitors real-time weather conditions
#              at EV charging station locations and assesses whether conditions
#              are SAFE, CAUTION, or DANGER for charging operations.
#              Also retrieves live ISS astronaut data as a demonstration of
#              remote infrastructure monitoring — relevant to smart grid and
#              cyber-physical systems research.
#
# APIS USED:
#   1. Open Notify API (http://api.open-notify.org/astros.json)
#      - No API key required. Freely accessible.
#      - Returns the number of people currently aboard the ISS.
#
#   2. wttr.in Weather API (https://wttr.in/)
#      - No API key required. Freely accessible.
#      - Returns real-time weather data for any city in JSON format.
#
# ADDITIONAL MODULE: 'datetime'
#   - Built into Python, no installation needed.
#   - Used to timestamp the monitoring report.
#
# HOW TO RUN:
#   1. Make sure Python 3 is installed
#   2. Install the requests library if not already installed:
#      pip install requests
#   3. Run the file:
#      python assignment2.py
# ----------------------------------

#imports
import requests   # For making HTTP requests to APIs
import datetime   # Additional module — used for timestamping reports (built-in, no install needed)

# CONSTANTS — Thresholds for EV charging safety assessment
TEMP_DANGER_HIGH = 40      # Above 40°C is dangerous for EV batteries (overheating risk)
TEMP_CAUTION_HIGH = 35     # Above 35°C warrants caution
TEMP_DANGER_LOW = -20      # Below -20°C is dangerous (battery freeze risk)
TEMP_CAUTION_LOW = -10     # Below -10°C warrants caution
WIND_DANGER = 60           # Above 60 km/h wind is dangerous (structural risk)
WIND_CAUTION = 40          # Above 40 km/h warrants caution
HUMIDITY_DANGER = 95       # Above 95% humidity risks electrical safety


# ------------------------------------------------------------------
# FUNCTION: display_welcome
# Displays a welcome banner when the program starts
def display_welcome():
    print("=" * 60)
    print("    EV CHARGING STATION ENVIRONMENT MONITOR ")
    print("=" * 60)
    print("   Monitoring weather safety for EV charging locations")
    print("   Inspired by smart grid & cyber-physical systems research")
    print("=" * 60)
    print()

# --------------------------------------------------------------------
# FUNCTION: get_iss_crew
# Fetches the current number of astronauts aboard the ISS
# from the Open Notify API — demonstrates remote infrastructure monitoring
# Returns: a tuple of (count, names_list) or (None, None) on failure

def get_iss_crew():
    url = "http://api.open-notify.org/astros.json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
 
        # Use a list to store astronaut names
        names = [person["name"] for person in data["people"]]
        count = data["number"]
        return count, names
 
    except Exception as e:
        print(f"  Could not retrieve ISS data: {e}")
        return None, None

# --------------------------------------------------------------------  
# FUNCTION: get_weather  
# Fetches real-time weather data for a given city using wttr.in API
# Parameter: city (string) — the city name to check
# Returns: a dictionary with weather details, or None on failure

def get_weather(city):
    # Format the city name for the URL — replace spaces with +
    formatted_city = city.strip().replace(" ", "+")
    url = f"https://wttr.in/{formatted_city}?format=j1"
 
    try:
        response = requests.get(url, timeout=10)
 
        # Check the response was successful
        if response.status_code != 200:
            return None
 
        data = response.json()
 
        # Extract current weather values from the nested JSON
        current = data["current_condition"][0]
 
        # Use string slicing to extract the first 5 characters of description
        description = current["weatherDesc"][0]["value"]
        short_desc = description[:20]  # String slicing — first 20 characters
 
        # Store weather data in a dictionary
        weather = {
            "city": city.title(),
            "temp_c": int(current["temp_C"]),
            "feels_like_c": int(current["FeelsLikeC"]),
            "humidity": int(current["humidity"]),
            "wind_kmph": int(current["windspeedKmph"]),
            "description": description,
            "short_desc": short_desc,
            "visibility": int(current["visibility"]),
        }
 
        return weather
 
    except Exception as e:
        print(f"  Could not retrieve weather for {city}: {e}")
        return None

# --------------------------------------------------------------------  
# FUNCTION: assess_safety
# Assesses whether weather conditions are SAFE, CAUTION, or DANGER
# for EV charging operations based on thresholds
# Parameter: weather (dictionary) — weather data from get_weather()
# Returns: a tuple of (status string, list of reasons)

def assess_safety(weather):
    reasons = []  # List to store all safety concerns found
    is_danger = False
    is_caution = False
 
    temp = weather["temp_c"]
    wind = weather["wind_kmph"]
    humidity = weather["humidity"]
 
    # Temperature checks
    if temp > TEMP_DANGER_HIGH:
        is_danger = True
        reasons.append(f"Extreme heat ({temp}°C) — risk of EV battery overheating")
    elif temp > TEMP_CAUTION_HIGH:
        is_caution = True
        reasons.append(f"High temperature ({temp}°C) — monitor battery temperature closely")
 
    if temp < TEMP_DANGER_LOW:
        is_danger = True
        reasons.append(f"Extreme cold ({temp}°C) — risk of battery freeze and capacity loss")
    elif temp < TEMP_CAUTION_LOW:
        is_caution = True
        reasons.append(f"Low temperature ({temp}°C) — reduced battery efficiency expected")
 
    #  Wind speed checks
    if wind > WIND_DANGER:
        is_danger = True
        reasons.append(f"Dangerous wind speed ({wind} km/h) — structural risk to charging equipment")
    elif wind > WIND_CAUTION:
        is_caution = True
        reasons.append(f"High wind speed ({wind} km/h) — secure charging cables")
 
    # Humidity checks
    if humidity > HUMIDITY_DANGER:
        is_danger = True
        reasons.append(f"Extreme humidity ({humidity}%) — electrical safety risk")
 
    # Use boolean values to determine final status
    if is_danger:
        status = "DANGER"
    elif is_caution:
        status = "CAUTION"
    else:
        status = "SAFE"
        reasons.append("All environmental parameters within safe operating range")
 
    return status, reasons

 
# --------------------------------------------------------------------  
# FUNCTION: display_weather_report
# Displays a formatted weather and safety report for a single location
# Parameter: weather (dictionary), status (string), reasons (list)

def display_weather_report(weather, status, reasons):
    # Choose status symbol using if/else
    if status == "SAFE":
        symbol = "SAFE"
    elif status == "CAUTION":
        symbol = "CAUTION"
    else:
        symbol = "DANGER"
 
    print(f"\n   Location: {weather['city']}")
    print(f"   Temperature: {weather['temp_c']}°C (feels like {weather['feels_like_c']}°C)")
    print(f"   Humidity: {weather['humidity']}%")
    print(f"  Wind Speed: {weather['wind_kmph']} km/h")
    print(f"   Visibility: {weather['visibility']} km")
    print(f"   Conditions: {weather['description']}")
    print(f"\n  EV CHARGING STATUS: {symbol}")
    print()
 
    # Loop through all reasons using a for loop
    for reason in reasons:
        print(f"    {reason}")
 
 
# -------------------------------------------------------------------- 
# FUNCTION: save_report
# Writes the full monitoring report to a text file
# Parameters: results (list of dicts), iss_count, iss_names

def save_report(results, iss_count, iss_names):
    filename = "ev_monitoring_report.txt"
 
    # Use datetime module to timestamp the report
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    with open(filename, "w") as file:
        file.write("=" * 60 + "\n")
        file.write("  EV CHARGING STATION ENVIRONMENT MONITOR - REPORT\n")
        file.write("=" * 60 + "\n")
        file.write(f"  Generated: {timestamp}\n")
        file.write("  Author: Gifty Acquah - CFG Data Science & ML\n")
        file.write("=" * 60 + "\n\n")
 
        # Write ISS section
        file.write("ISS REMOTE INFRASTRUCTURE STATUS\n")
        file.write("-" * 40 + "\n")
        if iss_count is not None:
            file.write(f"  People currently aboard ISS: {iss_count}\n")
            file.write("  Crew members:\n")
            for name in iss_names:
                file.write(f"    - {name}\n")
        else:
            file.write("  ISS data unavailable\n")
 
        file.write("\n\nEV CHARGING LOCATION REPORTS\n")
        file.write("-" * 40 + "\n")
 
        # Write each location result using a for loop
        for result in results:
            weather = result["weather"]
            status = result["status"]
            reasons = result["reasons"]
 
            file.write(f"\n  Location: {weather['city']}\n")
            file.write(f"  Temperature: {weather['temp_c']}C\n")
            file.write(f"  Humidity: {weather['humidity']}%\n")
            file.write(f"  Wind Speed: {weather['wind_kmph']} km/h\n")
            file.write(f"  Conditions: {weather['description']}\n")
            file.write(f"  EV Charging Status: {status}\n")
            file.write("  Details:\n")
            for reason in reasons:
                # Use string slicing to remove emoji characters for clean file output
                clean_reason = clean_reason = reason.strip()
                file.write(f"    - {clean_reason}\n")
 
    print(f"\n  Report saved to: {filename}")
    return filename
 
 

# -------------------------------------------------------------------- 
# FUNCTION: get_user_locations
# Asks the user to enter EV charging station locations to monitor
# Returns: a list of city names

def get_user_locations():
    locations = []  # List to store user-entered locations
    print("\n  Enter EV charging station locations to monitor.")
    print("  (Enter city names one at a time. Type 'done' when finished)\n")
 
    # Use a while loop to keep asking until user types done
    while True:
        city = input("  Enter city name (or 'done' to finish): ").strip()
 
        if city.lower() == "done":
            # Check we have at least one location
            if len(locations) == 0:
                print("    Please enter at least one location.")
                continue
            break
        elif len(city) == 0:
            print("    City name cannot be empty. Please try again.")
            continue
        else:
            locations.append(city)
            print(f"   Added: {city.title()}")
 
    return locations
 
 
# -------------------------------------------------------------------- 
# MAIN PROGRAM

def main():
    # Display welcome banner
    display_welcome()
 
    #  Step 1: Fetch ISS crew data 
    print("   Fetching ISS crew data (remote infrastructure monitoring)...")
    iss_count, iss_names = get_iss_crew()
 
    if iss_count is not None:
        print(f"\n  Currently {iss_count} people aboard the International Space Station:")
        for name in iss_names:
            print(f"     {name}")
    print()
 
    # Step 2: Get locations from user
    locations = get_user_locations()
 
    # Store results in a list of dictionaries
    results = []
 
    print("\n" + "=" * 60)
    print("  WEATHER SAFETY ASSESSMENT FOR EV CHARGING LOCATIONS")
    print("=" * 60)
 
    # Step 3: Check weather for each location using a for loop
    for city in locations:
        print(f"\n   Checking weather for: {city.title()}...")
        weather = get_weather(city)
 
        if weather is not None:
            status, reasons = assess_safety(weather)
            display_weather_report(weather, status, reasons)
 
            # Store result in list
            results.append({
                "weather": weather,
                "status": status,
                "reasons": reasons
            })
        else:
            print(f"   Could not retrieve data for {city}. Skipping.")
 
    #  Step 4: Summary using inbuilt functions
    if len(results) > 0:
        print("\n" + "=" * 60)
        print("  SUMMARY")
        print("=" * 60)
 
        # Use inbuilt functions: len() and sorted()
        total = len(results)
        danger_count = len([r for r in results if r["status"] == "DANGER"])
        caution_count = len([r for r in results if r["status"] == "CAUTION"])
        safe_count = len([r for r in results if r["status"] == "SAFE"])
 
        # Sort locations alphabetically using sorted() — inbuilt function
        sorted_locations = sorted([r["weather"]["city"] for r in results])
 
        print(f"\n  Total locations monitored: {total}")
        print(f"   Safe:    {safe_count}")
        print(f"    Caution: {caution_count}")
        print(f"   Danger:  {danger_count}")
        print(f"\n  Locations checked (A-Z): {', '.join(sorted_locations)}")
 
        # Boolean check — alert if any danger locations found
        has_danger = danger_count > 0
        if has_danger:
            print("\n   ALERT: One or more locations require immediate attention!")
        else:
            print("\n   All monitored locations are within acceptable safety parameters.")
 
        #  Step 5: Save report to file
        print()
        save_report(results, iss_count, iss_names)
 
    print("\n" + "=" * 60)
    print("  Thank you for using the EV Charging Environment Monitor")
    print("  Stay safe. Charge smart. ")
    print("=" * 60 + "\n")
 
 
# Run the program
if __name__ == "__main__":
    main()
 