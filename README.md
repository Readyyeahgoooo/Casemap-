# Casemap-

Casemap- is a dependency-light MVP for turning `Contract big .docx` into a legal GraphRAG knowledge map. It builds a typed graph of sections, concepts, statutes, and cases; creates retrieval chunks; reranks search results with graph context; and writes an interactive HTML map you can open locally.

## What It Produces

- `graph.json`: knowledge graph nodes and edges
- `chunks.json`: retrieval chunks with lexical and graph metadata
- `manifest.json`: build summary
- `sample_queries.json`: example reranked retrieval output
- `knowledge_map.html`: interactive local viewer

## Quick Start

```bash
cd /Users/puiyuenwong/PolymarketCorrelationStrategy/Casemap-
PYTHONPATH=src python3 -m casemap build \
  --input "/Users/puiyuenwong/Desktop/桌面 - Pui的MacBook Air/Real uni (1)/PCLL 2023 /Haldanes demo try /Album /Contract big .docx" \
  --output-dir artifacts/contract_big
```

Open `artifacts/contract_big/knowledge_map.html` in a browser.

Run a reranked query:

```bash
cd /Users/puiyuenwong/PolymarketCorrelationStrategy/Casemap-
PYTHONPATH=src python3 -m casemap query \
  --graph artifacts/contract_big/graph.json \
  --chunks artifacts/contract_big/chunks.json \
  --question "When can a third party enforce a contract term?" \
  --top-k 5
```

## Design

This MVP avoids external Python dependencies so it can run cleanly in a minimal environment:

- `.docx` parsing uses the Office XML inside the archive
- graph building uses heuristics over headings, concept labels, statutes, and case references
- retrieval uses a TF-IDF style lexical score
- reranking boosts graph neighbors, cited authorities, and structurally central nodes
- the viewer is a static HTML file with inline data and client-side interactions

## Project Layout

```text
Casemap-/
  src/casemap/
    __init__.py
    __main__.py
    docx_parser.py
    graphrag.py
    viewer.py
  artifacts/
  pyproject.toml
  README.md
```

## Next Step Ideas

- Replace heuristic extraction with LLM-assisted triplet/entity extraction
- Persist the graph in Neo4j, Oracle Database, or another graph-capable backend
- Add embeddings and a cross-encoder reranker
- Layer in answer generation once your cloud backend is ready
