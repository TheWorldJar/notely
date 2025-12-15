import os

from src.tome.config import config_exists, make_default_config, init_config
from src.tome.database import (
    create_db,
    setup_db,
    insert_row,
    get_transcription_by_hash_and_model,
)


def test_setup_db():
    if not config_exists():
        make_default_config()
    config = init_config()

    if os.path.exists(config["DB_PATH"]):
        os.remove(config["DB_PATH"])

    cur, conn = create_db(config)
    assert cur.rowcount == -1

    setup_db(cur, conn, config)
    assert cur.rowcount == -1
    conn.close()


def test_double_setup_db():
    if not config_exists():
        make_default_config()
    config = init_config()

    if os.path.exists(config["DB_PATH"]):
        os.remove(config["DB_PATH"])

    cur, conn = create_db(config)
    assert cur.rowcount == -1

    setup_db(cur, conn, config)
    assert cur.rowcount == -1
    setup_db(cur, conn, config)
    assert cur.rowcount == -1
    conn.close()


def test_db_entry():
    if not config_exists():
        make_default_config()
    config = init_config()

    if os.path.exists(config["DB_PATH"]):
        os.remove(config["DB_PATH"])

    cur, conn = create_db(config)
    assert cur.rowcount == -1

    setup_db(cur, conn, config)
    assert cur.rowcount == -1

    test_row = {
        "audio_file_hash": "101-test-101-audio",
        "transcription_location": "./src/tests/transcriptions/test_transcription.txt",
        "transcription_hash": "101-test-101-transcription",
    }

    insert_row(
        cur,
        conn,
        config["TRANSCRIBE_DB_NAME"],
        test_row,
        config,
    )

    row = get_transcription_by_hash_and_model(cur, "101-test-101-audio", config)
    assert row is not None
    assert test_row["audio_file_hash"] in row["audio_file_hash"]
    assert test_row["transcription_location"] in row["transcription_location"]
    assert test_row["transcription_hash"] in row["transcription_hash"]

    conn.close()


def test_duplicate_db_entry():
    if not config_exists():
        make_default_config()
    config = init_config()

    if os.path.exists(config["DB_PATH"]):
        os.remove(config["DB_PATH"])

    cur, conn = create_db(config)
    assert cur.rowcount == -1

    setup_db(cur, conn, config)
    assert cur.rowcount == -1

    test_row = {
        "audio_file_hash": "101-test-101-audio",
        "transcription_location": "./src/tests/transcriptions/test_transcription.txt",
        "transcription_hash": "101-test-101-transcription",
    }

    insert_row(
        cur,
        conn,
        config["TRANSCRIBE_DB_NAME"],
        test_row,
        config,
    )

    row = get_transcription_by_hash_and_model(cur, "101-test-101-audio", config)
    assert row is not None
    assert test_row["audio_file_hash"] in row["audio_file_hash"]
    assert test_row["transcription_location"] in row["transcription_location"]
    assert test_row["transcription_hash"] in row["transcription_hash"]

    test_row = {
        "audio_file_hash": "101-test-101-audio",
        "transcription_location": "./src/tests/transcriptions/test_transcription.txt",
        "transcription_hash": "101-test-101-transcription",
    }

    insert_row(
        cur,
        conn,
        config["TRANSCRIBE_DB_NAME"],
        test_row,
        config,
    )

    row = get_transcription_by_hash_and_model(cur, "101-test-101-audio", config)
    assert row is not None
    assert test_row["audio_file_hash"] in row["audio_file_hash"]
    assert test_row["transcription_location"] in row["transcription_location"]
    assert test_row["transcription_hash"] in row["transcription_hash"]

    test_row2 = {
        "audio_file_hash": "101-test-101-audio",
        "transcription_location": "./src/tests/transcriptions/test2_transcription2.md",
        "transcription_hash": "202-test-202-transcription2",
    }
    insert_row(
        cur,
        conn,
        config["TRANSCRIBE_DB_NAME"],
        test_row2,
        config,
    )

    row = get_transcription_by_hash_and_model(cur, "101-test-101-audio", config)
    assert row is not None
    assert test_row["audio_file_hash"] in row["audio_file_hash"]
    assert test_row["transcription_location"] in row["transcription_location"]
    assert test_row["transcription_hash"] in row["transcription_hash"]

    conn.close()
