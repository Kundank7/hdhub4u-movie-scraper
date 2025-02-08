from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)  # Ensure Gunicorn can find `app`

BASE_URL = "https://hdhub4u.phd"

@app.route('/movie', methods=['GET'])
def get_movie_details():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400

    search_url = f'{BASE_URL}/search/{movie_name.replace(" ", "%20")}'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract first movie result link
        first_movie_link = soup.find('a', href=True)
        if first_movie_link:
            movie_page_url = first_movie_link['href']
            if not movie_page_url.startswith("http"):
                movie_page_url = BASE_URL + movie_page_url
        else:
            return jsonify({'error': 'Movie not found'}), 404

        # Fetch the movie page
        response = requests.get(movie_page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract movie details
        movie_info_tag = soup.find('span', class_='material-text')
        movie_info = movie_info_tag.get_text(strip=True) if movie_info_tag else "Movie details not available."

        # Extract ONLY the 720p x264 download link
        download_btn = soup.find('a', href=True, text=lambda t: t and "720p x264" in t)
        download_url = download_btn['href'] if download_btn else "No 720p x264 link found."

        return jsonify({'movie_info': movie_info, 'download_url': download_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
