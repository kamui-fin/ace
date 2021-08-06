import pathlib 
import os
import yaml
from typing import Dict

HOME = os.path.dirname(__file__)
DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "image_audio"
FALLBACK_DIR = pathlib.Path(__file__).parent / "data" / "dict" / "fallback"
PRIORITY_DIR = pathlib.Path(__file__).parent / "data" / "dict" / "priority"

def parse_config(filename: str) -> Dict[str, str]:
    with open(filename, "r") as f:
        try:
            obj = yaml.safe_load(f)
            return obj["anki"]
        except yaml.YAMLError as exc:
            print("Error reading config file!\n", exc)
            return {}
