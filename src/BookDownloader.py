from config import *
from requests import Session

class BookDownloader:

  def __init__(self):
    self.s = Session()

  def __request(self, endpoint="/", params={}):
    res = self.s.get(f"{BASE_URL}{endpoint}", params=params)
    return res.json()

  def __get_download_info(self, book_slug):
    payload = {}
    for format in ["epub", "mobi", "pdf"]:
        if format in book_slug:
            book_slug, format = [book_slug.replace(f"-{format}", ""), format]
            payload = {"book_slug": book_slug, "book_format": format}
    return payload

  def __get_book_download_uri(self, book_id=None):
    if book_id:
      book_info = self.get_book_info(book_id)
      author_info = self.get_author_info(book_info["autore"][0])
      download_data = self.__get_download_info(book_info["slug"])
      book_name = download_data["book_slug"].split(f"-{author_info['slug']}")[0]

      return f"""{DOWNLOAD_URL}/{author_info['slug']}/{download_data['book_slug']}/{book_name}.{download_data['book_format']}""", download_data["book_format"]

  def get_book_info(self, book_id, args={}):
      res = self.__request(f"/posts/{book_id}", params={**args})
      return res

  def get_author_info(self, author_id, args={}):
      res = self.__request(f"/autore/{author_id}", params={**args})
      return res

  def search(self, query, args={}):
    res = self.__request("/search", params={"search": query, **args})
    return res

  def __download_book(self, book_uri=None, book_format=None):
    if book_uri and book_format:
      res = self.s.get(book_uri)
      if res.status_code == 200:
          with open(f"output.{book_format}", "wb") as output_file:
              output_file.write(res.content)

  def download(self, book_id):
    download_uri, book_format = self.__get_book_download_uri(book_id)
    self.__download_book(download_uri, book_format)