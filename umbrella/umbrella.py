"""
🌂 Umbrella Reminder – Python Automation
----------------------------------------
This script checks the live weather using OpenWeather API and sends you an
email reminder to carry an umbrella when it's rainy, cloudy, or stormy.

✨ Features:
- Fetches real-time weather data.
- Sends an email reminder via Gmail.
- Runs automatically every 30 minutes.
- Prevents duplicate spam emails.
- Pretty console output.
"""

# --- Imports ---
import requests
import smtplib
import schedule
import time
from plyer import notification   # Optional: for desktop popup notifications

# --- Configuration ---
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASS = "your_gmail_app_password"  # use Gmail App Password
RECEIVER_EMAIL = "receiver_email@gmail.com"

API_KEY = "your_openweather_api_key"
CITIES = ["Hyderabad"]  # You can add multiple cities here
CHECK_INTERVAL = 30     # in minutes

# --- Global variable to avoid duplicate alerts ---
last_alert = {}

# --- Helper Functions ---
def get_weather(city):
    """Fetch weather data for a city using OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data["main"]["temp"]
            condition = data["weather"][0]["main"]
            return temp, condition
        else:
            print(f"❌ Error fetching weather for {city}: {data.get('message')}")
            return None, None
    except Exception as e:
        print(f"⚠️ Network error for {city}: {e}")
        return None, None


def send_email(subject, body):
    """Send an email using Gmail SMTP server."""
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()
        smtp_object.login(SENDER_EMAIL, SENDER_PASS)

        msg = f"Subject:{subject}\n\n{body}".encode("utf-8")
        smtp_object.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)
        smtp_object.quit()
        print("✅ Email Sent!")
    except Exception as e:
        print(f"❌ Email Error: {e}")


def send_notification(title, message):
    """Send a desktop notification."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )
    except Exception as e:
        print(f"⚠️ Notification Error: {e}")


# --- Main Function ---
def umbrella_reminder():
    global last_alert

    print("\n" + "=" * 50)
    print("⏳ Checking weather conditions...")
    print("=" * 50)

    for city in CITIES:
        temp, sky = get_weather(city)

        if temp is None or sky is None:
            continue

        print(f"🌆 City: {city}")
        print(f"🌡️ Temperature: {temp}°C | Sky: {sky}")

        # Alert conditions
        if sky in ["Rain", "Drizzle", "Thunderstorm", "Clouds"]:
            if last_alert.get(city) != sky:
                subject = f"🌂 Umbrella Reminder for {city}"
                body = f"""
Hello,

Take an umbrella before leaving the house today!
Weather condition: {sky}
Temperature: {temp}°C
City: {city}

Stay safe!
                """
                send_email(subject, body)
                send_notification("🌂 Umbrella Reminder", f"{city}: {sky}, {temp}°C — Take your umbrella!")
                last_alert[city] = sky
            else:
                print(f"⚠️ Already alerted for {city} ({sky}). Skipping email.")
        else:
            print(f"☀️ No umbrella needed in {city}.")
            last_alert[city] = None

    print("=" * 50)
    print("✅ Check complete! Next run in", CHECK_INTERVAL, "minutes.")
    print("=" * 50)


# --- Scheduler Setup ---
print("🚀 Umbrella Reminder Service is running...\n")
schedule.every(CHECK_INTERVAL).minutes.do(umbrella_reminder)

# Run once immediately on startup
umbrella_reminder()

while True:
    schedule.run_pending()
    time.sleep(1)
