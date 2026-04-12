"""Act 2: Embeddings — What they are, and an interactive 3D playground."""

from typing import Any

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from frontend.utils import api
from frontend.utils.theme import ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED, IST_BLUE
from sklearn.decomposition import PCA

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🔢 Embeddings</h1>", unsafe_allow_html=True)
st.caption("Turn sentences into vectors and watch meaning come alive in 3D space.")

st.divider()

# ---------------------------------------------------------------------------
# Educational intro
# ---------------------------------------------------------------------------
st.subheader("📖 What are Embeddings?")

intro_col1, intro_col2 = st.columns(2)

with intro_col1:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #009de0; margin-top: 0;">🔢 Vectors of Meaning</h4>
            <p>An <b>embedding</b> is a list of numbers (a vector) that captures the <em>meaning</em>
            of a piece of text. A neural network reads the text and outputs, for example, 3072 numbers —
            one per dimension. Similar texts produce similar vectors.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with intro_col2:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #00c896; margin-top: 0;">📐 Cosine Similarity</h4>
            <p>To compare two embeddings we measure the <b>angle</b> between them — cosine similarity.
            A score of <b>1.0</b> means identical meaning; <b>0.0</b> means completely unrelated.
            This is how the knowledge base finds the most relevant chunks for your question.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="card">
        <h4 style="color: #f59e0b; margin-top: 0;">🔭 Why 3D?</h4>
        <p>Our embeddings live in <b>3072 dimensions</b> — impossible to visualise directly.
        We use <b>PCA</b> (Principal Component Analysis) to squash those 3072 numbers down to 3,
        preserving as much of the original structure as possible.
        Points that are close together in 3D were close together in 3072D.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Haystack pipeline section
# ---------------------------------------------------------------------------
st.subheader("⚙️ Under the Hood — The Haystack Pipeline")
st.markdown(
    """
    This page calls the backend's **`embed_text`** endpoint, which runs a one-step
    [Haystack](https://haystack.deepset.ai/) pipeline. Haystack is an open-source framework
    for building LLM-powered applications — you wire together **components** into a **pipeline**
    and Haystack handles data flow between them.
    Here the pipeline has a single component: it takes your raw text string, sends it to
    **Azure OpenAI**, and returns a 3 072-dimensional embedding vector.
    """
)

st.markdown(
    """
    <div style="overflow-x: auto; padding: 16px 0 4px;">
    <svg viewBox="0 0 530 205" xmlns="http://www.w3.org/2000/svg"
         style="width:100%; max-width:560px; display:block; margin:0 auto; font-family:sans-serif;">
      <defs>
        <marker id="p2ah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <style>
          @keyframes p2flow   { to { stroke-dashoffset: -13; } }
          @keyframes p2glow-a { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes p2glow-b { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .p2fl   { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                    animation: p2flow 0.5s linear infinite; }
          .p2gnc  { fill:rgba(0,157,224,.22); stroke:none; animation: p2glow-a 3s ease-in-out infinite; }
          .p2gnc2 { fill:rgba(0,157,224,.09); stroke:none; animation: p2glow-b 3s ease-in-out infinite; }
          .p2gnd  { fill:rgba(0,200,150,.22); stroke:none; animation: p2glow-a 3s ease-in-out infinite; }
          .p2gnd2 { fill:rgba(0,200,150,.09); stroke:none; animation: p2glow-b 3s ease-in-out infinite; }
          .p2nc   { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .p2nd   { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:2; }
          .p2nt   { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .p2ns   { font-size:12px; fill:#009de0; text-anchor:middle; opacity:.65; font-style:italic; }
          .p2dt   { font-size:15px; fill:#00c896; text-anchor:middle; font-weight:600; }
          .p2ds   { font-size:12px; fill:#00c896; text-anchor:middle; opacity:.65; font-style:italic; }
          .p2ico  { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── Node 1: Input Text (data, green) ── -->
      <circle cx="90"  cy="95" r="64" class="p2gnd2" style="animation-delay:0s;"/>
      <circle cx="90"  cy="95" r="53" class="p2gnd"  style="animation-delay:0s;"/>
      <circle cx="90"  cy="95" r="42" class="p2nd"/>
      <text   x="90"  y="95"  class="p2ico">📝</text>
      <text   x="90"  y="158" class="p2dt">Input Text</text>
      <text   x="90"  y="175" class="p2ds">str · plain text</text>

      <!-- Arrow 1 -->
      <path d="M 132,95 L 223,95" class="p2fl" marker-end="url(#p2ah)"/>

      <!-- ── Node 2: Text Embedder (component, blue) ── -->
      <circle cx="265" cy="95" r="64" class="p2gnc2" style="animation-delay:1s;"/>
      <circle cx="265" cy="95" r="53" class="p2gnc"  style="animation-delay:1s;"/>
      <circle cx="265" cy="95" r="42" class="p2nc"/>
      <text   x="265" y="95"  class="p2ico">🤖</text>
      <text   x="265" y="158" class="p2nt">Text Embedder</text>
      <text   x="265" y="175" class="p2ns">AzureOpenAITextEmbedder</text>

      <!-- Arrow 2 -->
      <path d="M 307,95 L 398,95" class="p2fl" marker-end="url(#p2ah)"/>

      <!-- ── Node 3: Embedding Vector (data, green) ── -->
      <circle cx="440" cy="95" r="64" class="p2gnd2" style="animation-delay:2s;"/>
      <circle cx="440" cy="95" r="53" class="p2gnd"  style="animation-delay:2s;"/>
      <circle cx="440" cy="95" r="42" class="p2nd"/>
      <text   x="440" y="95"  class="p2ico">🔢</text>
      <text   x="440" y="158" class="p2dt">Embedding Vector</text>
      <text   x="440" y="175" class="p2ds">list[float] · 3 072 dims</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Playground
# ---------------------------------------------------------------------------
st.markdown("<h2>🚀 Embedding Playground</h2>", unsafe_allow_html=True)
st.caption("Type sentences, turn them into 3072-dimensional vectors, and explore meaning in 3D.")

# Colors for up to 8 texts in the 3D plot
POINT_COLORS = [
    IST_BLUE,
    ACCENT_GREEN,
    ACCENT_ORANGE,
    ACCENT_RED,
    "#8b5cf6",  # purple
    "#ec4899",  # pink
    "#06b6d4",  # cyan
    "#84cc16",  # lime
]

_DOT_EMOJIS = "🔵🟢🟡🔴🟣🩷🩵🟩"


def _similarity_color(sim: float) -> str:
    """Return a color based on similarity value."""
    if sim >= 0.8:
        return ACCENT_GREEN
    if sim >= 0.5:
        return ACCENT_ORANGE
    return ACCENT_RED


def _similarity_label(sim: float) -> str:
    """Return a short label describing how similar two texts are."""
    if sim >= 0.9:
        return "Very high similarity"
    if sim >= 0.8:
        return "High similarity"
    if sim >= 0.6:
        return "Moderate similarity"
    if sim >= 0.4:
        return "Low similarity"
    return "Very low similarity"


# ---------------------------------------------------------------------------
# Input area
# ---------------------------------------------------------------------------
st.subheader("✏️ Input Sentences")
st.caption("Add 2-8 sentences. Give each a short label for the graph, then write the full text.")

_DEFAULTS = [
    (
        "SINFO Conference",
        "SINFO is the largest student-run tech conference in Portugal,"
        " held annually at Instituto Superior Tecnico in Lisbon.",
    ),
    (
        "IST Tech Week",
        "Every year, thousands of engineering students gather in Lisbon"
        " for a week of tech talks, workshops, and networking at IST.",
    ),
    (
        "RAG Overview",
        "Retrieval-Augmented Generation combines a vector search over"
        " document embeddings with a large language model to answer"
        " questions using real sources.",
    ),
    (
        "RAG Pipeline",
        "RAG pipelines first retrieve relevant text chunks from a"
        " database and then feed them as context to an LLM for"
        " grounded answers.",
    ),
    (
        "Pasta Recipe",
        "The best recipe for homemade pasta starts with 100 grams of"
        " flour per egg, kneaded for ten minutes until the dough is"
        " smooth and elastic.",
    ),
]

if "embed_entries" not in st.session_state:
    st.session_state["embed_entries"] = list(_DEFAULTS)

entries = st.session_state["embed_entries"]

updated_entries: list[tuple[str, str]] = []
for i in range(len(entries)):
    dot = _DOT_EMOJIS[i] if i < len(_DOT_EMOJIS) else "⚪"
    color = POINT_COLORS[i % len(POINT_COLORS)]

    with st.container(border=True):
        header_left, header_right = st.columns([9, 1])
        with header_left:
            lbl = st.text_input(
                f"Label {i + 1}",
                value=entries[i][0],
                key=f"embed_label_{i}",
                label_visibility="collapsed",
                placeholder=f"Label for sentence {i + 1}",
            )
        with header_right:
            if len(entries) > 2 and st.button("✕", key=f"remove_{i}", help="Remove this entry"):
                st.session_state["embed_entries"] = [e for j, e in enumerate(entries) if j != i]
                st.rerun()

        txt = st.text_area(
            f"Sentence {i + 1}",
            value=entries[i][1],
            key=f"embed_text_{i}",
            label_visibility="collapsed",
            placeholder="Full sentence to embed...",
            height=80,
        )

    if lbl and txt:
        updated_entries.append((lbl.strip(), txt.strip()))

st.session_state["embed_entries"] = updated_entries

btn_col1, btn_col2 = st.columns([1, 1])
with btn_col1:
    if len(entries) < 8 and st.button("➕  Add sentence", use_container_width=True):
        st.session_state["embed_entries"].append(("", ""))
        st.rerun()
with btn_col2:
    compare_clicked = st.button("🚀  Compare Embeddings", use_container_width=True, type="primary")

st.divider()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if compare_clicked:
    valid_entries = [(lbl or f"Sentence {i + 1}", txt) for i, (lbl, txt) in enumerate(updated_entries) if txt]

    if len(valid_entries) < 2:
        st.warning("Enter at least 2 non-empty sentences to compare.")
        st.stop()

    _labels = [lbl for lbl, _ in valid_entries]
    _texts = [txt for _, txt in valid_entries]

    with st.spinner("Turning words into vectors... 🔢"):
        try:
            _api_result = api.compare_embeddings(_texts)
        except Exception as exc:
            st.error(f"API call failed: {exc}")
            st.stop()

    st.session_state["embed_result"] = _api_result
    st.session_state["embed_valid_texts"] = _texts
    st.session_state["embed_valid_labels"] = _labels

result: dict[str, Any] | None = st.session_state.get("embed_result")
valid_texts: list[str] | None = st.session_state.get("embed_valid_texts")
valid_labels: list[str] | None = st.session_state.get("embed_valid_labels")

if result is None or valid_texts is None:
    st.markdown(
        """
        <div class="cta-placeholder">
            <p style="font-size: 1.3em;">👆 Enter some sentences and hit
            <b style="color: #009de0;">Compare Embeddings</b></p>
            <p style="font-size: 0.9em;">The magic happens when you mix related and unrelated sentences!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

embeddings_data = result.get("embeddings", [])
similarities = result.get("similarities", [])

text_to_label: dict[str, str] = {}
if valid_labels:
    for txt, lbl in zip(valid_texts, valid_labels, strict=True):
        text_to_label[txt] = lbl
for e in embeddings_data:
    if e["text"] not in text_to_label:
        text_to_label[e["text"]] = e["text"][:30] + "..."

# ---------------------------------------------------------------------------
# 3D Visualization
# ---------------------------------------------------------------------------
st.subheader("🌌 3D Embedding Space")
st.caption("3072 dimensions → 3D via PCA. Points that are close together share similar meaning.")

vectors = [e["embedding"] for e in embeddings_data]
full_texts = [e["text"] for e in embeddings_data]
point_labels = [text_to_label.get(t, t[:30]) for t in full_texts]

if len(vectors) < 2:
    st.warning("Need at least 2 embeddings to visualize.")
    st.stop()

matrix = np.array(vectors)
meaningful_dims = min(3, max(len(vectors) - 1, 1))
pca = PCA(n_components=meaningful_dims)
coords = pca.fit_transform(matrix)

if coords.shape[1] < 3:
    spread = np.ptp(coords, axis=0).mean() if coords.size else 1.0
    jitter_scale = spread * 0.3
    rng = np.random.default_rng(42)
    jitter = rng.normal(scale=jitter_scale, size=(coords.shape[0], 3 - coords.shape[1]))
    coords = np.concatenate([coords, jitter], axis=1)

fig = go.Figure()

for i, (plabel, coord, full_text) in enumerate(zip(point_labels, coords, full_texts, strict=True)):
    color = POINT_COLORS[i % len(POINT_COLORS)]
    fig.add_trace(
        go.Scatter3d(
            x=[coord[0]],
            y=[coord[1]],
            z=[coord[2]],
            mode="markers+text",
            marker=dict(size=12, color=color, opacity=0.9),
            text=[plabel],
            textposition="top center",
            textfont=dict(size=12, color=color),
            name=plabel,
            hovertext=full_text,
            hoverinfo="text",
        )
    )

for pair in similarities:
    text_a = pair["text_a"]
    text_b = pair["text_b"]
    sim = pair["similarity"]
    idx_a = full_texts.index(text_a)
    idx_b = full_texts.index(text_b)
    label_a = text_to_label.get(text_a, "")
    label_b = text_to_label.get(text_b, "")
    line_color = _similarity_color(sim)
    opacity = 0.2 + 0.6 * sim
    fig.add_trace(
        go.Scatter3d(
            x=[coords[idx_a][0], coords[idx_b][0]],
            y=[coords[idx_a][1], coords[idx_b][1]],
            z=[coords[idx_a][2], coords[idx_b][2]],
            mode="lines",
            line=dict(color=line_color, width=3),
            opacity=opacity,
            name=f"{label_a} ↔ {label_b}: {sim:.3f}",
            hovertext=f"{label_a} ↔ {label_b}: {sim:.4f}",
            hoverinfo="text",
            showlegend=False,
        )
    )

fig.update_layout(
    scene=dict(
        xaxis=dict(title="PC1"),
        yaxis=dict(title="PC2"),
        zaxis=dict(title="PC3"),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=30, b=0),
    height=600,
    legend=dict(font=dict(size=11)),
)

st.plotly_chart(fig, width="stretch")

explained = pca.explained_variance_ratio_
total_explained = sum(explained) * 100
pca_parts = [f"PC{i + 1}: {v * 100:.1f}%" for i, v in enumerate(explained)]
pca_detail = ", ".join(pca_parts)
jitter_note = ""
if meaningful_dims < 3:
    missing = 3 - meaningful_dims
    pc_label = "PC3 is" if missing == 1 else "PC2 & PC3 are"
    jitter_note = f"  |  {pc_label} synthetic jitter (not enough points for full 3D PCA)"
st.caption(f"PCA explained variance: {total_explained:.1f}% ({pca_detail}){jitter_note}")

st.divider()

# ---------------------------------------------------------------------------
# Similarity scores
# ---------------------------------------------------------------------------
st.subheader("📏 Similarity Scores")
st.caption(
    "Cosine similarity between each pair of sentences. Ranges from 0 (completely unrelated) to 1 (identical meaning)."
)

for pair in similarities:
    sim = pair["similarity"]
    color = _similarity_color(sim)
    label_a = text_to_label.get(pair["text_a"], pair["text_a"][:40])
    label_b = text_to_label.get(pair["text_b"], pair["text_b"][:40])
    sim_label = _similarity_label(sim)
    pct = max(0, min(100, sim * 100))
    st.markdown(
        f"""
        <div class="sim-card">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div style="flex: 1; min-width: 200px;">
                    <b>{label_a}</b>
                    <span class="text-muted"> vs. </span>
                    <b>{label_b}</b>
                </div>
                <div style="text-align: right; min-width: 120px;">
                    <span style="color: {color}; font-weight: bold; font-size: 1.5em;">{sim:.4f}</span><br/>
                    <span style="color: {color}; font-size: 0.8em;">{sim_label}</span>
                </div>
            </div>
            <div class="sim-bar" style="margin-top: 10px;">
                <div class="sim-bar-fill" style="width: {pct}%; background-color: {color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# Embedding details
# ---------------------------------------------------------------------------
st.subheader("🔬 Embedding Details")
st.caption("Dive into the raw numbers behind each sentence's vector.")

for i, emb in enumerate(embeddings_data):
    dot = _DOT_EMOJIS[i] if i < len(_DOT_EMOJIS) else "⚪"
    plabel = text_to_label.get(emb["text"], f"Sentence {i + 1}")
    with st.expander(f"{dot}  {plabel}"):
        st.markdown(f"**Full text:** {emb['text']}")
        st.markdown(f"**Dimensions:** `{emb['dimensions']}`")
        vec = emb["embedding"]
        st.markdown("**First 20 values** (out of 3072):")
        st.code(
            ", ".join(f"{v:.6f}" for v in vec[:20]) + f"  ... ({len(vec)} total)",
            language=None,
        )
        st.markdown("**Vector statistics:**")
        arr = np.array(vec)
        stat_cols = st.columns(4)
        stat_cols[0].metric("Min", f"{arr.min():.6f}")
        stat_cols[1].metric("Max", f"{arr.max():.6f}")
        stat_cols[2].metric("Mean", f"{arr.mean():.6f}")
        stat_cols[3].metric("Std Dev", f"{arr.std():.6f}")
