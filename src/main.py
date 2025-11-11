import sys
import time
import asyncio

from datetime import timedelta
from halo import Halo
from transcription import transcribe_text, load_model


async def main():
    try:
        start = time.time()
        model = load_model()
        location = sys.argv[1]
        spinner = Halo(text="Processing...", spinner="dots")
        print(f"Transcribing {location}")
        spinner.start()
        await transcribe_text(location, model)
        spinner.succeed("Done!")
        print("Transcription time: " + str(timedelta(seconds=time.time() - start)))
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
