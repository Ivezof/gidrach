import time

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from models.oc_product import Product
import config
import pandas as pd

engine = create_engine(
    f'mysql+pymysql://{config.site_login}:{config.site_password}@{config.site_db_ip}/{config.site_db}')

session = Session(bind=engine)


# Запрос к базе данных для получения всех товаров
def init():
    result = session.query(Product).all()
    return result


timestart = time.time()
products = init()
print(f'get all products at {time.time() - timestart}')