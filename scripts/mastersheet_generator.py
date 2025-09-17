import os
import pandas as pd

langs = ["bn","en","gu","hi","kn","ml","mr","ta","te","ur", "as", "or"]

all_data = {}

for lang in langs:
    csv_file = os.path.join('../data', lang, f"{lang}_textdata.csv")
    voice_folder = os.path.join('../data', lang, f"{lang}_voicedata")
    if not os.path.exists(csv_file) or not os.path.exists(voice_folder):
        print(f"Skipping {lang} (missing csv or voice folder)")
        continue
    try:
        df = pd.read_csv(csv_file, header=None)
        if df.shape[1] > 1:
            df = df.iloc[:, -1]  # last column as sentence
        else:
            df = df.iloc[:, 0]
        sentences = df.astype(str).tolist()
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        continue
    # Only take first 100 sentences
    sentences = sentences[:100]
    # Build voice file paths (assumes 1.mp3, 2.mp3, ...)
    voices = [os.path.join(voice_folder, f"{i+1}.mp3") for i in range(len(sentences))]
    # Store in dictionary
    all_data[f"{lang}_sentence"] = sentences
    all_data[f"{lang}_voice"] = voices

# Combine into a single DataFrame
mastersheet = pd.DataFrame(all_data)

# Save as CSV
mastersheet.to_csv("../mastersheet.csv", index=False, encoding="utf-8-sig")

print("mastersheet.csv created with all languages")