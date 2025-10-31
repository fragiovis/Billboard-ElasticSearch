from elasticsearch import Elasticsearch, helpers
import pathlib
import time

ES_URL = "http://localhost:9200"
INDEX  = "files"
DATA_DIR = "../data/billboard_split/"

es = Elasticsearch(ES_URL, request_timeout=60)

def extract_name(filename):
    # Rimuove l'estensione e l'ID finale (es: "ShapeOfYou_012.txt" -> "ShapeOfYou")
    stem = pathlib.Path(filename).stem   # "ShapeOfYou_012"
    name = stem.rsplit("_", 1)[0]        # "ShapeOfYou"
    return name

def gen_docs():
    for path in pathlib.Path(DATA_DIR).glob("*.txt"):
        song_name = extract_name(path.name)
        text = path.read_text(encoding="utf-8").strip()
        yield {
            "_index": INDEX,
            "_id": path.stem,
            "_source": {
                "name": song_name,
                "content": text,
                "path": str(path.resolve())
            }
        }
start = time.time()
helpers.bulk(es, gen_docs())
print(f"Indicizzazione completata! Tempo impiegato: {time.time() - start:.2f} secondi")
# Vedere i documenti indicizzati nell'indice:
# curl -X GET "localhost:9200/files/_search?pretty"
