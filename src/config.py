import pathlib 
import os
import yaml
import glob
from typing import Dict
from utils import error_out

HOME = pathlib.Path(__file__).parent.parent
DATA_DIR = HOME / "data" / "image_audio"
FALLBACK_DIR = HOME / "data" / "dict" / "fallback"
PRIORITY_DIR = HOME / "data" / "dict" / "priority"

def parse_config(filename: pathlib.Path) -> Dict[str, str]:
    with open(filename, "r") as f:
        obj = yaml.safe_load(f)
        return obj["anki"]

try:
    config = parse_config(HOME / "config.yml")
except yaml.YAMLError as exc:
    error_out("Could not read config file")

words_file = config.get("words_file")
failed_words_file = config.get("failed_words_file")
col_file = config.get("collection")
deck_name = config.get("deck")
note_type = config.get("note_type")
sentence_field = config.get("sentence_field")
word_field = config.get("word_field")
image_field = config.get("image_field")
audio_field = config.get("audio_field")
meaning_field = config.get("meaning_field")

if not col_file:
    error_out("Must fill in collection.anki2 path")

if not all([deck_name, note_type, sentence_field, word_field, image_field, audio_field, meaning_field]):
    error_out("Must fill out all deck metadata")

if not words_file or not pathlib.Path(words_file).exists():
    error_out("Invalid words file path")

fallback_dict = glob.glob(str(FALLBACK_DIR / "*") + os.path.sep)
priority_dict = glob.glob(str(PRIORITY_DIR / "*") + os.path.sep)

if not priority_dict:
    error_out("You have no yomichan dictionaries in the dict/ folder!")

if fallback_dict:
    fallback_dict = fallback_dict[0]
