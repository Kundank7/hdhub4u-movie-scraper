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

    search_url = f"{BASE_URL}/?s=" + movie_name.replace(" ", "+")  # Search for the movie

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3',
            'Referer': BASE_URL,  
            'Accept-Language': 'en-US,en;q=0.9'
        }

        # 🔍 Step 1: Search for the movie
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
        search_soup = BeautifulSoup(search_response.content, 'html.parser')

        # Find the first search result
        first_result = search_soup.find('h2', class_='post-title').find('a', href=True)
        if not first_result:
            return jsonify({'error': 'Movie not found'}), 404

        movie_page_url = first_result['href']
        if not movie_page_url.startswith("http"):  
            movie_page_url = BASE_URL + movie_page_url  # Fix missing "https://"

        # 🔍 Step 2: Scrape the actual movie page
        response = requests.get(movie_page_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract Movie Title
        movie_title_tag = soup.find('h1', class_='entry-title')
        movie_title = movie_title_tag.get_text(strip=True) if movie_title_tag else "Title not found"

        # Extract Movie Description
        movie_info_tag = soup.find('div', class_='entry-content')
        movie_info = movie_info_tag.get_text(strip=True) if movie_info_tag else "Movie details not available."

        # 🔍 Step 3: Extract all available download links from `bgmiaimassist.in`
        download_links = {}
        for link in soup.find_all('a', href=True):
            href = link["href"]
            text = link.get_text(strip=True)

            if "bgmiaimassist.in" in href:
                if "720p" in text:
                    download_links["720p"] = href
                elif "480p" in text:
                    download_links["480p"] = href
                elif "1080p" in text:
                    download_links["1080p"] = href

        # If no download links are found, return an error
        if not download_links:
            download_links["error"] = "No valid download links found."

        # 🔍 Step 4: Return JSON Response
        response = jsonify({
            'movie_title': movie_title,
            'movie_info': movie_info,
            'download_links': download_links
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
