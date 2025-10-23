import smtplib
import requests
import time

# --- Weather function ---
def get_weather(city):
    api_key = "cdaac453b63304c6cf6170c8c491ef57"   # 🔑 Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        condition = data['weather'][0]['main']   # e.g., Rain, Mist, Clouds
        return temp, condition
    else:
        print("❌ Error fetching weather:", response.json().get("message"))
        return None, None

# --- Email function ---
def send_email(subject, body):
    try:
        smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_object.starttls()

        sender_email = "bhuvaneshwaritsms010@gmail.com"
        sender_pass = "ifqm ddde msbu vjti"  # 🔑 Gmail App Password
        receiver_email = "bhuvaneshwaritsms010@gmail.com"

        smtp_object.login(sender_email, sender_pass)

        msg = f"Subject:{subject}\n\n{body}".encode("utf-8")
        smtp_object.sendmail(sender_email, receiver_email, msg)
        smtp_object.quit()
        print("✅ Email Sent!")
    except Exception as e:
        print("❌ Email Error:", e)

# --- Umbrella Reminder ---
def umbrellaReminder():
    global last_alert
    city = "Maharastra"
    temp, sky = get_weather(city)

    if not temp or not sky:
        return

    print(f"🌡️ Temp: {temp}°C, Sky: {sky}")

    # Check if condition is rainy/cloudy and not already alerted
    if sky in ["Rain", "Rain And Snow", "Showers", "Thunderstorm", "Clouds"] and last_alert != sky:
        subject = "🌂 Umbrella Reminder!"
        body = f"""
Hello,

Take an umbrella before leaving the house today!
Weather condition: {sky}
Temperature: {temp}°C
City: {city}

Stay safe!
"""
        send_email(subject, body)
        last_alert = sky   # ✅ update last alert so it won’t spam repeatedly
    else:
        print("☀️ No umbrella needed right now.")

# --- Main Loop ---
last_alert = None   # to prevent duplicate mails for same weather
print("⏳ Umbrella Reminder Service is running...")

while True:
    umbrellaReminder()
    time.sleep(1800)  # ⏰ check every 30 minutes (1800 sec)
