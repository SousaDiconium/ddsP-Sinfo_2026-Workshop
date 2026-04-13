"""Act 7: Configure OpenClaw — set up models and agent config."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        ⚙️ Configure <span style="color: #009de0;">OpenClaw</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        Wire up the Azure model and register the Trivial Fenix agent — all through the
        <code>openclaw onbooard</code> or <code>openclaw config</code> wizard.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Step 1 — Install the right version
# ---------------------------------------------------------------------------
st.subheader("Step 1 — Install OpenClaw 2026.4.9")

st.markdown(
    """
    The **latest** OpenClaw release has a known issue with browser integration.
    Make sure you have exactly version **2026.4.9** installed:
    """
)

st.code("openclaw --version", language="bash")

st.markdown(
    """
    If you have a different version, reinstall OpenClaw to the correct version:
    ```bash
    openclaw update --tag 2026.4.9
    ```
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Step 2 — Run the config wizard
# ---------------------------------------------------------------------------
st.subheader("Step 2 — Run the Config Wizard")

st.markdown(
    """
    Run the interactive configuration wizard:
    """
)

st.code("openclaw config", language="bash")

st.markdown(
    """
    When prompted, make the following selections:

    | Prompt | Selection |
    |---|---|
    | Where will the Gateway run? | **Local (this machine)** |
    | Select sections to configure | **Model** |
    | Model/auth provider | **Microsoft Foundry** |
    | Microsoft Foundry auth method | **Microsoft Foundry (API key)** |
    | Enter Azure OpenAI API key | *provided at the workshop* |
    | Microsoft Foundry endpoint URL | `https://sinfo-2026-workshop-ge-west.openai.azure.com` |
    | Default model/deployment name | `gpt-5.4` |
    | Model family | **GPT-5 series / o-series / Codex** |
    | Select request API | **Responses API** |
    | Select sections to configure | **Continue** |
    """
)

st.info("🔑 The API key will be handed out at the workshop. Don't share it or commit it to any repository.")

st.divider()

# ---------------------------------------------------------------------------
# Step 3 — Verify it works
# ---------------------------------------------------------------------------
st.subheader("Step 3 — Verify the Setup")

st.markdown(
    """
    Launch the text UI and send a quick message to confirm the model responds:
    """
)

st.code("openclaw tui", language="bash")

st.markdown(
    """
    Once inside, type **`hello`** and press Enter.  
    If you get a reply, the gateway and model are working correctly.
    Type `/exit` to quit the TUI.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Step 4 — Register the Trivial Fenix agent
# ---------------------------------------------------------------------------
st.subheader("Step 4 — Register the Trivial Fenix Agent")

st.markdown(
    """
    Register the agent workspace that lives inside this repository.  
    This will jump-start the agent with the right config, skills, and tools to follow along with the workshop exercises:
    """
)

st.code(
    'openclaw agents add trivial-fenix-sinfo-2026 --workspace "<path-to-repo>/workspace-trivial-fenix-sinfo-2026"',
    language="bash",
)

st.warning(
    "⚠️ Replace `<path-to-repo>` with the **absolute path** to the cloned repository on your machine "
    "(e.g. `/Users/yourname/Desktop/ddsP-Sinfo_2026-Workshop`)."
)

st.divider()

# ---------------------------------------------------------------------------
# Step 5 — Restart the gateway
# ---------------------------------------------------------------------------
st.subheader("Step 5 — Restart the Gateway")

st.markdown(
    """
    Restart the OpenClaw gateway so it picks up the new model config and the registered agent:
    """
)

st.code("openclaw gateway restart", language="bash")

st.divider()

# ---------------------------------------------------------------------------
# Step 6 — Enable the browser plugin
# ---------------------------------------------------------------------------
st.subheader("Step 6 — Enable the Browser Plugin")

st.markdown(
    """
    The Trivial Fenix agent uses browser automation to scrape Fenix pages.
    Enable the browser plugin:
    """
)

st.code("openclaw plugins enable browser", language="bash")

st.warning(
    "🌐 The browser plugin requires a **Chromium-based browser** to be installed on your machine — "
    "Google Chrome, Microsoft Edge, or Brave all work."
)

st.success(
    "✅ That's it! OpenClaw is configured, the agent is registered, and the browser plugin is ready. "
    "Head to the next section to start using the agent."
)
