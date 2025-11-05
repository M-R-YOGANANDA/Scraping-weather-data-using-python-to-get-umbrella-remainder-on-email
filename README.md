# scraping-weather-data-using-python-to-get-umbrella-reminder-on-email

🌂 Umbrella Reminder – Python Automation

This project is a simple Python automation script that checks the weather (using the OpenWeather API
) and sends you an email reminder to carry an umbrella whenever it’s cloudy, rainy, or stormy.

✨ Features

Fetches real-time weather data for your city.

Sends an email reminder via Gmail when the weather is rainy/cloudy.

Runs automatically in the background and checks weather every 30 minutes.

Prevents duplicate spam emails by only sending one alert per weather condition.

🛠️ Requirements

Python 3.7+

Gmail account with App Password enabled

OpenWeather API Key

📦 Installation

Clone the repo

git clone https://github.com/your-username/umbrella-reminder.git
cd umbrella-reminder


Install dependencies

pip install requests


Set up Gmail App Password

Enable 2-Step Verification on your Gmail.

Generate an App Password from Google Security Settings
.

Copy the 16-character app password.

Get OpenWeather API Key

Sign up on OpenWeather
.

Go to API Keys → Copy your key.

⚙️ Usage

Edit umbrella.py and update these values:

sender_email = "your_email@gmail.com"
sender_pass = "your_gmail_app_password"
receiver_email = "receiver_email@gmail.com"
api_key = "your_openweather_api_key"
city = "Hyderabad"   # change to your city


Run the script:

python umbrella.py


The script will:

Check the weather every 30 minutes

📸 Example Output
⏳ Umbrella Reminder Service is running...
🌡️ Temp: 26.15°C, Sky: Clouds
✅ Email Sent!
<img width="905" height="471" alt="image" src="https://github.com/user-attachments/assets/b84ba1e5-fb88-4894-87a2-762bac929c75" />


⏳ Umbrella Reminder Service is running...
🌡️ Temp: 24.23°C, Sky: Mist
☀️ No umbrella needed right now.




🚀 Future Improvements

Support for multiple cities.

Desktop notifications instead of email.

Docker setup for background service.

📜 License

This project is licensed under the MIT License – feel free to use and modify.


Print the current condition

Send an email reminder when it’s rainy/cloudy










issue of docker image is solved by the following 
Running the Project with Docker
1️⃣ Build the Docker image
docker build -t umbrella-reminder .

2️⃣ Run the container
docker run --env-file .env umbrella-reminder


🪄 Tip: The .env file automatically passes your credentials and settings into the container.

3️⃣ Stop the container

To stop it manually:

docker ps          # find the container ID
docker stop <container_id>

🧠 How It Works

Fetches live weather data for each city listed in CITIES.

Checks if the weather is Rain, Drizzle, Thunderstorm, or Clouds.

Sends an email or desktop notification depending on your ALERT_METHOD.

Uses anti-spam tracking (last_alerts_map) to avoid duplicate alerts.

Runs continuously using the schedule module to check every few seconds/minutes.

🧪 Local Testing (Optional)

You can run it directly without Docker too:

pip install -r requirements.txt
python umbrella_reminder.py

📋 Requirements

Python 3.10+

OpenWeatherMap API key

Gmail App Password (if using email)

Docker (optional for containerized setup)