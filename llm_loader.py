from llama_cpp import Llama
from config import LLM_COMMON_CONFIG

def load_llm(model_path: str):
    return Llama(
        model_path=model_path,
        n_ctx=LLM_COMMON_CONFIG["n_ctx"],
        temperature=LLM_COMMON_CONFIG["temperature"],
        top_p=LLM_COMMON_CONFIG["top_p"],
        verbose=LLM_COMMON_CONFIG["verbose"]
    )
