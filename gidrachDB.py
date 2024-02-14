import html
import time

import requests
from sqlalchemy import create_engine, select, text, and_
from sqlalchemy.orm import Session
from models.oc_product import Product, InformationDescription
import config
import pandas as pd
import xml.etree.ElementTree as ET

engine = create_engine(
    f'mysql+pymysql://{config.site_login}:{config.site_password}@{config.site_db_ip}/{config.site_db}')

session = Session(bind=engine)

req_res = requests.get("https://autoload.avito.ru/format/Autocatalog.xml")
tree = ET.fromstringlist(req_res.text)
gen_dict = {}
for make in tree:
    for model in make:
        for gen in model:
            gen_dict[int(gen.attrib["id"])] = gen.attrib["name"]


def get_generation_name(gen_id):
    name = gen_dict.get(gen_id)
    if name:
        return name
    else:
        return None


def unescape_text(un_text):
    return html.unescape(un_text).replace("&nbsp;", " ").replace("&quot;", "\"")


info_msg_1 = session.query(InformationDescription).where(InformationDescription.title == 'Объявление 1').first()
info_msg_1 = unescape_text(info_msg_1.description)

info_msg_2 = session.query(InformationDescription).where(InformationDescription.title == 'Объявление 2').first()
info_msg_2 = unescape_text(info_msg_2.description)


# Запрос к базе данных для получения всех товаров
def init():
    result = (session.query(Product)
              .filter(and_(Product.main_car_sku != '', Product.main_car_sku != '0', Product.main_car_sku is not None))
              .filter(Product.main_car.has())
              .filter(Product.manufacturer_id != 0)
              .all())

    return result


timestart = time.time()
products = init()
print(f'get all products at {time.time() - timestart}')
