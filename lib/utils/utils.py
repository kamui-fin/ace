import pathlib
from bs4 import BeautifulSoup as BS
import requests
from pprint import pprint
import yaml


def read_words(filename):
    return [x.strip() for x in pathlib.Path(filename).read_text(encoding="utf-8").split("\n") if x]


def get_sentence_from_word(word):
    res = requests.get(f"http://yourei.jp/{word}")
    soup = BS(res.text, "lxml")
    for rt in soup.findAll("rt"):
        rt.decompose()
    sentence = soup.select_one(".list-group-item.sentence")
    if not sentence:
        print("Could not find a sentence for " + word)
        return ""
    return sentence.select_one(".the-sentence").get_text()


def add_to_deck(col, sentence, word, audio, image, meanings, info):
    deckId = col.decks.id(info.get("deck"))
    col.decks.select(deckId)
    basic_model = col.models.byName(info.get("note_type"))
    basic_model['did'] = deckId
    col.models.save(basic_model)
    col.models.setCurrent(basic_model)

    senCard = col.newNote()
    senCard[info.get("sentence_field")] = sentence
    senCard[info.get("word_field")] = word
    senCard[info.get("image_field")] = image
    senCard[info.get("audio_field")] = audio
    senCard[info.get("meaning_field")] = "<br><br>".join(meanings)

    col.addNote(senCard)
    col.save()


def parse_config(filename):
    with open(filename, "r") as f:
        try:
            obj = yaml.safe_load(f)
            return obj["anki"]
        except yaml.YAMLError as exc:
            print("Error reading config file!\n", exc)


def deconjugate(word):
    res = requests.get(
        f"https://jisho.org/api/v1/search/words?keyword={word}").json()["data"]
    if res:
        word_deconj = res[0]["slug"]
        return word_deconj
    else:
        return word


def all_kana(word):
    is_all_kana = all([(x > '\u3040' and x < '\u309F')
                       or (x > '\u30A0' and x < '\u30FF') for x in word])
    return is_all_kana


def all_none(array):
    return all([x is None for x in array])


def katakana_to_hiragana(string):
    result = ''
    for character in string:
        code = ord(character)
        if ord('ァ') <= code <= ord('ヶ'):
            result += chr(code - ord('ァ') + ord('ぁ'))
        else:
            result += character
    return result


def isAllHiragana(word):
    return all([isHiragana(x) for x in word])


def isHiragana(c):
    return (('\u3041' <= c) and (c <= '\u309e'))
