from datetime import datetime as dt, timedelta as td

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from fastapi import FastAPI, HTTPException
from src.agent import DevPython, Sale

from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(f"postgresql+psycopg://{getenv('DEVPYTHON')}:@localhost/{getenv('DEVPYTHON')}")
session = sessionmaker(bind=engine)()

app = FastAPI()

@app.get("/sales-insights", tags=["Teste Técnico | Dev Python"])
def sales_insights(question:str):

    try: return { "answer": DevPython().run(question)}
    except Exception as e: raise HTTPException(500, str(e))

@app.get("/top-products", tags=["Teste Técnico | Dev Python"])
def top_products():

    last_month = [ Sale.sale_date >= (end := dt.today().replace(day=1) - td(days=1)).replace(day=1), Sale.sale_date <= end ]
    sales = session.query(Sale).filter(*last_month).order_by(Sale.total_amount.desc()).limit(5).all()
    return { "products": [ sale.product.name for sale in sales ]}
