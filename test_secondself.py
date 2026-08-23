"""Unit and integration checks for SecondSelf."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ask import ask
from build_graph import process_build_graph
from capture import capture_link, capture_note
from lib.embeddings import cosine_similarity, embed_text
from lib.markdown import extract_frontmatter, extract_wikilinks, strip_frontmatter
from lib.models import AskResult
from lib.storage import content_hash, generate_capture_id, read_wiki_notes
from mcp_server import get_wiki_page, search_second_brain
import obsidian_inbox


class TestSecondSelfSuite(unittest.TestCase):
    def test_capture_id_format(self):
        capture_id = generate_capture_id()
        self.assertRegex(capture_id, r"^\d{4}-\d{2}-\d{2}_[0-9a-f]{8}$")

    def test_content_hash(self):
        self.assertEqual(content_hash("Hello World"), content_hash("Hello World"))
        self.assertNotEqual(content_hash("Hello World"), content_hash("Different Text"))

    def test_fallback_embedding_is_stable(self):
        import lib.embeddings as embeddings
        with patch.object(embeddings, "_EMBEDDING_MODEL", "FALLBACK"):
            first = embed_text("stable fallback vector")
            second = embed_text("stable fallback vector")
        self.assertEqual(first, second)
        self.assertEqual(len(first), 384)

    def test_cosine_similarity_identical(self):
        with patch("lib.embeddings._EMBEDDING_MODEL", "FALLBACK"):
            self.assertAlmostEqual(cosine_similarity(embed_text("same"), embed_text("same")), 1.0, places=6)

    def test_wikilink_parser_ignores_code_examples(self):
        markdown = "Prose [[real-id]]\n\n" + chr(96) * 3 + "python\n[[target-id]]\n" + chr(96) * 3
        self.assertEqual(extract_wikilinks(markdown), {"real-id"})

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            capture_note("")
        with self.assertRaises(ValueError):
            capture_link("not-a-url")

    def test_frontmatter_parser(self):
        markdown = "---\npara: Areas\ntags: [python, notes]\n---\n\nBody text"
        frontmatter, body = extract_frontmatter(markdown)
        self.assertEqual(frontmatter["para"], "Areas")
        self.assertEqual(frontmatter["tags"], ["python", "notes"])
        self.assertEqual(strip_frontmatter(markdown).strip(), "Body text")
        self.assertEqual(extract_frontmatter("plain text"), ({}, "plain text"))

    def test_obsidian_inbox_import_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inbox = root / "wiki" / "Inbox"
            processed = inbox / "Processed"
            raw = root / "raw"
            data = root / "data"
            static = root / "static"
            inbox.mkdir(parents=True)
            note = inbox / "idea.md"
            note.write_text(
                "---\npara: Resources\ntags: [inbox]\nsummary: An inbox idea\n---\n\n"
                "A useful idea captured from Obsidian.\n",
                encoding="utf-8",
            )
            with patch.object(obsidian_inbox, "PROJECT_ROOT", root), \
                 patch.object(obsidian_inbox, "INBOX_DIR", inbox), \
                 patch.object(obsidian_inbox, "PROCESSED_DIR", processed), \
                 patch("lib.storage.RAW_DIR", raw), \
                 patch("lib.storage.WIKI_DIR", root / "wiki"), \
                 patch("lib.storage.DATA_DIR", data), \
                 patch("lib.storage.STATIC_DIR", static), \
                 patch("lib.storage.INDEX_FILE", data / "index.json"):
                self.assertEqual(obsidian_inbox.ingest_obsidian_inbox(), 1)
                self.assertFalse(note.exists())
                self.assertEqual(len(list(processed.glob("*.md"))), 1)
                self.assertEqual(len(list(raw.iterdir())), 1)
                self.assertEqual(obsidian_inbox.ingest_obsidian_inbox(), 0)

    def test_read_wiki_notes(self):
        self.assertIsInstance(read_wiki_notes(), list)

    def test_graph_building_has_unique_edges(self):
        graph = process_build_graph()
        pairs = {(edge["source"], edge["target"]) for edge in graph["edges"]}
        self.assertEqual(len(pairs), len(graph["edges"]))
        self.assertEqual(graph["metadata"]["edge_count"], len(graph["edges"]))

    def test_rag_search_contract(self):
        result = ask("What is SecondSelf?", top_k=2)
        self.assertIsInstance(result, AskResult)
        self.assertTrue(result.answer)
        self.assertLessEqual(len(result.sources), 2)
        self.assertEqual(ask("question", top_k=0).sources, [])

    def test_mcp_server_tools(self):
        search_result = search_second_brain("SecondSelf goals")
        self.assertIn("answer", search_result)
        self.assertIn("sources", search_result)
        first_note = read_wiki_notes()[0]
        self.assertEqual(get_wiki_page(first_note.id)["id"], first_note.id)


if __name__ == "__main__":
    unittest.main()
