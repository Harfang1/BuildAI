#!/usr/bin/env python3
"""
Index raw scraped data (HTML articles) into Qdrant vector DB and Elasticsearch BM25 index.

Usage:
  python scripts/index_raw_data_to_qdrant_and_es.py [--limit N] [--raw-dir PATH]
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import requests
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("indexer")

# Spacy (French lemmatizer)
try:
    import spacy
    _nlp = spacy.load("fr_core_news_sm")
    logger.info("Loaded spaCy French model")
except Exception as e:
    _nlp = None
    logger.warning(f"spaCy not available or model not installed ({e}); using regex word tokenizer")

# Elasticsearch
try:
    from elasticsearch import Elasticsearch, helpers
except ImportError:
    Elasticsearch = None
    helpers = None

# Qdrant client
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, VectorParams, Distance
except ImportError:
    QdrantClient = None


def normalize_and_lemmatize(text: str) -> str:
    """Clean text + lowercase + French lemmatization."""
    # Clean markdown / html relics
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[{}\[\]]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()

    if _nlp:
        doc = _nlp(text[:20000])  # limit length per spacy call
        lemmas = [t.lemma_ for t in doc if not t.is_punct and not t.is_space]
        return " ".join(lemmas)
    else:
        # Fallback: simple lowercased words
        words = re.findall(r"\b\w+\b", text)
        return " ".join(words)


def extract_html_article(file_path: Path) -> Optional[Tuple[str, str, str]]:
    """
    Extract title, clean text, and guessed source URL from an HTML article.
    """
    try:
        raw_html = file_path.read_text(encoding="utf-8", errors="ignore")
        if len(raw_html) < 100:
            return None

        soup = BeautifulSoup(raw_html, "html.parser")

        # Extract title
        title_el = soup.find("h1") or soup.find("h2", class_="entry-title") or soup.find("h2") or soup.find("title")
        title = title_el.get_text(strip=True) if title_el else file_path.stem
        title = re.sub(r"\s+", " ", title).strip()

        # Clean non-content elements
        content_div = soup.find("div", class_="entry-content") or soup.find("article") or soup
        for unwanted in content_div(["script", "style", "nav", "header", "footer", "aside"]):
            unwanted.decompose()

        clean_text = content_div.get_text(separator=" ", strip=True)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        if len(clean_text) < 80:
            return None

        # Build clean slug
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
        source_url = f"https://www.btp-cours.com/{slug}/"

        return title, clean_text, source_url
    except Exception as err:
        logger.warning(f"Error parsing {file_path.name}: {err}")
        return None


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """Split text into overlapping character chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) >= 50:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def get_embedding(ollama_url: str, text: str, model: str = "embeddinggemma") -> List[float]:
    """Get embedding from Ollama."""
    resp = requests.post(
        f"{ollama_url.rstrip('/')}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def ensure_qdrant_collection(qdrant_url: str, collection_name: str, vector_dim: int = 768):
    """Ensure Qdrant collection exists."""
    resp = requests.get(f"{qdrant_url.rstrip('/')}/collections/{collection_name}", timeout=10)
    if resp.status_code == 200:
        logger.info(f"Qdrant collection '{collection_name}' already exists")
        return

    logger.info(f"Creating Qdrant collection '{collection_name}' (dim={vector_dim}, Cosine)...")
    payload = {
        "vectors": {
            "size": vector_dim,
            "distance": "Cosine"
        }
    }
    create_resp = requests.put(
        f"{qdrant_url.rstrip('/')}/collections/{collection_name}",
        json=payload,
        timeout=10
    )
    create_resp.raise_for_status()
    logger.info(f"Collection '{collection_name}' created successfully")


def ensure_es_index(es_url: str, index_name: str):
    """Ensure Elasticsearch index exists with doc_id and text mapping."""
    resp = requests.get(f"{es_url.rstrip('/')}/{index_name}", timeout=10)
    if resp.status_code == 200:
        logger.info(f"Elasticsearch index '{index_name}' already exists")
        return

    logger.info(f"Creating Elasticsearch index '{index_name}'...")
    mapping = {
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword", "store": True},
                "text": {"type": "text"},
                "metadata": {"type": "object", "enabled": False}
            }
        }
    }
    create_resp = requests.put(
        f"{es_url.rstrip('/')}/{index_name}",
        json=mapping,
        timeout=10
    )
    create_resp.raise_for_status()
    logger.info(f"Elasticsearch index '{index_name}' created successfully")


def main():
    parser = argparse.ArgumentParser(description="Index BTP raw HTML files into Qdrant & Elasticsearch")
    parser.add_argument("--raw-dir", default="scrapping/raw_data", help="Path to raw_data folder")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of HTML files to index (0 = all)")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for Qdrant and ES upserts")
    parser.add_argument("--qdrant-url", default=os.getenv("QDRANT_URL", "http://localhost:6335"))
    parser.add_argument("--qdrant-collection", default=os.getenv("QDRANT_COLLECTION", "btp_rag_docs_v2"))
    parser.add_argument("--es-url", default=os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"))
    parser.add_argument("--es-index", default=os.getenv("ELASTICSEARCH_INDEX", "btp_bm25_v2_index"))
    parser.add_argument("--ollama-url", default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11435"))
    parser.add_argument("--embed-model", default="embeddinggemma")
    parser.add_argument("--workers", type=int, default=4, help="Concurrent workers for embeddings")

    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    if not raw_dir.exists():
        logger.error(f"Raw data dir '{raw_dir}' does not exist")
        sys.exit(1)

    html_files = sorted(raw_dir.glob("*.html"))
    if args.limit > 0:
        html_files = html_files[:args.limit]

    logger.info(f"Found {len(html_files)} HTML files to process")
    if not html_files:
        return

    # Ensure destinations are ready
    ensure_qdrant_collection(args.qdrant_url, args.qdrant_collection, vector_dim=768)
    ensure_es_index(args.es_url, args.es_index)

    # Gather chunks
    logger.info("Extracting and chunking HTML documents...")
    all_chunks = []
    for file_path in html_files:
        parsed = extract_html_article(file_path)
        if not parsed:
            continue
        title, text, url = parsed
        file_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            # Deterministic UUID per chunk
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{file_path.name}_{idx}"))
            all_chunks.append({
                "id": chunk_id,
                "file_name": file_path.name,
                "title": title,
                "url": url,
                "hash": file_hash,
                "chunk_text": chunk,
            })

    total_chunks = len(all_chunks)
    logger.info(f"Generated {total_chunks} total chunks from {len(html_files)} files")

    # Embedding & Indexing in batches
    start_time = time.time()
    indexed_count = 0

    for i in range(0, total_chunks, args.batch_size):
        batch = all_chunks[i:i + args.batch_size]
        batch_texts = [item["chunk_text"] for item in batch]

        # Compute embeddings concurrently
        def embed_worker(txt):
            return get_embedding(args.ollama_url, txt, model=args.embed_model)

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            vectors = list(pool.map(embed_worker, batch_texts))

        # Build Qdrant points
        qdrant_points = []
        es_bulk_lines = []

        for item, vec in zip(batch, vectors):
            doc_id = item["id"]
            title = item["title"]
            url = item["url"]
            c_text = item["chunk_text"]

            # Qdrant point
            qdrant_points.append({
                "id": doc_id,
                "vector": vec,
                "payload": {
                    "chunk_text": c_text,
                    "hash": item["hash"],
                    "metadata": {
                        "title": title,
                        "source_url": url,
                        "file_name": item["file_name"]
                    }
                }
            })

            # Elasticsearch action
            lemmatized = normalize_and_lemmatize(c_text)
            es_bulk_lines.append(json.dumps({"index": {"_index": args.es_index, "_id": doc_id}}))
            es_bulk_lines.append(json.dumps({
                "doc_id": doc_id,
                "text": lemmatized,
                "metadata": {
                    "title": title,
                    "source_url": url
                }
            }))

        # Upsert Qdrant
        qdrant_resp = requests.put(
            f"{args.qdrant_url.rstrip('/')}/collections/{args.qdrant_collection}/points?wait=true",
            json={"points": qdrant_points},
            timeout=30
        )
        qdrant_resp.raise_for_status()

        # Bulk index Elasticsearch
        es_payload = "\n".join(es_bulk_lines) + "\n"
        es_resp = requests.post(
            f"{args.es_url.rstrip('/')}/_bulk",
            data=es_payload,
            headers={"Content-Type": "application/x-ndjson"},
            timeout=30
        )
        es_resp.raise_for_status()

        indexed_count += len(batch)
        elapsed = time.time() - start_time
        rate = indexed_count / elapsed if elapsed > 0 else 0
        eta = (total_chunks - indexed_count) / rate if rate > 0 else 0

        logger.info(
            f"Progress: [{indexed_count}/{total_chunks}] "
            f"({(indexed_count / total_chunks) * 100:.1f}%) "
            f"- {rate:.1f} chunks/sec - ETA: {eta:.0f}s"
        )

    total_time = time.time() - start_time
    logger.info(f"✅ Successfully indexed {indexed_count} chunks into Qdrant and Elasticsearch in {total_time:.1f}s")


if __name__ == "__main__":
    main()
