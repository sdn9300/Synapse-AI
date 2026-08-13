"""Vault integrity, orphan, and near-duplicate audit."""

from typing import Any, Dict, List, Tuple

from lib.embeddings import cosine_similarity, ensure_embeddings
from lib.markdown import extract_wikilinks
from lib.storage import WIKI_DIR, read_wiki_notes


def run_vault_lint() -> Dict[str, Any]:
    notes = read_wiki_notes()
    note_ids = {note.id for note in notes}
    broken_links: List[Tuple[str, str]] = []
    incoming = {note.id: 0 for note in notes}
    outgoing = {note.id: 0 for note in notes}

    for note in notes:
        targets = set(note.links) | extract_wikilinks(note.body)
        for target in targets:
            outgoing[note.id] += 1
            if target in note_ids:
                incoming[target] += 1
            else:
                broken_links.append((note.id, target))

    orphans = sorted(note_id for note_id in note_ids if incoming[note_id] == 0 and outgoing[note_id] == 0)
    embeddings = ensure_embeddings(notes)
    near_duplicates: List[Tuple[str, str, float]] = []
    for index, first in enumerate(notes):
        for second in notes[index + 1:]:
            first_vector = embeddings.get(first.id)
            second_vector = embeddings.get(second.id)
            if first_vector and second_vector:
                score = cosine_similarity(first_vector, second_vector)
                if score >= 0.92:
                    near_duplicates.append((first.id, second.id, round(score, 3)))

    synthesis_dir = WIKI_DIR / "synthesis"
    synthesis_dir.mkdir(parents=True, exist_ok=True)
    report_path = synthesis_dir / "health_report.md"
    lines = [
        "# SecondSelf Vault Health and Lint Report",
        "",
        "- Total Wiki Pages: {}".format(len(notes)),
        "- Broken Wikilinks: {}".format(len(broken_links)),
        "- Orphan Pages: {}".format(len(orphans)),
        "- Near-Duplicate Pairs: {}".format(len(near_duplicates)),
        "",
        "## Broken Wikilinks",
    ]
    lines.extend(
        ["- [[{}]] points to missing target [[{}]]".format(source, target) for source, target in broken_links]
        or ["- No broken wikilinks detected."]
    )
    lines.append("")
    lines.append("## Orphan Pages")
    lines.extend(["- [[{}]] has no incoming or outgoing connections.".format(note_id) for note_id in orphans] or ["- No orphan pages detected."])
    lines.append("")
    lines.append("## Near-Duplicate Notes (similarity >= 0.92)")
    lines.extend(
        ["- [[{}]] and [[{}]] are {:.1f}% similar.".format(first, second, score * 100) for first, second, score in near_duplicates]
        or ["- No high-similarity duplicate pages detected."]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Lint complete -> {}".format(report_path))
    return {
        "total_notes": len(notes),
        "broken_links": broken_links,
        "orphans": orphans,
        "near_duplicates": near_duplicates,
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    run_vault_lint()
