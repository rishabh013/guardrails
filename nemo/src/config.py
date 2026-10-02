OPENAI_MODELS = {
    "gpt-4o":        "GPT-4o  ★ recommended for guardrails",
    "gpt-4.1":       "GPT-4.1  — strong reasoning",
    "gpt-4.1-mini":  "GPT-4.1 mini  ★ fast & cheap",
    "gpt-4o-mini":   "GPT-4o mini  — fast & cheap",
}

GUARD_MODEL_DEFAULT = "gpt-4o"
CHAT_MODEL_DEFAULT  = "gpt-4.1-mini"

HR_SYSTEM_PROMPT = (
    "You are the HR Policy Assistant for Acme Corp. "
    "Answer the employee's question using ONLY the policy excerpts provided below. "
    "Be concise, cite the relevant policy section, and include specific numbers or rules where applicable. "
    "If the answer is not covered in the excerpts, say so clearly and direct the employee to hr@acmecorp.com.\n\n"
    "Policy Excerpts:\n{context}"
)

SENSITIVE_OUTPUT_PATTERNS = {
    "credential_leak":  r"(?i)(password|passwd|secret|api[_\-]?key|token)\s*[:=]\s*['\"]?\w{6,}",
    "ssn_in_output":    r"\b\d{3}-\d{2}-\d{4}\b",
    "hardcoded_salary": r"(?i)\b(earns?|is paid|salary of)\s+\$[\d,]+\b",
}
