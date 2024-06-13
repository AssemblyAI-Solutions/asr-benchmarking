from datasets import load_dataset, load_dataset_builder, get_dataset_config_names, get_dataset_split_names, Audio
import pandas as pd

def load_commonvoice():
    dataset = load_dataset("mozilla-foundation/common_voice_5_1", "en", split="test", trust_remote_code=True)
    cv_df = pd.DataFrame(
        {
            "path": dataset['path'],
            "target": dataset['sentence']
        }
    )
    return cv_df

def load_librispeech_test_clean():
    dataset = load_dataset("librispeech_asr", 'clean', split="test", trust_remote_code=True)
    print(dataset['audio'][0])
    cv_df = pd.DataFrame(
        {
            "path": dataset['file'],
            "target": dataset['text']
        }
    )
    return cv_df