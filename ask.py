"""Retrieval-augmented search over the SecondSelf wiki vault."""

import argparse
from typing import List

from lib.embeddings import cosine_similarity, embed_text, ensure_embeddings
from lib.llm import synthesize_answer
from lib.models import AskResult, WikiNote
from lib.storage import read_wiki_notes


MIN_RELEVANCE_SCORE = 0.15
DEFAULT_TOP_K = 5


def ask(question: str, top_k: int = DEFAULT_TOP_K) -> AskResult:
    """Retrieve relevant notes and synthesize a grounded answer."""
    question = (question or "").strip()
    if not question:
        return AskResult(answer="Please provide a non-empty question.", sources=[])
    if top_k <= 0:
        return AskResult(answer="top_k must be greater than zero.", sources=[])

    notes = read_wiki_notes()
    if not notes:
        return AskResult(answer="Your SecondSelf brain vault is currently empty.", sources=[])

    embeddings = ensure_embeddings(notes)
    question_vector = embed_text(question)
    ranked = []
    for note in notes:
        vector = embeddings.get(note.id)
        if vector:
            ranked.append((cosine_similarity(question_vector, vector), note))
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    top_items = ranked[:top_k]

    if not top_items or top_items[0][0] < MIN_RELEVANCE_SCORE:
        return AskResult(
            answer="I don't have notes about that in your second brain.",
            sources=[],
        )

    sources = [
        {
            "id": note.id,
            "summary": note.summary,
            "para": note.para,
            "relevance_score": round(score, 3),
        }
        for score, note in top_items
    ]
    context = [
        {
            "id": note.id,
            "summary": note.summary,
            "para": note.para,
            "body": note.body[:2000],
        }
        for _, note in top_items
    ]
    return AskResult(answer=synthesize_answer(context, question), sources=sources)


def main() -> None:
    parser = argparse.ArgumentParser(description="SecondSelf Ask-Your-Brain RAG engine")
    parser.add_argument("question", type=str, help="Natural-language question")
    parser.add_argument("--top_k", type=int, default=DEFAULT_TOP_K)
    args = parser.parse_args()
    result = ask(args.question, top_k=args.top_k)
    print("\n=== ANSWER ===")
    print(result.answer)
    print("\n=== SOURCES CITED ===")
    for source in result.sources:
        print(f" - [{source['id']}] ({source['para']}) Relevance: {source['relevance_score']} | {source['summary']}")


if __name__ == "__main__":
    main()
