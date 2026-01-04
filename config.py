INTENT_MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
QUERY_MODEL_PATH = "models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf"

LLM_COMMON_CONFIG = {
    "n_ctx": 4096,
    "temperature": 0.1,
    "top_p": 0.9,
    "verbose": False
}

DB_CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=SUJIYETTAN\SQLEXPRESS;DATABASE=student_admin;Trusted_Connection=yes;"
