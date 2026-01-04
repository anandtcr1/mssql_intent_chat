# import json
# from llm_loader import load_llm
# from intent_schema import IntentResult
# from config import INTENT_MODEL_PATH

# llm = load_llm(INTENT_MODEL_PATH)

# SYSTEM_PROMPT = """
# You are an intent extraction engine.

# Extract:
# - intent (short verb-based)
# - confidence (0-1)
# - entities

# Return ONLY valid JSON.
# """

# def extract_intent(user_input: str) -> dict:
#     prompt = f"""
# <SYSTEM>{SYSTEM_PROMPT}</SYSTEM>
# <USER>{user_input}</USER>
# <ASSISTANT>
# """

#     res = llm(prompt, max_tokens=256)
#     raw = res["choices"][0]["text"].strip()

#     try:
#         return IntentResult(**json.loads(raw)).dict()
#     except:
#         return {"intent": "unknown", "confidence": 0, "entities": {}}

import json
from llm_loader import load_llm
from intent_schema import IntentResult
from config import INTENT_MODEL_PATH

llm = load_llm(INTENT_MODEL_PATH)

SYSTEM_PROMPT = """
You are an intent extraction engine.

Analyze the user query and extract:
1. Primary intent (short, verb-based)
2. Confidence score (0.0 to 1.0)
3. Any entities if present

Respond ONLY in valid JSON format:

{
  "intent": "",
  "confidence": 0.0,
  "entities": {}
}

Rules:
- Do NOT answer the question
- Do NOT explain anything
- Output JSON only
- Replace intent with under score, if it has sapce
"""

def extract_intent(user_input: str) -> dict:
    prompt = f"""
<s>[SYSTEM]
{SYSTEM_PROMPT}
[/SYSTEM]

[USER]
{user_input}
[/USER]

[ASSISTANT]
"""

    response = llm(
        prompt,
        max_tokens=256,
        stop=["</s>"]
    )

    raw_output = response["choices"][0]["text"].strip()

    try:
        parsed = json.loads(raw_output)
        validated = IntentResult(**parsed)
        return validated.dict()
    except Exception as e:
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "entities": {},
            "error": str(e),
            "raw_output": raw_output
        }
