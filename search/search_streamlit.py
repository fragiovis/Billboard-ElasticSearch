import streamlit as st
from elasticsearch import Elasticsearch
from html import escape

ES_URL = "http://localhost:9200"
INDEX = "files"

es = Elasticsearch(ES_URL, request_timeout=60)

st.title("Billboard Lyrics Search")
st.write("Search by title, lyrics, or exact line. Expand each result for details.")

search_type = st.radio("Choose search type:", ("Title", "Lyrics Content", "Line Content"))
query = st.text_input("Enter your query...")

if st.button("Search") and query.strip():
    if search_type == "Title":
        body = {
            "query": {
                "match": {
                    "name": query
                }
            }
        }
    elif search_type == "Lyrics Content":
        body = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }
    else:  # Line Content
        # Usa match_phrase su content.by_line per cercare la linea esatta
        body = {
            "query": {
                "match_phrase": {
                    "content.by_line": query
                }
            }
        }
    res = es.search(index=INDEX, body=body)
    st.subheader(f"Results ({res['hits']['total']['value']})")
    for d in res['hits']['hits']:
        with st.expander(f'🎵 {d["_source"]["name"]}'):
            lyrics = d['_source'].get('content', '')
            # Preserva gli accapo e gli spazi come nel file originale
            st.markdown(f"<div style='white-space: pre-wrap'>{escape(lyrics)}</div>", unsafe_allow_html=True)
            st.caption(f"Score: {d['_score']}")
else:
    st.info("Enter a query and press Search!")
