import os
import subprocess
from pydub import AudioSegment

def load_files(text_file_dir, audio_file_dir):
    text_files = os.listdir(text_file_dir)
    paths = []
    for file in text_files:
        split_path = file.split(".txt")[0]
        audio_path = f"{audio_file_dir}/{split_path}"
        file_mapping = {
            "audio": audio_path,
            "truth": f"{text_file_dir}/{file}"
        }
        paths.append(file_mapping)
    return paths

#needed at times for whisper
def convert_flac_to_mp3(flac_path):
    """Converts a FLAC file to MP3 format and saves it in the 'mp3s' folder."""
    # Ensure the 'mp3s' directory exists
    mp3_dir = "mp3s"
    os.makedirs(mp3_dir, exist_ok=True)
    
    # Construct the MP3 path from the FLAC path
    mp3_path = os.path.join(mp3_dir, os.path.basename(flac_path).replace('.mp3', '.flac'))
    
    # Convert and save the MP3
    audio = AudioSegment.from_file(flac_path, "mp3")
    audio.export(mp3_path, format="flac")
    
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