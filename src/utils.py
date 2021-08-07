import pathlib
import requests
from bs4 import BeautifulSoup as BS
from anki.collection import Collection
from typing import List, Any
import config

def read_words(filename: str) -> List[str]:
    return [x.strip() for x in pathlib.Path(filename).read_text(encoding="utf-8").split("\n") if x]

def get_sentence_from_word(word: str) -> str:
    res = requests.get(f"http://yourei.jp/{word}")
    soup = BS(res.text, "lxml")
    for rt in soup.findAll("rt"):
        rt.decompose() 
    sentence = soup.select_one(".list-group-item.sentence")
    if not sentence:
        return ""
    return sentence.select_one(".the-sentence").get_text()

def add_to_deck(col: Collection, sentence: str, word: str, audio: str, image: str, meanings: List[str]):
    deckId = col.decks.id(config.deck_name)
    col.decks.select(deckId)
    basic_model = col.models.by_name(config.note_type)
    basic_model['did'] = deckId
    col.models.save(basic_model)
    col.models.set_current(basic_model)

    card = col.newNote()

    card[config.sentence_field] = sentence
    card[config.word_field] = word
    card[config.image_field] = image
    card[config.audio_field] = audio
    card[config.meaning_field] = "<br><br>".join(meanings)

    col.addNote(card)
    col.save()

def deconjugate(word: str) -> str:
    res = requests.get(
        f"https://jisho.org/api/v1/search/words?keyword={word}").json()["data"]
    if res:
        jp_data = res[0]["japanese"]
        if jp_data:
            return jp_data[0]["reading"]
    return word

def all_kana(word: str) -> bool:
    is_all_kana = all([(x > '\u3040' and x < '\u309F')
                       or (x > '\u30A0' and x < '\u30FF') for x in word])
    return is_all_kana

def all_none(array: List[Any]) -> bool:
    return all([x is None for x in array])

def katakana_to_hiragana(word: str) -> str:
    result = ''
    for character in word:
        code = ord(character)
        if ord('ァ') <= code <= ord('ヶ'):
            result += chr(code - ord('ァ') + ord('ぁ'))
        else:
            result += character
    return result

def is_all_hiragana(word: str) -> bool:
    return all([is_hiragana(x) for x in word])

def is_hiragana(c: str) -> bool:
    return (('\u3041' <= c) and (c <= '\u309e'))

def error_out(msg: str, status = 1):
    print(msg)
    exit(status)
