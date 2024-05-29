import assemblyai as aai 
import json
import sys
import os 
import pandas as pd
import time
import ast
from utils import load_files
aai.settings.api_key = "KEY"
config = aai.TranscriptionConfig(language_code="de")
transcriber = aai.Transcriber(config=config)

#test function..
def transcribe_audio(file):
    transcript = transcriber.transcribe(file)
    print(transcript.id)
    print(transcript.text)

def transcribe_all_files(audio_folder, labels_folder, output_csv_path):

    file_mappings = load_files(audio_folder, labels_folder)

    audio_paths = []
    truth_text = []
    transcript_outputs = []

    for file in file_mappings:
        transcript = transcriber.transcribe(file['audio'])
        print(transcript.text)

        with open(file["truth"], "r") as audio_file:
            truth_str = audio_file.read()
        
        truth_text.append(truth_str)
        audio_paths.append(file['audio'])
        transcript_outputs.append(transcript.text)

    df = pd.DataFrame({
        "audio_path": audio_paths,
        "target": truth_text,
        "prediction": transcript_outputs
    })

    df.to_csv(f"{output_csv_path}.csv", index=False)
    print(df)
    return df