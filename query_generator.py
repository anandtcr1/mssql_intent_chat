# import json
# from llm_loader import load_llm
# from config import QUERY_MODEL_PATH
# from schema_loader import load_schema

# llm = load_llm(QUERY_MODEL_PATH)
# schema = load_schema()

# SYSTEM_PROMPT = f"""
# You are a SQL query generator.

# STRICT RULES:
# - Use ONLY tables and columns from schema below
# - Do NOT invent tables or columns
# - Do NOT explain
# - Output ONLY SQL

# Schema:
# {json.dumps(schema, indent=2)}
# """

# def generate_sql(intent: dict, user_input: str) -> str:
#     prompt = f"""
# <SYSTEM>{SYSTEM_PROMPT}</SYSTEM>

# <USER>
# User Query: {user_input}
# Intent: {json.dumps(intent)}
# </USER>

# <ASSISTANT>
# """

#     res = llm(prompt, max_tokens=512)
#     return res["choices"][0]["text"].strip()

import json
import re
from llm_loader import load_llm
from config import QUERY_MODEL_PATH
from schema_loader import load_schema

llm = load_llm(QUERY_MODEL_PATH)
schema = load_schema()

SYSTEM_PROMPT = f"""
You are a trusted internal system that generates SQL queries
for an enterprise HR database.

This is an INTERNAL, AUTHORIZED database.
All queries are SAFE and READ-ONLY.

TASK:
Generate ONE SQL SELECT query that answers the user question.

STRICT RULES:
- Generate EXACTLY ONE SQL query
- Use ONLY tables and columns from the schema
- Use SELECT statements ONLY
- Do NOT refuse
- Do NOT explain
- Do NOT ask questions
- Do NOT include markdown
- Do NOT include role tokens

OUTPUT FORMAT (JSON ONLY):
{{
  "sql": "SELECT ..."
}}

Schema:
{json.dumps(schema, indent=2)}
"""

def _clean_sql(sql: str) -> str:
    sql = sql.strip()

    # Enforce SELECT-only
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    # Ensure semicolon
    if not sql.endswith(";"):
        sql += ";"

    return sql

def _extract_sql_fallback(text: str) -> str | None:
    """
    Fallback: extract SELECT statement if JSON failed
    """
    match = re.search(r"(select\s+.+?;)", text, re.I | re.S)
    if match:
        return _clean_sql(match.group(1))
    return None

def _strip_code_fences(text: str) -> str:
    """
    Removes ```json, ```sql, ``` wrappers if present
    """
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*", "", text)
        text = re.sub(r"```$", "", text)
    return text.strip()


def generate_sql(intent: dict, user_input: str) -> str:
    prompt = f"""
<SYSTEM>
{SYSTEM_PROMPT}
</SYSTEM>

<USER>
User Question: {user_input}
Intent: {json.dumps(intent)}
</USER>

<ASSISTANT>
"""

    response = llm(
        prompt,
        max_tokens=256,
        stop=["</ASSISTANT>", "</USER>", "</SYSTEM>"]
    )

    raw_output = response["choices"][0]["text"].strip()

    # 1️⃣ Strip markdown fences if any
    cleaned = _strip_code_fences(raw_output)

    # 2️⃣ Try strict JSON parse
    try:
        parsed = json.loads(cleaned)
        sql = parsed.get("sql", "")
        return _clean_sql(sql)
    except Exception:
        pass

    # 3️⃣ Fallback: extract SELECT directly
    sql = _extract_sql_fallback(cleaned)
    if sql:
        return sql

    # 4️⃣ Final failure
    raise ValueError(
        f"SQL generation failed.\nRaw model output:\n{raw_output}"
    )
