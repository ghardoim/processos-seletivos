from datetime import datetime as dt, timedelta as td
from fastapi import FastAPI, HTTPException
from src.agent import DevPython, Sale

# INICIALIZANDO A API E O AGENTE

app = FastAPI()
agent = DevPython()

@app.get("/sales-insights", tags=["Teste Técnico | Dev Python"])
def sales_insights(question:str):

    # EXECUTAR O AGENTE COM BASE NA PERGUNTA
    try: return { "answer": agent.run(question)}

    # CASO O AGENTE NÃO ENTENDA OU TENHA QUALQUER PROBLEMA
    except Exception as e: raise HTTPException(500, str(e))

@app.get("/top-products", tags=["Teste Técnico | Dev Python"])
def top_products():

    # PEGA AS DATAS DE INÍCIO E FIM DO MÊS PASSADO
    last_month = [ Sale.sale_date >= (end := dt.today().replace(day=1) - td(days=1)).replace(day=1), Sale.sale_date <= end ]

    # CONSULTA NO BANCO
    sales = agent.session.query(Sale).filter(*last_month).order_by(Sale.total_amount.desc()).limit(5).all()

    # RETORNANDO APENAS OS NOMES
    return { "products": [ sale.product.name for sale in sales ]}
