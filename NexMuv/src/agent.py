from langchain.agents import initialize_agent, Tool, AgentType
from langchain_google_genai import GoogleGenerativeAI

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()

from .models import *

def cols_of(tModel) -> str:
    """ FUNÇÃO AUXILIAR PARA FORMATAR OS NOMES DA COLUNA DE UMA DAS TABELAS """
    return f"\n- {'\n\t- '.join([c.name for c in tModel.__table__.columns])}\n"

class DevPython():
    def __init__(self):

        # CRIA A CONEXÃO COM O BANCO DE DADOS
        self.session = sessionmaker(bind=create_engine(f"postgresql+psycopg://{getenv('USER')}:@localhost/{getenv('USER')}"))()

        # CRIA O LLM
        _LLM = GoogleGenerativeAI(model="gemini-2.0-flash", api_key=getenv("GOOGLE_API_KEY"), temperature=0)

        # USANDO O DB COMO CONTEXTO
        _sql = Tool(name="PostgreSQL DataBase",func=lambda q: self.session.execute(text("\n".join(q.split("\n")[1:-1]))).fetchall(),
            description=f"Ferramenta para consultar no postgresql as tabelas:\nproducts:{cols_of(Product)}\ncustomers:{cols_of(Customer)}\nsales:{cols_of(Sale)}")

        # INSTANCIANDO O AGENTE
        self._agent = initialize_agent(tools=[_sql], llm=_LLM, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION)
        
    def run(self, query:str) -> str:

        # RODANDO O AGENTE
        return self._agent.invoke(query)