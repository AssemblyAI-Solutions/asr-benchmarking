## Open Source ASR Benchmarking

1) Run `pip install -r requirements.txt`

2) Add audio files to `/audios` and add your human transcript labels to `/truth`

3) Add your respective API keys to a `.env` file (depending on the vendors you want to use) in the respective transcriber scripts. See `.env_sample`

4) Run `run_benchmark_local.py` to execute benchmarks on local files

5) If you want to also run benchmarks against a hugging face dataset (the default is librispeech test clean), then you can run run_benchmark_local.py. Note that you will likely need to download librispeech for the first time and change line 88 in `utils.py` to ensure that you are pointing to the correct place that the dataset was loaded in:
```    
base_dir = "/Users/samflamini/.cache/huggingface/datasets/downloads/extracted" #note - you should replace this with your path to the hugging face directory in .cache
```