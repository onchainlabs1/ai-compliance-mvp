import os
from groq import Groq
from crewai.llm import OpenAICompatibleLLM   # wrapper interno do CrewAI

def groq_llm():
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",  # OpenAI-compat
    )
    return OpenAICompatibleLLM(
        client=client,
        model=os.getenv("GROQ_MODEL", "llama3-70b-8192"),
    )