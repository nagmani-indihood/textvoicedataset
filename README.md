# Indian Language Text & Voice Dataset Generator

This repository provides a simple pipeline to generate parallel text and voice datasets in 12 Indian languages for testing machine learning models, speech synthesis, and translation systems.

## Supported Languages
- Bengali (`bn`)
- English (`en`)
- Gujarati (`gu`)
- Hindi (`hi`)
- Kannada (`kn`)
- Malayalam (`ml`)
- Marathi (`mr`)
- Tamil (`ta`)
- Telugu (`te`)
- Urdu (`ur`)

## Directory Structure
```
root/
├── data/
│   ├── <lang>/
│   │   ├── <lang>_textdata.csv
│   │   └── <lang>_voicedata/
│   │       └── [1.mp3, 2.mp3, ...]
├── eng_textdata.csv
├── scripts/
│   ├── textdata_generator.py
│   ├── voicedata_generator.py
│   ├── mastersheet_generator.py
│   ├── ai4bharat_voice_generator.py
├── requirements.txt
└── mastersheet.csv
```

## How to Use

### 1. Prepare English Sentences
- Add your English sentences to `eng_textdata.csv` in the root folder. Each line should be a separate sentence.

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Generate Translated Text Data
Run the translation script to create text data in all supported languages:
```bash
python scripts/textdata_generator.py
```
- This will read from `eng_textdata.csv` and create `<lang>_textdata.csv` files in `data/<lang>/` for each language.

### 4. Generate Voice Data
Run the voice generation script:
```bash
python scripts/voicedata_generator.py
```
- This will read each `<lang>_textdata.csv` and generate corresponding MP3 files in `data/<lang>/<lang>_voicedata/`.

### 5. Create Master Sheet
Run the master sheet generator:
```bash
python scripts/mastersheet_generator.py
```
- This will create `mastersheet.csv` in the root folder, containing all sentences and their corresponding voice file paths for each language.


## Voice Data Generation
For generating voice datasets, I used **Google Text-to-Speech (gTTS)** for most supported Indian languages to generate `.mp3` voice data from text datasets but for languages not supported in gTTS (like **Assamese – `as`** and **Odia – `or`**), I used the **AI4Bharat Indic Parler TTS model**.

The implementation is available at: `scripts/ai4bharat_voice_generator.py`

## Output
- `data/<lang>/<lang>_textdata.csv`: Translated sentences for each language.
- `data/<lang>/<lang>_voicedata/`: MP3 files for each sentence.
- `mastersheet.csv`: A CSV file with all sentences and voice file paths for all languages.

## Customization
- To add more languages, update the `langs` list in the scripts and ensure the translation/voice APIs support them.
- You can use your own English sentences by editing `eng_textdata.csv`.

## Author
Created by Nagmani. This dataset is intended for research and testing purposes related to banks & loans, but can be adapted for other domains.

