import whisper

from fileactions import write_transcript


def load_model():
    model = whisper.load_model("medium.en")
    return model


async def transcribe_text(location, model):
    options = {
        "language": "en",
        "task": "transcribe",
        "beam_size": 5,
        "best_of": 5,
        "fp16": False,
    }
    result = model.transcribe(location, **options)
    write_transcript(result)
