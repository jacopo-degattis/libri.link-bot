from config import *
# from requests import Session
import requests
# 
# de©f create_session() -> Session:
    # session = Session()
    # return session

def request(endpoint="/", params={}):
    res = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return res.json()

def search(query=None, args={}):
    if query:
        res = request("/search", params={"search": query, **args})
        return res

def search_author(author_id=None, args={}):
    if author_id:
        res = request(f"/editore/{author_id}", params={**args})
        return res

def book_info(book_id=None, args={}):
    if book_id:
        res = request(f"/posts/{book_id}", params={**args})
        return res

def get_author_info(author_id=None, args={}):
    if author_id:
        res = request(f"/autore/{author_id}", args={**args})
        return res

