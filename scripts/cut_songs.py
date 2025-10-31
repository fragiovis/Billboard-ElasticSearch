import csv
import pathlib
import re

INPUT = "../data/billboard.csv"
OUTPUT_DIR = "../data/billboard_split/"

def clean_lyrics(text):
    # Rimuove la stringa tipo "22Embed", "123Embed", etc. solo se è alla fine
    return re.sub(r"\d+Embed$", "", text).strip()

with open(INPUT, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        if i >= 500:
            break
        title = row["song"].strip().replace("/", "-").replace("\\", "-")  # Pulizia filename
        lyrics = row.get("lyrics", "").strip()
        lyrics = clean_lyrics(lyrics)
        fname = f"{OUTPUT_DIR}{title or 'untitled'}_{i+1:03d}.txt"
        with open(fname, "w", encoding="utf-8") as out:
            out.write(lyrics if lyrics else "[No lyrics available]")

print("Split completato: controlla la cartella billboard_split per i 500 file (solo titolo e testo pulito).")
