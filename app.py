from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import scraper
import db

app = Flask(__name__)

# Scheduler for periodic scraping
scheduler = BackgroundScheduler()
scheduler.add_job(scraper.fetch_bike_data, 'interval', minutes=5)
scheduler.add_job(scraper.fetch_weather_data, 'interval', hours=1)
scheduler.start()

@app.route("/")
def home():
    return jsonify({"message": "Flask scraper is running!"})

@app.route("/scrape")
def manual_scrape():
    """Manually trigger data scraping."""
    scraper.fetch_bike_data()
    scraper.fetch_weather_data()
    return jsonify({"message": "Data scraped successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
