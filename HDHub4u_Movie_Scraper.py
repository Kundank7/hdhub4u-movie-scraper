from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/movie', methods=['GET'])
def get_movie_details():
    movie_name = request.args.get('name')
    if not movie_name:
        return jsonify({'error': 'Movie name is required'}), 400

    search_url = f'https://hdhub4u.phd/search/{movie_name.replace(" ", "%20")}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract movie details
        movie_section = soup.find(class_='post-info')  # Adjust if needed
        movie_info = movie_section.get_text(strip=True) if movie_section else "Movie details not available."

        # Extract download link (new selector)
        download_btn = soup.find('a', id='lk3b')
        download_url = download_btn['href'] if download_btn else "No download link found."

        return jsonify({'movie_info': movie_info, 'download_url': download_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
