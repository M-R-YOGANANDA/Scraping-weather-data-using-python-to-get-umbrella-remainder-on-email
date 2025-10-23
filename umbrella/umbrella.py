import schedule
import smtplib
import requests
import time


def umbrellaReminder():
    city = "Hyderabad"
    api_key = "cdaac453b63304c6cf6170c8c491ef57"   # 👈 put your OpenWeatherMap API key here
    
    # API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    
    if response.get("cod") != 200:
        print("❌ Error fetching weather:", response.get("message", "Unknown error"))
        return
    
    temperature = response["main"]["temp"]
    sky = response["weather"][0]["main"]   # e.g., Rain, Clouds, Clear
    
    print(f"🌡️ Temp: {temperature}°C, Sky: {sky}")
    
    if sky in ["Rain", "Drizzle", "Thunderstorm", "Clouds"]:
        try:
            smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_object.starttls()
            
            sender_email = "bhuvaneshwaritsms010@gmail.com"
            sender_pass = "ifqm ddde msbu vjti"  # Gmail app password
            receiver_email = "bhuvaneshwaritsms010@gmail.com"
            
            smtp_object.login(sender_email, sender_pass)
            
            subject = "Umbrella Reminder 🌂"
            body = f"""
Hello,

Take an umbrella before leaving the house today!
Weather condition: {sky}
Temperature: {temperature}°C
City: {city}

Stay safe!
"""
            msg = f"Subject:{subject}\n\n{body}".encode("utf-8")
            
            smtp_object.sendmail(sender_email, receiver_email, msg)
            smtp_object.quit()
            print("✅ Email Sent!")
        
        except Exception as e:
            print("❌ Error sending email:", e)
    else:
        print("☀️ No umbrella needed today!")


# run every 10 seconds for testing
schedule.every(10).seconds.do(umbrellaReminder)

while True:
    schedule.run_pending()
    time.sleep(1)
