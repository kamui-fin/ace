import argparse
import json
import os
import urllib
from bs4 import BeautifulSoup
import requests
import time
import re
import uuid
import pathlib
from urllib.parse import urlparse

DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "Image_Audio"


class Google():

    def __init__(self):
        self.GOOGLE_SEARCH_URL = "https://www.google.com/search"
        self.term = False
        self.initSession()

    def initSession(self):
        self.session = requests.session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                    Gecko/20100101 Firefox/10.0"
            }
        )

    def search(self, keyword, maximum):
        query = self.query_gen(keyword)

        return self.image_search(query, maximum)

    def query_gen(self, keyword):
        params = urllib.parse.urlencode(
            {"q": keyword, "tbm": "isch"}
        )
        url = 'https://www.google.co.jp/search'
        yield url + "?" + params

    def getResultsFromRawHtml(self, html):
        pattern = r"AF_initDataCallback[\s\S]+AF_initDataCallback\({key: '[\s\S]+?',[\s\S]+?data:(\[[\s\S]+\])[\s\S]+?<\/script><script id="
        matches = re.findall(pattern, html)
        results = []
        try:
            if len(matches) > 0:
                decoded = json.loads(matches[0])[31][0][12][2]
                for d in decoded:
                    d1 = d[1]
                    if d1:
                        results.append(str(d1[3][0]))   
            return results
        except:
            return []

    def image_search(self, query_gen, maximum):
        results = []
        total = 0
        finished = False
        while True:
            try:
                count = 0
                while not finished:
                    count+= 1
                    hr = self.session.get(next(query_gen)+ '&ijn=0&cr=' + "countryJP")
                    html = hr.text
                    if not html and not '<!doctype html>' in html:
                        if count > 5:
                            finished = True
                            break
                        self.initSession()
                        time.sleep(.1)
                    else:
                        finished = True
                        break
            except:
                return False
            results = self.getResultsFromRawHtml(html)
            if len(results) == 0:
                soup = BeautifulSoup(html, "html.parser")
                elements = soup.select(".rg_meta.notranslate")
                jsons = [json.loads(e.get_text()) for e in elements]

                image_url_list = [js["ou"] for js in jsons]
                if not len(image_url_list):
                    break
                elif len(image_url_list) > maximum - total:
                    results += image_url_list[: maximum - total]
                    break
                else:
                    results += image_url_list
                    total += len(image_url_list)
            else:
                break
        return results


def search(target):
    google = Google()
    result = google.search(target, maximum=2)
    return result[0] if result else ""


def get_pic_from_word(col, word):
    url = search(word)
    if url:
        urlparsed = urlparse(url)
        root, ext = os.path.splitext(urlparsed.path)
        pic_filename = pathlib.Path(DATA_DIR).joinpath(
            f'{word}_{uuid.uuid4()}{ext}')
        with open(pic_filename, mode="wb") as file:
            res = requests.get(url,  headers={
                               'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            file.write(res.content)

        picfname = col.media.addFile(pic_filename)
        tag = f'<img src="{picfname}">'
    else:
        tag = ""
    return tag

