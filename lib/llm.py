"""
LLM Generation & Classification Provider for SecondSelf (Phase 2).
Decoupled generation provider interfacing with Groq API (Llama 3.1 8B Instant)
with intelligent heuristic fallback.
"""

import os
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


def call_llm(prompt: str, system_prompt: str = "") -> str:
    """Call Groq API for text generation using OpenAI-compatible or Groq client."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if api_key and api_key != "your_groq_api_key_here":
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt or "You are an AI Second Brain assistant."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
                "max_tokens": 1000,
            }
            resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"Groq API returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"Warning: Groq API call failed: {e}")

    # Fallback response generation if API key not available or request failed
    return ""


def classify_content(text: str, source_type: str = "note") -> Dict[str, Any]:
    """
    Classify raw captured text into PARA categories (Projects, Areas, Resources, Archives),
    extract tags, and generate a one-line summary.
    """
    system_prompt = (
        "You are SecondSelf's AI Librarian. Analyze the provided note/document text "
        "and classify it according to the PARA method.\n"
        "Categories must be strictly one of: ['Projects', 'Areas', 'Resources', 'Archives'].\n"
        "Return ONLY a JSON object with keys:\n"
        '{"para": "Projects|Areas|Resources|Archives", "tags": ["tag1", "tag2"], "summary": "One-line summary"}'
    )
    prompt = f"Classify this captured content:\n\n{text[:3000]}"

    llm_output = call_llm(prompt, system_prompt=system_prompt)

    if llm_output:
        try:
            # Try to find JSON block in output
            json_match = re.search(r"\{.*\}", llm_output, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                para = parsed.get("para", "Resources")
                if para not in ["Projects", "Areas", "Resources", "Archives"]:
                    para = "Resources"
                raw_tags = parsed.get("tags", [])
                if isinstance(raw_tags, str):
                    raw_tags = [raw_tags]
                tags = [str(tag).strip().lower().replace(" ", "-") for tag in raw_tags if str(tag).strip()]
                summary = str(parsed.get("summary", "")).strip() or text[:100].replace("\n", " ") + "..."
                return {"para": para, "tags": tags, "summary": summary}
        except Exception as e:
            print(f"Warning: Failed to parse LLM JSON output: {e}")

    # Heuristic Fallback Classifier
    text_lower = text.lower()
    if any(k in text_lower for k in ["project", "roadmap", "implementation", "mission", "architecture", "sprint"]):
        para = "Projects"
    elif any(k in text_lower for k in ["devops", "agentic", "skill", "career", "responsibility", "learning"]):
        para = "Areas"
    elif any(k in text_lower for k in ["http", "github", "huggingface", "paper", "reference", "doc", "link"]):
        para = "Resources"
    else:
        para = "Archives"

    # Extract tags
    extracted_tags = []
    for kw in ["ai", "rag", "embeddings", "devops", "groq", "streamlit", "python", "graph", "architecture", "secondbrain"]:
        if kw in text_lower:
            extracted_tags.append(kw)
    if not extracted_tags:
        extracted_tags = [source_type, "note"]

    # One line summary
    first_line = text.strip().split("\n")[0]
    summary = first_line[:120] if len(first_line) > 10 else text.strip()[:120]

    return {
        "para": para,
        "tags": extracted_tags,
        "summary": summary,
    }


def synthesize_answer(context_notes: List[Dict[str, Any]], question: str) -> str:
    """Synthesize RAG answer using retrieved note contexts."""
    formatted_notes = ""
    for n in context_notes:
        formatted_notes += f"--- Note [{n['id']}] ({n['para']}) ---\nSummary: {n['summary']}\nBody: {n['body']}\n\n"

    system_prompt = (
        "You are SecondSelf, answering questions from the user's personal knowledge base.\n"
        "Use ONLY the provided notes context. If the answer is not in the notes, say: "
        "'I don't have notes about that.'\n"
        "Cite source notes inline as [note-id]."
    )
    prompt = f"Context Notes:\n{formatted_notes}\nQuestion: {question}\nAnswer:"

    llm_output = call_llm(prompt, system_prompt=system_prompt)

    if llm_output:
        return llm_output

    # Heuristic synthesis fallback
    if not context_notes:
        return "I don't have notes about that in my second brain."

    synthesis = f"Based on your notes, here is what I found regarding '{question}':\n\n"
    for n in context_notes:
        synthesis += f"- **[{n['id']}]** ({n['para']}): {n['summary']}\n"
    return synthesis
