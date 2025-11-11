from datetime import timedelta


def write_transcript(transcription):
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

    with open("./transcript.txt", "w") as f:
        f.write(text)
