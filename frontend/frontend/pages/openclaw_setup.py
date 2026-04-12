"""Act 7: Configure OpenClaw — set up models and agent config."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        ⚙️ Configure <span style="color: #009de0;">OpenClaw</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        Wire up the Azure models and register the Trivial Fenix agent on your machine.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Two config files need to be updated. We'll configure the same three Azure-hosted models in both:
    - `~/.openclaw/agents/trivial-fenix-sinfo-2026/agent/models.json` — agent-level model overrides
    - `~/.openclaw/openclaw.json` — global OpenClaw config (models + agent registration)

    Replace every `"API KEY"` placeholder with the **actual API key** provided at the workshop.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Step 1 — agent models.json
# ---------------------------------------------------------------------------
st.subheader("Step 1 — Agent Model Config")

st.markdown(
    """
    Edit the file at:
    ```
    ~/.openclaw/agents/trivial-fenix-sinfo-2026/agent/models.json
    ```
    Replace its contents with:
    """
)

models_json = """{
  "providers": {
    "azure-openai-responses": {
      "baseUrl": "https://sinfo-2026-workshop-foundry.openai.azure.com/openai/v1",
      "apiKey": "API KEY",
      "authHeader": true,
      "models": [
        {
          "id": "gpt-5.1-codex",
          "name": "GPT-5.1-Codex (Azure)",
          "reasoning": true,
          "input": ["text", "image"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 400000,
          "maxTokens": 16384,
          "compat": { "supportsStore": false }
        },
        {
          "id": "gpt-5.3-codex",
          "name": "GPT-5.3-Codex (Azure)",
          "reasoning": true,
          "input": ["text", "image"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 400000,
          "maxTokens": 16384,
          "compat": { "supportsStore": false }
        },
        {
          "id": "claude-sonnet-4-6",
          "name": "Claude Sonnet 4-6 (Azure)",
          "reasoning": true,
          "input": ["text", "image"],
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 400000,
          "maxTokens": 16384,
          "compat": { "supportsStore": false }
        }
      ]
    }
  }
}"""

st.code(models_json, language="json")

st.info(
    "💡 This file overrides the model list **just for this agent**, without affecting other agents on your machine."
)

st.divider()

# ---------------------------------------------------------------------------
# Step 2 — global openclaw.json
# ---------------------------------------------------------------------------
st.subheader("Step 2 — Global OpenClaw Config")

st.markdown(
    """
    Edit the file at:
    ```
    ~/.openclaw/openclaw.json
    ```
    Merge the following into the relevant sections of your existing config
    (or replace the whole file if starting fresh):
    """
)

openclaw_json = """{
  "models": {
    "providers": {
      "azure-openai-responses": {
        "baseUrl": "https://sinfo-2026-workshop-foundry.openai.azure.com/openai/v1",
        "apiKey": "API KEY",
        "authHeader": true,
        "models": [
          {
            "id": "gpt-5.1-codex",
            "name": "GPT-5.1-Codex (Azure)",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 400000,
            "maxTokens": 16384,
            "compat": { "supportsStore": false }
          },
          {
            "id": "gpt-5.3-codex",
            "name": "GPT-5.3-Codex (Azure)",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 400000,
            "maxTokens": 16384,
            "compat": { "supportsStore": false }
          },
          {
            "id": "claude-sonnet-4-6",
            "name": "Claude Sonnet 4-6 (Azure)",
            "reasoning": true,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 400000,
            "maxTokens": 16384,
            "compat": { "supportsStore": false }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "azure-openai-responses/gpt-5.3-codex"
      },
      "models": {
        "azure-openai-responses/gpt-5.1-codex": {},
        "azure-openai-responses/gpt-5.3-codex": {},
        "azure-openai-responses/claude-sonnet-4-6": {}
      },
      "workspace": "~/.openclaw/workspace",
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4,
      "subagents": { "maxConcurrent": 8 }
    },
    "list": [
      {
        "id": "trivial-fenix-sinfo-2026",
        "default": true,
        "name": "trivial-fenix-sinfo-2026",
        "workspace": "<PATH_TO_REPO>/workspace-trivial-fenix-sinfo-2026",
        "agentDir": "~/.openclaw/agents/trivial-fenix-sinfo-2026/agent",
        "model": "azure-openai-responses/gpt-5.3-codex",
        "identity": {
          "name": "Trivial-Fenix",
          "theme": "AI assistant posing as a workshop demo companion",
          "emoji": "🤖",
          "avatar": "<PATH_TO_REPO>/workspace-trivial-fenix-sinfo-2026/resources/avatar.png"
        }
      }
    ]
  }
}"""

st.code(openclaw_json, language="json")

st.warning(
    "⚠️ Replace `<PATH_TO_REPO>` with the absolute path to this repository on your machine "
    "(e.g. `/Users/yourname/Desktop/ddsP-Sinfo_2026-Workshop`)."
)

st.divider()

# ---------------------------------------------------------------------------
# Models explained
# ---------------------------------------------------------------------------
st.subheader("🧠 About the Models")

model_rows = [
    ("gpt-5.1-codex", "GPT-5.1-Codex (Azure)", "Fast reasoning model — great for quick tasks and tool use"),
    ("gpt-5.3-codex", "GPT-5.3-Codex (Azure)", "Default model — balanced capability and speed"),
    (
        "claude-sonnet-4-6",
        "Claude Sonnet 4-6 (Azure)",
        "Anthropic model — strong instruction following and long context",
    ),
]

col1, col2, col3 = st.columns(3)
for i, (model_id, name, desc) in enumerate(model_rows):
    with [col1, col2, col3][i]:
        st.markdown(
            f"""
            <div class="card" style="height: 100%;">
                <h4 style="margin: 0 0 4px; font-size: 1em; color: #7dd3fc;">{name}</h4>
                <code style="font-size: 0.8em; color: #aaa;">{model_id}</code>
                <p style="font-size: 0.9em; margin: 8px 0 0;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div style="margin-top: 1rem; padding: 0.75rem 1rem; background: #1a2a1a; border-radius: 8px;
                border-left: 3px solid #4caf50; font-size: 0.9em; color: #aaa; line-height: 1.6;">
        <strong style="color: #e0e0e0;">💳 Billing & Access</strong><br>
        These models are provided by <strong style="color: #4caf50;">Diconium</strong> at
        <strong style="color: #4caf50;">zero cost</strong> during this workshop via a shared Azure
        OpenAI resource. Access will be <strong>revoked after the event</strong>.<br><br>
        The good news: OpenClaw is <strong>plug-and-play with any provider</strong>. You can swap in
        your own API keys at any time — just update the <code>baseUrl</code> and <code>apiKey</code>
        fields. There are also student offers worth exploring — for example, OpenAI occasionally offers
        free credits for students. Any provider supported by OpenAI-compatible APIs works.
    </div>
    """,
    unsafe_allow_html=True,
)
