from hf_datasets import load_librispeech_test_clean
from assemblyai_transcribe_hf import transcribe_all_files_assembly
from openai_whisper_transcribe_hf import transcribe_all_files_whisper
from datetime import datetime

providers = {
    "assemblyai": transcribe_all_files_assembly,
    "openai_whisper": transcribe_all_files_whisper 
}

providers_to_use = [
    "assemblyai",
    "openai_whisper"
]

dataset = load_librispeech_test_clean()

path_list = dataset['path'][:3]
labels_list = dataset['target'][:3]
#important: the audio_files list and labels list need to have the same files in the same order.
def run(providers_list, file_list=[], labels_list=[]):
    for provider in providers_list:
        script = providers[provider]  
        # Get the current timestamp
        now = datetime.now() 
        script(file_list, labels_list, f"{provider}_{now}.csv")

run(providers_to_use, path_list, labels_list)