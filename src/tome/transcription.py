import os
import uuid

import whisper

from .database import get_transcription_by_hash_and_model, insert_row
from .fileactions import write_transcript, get_file_hash


def load_model(config):
    return whisper.load_model(config["transcription_model"])


def transcribe_text(audio_location, model, cur, conn, config):
    options = {
        "task": "transcribe",
        "beam_size": 5,
        "best_of": 5,
        "fp16": False,
    }

    audio_hash = get_file_hash(audio_location, config)
    transcribe_row = get_transcription_by_hash_and_model(cur, audio_hash, config)
    if transcribe_row is None or not os.path.exists(
        transcribe_row["transcription_location"]
    ):
        file_id = uuid.uuid4()
        transcription_location = write_transcript(
            model.transcribe(audio_location, **options),
            file_id,
            config,
        )
        transcription_hash = get_file_hash(transcription_location, config)
        insert_row(
            cur,
            conn,
            config["TRANSCRIBE_DB_NAME"],
            {
                "audio_file_hash": audio_hash,
                "transcription_location": transcription_location,
                "transcription_hash": transcription_hash,
            },
            config,
        )
        print(f"Finished transcribing {transcription_location}!")
    else:
        transcription_location = transcribe_row["transcription_location"]
        file_id = os.path.splitext(os.path.basename(transcription_location))[0]
        print(f"Found transcription location: {transcription_location}!")

    return transcription_location, file_id
