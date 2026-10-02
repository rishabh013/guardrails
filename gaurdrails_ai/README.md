check uv install or not
1) 
-- uv init

2) 
-- requiemnets.txt

3) 
-- uv venv -- python 3.12

4) 
-- source .venv/bin/activate

5) 

-- uv pip install -r requirements.txt

uv add guardrails-ai-detect-pii

uv add guardrails-ai-competitor-check
uv run python -m guardrails_ai.competitor_check.post_install   # Local

uv add guardrails-ai-toxic-language
uv run python -m guardrails_ai.toxic_language.post_install  # Local

uv add pip guardrails-ai-restrict-to-topic

uv add guardrails-ai-detect-jailbreak
uv run python -m guardrails_ai.detect_jailbreak.post_install

