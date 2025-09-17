import os
from deep_translator import GoogleTranslator
import csv

def create_translated_csvs(source_csv, langs):
    with open(source_csv, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]

    for lang in langs:
        translated_sentences = []
        translator = GoogleTranslator(source='en', target=lang)
        for sentence in sentences:
            try:
                translated = translator.translate(sentence)
            except Exception as e:
                translated = f"[Translation error: {e}]"
            translated_sentences.append(translated)
        out_dir = os.path.join('../data', lang)
        os.makedirs(out_dir, exist_ok=True)
        out_csv = os.path.join(out_dir, f"{lang}_textdata.csv")
        with open(out_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for line in translated_sentences:
                writer.writerow([line])
        print(f"Created {out_csv}")

langs = ["bn","en","gu","hi","kn","ml","mr","ta","te","ur","as","or"]
create_translated_csvs('../eng_textdata.csv', langs)