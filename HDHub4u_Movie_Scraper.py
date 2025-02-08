# HDHub4u Movie Scraper

from flask import Flask, request, jsonify
import requests
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/movie', methods=['GET'])
def get_movie_details():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400

    search_url = f'https://hdhub4u.phd/search/{movie_name.replace(" ", "%20")}'

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        movie_section = soup.find(class_='post-info')
        download_link = soup.find(class_='download-link')

        if not movie_section or not download_link:
            return jsonify({'error': 'Movie not found or no download link available'}), 404

        movie_info = movie_section.get_text(strip=True)
        download_url = download_link.find('a')['href']

        return jsonify({'movie_info': movie_info, 'download_url': download_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Uses PORT from the environment
    app.run(host='0.0.0.0', port=port)
