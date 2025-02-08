from flask import Flask, request, jsonify, make_response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://hdhub4u.phd"

@app.route('/movie', methods=['GET'])
def get_movie_details():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400

    formatted_name = movie_name.lower().replace(" ", "-")
    movie_url = f"{BASE_URL}/{formatted_name}-2025-hindi-pre-hd-full-movie/"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3',
            'Referer': BASE_URL,  
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_title_tag = soup.find('h1')
        movie_title = movie_title_tag.get_text(strip=True) if movie_title_tag else "Title not found"

        movie_info_tag = soup.find('span', class_='material-text')
        movie_info = movie_info_tag.get_text(strip=True) if movie_info_tag else "Movie details not available."

        download_links = {}
        for link in soup.find_all('a', href=True):
            href = link["href"]
            text = link.get_text(strip=True)

            if "720p x264" in text and "download" in href:
                download_links["720p x264"] = href
            elif "480p" in text and "download" in href:
                download_links["480p"] = href
            elif "1080p" in text and "download" in href:
                download_links["1080p"] = href

        # Add CORS headers manually
        response = jsonify({
            'movie_title': movie_title,
            'movie_info': movie_info,
            'download_links': download_links
        })
        response.headers.add("Access-Control-Allow-Origin", "*")  # Allow any site
        response.headers.add("Access-Control-Allow-Methods", "GET")  # Allow GET requests
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")  # Allow content-type header
        return response

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
