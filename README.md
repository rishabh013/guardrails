# Guardrails

This repo is a working comparison of two ways to put **safety rails around LLM apps**: NVIDIA **NeMo Guardrails** and **Guardrails AI**. Both sides answer the same problem — stop unsafe, off-policy, or leaking answers before they reach a user — but they do it with different products and patterns.

| Folder | Library | Role in this repo |
| --- | --- | --- |
| `nemo/` | NVIDIA NeMo Guardrails | End-to-end HR policy assistant: Streamlit UI, RAG, and rails that run *before* retrieval |
| `gaurdrails_ai/` | Guardrails AI validators | Notebooks that exercise individual validators (PII, jailbreak, toxicity, topics, and more) |

Use **NeMo** when you want a conversational policy layer (Colang flows, intent, dialog) in front of an app. Use **Guardrails AI** when you want composable validators on inputs and outputs, including structured checks and LangChain.

---

## `nemo/` — NeMo Guardrails + RAG

A Streamlit **HR Policy Assistant** for a fictional company. Employees ask about leave, benefits, remote work, and reviews. NeMo sits as a **semantic security gate** in front of a FAISS RAG pipeline so the main chat model never sees blocked questions.

**What it allows**

- Policy questions such as vacation after three years, 401(k) match, remote work, performance ratings

**What it blocks**

- Colleague salary / confidential employee data
- Jailbreak-style “ignore previous instructions”
- PII in the prompt (SSN, email, API keys)
- Off-topic chat (jokes, weather, coding help)

**How it is wired**

1. **Input rail** — regex PII check, then a guard LLM classifies intent (off-topic, jailbreak, confidential, greeting, HR question)
2. **RAG** — only HR questions that pass the rail are embedded and searched in FAISS (`BAAI/bge-small-en-v1.5`)
3. **Generation** — a second LLM answers from retrieved chunks; output can be sanitized so sensitive data is not returned

Colang rules and Python actions live in `nemo/src/guards.py`. The UI and pipeline live under `nemo/src/`. Entry point: `nemo/app.py`.

```bash
cd nemo
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
streamlit run app.py
```

You need an OpenAI (or compatible) API key in the sidebar / `.env`.

---

## `gaurdrails_ai/` — Guardrails AI validators

A set of Jupyter notebooks on **Guardrails AI**: drop-in validators you attach to LLM calls for input/output checks, fail actions, streaming, and LangChain.

| Notebook | What it covers |
| --- | --- |
| `01_PII_detection.ipynb` | Detect / redact personal data |
| `02_competitor_check.ipynb` | Flag competitor mentions |
| `03_toxic_language.ipynb` | Toxic or abusive language |
| `04_restrict_to_topic.ipynb` | Keep the model on an allowed topic |
| `05_jailbreak.ipynb` | Detect jailbreak attempts |
| `06_On_FailAction.ipynb` | What to do when a validator fails |
| `07_Input_output_structured_validation.ipynb` | Structured input/output validation |
| `08_guardrails_validation_during_streaming.ipynb` | Validation while tokens stream |
| `09_Guardrails_langchain.ipynb` | Using validators with LangChain |

This folder is for **learning and comparing validators**, not a full product UI. Packages include `guardrails-ai` plus hubs such as detect-pii, competitor-check, toxic-language, restrict-to-topic, and detect-jailbreak.

```bash
cd gaurdrails_ai
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
# extra hub validators as needed, e.g.:
# uv add guardrails-ai-detect-pii
```

Some validators need a one-time `post_install` after install. See `gaurdrails_ai/README.md`.

---

## When to look at which folder

- **Ship a gated RAG chatbot** → start in `nemo/`
- **Try a specific check** (PII, toxicity, jailbreak, topic, streaming, LangChain) → start in `gaurdrails_ai/`

Both folders use their own virtualenv. Keep API keys in `.env`; that file is ignored at the repo root.
