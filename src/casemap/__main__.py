from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graphrag import RerankedRetriever, build_artifacts


def build_command(args: argparse.Namespace) -> int:
    manifest = build_artifacts(docx_path=args.input, output_dir=args.output_dir)
    print(json.dumps(manifest, indent=2))
    return 0


def query_command(args: argparse.Namespace) -> int:
    retriever = RerankedRetriever.from_files(args.graph, args.chunks)
    results = retriever.search(args.question, top_k=args.top_k)
    if args.as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    for result in results:
        print(f"[{result['rank']}] {result['title']} | {result['section']} | score={result['score']}")
        print(result["text"])
        if result["citations"]:
            print("Citations:", "; ".join(result["citations"]))
        if result["graph_neighbors"]:
            print("Graph neighbors:", "; ".join(result["graph_neighbors"]))
        print()
    return 0


def parser() -> argparse.ArgumentParser:
    main_parser = argparse.ArgumentParser(description="Casemap MVP GraphRAG pipeline")
    subparsers = main_parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build graph and retrieval artifacts")
    build_parser.add_argument("--input", required=True, help="Path to the source .docx file")
    build_parser.add_argument("--output-dir", required=True, help="Directory for generated artifacts")
    build_parser.set_defaults(func=build_command)

    query_parser = subparsers.add_parser("query", help="Run reranked retrieval over built artifacts")
    query_parser.add_argument("--graph", required=True, help="Path to graph.json")
    query_parser.add_argument("--chunks", required=True, help="Path to chunks.json")
    query_parser.add_argument("--question", required=True, help="Question to search for")
    query_parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    query_parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output")
    query_parser.set_defaults(func=query_command)

    return main_parser


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
