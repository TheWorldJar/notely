import os
import yaml

DB_PATH = "./db/note.db"
DB_FOLDER = "./db/"
TRANSCRIBE_DB_NAME = "transcriptions"
NOTES_DB_NAME = "notes"
DEFAULT_TRANSCRIBE_PATH = "./transcribe/"
DEFAULT_OUTPUT_PATH = "./note/"
DEFAULT_TRANSCRIBE_MODEL = "turbo"
DEFAULT_OUTPUT_MODEL = "gemma3:4b"
HASH_ALGORITHM = "sha256"
PROMPT_EXTENSIONS = [".txt", ".md"]


def config_exists():
    return os.path.exists("./config.yaml") and os.path.isfile("config.yaml")


def make_default_config():
    data = {
        "transcripts_folder": DEFAULT_TRANSCRIBE_PATH,
        "output_folder": DEFAULT_OUTPUT_PATH,
        "transcription_model": DEFAULT_TRANSCRIBE_MODEL,
        "output_model": DEFAULT_OUTPUT_MODEL,
    }
    with open("config.yaml", "w") as f:
        yaml.dump(data, f)


def init_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    if (
        "transcription_model" not in config
        or "output_model" not in config
        or "transcripts_folder" not in config
        or "output_folder" not in config
    ):
        print("Invalid configuration. Loading default config.")
        config = {}
        make_default_config()
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
    config["DB_PATH"] = DB_PATH
    config["DB_FOLDER"] = DB_FOLDER
    config["TRANSCRIBE_DB_NAME"] = TRANSCRIBE_DB_NAME
    config["NOTES_DB_NAME"] = NOTES_DB_NAME
    config["HASH_ALGORITHM"] = HASH_ALGORITHM
    config["PROMPT_EXTENSIONS"] = PROMPT_EXTENSIONS
    return config
