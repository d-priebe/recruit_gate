from bs4 import BeautifulSoup
import requests

def scrape_website(url):
    """Fetch the website content."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        hyper_links = soup.find_all('a')
        # Extract the href attributes from each link
        urls = [link.get('href') for link in hyper_links if link.get('href')]
        text = soup.get_text()
        return text, urls
    except requests.RequestException as e:
        print(f"Request failed: {e}")
