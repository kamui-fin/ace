import os
import argparse
import pyperclip
import pathlib
from tqdm import tqdm
from anki import Collection
from lib.utils import utils
from lib.utils.image import get_pic_from_word
from lib.utils.audio import get_audio_from_word
from lib.utils.dict import lookup

HOME = os.path.dirname(__file__)
config = utils.parse_config(os.path.join(HOME, "config.yml"))
col = Collection(config.get("collection"))


def package_card(word):
    deconjugated_word = utils.deconjugate(word)
    sentence = utils.get_sentence_from_word(word)
    if not sentence:
        return False

    meanings = lookup(deconjugated_word)
    if not meanings:
        print("No meanings found for " + deconjugated_word)
        return False
    try:
        image, audio = get_pic_from_word(
            col, word), get_audio_from_word(col, word)
    except:
        print(f"No media found for {deconjugated_word}")
        return False

    utils.add_to_deck(col, sentence, deconjugated_word, audio,
                      image, meanings,  dict(list(config.items())[1:]))
    return True


def text_file():
    words_file = config.get("words_file")
    if not pathlib.Path.exists(words_file):
        print("Invalid words file path")
        return False

    failed_words_file = config.get("failed_words_file")
    words = utils.read_words(words_file)
    words = list(set(words))
    pbar = tqdm(words)

    for word in pbar:
        res = package_card(word)
        if not res and failed_words_file != "":
            with open(failed_words_file, mode="a", encoding="utf-8") as f:
                f.write(word + "\n")
    col.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Program to swiftly make anki cards')
    parser.add_argument("--word", action="store_true")  # default
    parser.add_argument("--parsefile", action="store_true")
    args = parser.parse_args()
    if args.parsefile:
        text_file()
    else:
        package_card(pyperclip.paste())
