import os
import pandas as pd
from gtts import gTTS

# Not Supported languages ("as", "or")
langs = ["bn","en","gu","hi","kn","ml","mr","ta","te","ur"]

for lang in langs:
    csv_file = os.path.join('../data', lang, f"{lang}_textdata.csv")
    output_folder = os.path.join('../data', lang, f"{lang}_voicedata")
    if not os.path.exists(csv_file):
        print(f"Skipping {lang} (no file: {csv_file})")
        continue
    os.makedirs(output_folder, exist_ok=True)
    
    # Always read without assuming header
    try:
        df = pd.read_csv(csv_file, header=None)  
        # Flatten it into one column called 'sentence'
        if df.shape[1] > 1:  
            # Try to find a column containing text
            possible_cols = [c for c in df.columns if "sent" in str(c).lower() or "text" in str(c).lower()]
            if possible_cols:
                df = df[possible_cols].astype(str)
                df.columns = ["sentence"]
            else:
                df = df.iloc[:, -1].astype(str)  # fallback: last column
                df = df.to_frame(name="sentence")
        else:
            df.columns = ["sentence"]
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        continue
    
    # Generate audio
    for idx, row in df.iterrows():
        text = str(row["sentence"]).strip()
        if not text:
            continue
        try:
            tts = gTTS(text=text, lang=lang)
            filename = os.path.join(output_folder, f"{idx+1}.mp3")
            tts.save(filename)
            print(f"{lang}: Saved {filename}")
        except Exception as e:
            print(f"Error in {lang} sentence {idx+1}: {e}")

print("All available languages processed!")