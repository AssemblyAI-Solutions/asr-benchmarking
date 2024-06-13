from assemblyai_transcribe_local import transcribe_all_files_assembly
from openai_whisper_transcribe_local import transcribe_all_files_whisper
from utils import load_local_files
from datetime import datetime

providers = {
    "assemblyai": transcribe_all_files_assembly,
    "openai_whisper": transcribe_all_files_whisper 
}

providers_to_use = [
    "assemblyai",
    "openai_whisper"
]

audio_files_dir = "audio"
truth_files_dir = "truth"
dataset = load_local_files(audio_files_dir, truth_files_dir)

def run(providers_list, file_mappings):
    for provider in providers_list:
        script = providers[provider]  
        now = datetime.now() 
        script(file_mappings, f"{provider}_{now}.csv")

run(providers_to_use, dataset)