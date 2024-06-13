import assemblyai as aai 
import os
from dotenv import load_dotenv
import pandas as pd
from calculate_wer import calculate_wer
from utils import load_files
load_dotenv()
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

config = aai.TranscriptionConfig(language_code="en")
transcriber = aai.Transcriber(config=config)


#test function..
def transcribe_audio(file):
    transcript = transcriber.transcribe(file)
    print(transcript.id)
    print(transcript.text)

def transcribe_all_files_assembly(audio_files, labels_list, output_csv_path):

    file_mappings = load_files(audio_files, labels_list)
    print(file_mappings)
    audio_paths = []
    truth_text = []
    transcript_outputs = []

    for file in file_mappings:
        transcript = transcriber.transcribe(file['audio'])
        print(transcript.text)

        truth_str = file['truth']
        
        truth_text.append(truth_str)
        audio_paths.append(file['audio'])
        transcript_outputs.append(transcript.text)

    df = pd.DataFrame({
        "audio_path": audio_paths,
        "target": truth_text,
        "prediction": transcript_outputs
    })

    df.to_csv(f"table_csvs/{output_csv_path}", index=False)
    print(df)
    calculate_wer(f"table_csvs/{output_csv_path}", f"table_wers/{output_csv_path}")
    return df