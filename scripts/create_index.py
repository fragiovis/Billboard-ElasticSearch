import json, pathlib
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", request_timeout=60)
body = json.loads(pathlib.Path("../config/files.mapping.json").read_text(encoding="utf-8"))
try:
    es.indices.create(index="files", body=body)
except Exception as e:
    print(f"Errore nella creazione indice: {e}")

print("Indice creato o già esistente.")
