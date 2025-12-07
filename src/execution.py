import ollama
from ollama import GenerateResponse

from src.const import NOTE_MODEL, NOTES_DB_NAME
from src.database import get_note_by_hash, insert_row, update_note
from src.fileactions import read_transcript, get_file_hash, write_note


def get_ollama_response(cur, transcription_location, prompt, file_id):
    transcription_content = read_transcript(transcription_location)
    transcription_hash = get_file_hash(transcription_content)

    res: GenerateResponse = ollama.generate(
        model=NOTE_MODEL, prompt=f"{prompt}\n\nFILE CONTENT:\n{transcription_content}"
    )

    note_location = write_note(res.response, file_id)
    note_hash = get_file_hash(note_location)

    note_row = get_note_by_hash(cur, transcription_hash)
    if note_row is None:
        insert_row(
            cur,
            NOTES_DB_NAME,
            {
                "transcription_location": transcription_location,
                "transcription_hash": transcription_hash,
                "note_location": note_location,
                "note_hash": note_hash,
            },
        )
    else:
        update_note(
            cur,
            transcription_hash,
            {
                "transcription_location": transcription_location,
                "note_location": note_location,
                "note_hash": note_hash,
            },
        )
    return note_location
