import json
import pathlib
import glob
import os
from lib.utils.utils import all_kana, isAllHiragana, katakana_to_hiragana, all_none

FALLBACK_DIR = pathlib.Path(
    __file__).parent.parent.parent / "data" / "dict" / "fallback"
PRIORITY_DIR = pathlib.Path(
    __file__).parent.parent.parent / "data" / "dict" / "priority"


fallback_dict = glob.glob(str(FALLBACK_DIR / "*") + os.path.sep)
priority_dict = glob.glob(str(PRIORITY_DIR / "*") + os.path.sep)

if not priority_dict:
    print("You have no yomichan dictionaries in the dict/ folder!")
    quit()

if fallback_dict:
    fallback_dict = fallback_dict[0]


class Dictionary(object):
    def __init__(self, path):
        self.path = path
        self.banks = glob.glob(str(pathlib.Path(self.path) / "ter*"))
        self._dict = self.load_dict()

    def load_dict(self):
        entrs = []
        for bank in self.banks:
            with open(bank, encoding="utf-8") as f:
                obj = json.load(f)
                entrs.extend(obj)
        return entrs

    def lookup(self, word):
        allKana = all_kana(word)
        if allKana:
            if not isAllHiragana(word):
                word = katakana_to_hiragana(word)

        for ent in self._dict:
            loc = 1 if allKana else 0
            res = ent[loc]
            if res == word:
                return (ent[5][0], ent[1])


priority_dictonaries = [Dictionary(d) for d in priority_dict]
if fallback_dict:
    fallback_dictionary = Dictionary(fallback_dict)


def lookup(word):
    meanings = []
    for pr in priority_dictonaries:
        try:
            meaning_res, reading = pr.lookup(word)
        except:
            continue
        meanings.append(meaning_res)
    if fallback_dictionary:
        if all_none(meanings):
            try:
                meaning_res, reading = fallback_dictionary.lookup(word)
            except:
                pass
            else:
                meanings.append(f"{word}【{reading}】\n{meaning_res}")
    return [x.replace("\n", "<br>") for x in meanings if x]
