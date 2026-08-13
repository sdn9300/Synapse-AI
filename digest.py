"""
Weekly Digest & Synthesis Agent for SecondSelf (Module M3).
Aggregates and synthesizes wiki notes into weekly digest reports in wiki/synthesis/YYYY-Www.md.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from lib.storage import read_wiki_notes, WIKI_DIR
from lib.llm import call_llm


def generate_weekly_digest() -> str:
    """Generate weekly synthesis digest page in wiki/synthesis/YYYY-Www.md."""
    notes = read_wiki_notes()
    if not notes:
        print("No wiki notes found for digest synthesis.")
        return ""

    now = datetime.now(timezone.utc)
    year, week_num, _ = now.isocalendar()
    digest_filename = f"{year}-W{week_num:02d}.md"

    synthesis_dir = WIKI_DIR / "synthesis"
    synthesis_dir.mkdir(parents=True, exist_ok=True)
    digest_path = synthesis_dir / digest_filename

    # Group notes by PARA
    by_para: Dict[str, List[str]] = {"Projects": [], "Areas": [], "Resources": [], "Archives": []}
    for n in notes:
        category = n.para if n.para in by_para else "Resources"
        by_para[category].append(f"- **[{n.id}]**: {n.summary}")

    notes_summary_text = ""
    for para, items in by_para.items():
        if items:
            notes_summary_text += f"\n### {para} ({len(items)} notes)\n" + "\n".join(items) + "\n"

    # LLM Synthesis
    system_prompt = (
        "You are SecondSelf's AI Synthesis Agent. Create an executive weekly digest report "
        "summarizing the user's accumulated knowledge base, highlighting key themes, "
        "and noting connections across Projects, Areas, Resources, and Archives."
    )
    prompt = f"Synthesize this week's knowledge vault entries into a structured Markdown digest report:\n{notes_summary_text}"

    llm_synthesis = call_llm(prompt, system_prompt=system_prompt)

    if not llm_synthesis:
        llm_synthesis = (
            "## Weekly Summary\n"
            f"This week, **{len(notes)} knowledge notes** were captured and processed across the PARA framework.\n\n"
            f"### Categorization Breakdown\n"
            f"- **Projects:** {len(by_para['Projects'])} notes\n"
            f"- **Areas:** {len(by_para['Areas'])} notes\n"
            f"- **Resources:** {len(by_para['Resources'])} notes\n"
            f"- **Archives:** {len(by_para['Archives'])} notes\n"
        )

    digest_content = (
        f"# SecondSelf Weekly Digest — {year}-W{week_num:02d}\n\n"
        f"**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S UTC')}  \n"
        f"**Total Active Notes:** {len(notes)}\n\n"
        f"---"
        f"\n\n{llm_synthesis}\n\n"
        f"## Vault Note Catalog\n"
        f"{notes_summary_text}"
    )

    with open(digest_path, "w", encoding="utf-8") as f:
        f.write(digest_content)

    print(f"Weekly Digest generated successfully -> wiki/synthesis/{digest_filename}")
    return str(digest_path)


if __name__ == "__main__":
    generate_weekly_digest()
