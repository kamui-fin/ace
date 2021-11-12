# ACE (Anime Cards Exporter)

**This old version of ace has been deprecated and will no longer be supported. Please consider using the [rust rewrite](https://github.com/kamui-fin/ace-rs) instead**

This is a script to make [anime cards]("https://www.animecards.site") on the fly with a single hotkey on linux. It takes a sentence from [yourei](https://www.yourei.jp), an image from [google images](https://www.google.com/imghp?hl=ja), an audio recording from [forvo](https://www.forvo.com), and finally, a couple meanings from yomichan dictionaries of your choice, which is all packaged into 1 card and sent directly to your anki.

## Installation

```bash
$ git clone https://github.com/kamui-fin/ace.git
$ cd ace
$ pip install -r requirements.txt
$ mkdir -p data/dict/{fallback,priority}
$ mkdir -p data/image_audio
```

Next, fill out the missing blanks in [config.yml](config.yml). All options are documented.
Here's an example config file:

```yml
collection: "/home/username/.local/share/Anki2/profile1/collection.anki2"
deck: "My Deck"
note_type: "My Notetype"
word_field: "Word"
sentence_field: "Expression"
image_field: "Picture"
audio_field: "Audio"
meaning_field: "Meaning"
words_file: "/home/username/words.txt"
failed_words_file: "/home/username/failed.txt"
```

Notes:

1. You need to type in the fields _exactly_ as it is in anki or else it will not work.
2. The collection is your profile's database
3. You have to close anki before running this script

Now for the dictionary setup. There's 2 folders in the `dict` folder, fallback and priority. Priority is the folder where you will place your dictionaries that you want to search first. The dictionaries located in the fallback folder will be used if the program couldn't find any entries in your priority dicts.

Make sure you unzip the yomichan dictionaries to its own folder and move them to the appropriate directories inside `dict`. Here is an example of how it could look:

```
dict/
├── fallback/
│  └── jmdict_english/
└── priority
   ├── 三省堂　スーパー大辞林/
   └── 新明解国語辞典第五版v3/
```

## Options

There are 2 options to use when running this script, `--word` and `--parsefile`.

1. The `word` flag (which is the default) is used to make an anki card from the word in your clipboard.
2. The `parsefile` flag is used to batch export cards from a file with the list of words, where each word is on its own line.

### Hotkey

With all this setup, you can easily create a keybind for creating the card from the word in your clipboard. Most desktop environments and window managers have a place for keybinds in their system settings GUI or config file. Pick a keybind and set it to run the following command:

```bash
python src/main.py --parsefile
```

Note that you need to adjust to the path of `main.py`, depending on where you downloaded the script.
