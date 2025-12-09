import hashlib
import os
from datetime import timedelta


def write_transcript(transcription, file_id, config):
    segments = transcription["segments"]
    text = ""
    for segment in segments:
        text += (
            str(timedelta(seconds=segment["start"]))
            + " - "
            + str(timedelta(seconds=segment["end"]))
            + " : "
            + segment["text"].strip()
            + "\n"
        )
    if not os.path.exists(config["transcripts_folder"]) or not os.path.isdir(
        config["transcripts_folder"]
    ):
        os.makedirs(config["transcripts_folder"])
    location = os.path.join(config["transcripts_folder"], str(file_id)) + ".txt"
    with open(location, "w", encoding="utf-8") as f:
        f.write(text)
    return location


def get_file_hash(file_path, config):
    hash_func = hashlib.new(config["HASH_ALGORITHM"])
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def get_extension(file_path):
    return os.path.splitext(file_path)[1]


def read_file(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_note(note, file_id, config):
    if not os.path.exists(config["output_folder"]) or not os.path.isdir(
        config["output_folder"]
    ):
        os.makedirs(config["output_folder"])

    location = os.path.join(config["output_folder"], str(file_id)) + ".txt"
    with open(location, "w", encoding="utf-8") as f:
        f.write(note)
    return location
