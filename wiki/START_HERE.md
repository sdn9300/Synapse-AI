---
title: SecondSelf Vault
tags:
  - secondself
  - start-here
---

# SecondSelf Vault

This folder is the Obsidian-facing view of the SecondSelf knowledge system.

## Start here

- [[1ed3b5b3]] - Problem statement and project purpose
- [[e476c9f1]] - System architecture
- [[fdc70e24]] - Mission and implementation roadmap
- [[3d262007]] - Vault schema and conventions
- [[health_report]] - Current vault health report
- [[2026-W32]] - Weekly synthesis

## Vault layout

- Projects/ - Active project material
- Areas/ - Ongoing areas of responsibility
- Resources/ - External references and learning material
- Archives/ - Completed or inactive material
- synthesis/ - Generated health reports and weekly digests

## How to add knowledge

The reliable ingestion workflow is run from the repository root:

    cd "C:\\My Projects\\Masai Live Docs\\Second_Brain"
    python capture.py note "Your note"
    python pipeline.py process

You can also capture URLs and files:

    python capture.py link "https://example.com" --notes "Why it matters"
    python capture.py file ".\\path\\to\\document.pdf"

The pipeline classifies new captures, refreshes links, and rebuilds the graph. Run python lint.py after maintenance.

### Obsidian Inbox

- Create or paste a Markdown note directly inside Inbox/.
- Optional frontmatter fields are para, tags, and summary; leave them blank for automatic classification.
- From the repository root, run:

      python pipeline.py process

- The pipeline preserves the original in raw/, generates the PARA note, and moves the Inbox copy to Inbox/Processed/.
- Do not edit files in Inbox/Processed/; edit the generated PARA page or capture a new Inbox note.
- _template.md is a starter template and is ignored by ingestion.

## Editing rules

- Treat raw/ as the immutable source record; it is outside this Obsidian vault.
- The Markdown pages in this vault are generated/maintained by SecondSelf.
- Obsidian backlinks, search, tags, properties, and graph view work directly with these pages.
- Generated note filenames are short IDs, so use the summary and backlinks for navigation.
- The project currently has a sparse sample graph; orphan pages are reported honestly by the health report.

## Obsidian actions

- Use the left file explorer to browse PARA folders.
- Use the backlinks panel to see related notes.
- Use the graph view for the current vault topology.
- Use the command palette to run normal Obsidian actions.
- Use the repository terminal for Python capture and maintenance commands.

