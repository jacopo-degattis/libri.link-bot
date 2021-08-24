import requests
from config import BASE_URL, DOWNLOAD_URL

# DOWNLOAD_URI EXAMPLE
# https://dwnlg.link/book-n/giulio-cavalli/nuovissimo-testamento-giulio-cavalli/nuovissimo-testamento.epub

def __request(endpoint="/", params={}):
    res = requests.get(f"{BASE_URL}{endpoint}", params=params)
    return res.json()

def __get_download_info(book_slug):
    payload = {}
    for format in ["epub", "mobi", "pdf"]:
        if format in book_slug:
            book_slug, format = [book_slug.replace(f"-{format}", ""), format]
            payload = {"book_slug": book_slug, "book_format": format}
    return payload

def __get_book_download_uri(book_id=None):
    if book_id:
        book_info = get_book_info(book_id)
        author_info = get_author_info(book_info["autore"][0])
        download_data = __get_download_info(book_info["slug"])
        book_name = download_data["book_slug"].split(f"-{author_info['slug']}")[0]

        return f"""{DOWNLOAD_URL}/{author_info['slug']}/{download_data['book_slug']}/{book_name}.{download_data['book_format']}""", download_data["book_format"]

def get_book_info(book_id, args={}):
    res = __request(f"/posts/{book_id}", params={**args})
    return res

def get_author_info(author_id, args={}):
    res = __request(f"/autore/{author_id}", params={**args})
    return res

def search(query, args={}):
    res = __request("/search", params={"search": query, **args})
    return res

def __download_book(book_uri=None, book_format=None):
    if book_uri and book_format:
        res = requests.get(book_uri)
        if res.status_code == 200:
            with open(f"output.{book_format}", "wb") as output_file:
                output_file.write(res.content)

def download(book_id):
    download_uri, book_format = __get_book_download_uri(book_id)
    __download_book(download_uri, book_format)