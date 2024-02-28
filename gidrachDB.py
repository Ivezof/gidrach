import html
import time

import requests
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from models.oc_site_product import Product as LiteProduct
from models.oc_product import Product, InformationDescription
import config
from models import oc_product
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
info_msg_uns_1 = unescape_text(info_msg_1.description)

info_msg_2 = session.query(InformationDescription).where(InformationDescription.title == 'Объявление 2').first()
info_msg_uns_2 = unescape_text(info_msg_2.description)

# Запрос к базе данных для получения всех товаров

default_query = (session.query(Product)
                 .filter(
    and_(Product.main_car_sku != '', Product.main_car_sku != '0', Product.main_car_sku is not None))
                 .filter(Product.main_car.has())
                 .filter(Product.manufacturer_id != 0))


def get_all_products():
    result = session.query(LiteProduct).all()
    return {x.sku: x for x in result}


def get_products_to_drom(trucks=False):
    result = (default_query.filter(Product.categories
                                   .any(oc_product.ProductCategory.category_id.in_(config.drom_trucks_id))
                                   if trucks else oc_product.ProductCategory.category_id.not_in(config.drom_trucks_id))
              .all())

    return result


def get_accessories(separator=False):
    result = (default_query.filter(Product.attributes.any(attribute_id=22))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_products(separator=False):
    result = (default_query.filter(Product.attributes.any(oc_product.ProductAttribute.text
                                                          .not_in(config.category_blacklists)))
              .filter(~Product.attributes.any(attribute_id=22))
              .filter(Product.main_category not in [1232, 1226])
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())

    return result


def get_buses(separator=False):
    result = ((session.query(Product).where(Product.main_category == 1232))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_wheels(separator=False):
    result = ((session.query(Product).where(Product.main_category == 1226))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_caps(separator=False):
    result = ((session.query(Product).where(Product.main_category == 1244))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_disks(separator=False):
    result = ((session.query(Product).where(Product.main_category == 1233))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


timestart = time.time()
# products = get_battery()
print(f'get all products at {time.time() - timestart}')
