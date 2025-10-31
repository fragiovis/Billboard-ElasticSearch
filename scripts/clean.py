import os
import re

# Inserisci il percorso della directory
directory = input("Inserisci il percorso della directory: ").strip()

if not os.path.isdir(directory):
    print("❌ La directory specificata non esiste.")
    exit(1)

# Dizionario per memorizzare i prefissi già visti
seen = {}

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)

    if not os.path.isfile(filepath):
        continue  # Salta eventuali cartelle

    # Estrai la parte prima dell'underscore
    match = re.match(r"^(.*?)_", filename)
    if not match:
        continue

    prefix = match.group(1)

    if prefix not in seen:
        seen[prefix] = filepath
    else:
        # Se un duplicato viene trovato, elimina questo file
        print(f"🗑️ Rimuovo duplicato: {filename}")
        os.remove(filepath)

print("✅ Pulizia completata!")
