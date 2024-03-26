import html
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session

import config
import tezariusDB
from models import oc_drom_product
from models import oc_product
from models.oc_drom_product import Product as ProductDrom
from models.oc_product import Product, InformationDescription
from models.oc_site_product import Product as LiteProduct
from models.sales.oc_order import Order, OrderProduct

engine = create_engine(
    f'mysql+pymysql://{config.site_login}:{config.site_password}@{config.site_db_ip}/{config.site_db}')

engine.execution_options(stream_results=True)

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

default_query = (session.query(Product).distinct()
                 .filter(
    and_(Product.main_car_sku != '', Product.main_car_sku != '0', Product.main_car_sku is not None))
                 .filter(Product.main_car.has())
                 .filter(Product.manufacturer_id != 0).filter(Product.quantity > 0))


def get_all_products():
    result = session.query(LiteProduct).all()
    return {x.sku: x for x in result}


def get_products_to_drom(trucks=False):
    result = (session.query(ProductDrom).distinct().outerjoin(oc_drom_product.ProductCategory)
              .filter(
        and_(ProductDrom.main_car_sku != '', ProductDrom.main_car_sku != '0', ProductDrom.main_car_sku is not None))
              .filter(ProductDrom.main_car.has()).filter(ProductDrom.quantity > 0)
              .filter(ProductDrom.categories.any(oc_drom_product.ProductCategory
                                                 .category_id.in_(config.drom_trucks_id)) if trucks else
                      oc_drom_product.ProductCategory.category_id.not_in(config.drom_trucks_id)).all())
    return result


def get_accessories(separator=False):
    result = (default_query.filter(Product.attributes.any(attribute_id=22))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_audio(separator=False):
    result = (default_query.filter(Product.attributes.any(attribute_id=26))
              .filter(Product.price > config.avito_sep_summ if separator else Product.price <= config.avito_sep_summ)
              .filter(Product.price >= config.avito_min_summ if separator else Product.price <= config.avito_max_summ)
              .all())
    return result


def get_products(separator=False):
    result = (default_query.filter(Product.attributes.any(oc_product.ProductAttribute.text
                                                          .not_in(config.category_blacklists)))
              .filter(~Product.attributes.any(attribute_id=22))
              .filter(~Product.attributes.any(attribute_id=26))
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


def add_order(tz_product, sales: tezariusDB.Sales, product=None):
    custom_order = Order()
    custom_order_product = OrderProduct()
    if not tz_product.get('art_code'):
        return
    if not product:
        product = session.query(Product).where(Product.sku == tz_product.get('art_code')).first()

    if not product:
        return

    if not tz_product.get(
            'doc_date') or not product.description.name or not product.model or not product.product_id or tz_product.get(
            'total') is None or not product.price or not tz_product.get('qty') or not tz_product.get(
            'total') or not tz_product.get('CounterpartsName') or not tz_product.get('FirmName'):
        return

    custom_order_product.name = product.description.name
    custom_order_product.model = product.model
    custom_order_product.product_id = product.product_id
    custom_order_product.total = tz_product.get('total')
    custom_order_product.price = product.price
    custom_order_product.quantity = tz_product.get('qty')
    custom_order.order_product.append(custom_order_product)
    custom_order.total = tz_product.get('total')
    custom_order.payment_firstname = tz_product.get('CounterpartsName')[0:32]
    custom_order.shipping_firstname = tz_product.get('CounterpartsName')[0:32]
    custom_order.firstname = tz_product.get('CounterpartsName')[0:32]
    custom_order.order_status_id = 5 if int(tz_product.get('isCanceled')) == 0 else 8
    custom_order.store_name = tz_product.get('FirmName')

    if tz_product.get('id_rbCounterparts'):
        client = sales.get_client(tz_product.get('id_rbCounterparts'))
        if client:
            custom_order.telephone = sales.get_client(tz_product.get('id_rbCounterparts'))['phone_formated']

    dt = datetime.strptime(tz_product.get('doc_date'), '%Y-%m-%d')

    custom_order.date_added = dt
    custom_order.date_modified = dt
    session.add(custom_order)
