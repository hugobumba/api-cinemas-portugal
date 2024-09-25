# 🎥 API Cinemas Portugal
![image](https://github.com/user-attachments/assets/77c35e5f-62bc-49ec-a4ac-b2a5c61c3297)

- :link: Link on Render: https://api-cinemas-portugal.onrender.com/movies


## 🔎 Overview

This API provides information about movies currently playing in cinemas across Portugal. The data is collected via web scraping from various cinema websites and served through a RESTful API.


## ⭕ Endpoints

  - /movies
  - /cinema/(cinema)
  - /genre/(genre)
  - /status/(status)
  - /year/(year)
  - (Others soon...)


## :star2: Features

- Scrapes articles from multiple sources:
  - ✅ NOS Cinemas
  - ✅ UCI Cinemas
  - ✅ Cineplace
  - ✅ CinemaCity
  - ✅ Cinema Trindade
  - ✅ Castello Lopes
  - ✅ Medeia Filmes Cinemas
  - ❌ Cine Society
  - ❌ Cinemax
- Returns the movies info in JSON format
- ❌CronJob (every week)


## 🔧 Tech Stack

- Python: Backend development
- Flask: API
- MongoDB: Database
- Selenium: Scraping tool
- Render: Host service for deployment


## ⬇️ Installation

1. Clone the repository and go to directory:
   ```bash
   git clone https://github.com/yourusername/movies-api.git
   cd movies-api

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Set up environment variables: Create a .env file with the following values:
   ```bash
   pip install -r requirements.txt
   

## ▶️ Run

1. Run the scraper:
   ```bash
   flask run

2. Open the browser:
   - http://127.0.0.1:5000/movies
