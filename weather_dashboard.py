# weather app
#Uses OpenWeather API and Google firebase cloud  

import firebase_admin
from firebase_admin import firestore, credentials
import requests

# Firebase setup
cred = credentials.Certificate("weather-dashboard-d1fbf-firebase-adminsdk-jt3t4-4672c204bc.json")

# OpenWeatherMap API setup
API_KEY = "5b13fd7606ef8ee83d3c19d932d818b8"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#Saves user preferences to Firebase Cloud
def save_preferences():
    username = input("Enter a username: ")
    state = input("Enter your state: ")
    city = input("Enter your city: ")
    unit = input("Choose your temperature unit (Imperial for Farenheit and metric for Celcius)").lower()
    if unit not in ["imperial", "metric"]:
        print("Invalid unit! Defaulting to imperial.")
        unit = "imperial"

    prefs = {"username": username, "city": city, "state": state, "unit": unit}

    db.collection("preferences").document(username).set(prefs)
    print("Preferences saved successfully!")

#Gets the user preferences
def get_preferences(username):

    # Get prefs docs for that state and city
    prefs_doc = db.collection("preferences").document(username).get()

    if prefs_doc.exists:
        print(f"Preferences for {username}: {prefs_doc.to_dict()}")
        return prefs_doc.to_dict()
    else:
        print("No Preferences found")
        return None

#Get weather
def get_weather(state, city, unit):
    params = {"q": f"{city}, {state}", "appid": API_KEY, "units": unit}
    response = requests.get(WEATHER_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"city: {data['name']}")
        print(f"Temperature: {data['main']['temp']}° ({unit})")
        print(f"Weather: {data['weather'][0] ['description']}")
    else:
        print("Error fetching weather data:", response.json().get("message", "Unknown error"))

#The main stuff!
def main():
    while True:
        print("\nWeatherDashboard")
        print("1. Save Preferences")
        print("2. View Preferences")
        print("3. Get Weather")
        print("4 Exit")

        
        choice = input("Enter your choice: ")
        
        # Logic for saving preferences
        if choice == "1":
            save_preferences()

        # Logic for viewing preferences
        elif choice == "2":
            username = input("Enter your username: ")
            prefs = get_preferences(username)

        #Logic for viewing the weather
        elif choice == "3":
            username = input("Enter your username: ")
            if prefs:
                city = prefs["city"]
                state = prefs["state"]
                unit = prefs["unit"]
                get_weather(city, state, unit)
            else:
                print("No preferences found. Please save preferences first.")
        
        #Exit code
        elif choice == "4" or "exit":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again")


if __name__ == "__main__":
    main()