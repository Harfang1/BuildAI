import re
import spacy
from elasticsearch import Elasticsearch
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import requests
from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config_loader import settings

# ==========================================================
# CONFIG
# ==========================================================

# --- Elasticsearch ---
es = Elasticsearch(settings.ELASTICSEARCH_URL)

# --- Qdrant ---
qdrant = QdrantClient(url=settings.QDRANT_URL)

# --- Embeddings (Ollama) ---
session = requests.Session()

# --- Lemmatizer (French) ---
print("Loading spaCy French model...")
_nlp = spacy.load(settings.SPACY_MODEL)

# Hybrid weights
BM25_WEIGHT = settings.BM25_WEIGHT
VECTOR_WEIGHT = settings.VECTOR_WEIGHT

TOP_K = settings.RETRIEVER_TOP_K
FINAL_K = settings.RETRIEVER_FINAL_K


# ==========================================================
# NORMALIZATION + LEMMATIZATION
# ==========================================================

def normalize_and_lemmatize(text: str) -> str:
    """Clean markdown + lowercase + French lemmatization."""
    # --- Remove markdown blocks ---
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"#+\s*", " ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_]{1,3}", " ", text)
    text = re.sub(r"^\s*[-*+]\s*", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s*", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\|.*\|", " ", text)
    text = re.sub(r"[-*_]{3,}", " ", text)
    text = re.sub(r"[{}\[\]]", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip().lower()

    # Lemmatize
    doc = _nlp(text)
    lemmas = [t.lemma_ for t in doc if not t.is_punct and not t.is_space]

    return " ".join(lemmas)


# ==========================================================
# EMBEDDING (Qdrant)
# ==========================================================

def _embed(text: str):
    resp = session.post(
        f"{settings.OLLAMA_BASE_URL}/api/embeddings",
        json={"model": settings.EMBED_MODEL, "prompt": text}
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


# ==========================================================
# BM25 SEARCH
# ==========================================================

def bm25_search(query: str, top_k=TOP_K):
    query_lem = normalize_and_lemmatize(query)

    resp = es.search(
        index=settings.ELASTICSEARCH_INDEX,
        size=top_k,
        query={"match": {"text": query_lem}},
        stored_fields=["doc_id"]
    )

    results = []
    for hit in resp["hits"]["hits"]:
        results.append({
            "id": hit["fields"]["doc_id"][0],
            "score": hit["_score"],
            "method": "bm25"
        })
    return results


# ==========================================================
# PDF METADATA FORMATTING
# ==========================================================

def _format_pdf_metadata(meta: dict, chunk_text: str = "", point_id: str = "") -> dict:
    import urllib.parse
    if not isinstance(meta, dict):
        meta = {}
    else:
        meta = dict(meta)

    file_name = meta.get("file_name", "")
    title = meta.get("title", "")

    # Infer descriptive title if missing
    if not title or title in ["Document sans titre", "Document BTP"]:
        if file_name:
            title = Path(file_name).stem.replace("_", " ").strip()
        elif "rex b" in chunk_text.lower():
            title = "Dispositif REX Bâtiments Performants"
        elif "pacte" in chunk_text.lower():
            title = "Programme PACTE - Règles de l'art BTP"
        elif "proreno" in chunk_text.lower() or "profeel" in chunk_text.lower():
            title = "Programme PROFEEL / PRORENO"
        elif "tpdemain" in chunk_text.lower():
            title = "Fiche Travaux Publics Demain"
        elif "béton armé" in chunk_text.lower() or "beton arme" in chunk_text.lower():
            title = "Cours technique Béton Armé"
        elif "financement" in chunk_text.lower() or "coût" in chunk_text.lower():
            title = "Gestion et Financement de Projets BTP"
        else:
            first_words = " ".join(chunk_text.split()[:6]).strip()
            title = first_words.capitalize() if len(first_words) >= 8 else "Guide technique BTP"

    meta["title"] = title

    # Determine PDF filename on fileserver
    if file_name:
        pdf_target = f"{Path(file_name).stem}.pdf"
    elif title:
        clean_title = title.replace("/", "_").strip()
        pdf_target = f"{clean_title}.pdf"
    else:
        pdf_target = f"{point_id}.pdf"

    fileserver_base = getattr(settings, 'FILESERVER_BASE', 'http://localhost:7701')
    pdf_url = f"{fileserver_base}/download/{urllib.parse.quote(pdf_target)}"
    meta["pdf_url"] = pdf_url
    meta["source_url"] = pdf_url
    return meta


# ==========================================================
# QDRANT SEARCH
# ==========================================================

def vector_search(query: str, top_k=TOP_K):
    try:
        vec = _embed(query)

        res = qdrant.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=vec,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )

        results = []
        for pt in res.points:
            chunk_text = pt.payload.get("chunk_text", "") if pt.payload else ""
            raw_meta = pt.payload.get("metadata") or {} if pt.payload else {}
            formatted_meta = _format_pdf_metadata(raw_meta, chunk_text, str(pt.id))
            results.append({
                "id": pt.id,
                "score": pt.score,
                "chunk_text": chunk_text,
                "hash": pt.payload.get("hash") if pt.payload else None,
                "metadata": formatted_meta,
                "method": "vector"
            })
        return results
    except Exception as e:
        print(f"[WARN] vector_search failed: {e}")
        return []


# ==========================================================
# FETCH CHUNK FROM QDRANT (with Elasticsearch fallback)
# ==========================================================

def fetch_chunk(point_id: str):
    # 1. Try Qdrant
    try:
        res = qdrant.retrieve(
            collection_name=settings.QDRANT_COLLECTION,
            ids=[point_id],
            with_payload=True,
            with_vectors=False
        )
        if res:
            pt = res[0]
            chunk_text = pt.payload.get("chunk_text", "") if pt.payload else ""
            raw_meta = pt.payload.get("metadata") or {} if pt.payload else {}
            formatted_meta = _format_pdf_metadata(raw_meta, chunk_text, str(pt.id))
            return {
                "id": pt.id,
                "chunk_text": chunk_text,
                "hash": pt.payload.get("hash") if pt.payload else None,
                "metadata": formatted_meta
            }
    except Exception as e:
        print(f"[WARN] fetch_chunk Qdrant error for {point_id}: {e}")

    # 2. Fallback to Elasticsearch document
    try:
        es_res = es.search(
            index=settings.ELASTICSEARCH_INDEX,
            size=1,
            query={"term": {"doc_id": point_id}}
        )
        hits = es_res.get("hits", {}).get("hits", [])
        if hits:
            source = hits[0].get("_source", {})
            chunk_text = source.get("text", "")
            raw_meta = source.get("metadata") or {}
            formatted_meta = _format_pdf_metadata(raw_meta, chunk_text, str(point_id))
            return {
                "id": point_id,
                "chunk_text": chunk_text,
                "hash": raw_meta.get("content_hash"),
                "metadata": formatted_meta
            }
    except Exception as e:
        print(f"[WARN] fetch_chunk ES fallback error for {point_id}: {e}")

    return None


# ==========================================================
# HYBRID RRF FUSION (dynamic top_k)
# ==========================================================

def hybrid_re_rank(bm25_res, vec_res, final_k):
    """
    Combine BM25 + vector results using RRF.
    final_k: number of results to return.
    """

    scores = {}  # {doc_id: {"bm25": float, "vec": float}}

    # --- BM25 scoring ---
    bm25_sorted = sorted(bm25_res, key=lambda x: -x["score"])
    for rank, item in enumerate(bm25_sorted):
        doc_id = item["id"]
        scores.setdefault(doc_id, {"bm25": 0, "vec": 0})
        scores[doc_id]["bm25"] = 1 / (rank + 60)

    # --- Vector scoring ---
    vec_sorted = sorted(vec_res, key=lambda x: -x["score"])
    for rank, item in enumerate(vec_sorted):
        doc_id = item["id"]
        scores.setdefault(doc_id, {"bm25": 0, "vec": 0})
        scores[doc_id]["vec"] = 1 / (rank + 60)

    # --- Weighted merge ---
    fused = []
    for doc_id, s in scores.items():
        fused_score = BM25_WEIGHT * s["bm25"] + VECTOR_WEIGHT * s["vec"]
        fused.append((doc_id, fused_score))

    # --- Sort & return final_k ---
    fused_sorted = sorted(fused, key=lambda x: -x[1])[:final_k]
    return fused_sorted



# ==========================================================
# PUBLIC API — THE ONLY FUNCTION THE USER CALLS
# ==========================================================

def retrieve(prompt: str, top_k: int = 5):
    """
    Full hybrid pipeline:
    - top_k BM25 candidates
    - top_k vector candidates
    - Fuse and return top_k final results
    """
    # 1. BM25
    bm25_results = bm25_search(prompt, top_k)

    # 2. Vector
    vector_results = vector_search(prompt, top_k)

    # 3. Fusion
    fused = hybrid_re_rank(bm25_results, vector_results, final_k=top_k)

    # 4. Fetch chunks from Qdrant
    output = []
    for doc_id, fused_score in fused:
        chunk = fetch_chunk(doc_id)
        if chunk:
            chunk["fused_score"] = fused_score
            output.append(chunk)

    # Sort again by fused score just to be clean
    output = sorted(output, key=lambda x: -x["fused_score"])

    return output
