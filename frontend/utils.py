
import requests

def fetch_data(base_url, suffix):
    url = generate_url(base_url, suffix)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  
    else:
        return None

def generate_url(base_url, suffix):
    url = base_url.strip("/") + "/" + suffix.strip("/")
    return url
