import argparse
import pyperclip
from tqdm import tqdm
from anki.collection import Collection
from image import get_pic_from_word
from audio import get_audio_from_word
from dict import lookup
from utils import error_out, deconjugate, get_sentence_from_word, add_to_deck, read_words
import config

col = Collection(config.col_file)

def package_card(word: str):
    deconjugated_word = deconjugate(word)
    sentence = get_sentence_from_word(word)
    if not sentence:
        print("Could not find a sentence for " + word)
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

    add_to_deck(col, sentence, deconjugated_word, audio, image, meanings)

def text_file():
    words = read_words(config.words_file)
    words = list(set(words))
    pbar = tqdm(words)

    for word in pbar:
        res = package_card(word)
        if not res and config.failed_words_file:
            with open(config.failed_words_file, mode="a", encoding="utf-8") as f:
                f.write(word + "\n")
    col.close()

def main():
    parser = argparse.ArgumentParser(
        description='Program to swiftly make anki cards')
    parser.add_argument("--word", action="store_true")  # default
    parser.add_argument("--parsefile", action="store_true")
    args = parser.parse_args()
    if args.parsefile:
        text_file()
    else:
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            package_card(clipboard_text)
        else:
            error_out("No text in clipbopard")

if __name__ == "__main__":
    main()
