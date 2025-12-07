import os
import sys
import time
from datetime import timedelta

from halo import Halo

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.const import DB_PATH, PROMPT_EXTENSIONS
from src.database import create_db, setup_db
from src.execution import get_ollama_response
from src.fileactions import get_extension
from src.transcription import transcribe_text, load_model


# TODO: Test with updated PyTorch
# TODO: Move some consts to a config file
def main():
    try:
        spinner = Halo(text="This may take a while...", spinner="bouncingBall")

        db_con = create_db(DB_PATH)
        setup_db(db_con)

        if len(sys.argv) != 3:
            raise Exception("Usage: python main.py {audio_file} {prompt_file}")
        audio_file_path = sys.argv[1]
        prompt_file_path = sys.argv[2]
        prompt_extension = get_extension(prompt_file_path)
        if prompt_extension not in PROMPT_EXTENSIONS:
            raise Exception(
                f"Invalid prompt file extension! Got {prompt_extension}. Valid extensions are: {PROMPT_EXTENSIONS}"
            )
        print(f"Transcribing: {audio_file_path}")

        start = time.time()
        spinner.start()
        model = load_model()
        transcription_file_path, file_id = transcribe_text(
            audio_file_path, model, db_con
        )
        spinner.succeed("Done!")
        print("Transcription time: " + str(timedelta(seconds=time.time() - start)))

        print(f"Executing prompt: {prompt_file_path}")
        start = time.time()
        spinner.start()
        note_location = get_ollama_response(
            db_con, transcription_file_path, prompt_file_path, file_id
        )
        spinner.succeed("Done!")
        print("Execution time: " + str(timedelta(seconds=time.time() - start)))
        print(f"All done! You note is available at: {note_location}")
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
