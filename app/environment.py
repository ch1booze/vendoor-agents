from environs import env

env.read_env()

GROQ_API_KEY = env.str("GROQ_API_KEY")
GROQ_MODEL_NAME = env.str("GROQ_MODEL_NAME")
OPENAPI_JSON_URL = env.str("OPENAPI_JSON_URL")
