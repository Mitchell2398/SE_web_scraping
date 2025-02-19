# SE_web_scraping
Open repo to web scrape bike and weather data for SE project

# **Dublin Bikes & Weather Scraper** 🚲🌤️

This project scrapes **real-time bike availability data** from JCDecaux and **weather data** from OpenWeatherMap, storing them in a **Supabase database**. The scraper runs every **5 minutes for bikes** and **1 hour for weather**.

🚀 **Deployed on Railway for automatic execution**

---

## **📌 Features**

- 🚲 Fetches **Dublin Bikes availability** via [JCDecaux API](https://developer.jcdecaux.com/)
- 🌤️ Fetches **current weather** via [OpenWeatherMap API](https://openweathermap.org/)
- 📦 Stores data in **Supabase (PostgreSQL)**
- ⏰ **Runs automatically** every **5 min (bikes) & 1 hour (weather)**
- 🔧 **Easy deployment** with **Railway + GitHub auto-deploy**

---

## **📜 Table of Contents**

1. [**Setup & Installation**](#setup--installation)
2. [**Setting Up Supabase**](#setting-up-supabase)
3. [**Setting Up Railway**](#setting-up-railway)
4. [**Database Schema**](#database-schema)
5. [**Deployment (Railway)**](#deployment-railway)
6. [**Usage & Testing**](#usage--testing)
7. [**Troubleshooting**](#troubleshooting)

---

## **🔧 Setup & Installation**

### **1️⃣ Prerequisites**

- Python **3.10+**
- PostgreSQL database (**Supabase** recommended)
- API keys for:
  - **JCDecaux** (Dublin Bikes data)
  - **OpenWeatherMap** (Weather data)
  - **Supabase** (Database connection)

### **2️⃣ Clone the Repository**

```bash
git clone https://github.com/mitchell2398/SE_web_scraping.git
cd SE_web_scraping
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**

Create a `.env` file in the project root and add your API keys:

```ini
# JCDecaux API Key
JCDECAUX_API_KEY=your_jcdecaux_api_key
JCDECAUX_CONTRACT_NAME=dublin

# OpenWeatherMap API Key
OPENWEATHER_API_KEY=your_openweather_api_key
CITY_NAME=Dublin

# Supabase Credentials
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your_supabase_key
```

---

## **🛠 Setting Up Supabase**

### **1️⃣ Create a Supabase Account**

- Go to **[Supabase](https://supabase.com/)** and create an account.
- Click **New Project**.
- Enter a **Project Name** and choose a region.
- Click **Create New Project**.

### **2️⃣ Get Your Supabase Database Credentials**

- Go to **Project Settings** → **Database**.
- Copy your **Database URL** (`SUPABASE_URL`).
- Copy your **API Key** (`SUPABASE_KEY`).

### **3️⃣ Initialize Database Tables**

Run the following SQL commands in **Supabase SQL Editor**:

```sql
CREATE TABLE availability (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL,
    last_update TIMESTAMP NOT NULL,
    available_bikes INTEGER,
    available_bike_stands INTEGER,
    status VARCHAR(128),
    CONSTRAINT unique_station_timestamp UNIQUE (number, last_update)
);

CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    timestamp TIMESTAMP NOT NULL,
    temperature FLOAT,
    humidity INTEGER,
    weather_description VARCHAR(255)
);
```

---

## **🚀 Setting Up Railway**

### **1️⃣ Install Railway CLI**

```bash
curl -fsSL https://railway.app/install.sh | sh
railway login
```

### **2️⃣ Create a New Railway Project**

```bash
railway init
```

### **3️⃣ Set Environment Variables in Railway**

```bash
railway env set \
    JCDECAUX_API_KEY=your_jcdecaux_api_key \
    JCDECAUX_CONTRACT_NAME=dublin \
    OPENWEATHER_API_KEY=your_openweather_api_key \
    CITY_NAME=Dublin \
    SUPABASE_URL=https://your-supabase-url.supabase.co \
    SUPABASE_KEY=your_supabase_key
```

### **4️⃣ Deploy the Project**

```bash
git push origin main  # Railway auto-deploys via GitHub
```

If Railway **doesn’t detect the start command**, create a `Procfile`:

```
worker: gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

Commit & push:

```bash
git add Procfile
git commit -m "Added Procfile for Railway"
git push origin main
```

Railway will now **auto-deploy on every push**. 🎉

---

## **🚀 Usage & Testing**

### **Run Locally**

```bash
python app.py
```

### **Manually Trigger Data Collection**

```bash
curl http://127.0.0.1:5000/scrape
```

### **Check Logs in Railway**

```bash
railway logs
```

### **Verify Data in Supabase**

- Open **Supabase Dashboard**.
- Check the **availability** & **weather** tables.

---

##


