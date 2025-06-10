from langchain_google_genai import ChatGoogleGenerativeAI
from os import getenv

def ask_ai(message: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=getenv("GOOGLE_API_KEY"))
    return llm.invoke(f"""
        Você é o assistente da TechSolutio.
        Responda de forma clara, objetiva e, se possível, com exemplos práticos.
        Pergunta do usuário: {message}
    """).content