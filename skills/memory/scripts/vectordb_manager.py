"""
Vector DB Manager — ChromaDB integration stub.

This is a placeholder for future vector database integration. All functions
gracefully degrade when ChromaDB is not installed, returning empty results
with informative messages.

When ChromaDB is installed, this module will provide:
  - Semantic search over archived knowledge
  - Embedding-based fuzzy recall for topics not matched by file scan
  - Persistent vector storage at the project level

To enable:
    pip install chromadb
    Then update the CHROMADB_AVAILABLE flag below.

Usage (future):
    from scripts.vectordb_manager import search, add_document, init_db
"""

import json
import sys
from pathlib import Path


# Attempt to import ChromaDB
CHROMADB_AVAILABLE = False
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    pass


DEFAULT_COLLECTION = "agent_memory"


def get_db_path() -> Path:
    """Get the vector DB storage path (project-level)."""
    memory_root = Path(__file__).resolve().parent.parent
    return memory_root / "vectordb"


def init_db(db_path: Path | None = None) -> dict:
    """Initialize or open the ChromaDB persistent collection."""
    if not CHROMADB_AVAILABLE:
        return {
            "status": "unavailable",
            "message": "ChromaDB is not installed. Run: pip install chromadb",
        }

    path = db_path or get_db_path()
    path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(path))
    collection = client.get_or_create_collection(name=DEFAULT_COLLECTION)

    return {
        "status": "ready",
        "path": str(path),
        "collection": DEFAULT_COLLECTION,
        "count": collection.count(),
    }


def add_document(text: str, metadata: dict | None = None) -> dict:
    """
    Embed and store a text document in the vector DB.

    Args:
        text: The text content to embed and store
        metadata: Optional metadata dict (tags, source, date, etc.)

    Returns:
        dict with status and document ID
    """
    if not CHROMADB_AVAILABLE:
        return {
            "status": "unavailable",
            "message": "ChromaDB is not installed. Document was NOT stored.",
            "suggestion": "pip install chromadb",
        }

    db_path = get_db_path()
    db_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.get_or_create_collection(name=DEFAULT_COLLECTION)

    import hashlib
    doc_id = hashlib.sha256(text.encode()).hexdigest()[:16]

    # Flatten metadata: ChromaDB only accepts str/int/float/bool values
    flat_metadata = {}
    if metadata:
        for k, v in metadata.items():
            if isinstance(v, list):
                flat_metadata[k] = ", ".join(str(item) for item in v)
            else:
                flat_metadata[k] = v

    collection.add(
        documents=[text],
        metadatas=[flat_metadata],
        ids=[doc_id],
    )

    return {
        "status": "stored",
        "id": doc_id,
        "collection": DEFAULT_COLLECTION,
    }


def search(query: str, top_k: int = 3) -> dict:
    """
    Search the vector DB for documents similar to the query.

    Args:
        query: Natural language search query
        top_k: Number of results to return

    Returns:
        dict with source, content, and metadata
    """
    if not CHROMADB_AVAILABLE:
        return {
            "source": "none",
            "content": "",
            "message": "ChromaDB is not installed. Archive search unavailable.",
            "suggestion": "pip install chromadb",
        }

    db_path = get_db_path()
    if not db_path.exists():
        return {
            "source": "none",
            "content": "",
            "message": "Vector DB not initialized. No archive data.",
        }

    client = chromadb.PersistentClient(path=str(db_path))

    try:
        collection = client.get_collection(name=DEFAULT_COLLECTION)
    except Exception:
        return {
            "source": "none",
            "content": "",
            "message": f"Collection '{DEFAULT_COLLECTION}' not found.",
        }

    if collection.count() == 0:
        return {
            "source": "none",
            "content": "",
            "message": "Vector DB is empty.",
        }

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
    )

    if results["documents"] and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)

        return {
            "source": "vectordb",
            "content": docs[0],  # Best match
            "all_results": [
                {"content": d, "metadata": m}
                for d, m in zip(docs, metas)
            ],
        }

    return {
        "source": "none",
        "content": "",
        "message": "No matching documents found.",
    }


def get_status() -> dict:
    """Get the current status of the vector DB."""
    if not CHROMADB_AVAILABLE:
        return {
            "available": False,
            "message": "ChromaDB not installed",
        }

    db_path = get_db_path()
    if not db_path.exists():
        return {
            "available": True,
            "initialized": False,
            "message": "ChromaDB available but DB not yet initialized",
        }

    client = chromadb.PersistentClient(path=str(db_path))
    try:
        collection = client.get_collection(name=DEFAULT_COLLECTION)
        return {
            "available": True,
            "initialized": True,
            "document_count": collection.count(),
            "path": str(db_path),
        }
    except Exception:
        return {
            "available": True,
            "initialized": False,
        }


if __name__ == "__main__":
    status = get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))
