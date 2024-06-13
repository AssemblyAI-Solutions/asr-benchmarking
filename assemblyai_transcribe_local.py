import assemblyai as aai 
import os 
from dotenv import load_dotenv
import pandas as pd
from calculate_wer import calculate_wer
load_dotenv()
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
config = aai.TranscriptionConfig(language_code="en")
transcriber = aai.Transcriber(config=config)

#test function..
def transcribe_audio(file):
    transcript = transcriber.transcribe(file)
    print(transcript.id)
    print(transcript.text)

def transcribe_all_files_assembly(file_mappings, output_csv_path):

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

    df.to_csv(f"table_csvs/{output_csv_path}", index=False)
    print(df)
    calculate_wer(f"table_csvs/{output_csv_path}", f"table_wers/{output_csv_path}")
    return df