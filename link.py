"""Embedding-based auto-linker for SecondSelf."""

import sys
from typing import Dict, Set

from lib.embeddings import ensure_embeddings, cosine_similarity
from lib.markdown import extract_related_links, extract_wikilinks, remove_related_link_lines
from lib.storage import read_wiki_notes, write_wiki_note


SIMILARITY_THRESHOLD = 0.75


def process_auto_linking(threshold: float = SIMILARITY_THRESHOLD) -> int:
    """Refresh embeddings and rebuild generated links across all wiki notes."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")

    notes = read_wiki_notes()
    if not notes:
        print("No wiki notes found to auto-link.")
        return 0

    print(f"Loaded {len(notes)} wiki notes for vector auto-linking.")
    embeddings = ensure_embeddings(notes)

    desired: Dict[str, Set[str]] = {note.id: set() for note in notes}
    note_ids = {note.id for note in notes}
    for index, note_a in enumerate(notes):
        vector_a = embeddings.get(note_a.id)
        if not vector_a:
            continue
        for note_b in notes[index + 1:]:
            vector_b = embeddings.get(note_b.id)
            if not vector_b:
                continue
            score = cosine_similarity(vector_a, vector_b)
            if score >= threshold:
                desired[note_a.id].add(note_b.id)
                desired[note_b.id].add(note_a.id)
                print(f"  -> Connected [[{note_a.id}]] <===> [[{note_b.id}]] (similarity: {score:.3f})")

    changed_links = 0
    for note in notes:
        old_auto = extract_related_links(note.body)
        manual_links = (set(note.links) - old_auto) | (extract_wikilinks(note.body) - old_auto)
        manual_links &= note_ids - {note.id}
        new_links = manual_links | desired[note.id]
        if new_links != set(note.links) or old_auto != desired[note.id]:
            changed_links += len(new_links - set(note.links))
            clean_body = remove_related_link_lines(note.body)
            related_lines = [f"Related Note: [[{target}]]" for target in sorted(desired[note.id])]
            body = clean_body
            if related_lines:
                body = (body + "\n\n" if body else "") + "\n".join(related_lines)
            note.links = sorted(new_links)
            note.body = body
            write_wiki_note(note)

    print(f"Auto-linking complete. Added {changed_links} new cross-references.")
    return changed_links


if __name__ == "__main__":
    threshold_arg = SIMILARITY_THRESHOLD
    if len(sys.argv) > 1:
        try:
            threshold_arg = float(sys.argv[1])
        except ValueError:
            print("Invalid threshold; using default 0.75.")
    process_auto_linking(threshold=threshold_arg)
