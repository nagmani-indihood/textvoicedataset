# Used this translator for the languages which is not supported in gTTS like "as" and "or".

# Run this code in Kaggle notebook, create 4 code cell for these four steps and then run 1,2,3 then 4 cell.

# STEP 1: Install dependencies
!pip install git+https://github.com/huggingface/parler-tts.git
!pip install transformers soundfile pydub

import os
import torch
import pandas as pd
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
from pydub import AudioSegment


# STEP 2: Setup device and model
device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "ai4bharat/indic-parler-tts"
model = ParlerTTSForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)
description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

print("Model loaded:", model_name)


# STEP 3: Function to generate speech

def generate_speech(text, description, out_path):
    try:
        desc_ids = description_tokenizer(description, return_tensors="pt").to(device)
        prompt_ids = tokenizer(text, return_tensors="pt").to(device)
        generation = model.generate(
            input_ids=desc_ids.input_ids,
            attention_mask=desc_ids.attention_mask,
            prompt_input_ids=prompt_ids.input_ids,
            prompt_attention_mask=prompt_ids.attention_mask
        )
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(out_path, audio_arr, model.config.sampling_rate)
        print(f"Saved {out_path}")

    except Exception as e:
        print(f"Error for: {text[:30]}... | {e}")


# STEP 4: Generate for a CSV file (WAV only then convert it into mp3 if required).

def process_csv(lang_code, csv_file, description):
    # Create output folder
    out_dir = f"{lang_code}_voicedata"
    os.makedirs(out_dir, exist_ok=True)

    # Load sentences (force first column as 'sentence')
    df = pd.read_csv(csv_file, header=None, names=["sentence"])

    for i, row in df.iterrows():
        text = str(row["sentence"]).strip()
        if not text:
            continue

        # Define WAV path
        out_wav = os.path.join(out_dir, f"{i+1}.wav")

        # Generate WAV
        generate_speech(text, description, out_wav)


# STEP 5: As of now, Run for Assamese and Odia

# Example descriptions → you can adjust per language
as_desc = "Sita's voice is clear and natural, slightly expressive, with moderate speed and pitch, recorded in very high quality."
or_desc = "Manas's voice is deep, natural and clear, with a steady pace, recorded in excellent quality with no background noise."

# Assamese (as)
process_csv("as", "/kaggle/input/bank-and-loan-data/as_textdata.csv", as_desc)

# Odia (or)
process_csv("or", "/kaggle/input/bank-and-loan-data/or_textdata.csv", or_desc)
