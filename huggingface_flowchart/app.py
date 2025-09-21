"""
Streamlit app: Hugging Face + Flowchart generator

Flow:
- Upload files (pdf, docx, txt)
- Extract text
- Ask a HF model to extract ordered clauses/steps (numbered list)
- Render a flowchart image using graphviz
- Display image in Streamlit

Set environment variable: HF_API_KEY (your Hugging Face API token)
"""

import os
import io
import re
import tempfile
from typing import List, Optional

import streamlit as st
from huggingface_hub import InferenceApi
from PyPDF2 import PdfReader
import docx
from graphviz import Digraph

# ---------- Helpers: text extraction ----------
def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text_chunks = []
    for p in reader.pages:
        try:
            text_chunks.append(p.extract_text() or "")
        except Exception:
            # best-effort: continue
            continue
    return "\n".join(text_chunks)

def extract_text_from_docx(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    doc = docx.Document(tmp_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    try:
        os.remove(tmp_path)
    except Exception:
        pass
    return "\n".join(paragraphs)

def extract_text_from_txt(file_bytes: bytes) -> str:
    return file_bytes.decode(errors="ignore")

def extract_text_from_uploaded_file(uploaded_file) -> str:
    data = uploaded_file.read()
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(data)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(data)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(data)
    else:
        # try to be forgiving
        try:
            return extract_text_from_txt(data)
        except Exception:
            return ""

# ---------- Helpers: call HF to extract steps ----------
def call_hf_extract_steps(text: str, hf_token: Optional[str]) -> Optional[str]:
    """
    Call Hugging Face Inference API to extract numbered steps/clauses.
    Returns model text (expected to be a numbered list). If hf_token is None,
    returns None (caller should use fallback).
    """
    if not hf_token:
        return None

    # Choose a reasonably capable instruction-following model available on HF.
    # You can change this to another model you prefer.
    model_id = "google/flan-t5-large"  # good instruction-following smaller model

    inference = InferenceApi(repo_id=model_id, token=hf_token)

    prompt = (
        "Extract the main ordered clauses/sections from the document. "
        "For each, return a short heading and a one-line summary. "
        "Format each item like this:\n"
        "1. Heading — one line summary\n"
        "2. Heading — one line summary\n"
        "...\n\n"
        "Document text:\n"
        + text[:60000]
    )


    try:
        # `inference` returns a dict-like object or plain text depending on model.
        resp = inference(prompt)
        # resp might be string or list/dict. Make safe:
        if isinstance(resp, str):
            return resp.strip()
        elif isinstance(resp, dict) and "generated_text" in resp:
            return resp["generated_text"].strip()
        elif isinstance(resp, list) and len(resp) and isinstance(resp[0], dict) and "generated_text" in resp[0]:
            return resp[0]["generated_text"].strip()
        else:
            # try string conversion fallback
            return str(resp).strip()
    except Exception as e:
        st.warning(f"Hugging Face inference failed: {e}")
        return None

# ---------- Helpers: fallback simple parser ----------
def fallback_extract_numbered_items(text: str) -> List[dict]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    items = []
    for idx, ln in enumerate(lines):
        # treat numbered or Clause/Section lines as heading
        if re.match(r"^\d+[\.\)]\s+", ln) or re.match(r"^Clause\s+\d+", ln, re.I):
            summary = lines[idx+1].strip() if idx+1 < len(lines) else ""
            items.append({"heading": ln, "summary": summary})
    return items
    # 2) look for headings in ALL CAPS or lines with 'Clause' words in them
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    headings = [ln for ln in lines if len(ln.split()) <= 8 and (ln.isupper() or re.search(r"\bClause\b|\bSection\b|\bPayment\b|\bTermination\b", ln, re.I))]
    if headings:
        return headings[:50]

    # 3) fallback: take top 10 non-empty lines (heuristic)
    brief = []
    for ln in lines:
        if len(brief) >= 10:
            break
        if len(ln) > 20:  # prefer lines with substance
            brief.append(ln if len(ln) <= 200 else ln[:200] + "...")
    if brief:
        return brief

    # 4) last fallback: chunk text into pseudo-paragraphs
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    return [p for p in paras[:10]]

#---------- Helpers: parse HF output into list ----------
def parse_numbered_list(model_text: str) -> List[dict]:
    items = []
    for line in model_text.splitlines():
        ln = line.strip()
        if not ln:
            continue
        ln = re.sub(r"^\s*\d+[\.\)\-:]\s*", "", ln)

        if "—" in ln:  # em-dash
            parts = ln.split("—", 1)
        elif "-" in ln:
            parts = ln.split("-", 1)
        else:
            parts = [ln, ""]

        heading = parts[0].strip()
        summary = parts[1].strip() if len(parts) > 1 else ""
        items.append({"heading": heading, "summary": summary})
    return items


# ---------- Helpers: flowchart generation ----------
def build_flowchart_image(items: List[dict], title: str = "Document Flowchart") -> bytes:
    """
    Vertical flowchart with wrapped text, bright colors, termination highlighting,
    and SVG output for zoomable/scrollable display.
    """
    from graphviz import Digraph

    # Helper to wrap text at a given character limit
    def wrap_text(text: str, max_chars: int = 40) -> str:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= max_chars:
                current_line = (current_line + " " + word).strip()
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)

    # Escape special Graphviz characters
    def escape_gv(text: str) -> str:
        text = text or ""
        text = text.replace('"', r'\"').replace('{', r'\{').replace('}', r'\}').replace("—", "-").replace("\r", "")
        return text

    dot = Digraph(format="svg")
    dot.attr(rankdir="TB", fontsize="14")
    # Increase width and height: "width,height!" and ratio=fill
    dot.attr(size="13,40!", ratio="fill")  
    dot.attr("node", fontname="Helvetica", fontsize="12", style="filled", shape="rectangle", margin="0.3,0.2")

    # Bright color palette
    colors = ["#FFB347", "#FF6961", "#77DD77", "#84B6F4", "#FFD1DC", "#FFA07A", "#DDA0DD", "#FDFD96"]

    # Title node
    safe_title = wrap_text(escape_gv(title), 50)
    dot.node("TITLE", label=safe_title, shape="oval", style="filled", fillcolor="#87CEEB", fontsize="60")

    prev_id = "TITLE"

    for idx, item in enumerate(items, start=1):
        node_id = f"N{idx}"
        heading = wrap_text(escape_gv(item.get("heading", "")), 30)
        summary = wrap_text(escape_gv(item.get("summary", "")), 40)
        label = f"{heading}\n({summary})" if summary else heading

        # Highlight termination nodes
        color = "#FF6347" if "termination" in summary.lower() else colors[idx % len(colors)]

        dot.node(
            node_id,
            label=label,
            style="rounded,filled",
            fillcolor=color,
            fontsize="60",
            fontcolor="black",
            width="25",
        )
        dot.edge(prev_id, node_id)
        prev_id = node_id

    # End node
    dot.node("END", label="End", shape="oval", style="filled", fillcolor="red", fontcolor="white", fontsize="60")
    dot.edge(prev_id, "END")

    return dot.pipe(format="svg")


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Flowchart Generator (HF + Streamlit)", layout="wide")
st.title("🧭 Flowchart Generator — Upload docs, get a flowchart image")

st.markdown(
    "Upload a PDF, DOCX, or TXT. The app will extract text, ask a Hugging Face model to identify ordered clauses/steps, "
    "and render a flowchart image. If HF key isn't set, a local fallback parser tries its best."
)

hf_token = os.getenv("HF_API_KEY")
if not hf_token:
    st.info("No Hugging Face API key found in `HF_API_KEY`. The app will use a local heuristic fallback parser. "
            "Set HF_API_KEY for better extraction.")

uploaded_files = st.file_uploader("Upload document(s) (you can upload multiple)", accept_multiple_files=True, type=['pdf', 'docx', 'txt'])
user_title = st.text_input("Flowchart title (optional)", value="Document Flowchart")
process_btn = st.button("Generate flowchart image")

if process_btn:
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    else:
        full_text_pieces = []
        progress_text = st.empty()
        for i, uf in enumerate(uploaded_files, start=1):
            progress_text.text(f"Extracting text from {uf.name} ({i}/{len(uploaded_files)})...")
            try:
                txt = extract_text_from_uploaded_file(uf)
                if not txt.strip():
                    st.warning(f"No text found in {uf.name}.")
                full_text_pieces.append(f"--- {uf.name} ---\n" + txt)
            except Exception as e:
                st.error(f"Failed to extract from {uf.name}: {e}")

        document_text = "\n\n".join(full_text_pieces)
        progress_text.text("Requesting clause extraction (Hugging Face)..." if hf_token else "Using local heuristic extraction...")

        model_output = call_hf_extract_steps(document_text, hf_token) if hf_token else None

        if model_output:
            st.subheader("Raw model output (for debugging)")
            st.code(model_output[:5000])  # show first 5000 chars for sanity
            items = parse_numbered_list(model_output)
        else:
            st.info("Using fallback parsing to find clauses/steps.")
            items = fallback_extract_numbered_items(document_text)

        if not items:
            st.error("Could not extract any items / clauses. Try uploading a different file or use a simpler document.")
        else:
            st.success(f"Found {len(items)} item(s). Rendering flowchart...")
            # show items
            with st.expander("Extracted steps / clauses (click to view)"):
                for idx, it in enumerate(items, start=1):
                    st.markdown(f"**{idx}.** {it}")

            try:
                svg_bytes = build_flowchart_image(items, title=user_title)  # returns SVG now
                svg_text = svg_bytes.decode("utf-8")  # convert bytes → string

                # Render in a scrollable container
                st.components.v1.html(
                    f'<div style="width:100%; height:600px; overflow:auto; border:1px solid #ccc;">{svg_text}</div>',
                    height=600,
                )

                # Provide download (optional)
                st.download_button("Download flowchart SVG", data=svg_bytes, file_name="flowchart.svg", mime="image/svg+xml")

            except Exception as e:
                st.error(f"Failed to render flowchart image: {e}")

st.markdown("---")
st.caption("Tip: for best extraction, upload documents that have clear numbered clauses, headings, or short paragraphs. Hugging Face model helps extract structure; fallback parser is heuristic.")
