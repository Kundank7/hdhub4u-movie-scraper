from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess

app = Flask(__name__)

def install_chromium():
    """Download and set up a portable Chromium binary."""
    chrome_path = "/tmp/chrome/chrome"
    if not os.path.exists(chrome_path):
        os.makedirs("/tmp/chrome", exist_ok=True)
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "-O", "/tmp/chrome/chrome.deb"])
        subprocess.run(["dpkg", "-x", "/tmp/chrome/chrome.deb", "/tmp/chrome"])
        chrome_path = "/tmp/chrome/usr/bin/google-chrome-stable"
    return chrome_path

def get_movie_details(movie_name):
    search_url = f"https://hdhub4u.phd/search/{movie_name.replace(' ', '%20')}"

    # Get Chromium binary path
    chrome_path = install_chromium()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.binary_location = chrome_path  # Use downloaded Chromium
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(search_url)

        # Extract movie details
        try:
            movie_info = driver.find_element(By.CLASS_NAME, "post-info").text
        except:
            movie_info = "Movie details not available."

        # Extract download link
        try:
            download_btn = driver.find_element(By.ID, "lk3b")
            download_url = download_btn.get_attribute("href")
        except:
            download_url = "No download link found."

        driver.quit()
        return {"movie_info": movie_info, "download_url": download_url}

    except Exception as e:
        driver.quit()
        return {"error": str(e)}

@app.route('/movie', methods=['GET'])
def movie_api():
    movie_name = request.args.get("name")
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400

    movie_details = get_movie_details(movie_name)
    return jsonify(movie_details)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
