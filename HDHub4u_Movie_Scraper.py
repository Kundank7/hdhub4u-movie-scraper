from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://hdhub4u.phd"

@app.route('/movie', methods=['GET'])
def get_movie_details():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400

    # Convert movie name to lowercase and format it for the URL
    formatted_name = movie_name.lower().replace(" ", "-")
    movie_url = f"{BASE_URL}/{formatted_name}-2025-hindi-pre-hd-full-movie/"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3',
            'Referer': BASE_URL,  
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(movie_url, headers=headers, allow_redirects=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract movie title
        movie_title_tag = soup.find('h1')  # Adjust selector if needed
        movie_title = movie_title_tag.get_text(strip=True) if movie_title_tag else "Title not found"

        # Extract movie details/description
        movie_info_tag = soup.find('span', class_='material-text')
        movie_info = movie_info_tag.get_text(strip=True) if movie_info_tag else "Movie details not available."

        # Extract all available download links
        download_links = {}
        for link in soup.find_all('a', href=True):
            if "480p" in link.text:
                download_links["480p"] = link["href"]
            elif "720p x264" in link.text:
                download_links["720p x264"] = link["href"]
            elif "1080p" in link.text:
                download_links["1080p"] = link["href"]

        return jsonify({
            'movie_title': movie_title,
            'movie_info': movie_info,
            'download_links': download_links
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
