import argparse
import json
import os
import urllib
from bs4 import BeautifulSoup
import requests
import re
import base64
import pathlib
import uuid

DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "Image_Audio"


class Forvo():
    def __init__(self):
        self.selLang = "Japanese"
        self.term = False
        self.langShortCut = "ja"
        self.GOOGLE_SEARCH_URL = "https://forvo.com/word/◳t/#" + self.langShortCut  # ◳r
        self.session = requests.session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                    Gecko/20100101 Firefox/10.0"
            }
        )

    def run(self, term):
        resultList = self.attemptFetchForvoLinks(term)
        return resultList

    def search(self, term):
        query = self.GOOGLE_SEARCH_URL.replace(
            '◳t', re.sub(r'[\/\'".,&*@!#()\[\]\{\}]', '', term))
        return self.forvo_search(query)

    def decodeURL(self, url1, url2, protocol, audiohost, server):
        url2 = protocol + "//" + server + "/player-mp3-highHandler.php?path=" + url2
        url1 = protocol + "//" + audiohost + "/mp3/" + \
            base64.b64decode(url1).decode("utf-8", "strict")
        return url1, url2

    def attemptFetchForvoLinks(self, term):
        urls = self.search(term)
        if len(urls) > 0:
            return urls[0]
        else:
            return False

    def generateURLS(self, results):
        audio = re.findall(r'var pronunciations = \[([\w\W\n]*?)\];', results)
        if not audio:
            return []
        audio = audio[0]
        data = re.findall(
            "Japanese" + r'.*?Pronunciation by (?:<a.*?>)?(\w+).*?class="lang_xx"\>(.*?)\<.*?,.*?,.*?,.*?,\'(.+?)\',.*?,.*?,.*?\'(.+?)\'', audio)
        if data:
            server = re.search(
                r"var _SERVER_HOST=\'(.+?)\';", results).group(1)
            audiohost = re.search(
                r'var _AUDIO_HTTP_HOST=\'(.+?)\';', results).group(1)
            protocol = 'https:'
            urls = []
            for datum in data:
                url1, url2 = self.decodeURL(
                    datum[2], datum[3], protocol, audiohost, server)
                urls.append(url1)
            return urls
        else:
            return []

    def setSearchRegion(self, region):
        self.region = region

    def forvo_search(self, query_gen):
        try:
            html = self.session.get(query_gen).text
        except:
            return []
        results = html

        return self.generateURLS(results)


def get_audio_from_word(col,  word):
    forvo = Forvo()
    url = forvo.run(word)
    if url:
        audio_file_name = pathlib.Path(DATA_DIR).joinpath(
            f'{word}_{uuid.uuid4()}.mp3')
        with open(audio_file_name, mode="wb") as file:
            res = requests.get(url,  headers={
                               'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            file.write(res.content)

        audiofname = col.media.addFile(audio_file_name)
        tag = f'[sound:{audiofname}]'
    else:
        tag = ""
    return tag
