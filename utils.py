import os
import subprocess
from pydub import AudioSegment

def get_audio_file_type(file_path):
    try:
        audio = AudioSegment.from_mp3(file_path)
        return True
    except:
        pass
    
    try:
        audio = AudioSegment.from_wav(file_path)
        return True
    except:
        pass

    return False

def load_files(audio_files, text_files):
    paths = []
    for text_file, audio_file in zip(text_files, audio_files):
        updated_audio_file = reformat_file_path(audio_file)
        file_mapping = {
            "audio": updated_audio_file,
            "truth": text_file
        }
        paths.append(file_mapping)
    # for file in text_files:
    #     split_path = file.split(".txt")[0]
    #     audio_path = f"{audio_file_dir}/{split_path}"
    #     file_mapping = {
    #         "audio": audio_path,
    #         "truth": f"{text_file_dir}/{file}"
    #     }
    #     paths.append(file_mapping)
    return paths

def load_local_files(audio_file_dir, truth_file_dir):
    # Get list of files in the directories
    audio_files = os.listdir(audio_file_dir)
    truth_files = os.listdir(truth_file_dir)

    # Create a mapping of file names to paths (without extensions)
    audio_map = {os.path.splitext(f)[0]: os.path.join(audio_file_dir, f) for f in audio_files}
    truth_map = {os.path.splitext(f)[0]: os.path.join(truth_file_dir, f) for f in truth_files}

    # Create the output list
    output_list = []
    for key in audio_map:
        if key in truth_map:
            output_list.append({
                "audio": audio_map[key], 
                "truth": truth_map[key]
            })

    return output_list

#needed at times for whisper
def convert_flac_to_mp3(flac_path):
    """Converts a FLAC file to MP3 format and saves it in the 'mp3s' folder."""
    # Ensure the 'mp3s' directory exists
    mp3_dir = "mp3s"
    os.makedirs(mp3_dir, exist_ok=True)
    
    # Construct the MP3 path from the FLAC path
    mp3_path = os.path.join(mp3_dir, os.path.basename(flac_path).replace('.mp3', '.flac'))
    
    # Convert and save the MP3
    audio = AudioSegment.from_file(flac_path, "flac")
    audio.export(mp3_path, format="mp3")
    
    return mp3_path

def reencode_with_ffmpeg(input_path, output_path):
    try:
        # Run ffmpeg command to re-encode the MP3 file
        result = subprocess.run(['ffmpeg', '-i', input_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', output_path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Successfully re-encoded {input_path} to {output_path}")
        else:
            print(f"Failed to re-encode {input_path}: {result.stderr.decode()}")
    except Exception as e:
        print(f"Exception occurred while re-encoding {input_path}: {e}")

def reformat_file_path(wrong_path):
    base_dir = "/Users/samflamini/.cache/huggingface/datasets/downloads/extracted" #note - you should replace this with your path to the hugging face directory in .cache
    unique_id = wrong_path.split('/')[8]
    file_name = os.path.basename(wrong_path)
    
    # Extract the first two IDs from the file name
    first_id, second_id, _ = file_name.split('-')
    
    # Construct the correct path
    correct_path = os.path.join(base_dir, unique_id, "LibriSpeech", "test-clean", first_id, second_id, file_name)
    
    return correct_path