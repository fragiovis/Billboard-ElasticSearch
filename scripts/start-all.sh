#!/bin/bash

# Start Elastic (Docker) - decommenta se vuoi farlo partire qui!
# echo "Starting Elasticsearch via Docker..."
# docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.11.0
# sleep 20 # attesa per l'avvio di ES

echo "Creating index in Elasticsearch..."
python3 create_index.py

echo "Indexing documents in Elasticsearch..."
python3 fill_index.py

echo "Starting Streamlit UI..."
streamlit run ../search/search_streamlit.py
