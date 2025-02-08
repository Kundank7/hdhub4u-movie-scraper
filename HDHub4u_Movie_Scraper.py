from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def get_movie_details(movie_name):
    search_url = f"https://hdhub4u.phd/search/{movie_name.replace(' ', '%20')}"

    # Setup Selenium WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening a browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(search_url)
        time.sleep(3)  # Wait for JavaScript to load content

        # Extract movie details (modify the class if needed)
        try:
            movie_info = driver.find_element(By.CLASS_NAME, "post-info").text
        except:
            movie_info = "Movie details not available."

        # Extract download link (modify the ID or class if needed)
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
