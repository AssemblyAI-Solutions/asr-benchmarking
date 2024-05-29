import json
import sys
import os 
import time
import pandas as pd
from utils import load_files
import openai
from openai import OpenAI

openai_key = "KEY"
client = OpenAI(api_key=openai_key)

def transcribe_audio(mp3_path):
    """Transcribes the given MP3 file using OpenAI's transcription API."""
    with open(mp3_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            prompt="Context: voicemail order from a restaurant to their supplier.",
            response_format="text",
            language="de"
        )

    return transcript

def transcribe_all_files(audio_folder, labels_folder, output_csv_path):

    file_mappings = load_files(audio_folder, labels_folder)

    audio_paths = []
    truth_text = []
    transcript_outputs = []
    failed_files = []

    for file in file_mappings:
        try:
            with open(file['audio'], "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    prompt="Context: voicemail order from a restaurant to their supplier.",
                    response_format="text",
                    language="de"
                )
        except Exception as e:
            print(f"Error transcribing {file['audio']}: {e}")
            transcript = "transcription failed"
            failed_files.append(file['audio'])

        audio_paths.append(file["audio"])

        try:
            with open(file['truth'], "r") as truth_file:
                truth_str = truth_file.read()
        except Exception as e:
            print(f"Error reading truth file {file['truth']}: {e}")
            truth_str = "truth file read failed"

        truth_text.append(truth_str)
        print(transcript)
        transcript_outputs.append(transcript)
        time.sleep(3)

    df = pd.DataFrame({
        "audio_path": audio_paths,
        "target": truth_text,
        "prediction": transcript_outputs
    })

    df.to_csv(f"{output_csv_path}.csv", index=False)
    print(df)

    # Log the failed files
    with open("failed_files.log", "w") as log_file:
        for failed_file in failed_files:
            log_file.write(f"{failed_file}\n")

    return df