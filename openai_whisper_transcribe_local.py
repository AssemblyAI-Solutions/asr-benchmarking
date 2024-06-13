import os 
import time
import pandas as pd
from calculate_wer import calculate_wer
from utils import convert_flac_to_mp3, get_audio_file_type
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_key)

def transcribe_audio(mp3_path):
    
    """Transcribes the given MP3 file using OpenAI's transcription API."""
    with open(mp3_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            prompt="Context: voicemail order from a restaurant to their supplier.",
            response_format="text",
            language="en"
        )

    return transcript

def transcribe_all_files_whisper(file_mappings, output_csv_path):

    audio_paths = []
    truth_text = []
    transcript_outputs = []
    failed_files = []
    
    for file in file_mappings:
        try:
            if get_audio_file_type(file['audio']) == 'flac':
                file_path = convert_flac_to_mp3(file['audio'])
            else:
                file_path = file['audio']
            with open(file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1",
                    # prompt="Sample whisper context here.",
                    response_format="text",
                    language="en"
                )
        except Exception as e:
            print(f"Error transcribing {file['audio']}: {e}")
            transcript = "transcription failed"
            failed_files.append(file['audio'])

        audio_paths.append(file['audio'])

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

    df.to_csv(f"table_csvs/{output_csv_path}", index=False)
    print(df)
    calculate_wer(f"table_csvs/{output_csv_path}", f"table_wers/{output_csv_path}")

    # Log the failed files
    with open("failed_files.log", "w") as log_file:
        for failed_file in failed_files:
            log_file.write(f"{failed_file}\n")

    return df