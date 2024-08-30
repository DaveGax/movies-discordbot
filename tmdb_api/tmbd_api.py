import requests
import os
from dotenv import load_dotenv

load_dotenv()
ApiKey = os.getenv('ApiKey')

def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ApiKey}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        titles = [movie['title'] for movie in data['results']]
        return titles
    else:
        return None

def get_toprated_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {ApiKey}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        titles = [movie['title'] for movie in data['results']]
        return titles
    else:
        return None