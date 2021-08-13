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

# def search_author(author_id=None, args={}):
#     if author_id:
#         res = request(f"/editore/{author_id}", params={**args})
#         return res

# https://dwnlg.link/book-n/giulio-cavalli/nuovissimo-testamento-giulio-cavalli/nuovissimo-testamento.epub

def get_book_info(book_id=None, args={}):
    if book_id:
        res = request(f"/posts/{book_id}", params={**args})
        return res

def get_author_info(author_id=None, args={}):
    if author_id:
        res = request(f"/autore/{author_id}", params={**args})
        return res

def __get_download_url_data(book_slug=None):
    download_data = dict()
    print("here")
    for format in ["epub", "mobi", "pdf"]:
        if format in book_slug:
            book_slug, format = [book_slug.replace(f"-{format}", ""), format]
    return {
        "book_slug": book_slug,
        "book_format": format
    }
    # return [(book_slug.replace(f"-{format}", ""), format) for format in ["epub", "mobi", "pdf"] if format in book_slug]


def get_book_download_uri(book_id=None):
    if book_id:
        book_info = get_book_info(book_id)
        author_info = get_author_info(book_info["autore"][0])

        book_slug = book_info["slug"]
        author_slug = author_info["slug"]

        # print(updated_book_slug)
        download_data = __get_download_url_data(book_slug)
        # test = str(book_slug.split(f"-{author_slug}")[0]) + ".epub"
        book_name = download_data["book_slug"].split(f"-{author_slug}")[0]
        return f"https://dwnlg.link/book-n/{author_slug}/{download_data['book_slug']}/{book_name}.{download_data['book_format']}"

def download_book(book_uri=None):
    if book_uri:
        res = requests.get(book_uri)
        if res.status_code == 200:
            # TODO: move mapping somewhere else, not here
            mapping = {
                "application/pdf": ".pdf",
            }
            # print(res.headers["Content-Type"])
            # Prendere estensione in modo automaticato da header di risposta
            with open(f"output{mapping[res.headers['Content-Type']]}", "wb") as output_file:
                output_file.write(res.content)
            print('done')

books = search("viaggiare nello spaziotempo")
book_id = books[-1]["id"]
d = get_book_download_uri(book_id)
download_book(d)
