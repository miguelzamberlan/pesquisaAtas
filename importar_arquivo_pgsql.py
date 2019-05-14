import pandas as pd
import sqlite3
import pymysql
import psycopg2
from datetime import datetime as dt

from sqlalchemy import create_engine
import sqlalchemy

#engine = create_engine('postgresql+psycopg2://miguelzamberlan:pgsql.miguelzamberlan.com.br/miguelzamberlan')
engine = create_engine('postgresql://miguelzamberlan:a1b4k9ph@pgsql.miguelzamberlan.com.br/miguelzamberlan')



df = pd.read_csv("atas_vigentes-test.csv",sep=',')

#result = df.to_sql(name='pesquisa_ata', con=engine, if_exists='append', index=False)
#print(result)

result = df.to_sql("pesquisa_ata",
                  engine,
                  if_exists="append",  #options are ‘fail’, ‘replace’, ‘append’, default ‘fail’
                  index=False, #Do not output the index of the dataframe
                  dtype={'col1': sqlalchemy.types.NUMERIC,
                         'col2': sqlalchemy.types.String}
                  ) #Datatypes should be [sqlalchemy types][1]
print(result)