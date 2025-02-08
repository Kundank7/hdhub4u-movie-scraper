import requests
from bs4 import BeautifulSoup

# URL of the movie page
movie_url = "https://hdhub4u.phd/thandel-2025-hindi-pre-hd-full-movie/"

# Headers to simulate a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# Send the request
response = requests.get(movie_url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the 720p x264 link by looking for the specific text
    download_link = None
    for link in soup.find_all("a", href=True):
        if "720p x264" in link.text:
            download_link = link["href"]
            break

    # Print the result
    if download_link:
        print(f"720p x264 Download Link: {download_link}")
    else:
        print("720p x264 Download Link not found.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
