## Open Source ASR Benchmarking

1) Run `pip install -r requirements.txt`

2) Add audio files to `/audios` and add your human transcript labels to `/truth`

3) Add your respective API keys (depending on the vendors you want to use) in the respective transcriber scripts.

- For example, if you want to get results for assemblyai, you'd add your api key at the top of `assemblyai_transcribe.py`

4) Call `assemblyai_transcribe.py` or `openai_whisper_transcribe.py` by calling the `transcribe_all_files` function in each file and passing the path to the truth folder, the path to the audios folder, and the name of the output csv. Uncomment this line in `assemblyai_transcribe.py` or `openai_whisper_transcribe.py`

`transcribe_all_files("/audios", "/truth", "assemblyai_outputs.csv)`

This will produce a csv containing the outputs of the transcription requests. You'll need the path to that csv for step #5.

5) Run the `calculate_wer` script to generate WER results. Uncomment this path in `calculate_wer` and pass your own outputs path and the name of the metrics output file as arguments:

`calculate_wer(/path/to/outputs, assemblyai_english_metrics.csv)`

