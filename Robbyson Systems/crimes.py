
from sqlalchemy import create_engine
from os import getenv
import pandas as pd

bd_con = create_engine(f"postgresql://{getenv('HOST')}:{getenv('PASSWORD')}@{getenv('HOST')}:5432/crimes")
pd.read_csv("database.csv").to_sql("crimes", con = bd_con, schema = "crimes")
df = pd.read_sql("select * from crimes", bd_con)

def get_top(n, column_name, _df):
    return ", ".join([ top_five for top_five in _df[column_name].value_counts().head(n).index ])

def count_df_by(column_name):
    return df.groupby(column_name, as_index = False).count().sort_values(by = "Dates", ascending = False)

print(f"1°: {get_top(5, 'Category', df)}")
print(f"2°:\n{count_df_by('PdDistrict').PdDistrict}")
print(f"3°: {get_top(5, 'Resolution', df)}")
print(f"4°: Perigosa -> {count_df_by('Address').max().Address}")
print(f"4°: Segura -> {count_df_by('Address').min().Address}")

for _, distrito in df.groupby("PdDistrict", as_index = False):
    print(f"5°: {_} -> {get_top(10, 'Descript', distrito)}")