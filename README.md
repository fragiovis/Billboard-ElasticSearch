# Billboard Lyrics Search (Elasticsearch + Streamlit)

Ricerca di testi di canzoni indicizzati su Elasticsearch con una semplice UI in Streamlit. Il progetto indicizza i file `.txt` nella cartella `data/billboard_split/` e consente la ricerca per titolo, contenuto e riga esatta.

## Struttura del Progetto

- `config/files.mapping.json`
  - Configurazione dell'indice Elasticsearch: analyzer standard per `content` e tokenizer a newline per il sotto-campo `content.by_line`.
- `data/billboard.csv`
  - Dataset originale (CSV) con titoli e testi (usato da `cut_songs.py`).
- `data/billboard_split/`
  - 500 file di testo (uno per canzone) usati per l'indicizzazione.
- `scripts/create_index.py`
  - Crea l'indice `files` su Elasticsearch usando la mapping in `config/files.mapping.json`.
- `scripts/fill_index.py`
  - Indicizza i file in `data/billboard_split/` nell'indice `files`.
- `scripts/cut_songs.py`
  - Genera/aggiorna i file in `data/billboard_split/` a partire da `data/billboard.csv` (facoltativo, già forniti).
- `scripts/start-all.sh`
  - Orchestrazione: crea indice, indicizza documenti, avvia la UI.
- `search/search_streamlit.py`
  - UI Streamlit con le opzioni di ricerca e visualizzazione dei risultati (preserva gli accapo dei testi).
- `venv/`
  - Virtual environment Python.

## Prerequisiti

- Python 3.9+
- Virtualenv (la cartella `venv/` è già presente)
- Elasticsearch in esecuzione su `http://localhost:9200`
  - Suggerito via Docker:
    ```bash
    docker run -d \
      -p 9200:9200 -p 9300:9300 \
      -e "discovery.type=single-node" \
      docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    ```

## Setup

1. Attiva il virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

Nota: su macOS potresti vedere un avviso di `urllib3` relativo a LibreSSL. È un warning e non blocca l’esecuzione. In caso di problemi, puoi pinning `urllib3<2.0` o usare un Python installato via Homebrew.

## Creazione Indice e Indicizzazione

Esegui questi comandi dalla radice del progetto (`HW2-ElasticSearch`), con Elasticsearch già avviato:

```bash
python3 scripts/create_index.py
python3 scripts/fill_index.py
```

Questo creerà l’indice `files` e indicizzerà i documenti a partire da `data/billboard_split/`.

## Avvio della UI Streamlit

```bash
streamlit run search/search_streamlit.py
```

Apri il link fornito da Streamlit nel browser. La UI offre:

- `Title`: ricerca full-text nel campo `name` (titolo)
- `Lyrics Content`: ricerca full-text nel campo `content`
- `Line Content`: ricerca di una riga esatta nel campo `content.by_line`

I risultati mostrano il titolo del brano e il testo. La visualizzazione dei testi preserva gli accapo originali (come nei file `.txt`).

## Flusso Rapido (script di avvio)

Se preferisci automatizzare:

```bash
bash scripts/start-all.sh
```

Questo script presume che Elasticsearch sia già in esecuzione su `localhost:9200`.

## Troubleshooting

- `ConnectionRefusedError` o `Failed to establish a new connection`:
  - Assicurati che Elasticsearch sia avviato e raggiungibile su `http://localhost:9200`.
- Avviso `urllib3 v2 only supports OpenSSL 1.1.1+ ... LibreSSL` (macOS):
  - È un warning non bloccante. Puoi ignorarlo oppure usare `urllib3<2.0`.
- Nessun risultato per “Line Content”:
  - Verifica di cercare una riga completa presente nel file, inclusa punteggiatura, e ricorda che la ricerca è case-insensitive (grazie al filtro `lowercase`).

## Dettagli Mapping

`config/files.mapping.json` definisce:

- `content` (text) con analyzer `content_standard` (`standard` + `lowercase`, `stop`).
- Sub-field `content.by_line` (text) con analyzer `content_by_line` che usa un tokenizer `newline_tokenizer` basato su pattern `\n` per tokenizzare per riga, e applica `lowercase`.

Questo consente ricerche full-text su `content` e ricerche di riga esatta su `content.by_line` (via `match_phrase`).

## Dati

- I file `.txt` in `data/billboard_split/` contengono i testi di canzoni. Ogni file è indicizzato come un documento con:
  - `name`: titolo del brano (estratto dal nome file)
  - `content`: testo completo del brano
  - `path`: percorso del file

Se vuoi rigenerare questi file da `billboard.csv`, usa `scripts/cut_songs.py`.