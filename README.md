# 🎵 Billboard Lyrics Search — Elasticsearch + Streamlit

Full-text search engine over Billboard hit song lyrics. Songs are indexed in **Elasticsearch** with custom analyzers and searched through a small **Streamlit** UI by title, by lyrics content or by an exact lyric line.

*Data Engineering course (Ingegneria dei Dati), homework 2 · Università degli Studi Roma Tre (2025)*

## Features
| Search mode | Field | Query |
|---|---|---|
| **Title** | `name` | `match` (full text) |
| **Lyrics content** | `content` | `match` (full text, stop words removed) |
| **Exact line** | `content.by_line` | `match_phrase` on a line-tokenised sub-field |

Results show the song title and lyrics with their original line breaks.

## Index design
`config/files.mapping.json` defines two custom analyzers:
- `content_standard` — `standard` tokenizer + `lowercase` + `stop` filters, for full-text search on `content`;
- `content_by_line` — a `pattern` tokenizer on `\n`, so each lyric line becomes one token, + `lowercase`; used by the `content.by_line` sub-field for case-insensitive exact-line search.

Each document has `name` (song title, from the file name), `content` (full lyrics) and `path`.

## Data pipeline
1. `scripts/cut_songs.py` splits the Billboard CSV into one `.txt` file per song (first 500 songs), removing scraping artefacts such as trailing `…Embed` markers.
2. `scripts/clean.py` removes duplicate songs (same title prefix), leaving **361 unique songs** in `data/billboard_split/`.
3. `scripts/create_index.py` creates the `files` index with the mapping above.
4. `scripts/fill_index.py` indexes every file.

## Getting started
Start Elasticsearch (e.g. with Docker):
```bash
docker run -d -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0
```

Then, from the project root:
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cd scripts
python3 create_index.py
python3 fill_index.py
streamlit run ../search/search_streamlit.py
```
or run everything at once with `cd scripts && bash start-all.sh` (Elasticsearch must already be running on `localhost:9200`).

## Troubleshooting
- **`ConnectionRefusedError`**: make sure Elasticsearch is running and reachable at `http://localhost:9200`.
- **`urllib3 … LibreSSL` warning on macOS**: harmless; ignore it or pin `urllib3<2.0`.
- **No results for an exact line**: type a full line as it appears in the lyrics, punctuation included (matching is case-insensitive).

## Tech stack
Python · Elasticsearch 8 · Streamlit · Docker
