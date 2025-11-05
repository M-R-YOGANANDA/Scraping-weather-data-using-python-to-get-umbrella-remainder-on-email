import os
import time
import schedule
import smtplib
import requests
from plyer import notification
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
CITIES = os.getenv("CITIES", "Hyderabad")
ALERT_METHOD = os.getenv("ALERT_METHOD", "email").lower()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASS = os.getenv("SENDER_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Track last alert per city to prevent repeated emails
last_alerts_map = {}

def send_email(subject, body):
    try:
        smtp_object = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_object.starttls()
        smtp_object.login(SENDER_EMAIL, SENDER_PASS)
        msg = f"Subject:{subject}\n\n{body}".encode("utf-8")
        smtp_object.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)
        smtp_object.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

def send_desktop_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=10)
        print("💻 Desktop notification sent!")
    except Exception as e:
        print("❌ Error sending desktop notification:", e)

def umbrellaReminder():
    for city in [c.strip() for c in CITIES.split(",")]:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            print(f"❌ Error fetching weather for {city}: {response.get('message')}")
            continue

        temperature = response["main"]["temp"]
        sky = response["weather"][0]["main"]
        print(f"🌡️ {city}: {temperature}°C, Sky: {sky}")

        umbrella_needed = sky in ["Rain", "Drizzle", "Thunderstorm", "Clouds"]
        last_status = last_alerts_map.get(city)

        # Only send if status changed
        if umbrella_needed and last_status != "alerted":
            subject = f"Umbrella Reminder 🌂 - {city}"
            body = f"""
Hello,

Take an umbrella before leaving the house today!
Weather condition: {sky}
Temperature: {temperature}°C
City: {city}

Stay safe!
"""

            if ALERT_METHOD == "desktop":
                send_desktop_notification(subject, body)
            else:
                send_email(subject, body)

            last_alerts_map[city] = "alerted"

        elif not umbrella_needed and last_status != "clear":
            print(f"☀️ {city}: No umbrella needed today!")
            last_alerts_map[city] = "clear"

# Schedule every 10 seconds (use minutes/hour for production)
schedule.every(10).seconds.do(umbrellaReminder)

print("🌦️ Umbrella Reminder is running... (Press Ctrl+C to stop)")

while True:
    schedule.run_pending()
    time.sleep(1)
