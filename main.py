import re
import time

from line_profiler import profile

import tezariusDB
import xmlWriter
import config
import gidrachDB
from gidrachDB import info_msg_1, info_msg_2
from config import type_dict
from models import oc_product

avito_document = xmlWriter.Document(config.xml_path, config.avito_xml_name, 'Ads',
                                    {'formatVersion': '3', 'target': "Avito.ru"})


def get_type_product(product_attr):
    if product_attr in type_dict:
        return type_dict.get(product_attr)
    for k, v in type_dict.items():
        if re.search(k.replace('*', '\\w*').replace('|', '\\|'), product_attr):
            return v


def update_product_on_site(products):
    tz_products = tezariusDB.Products()
    for tz_product in tz_products:
        print(tz_product)


def validate_products_xml(products: list[gidrachDB.Product]):
    valid_products = {'default': []}
    for product in products:
        time_start = time.time()
        if not product.main_car or product.main_car == '' or config.attr_ids['make'] not in product.main_car.attributes:
            continue
        elif not product.main_car.dism_product:
            continue

        valid_products['default'].append(product)
        print(f'1 prods as {time.time() - time_start}')
    return valid_products


@profile
def avito_xml(products: list[gidrachDB.Product]):
    timestart = time.time()

    for product in products:
        print(product.product_id)

        timestart_one = time.time()
        ad = xmlWriter.Elem('Ad')

        # id товара
        id_ad = xmlWriter.Elem('Id', parent_elem=ad)
        id_ad.set_content(product.sku)

        # номер телефона
        phone = xmlWriter.Elem('ContactPhone', parent_elem=ad)
        phone.set_content('+79876543210')

        # avitoId
        xmlWriter.Elem("AvitoId", parent_elem=ad)

        # ad type
        timestart_ad = time.time()
        ad_type = xmlWriter.Elem('AdType', parent_elem=ad)
        ad_type.set_content('Товар приобретен на продажу')
        print('time ad elem: ', time.time() - timestart_ad)

        # description
        description = xmlWriter.Elem('Description', parent_elem=ad)
        description.set_content(info_msg_1
                                + "\n\n"
                                + gidrachDB.unescape_text(product.description.description)
                                + "\n\n"
                                + info_msg_2, cdata=True)

        # # make
        # make = xmlWriter.Elem('Make', parent_elem=ad)
        # make.set_content(product.main_car.attributes[config.attr_ids['make']].text)
        #
        # # model
        # model = xmlWriter.Elem('Model', parent_elem=ad)
        # model.set_content(product.main_car.attributes[config.attr_ids['model']].text)
        #
        # # generation
        # generation = xmlWriter.Elem('Generation', parent_elem=ad)
        # generation.set_content(product.main_car.attributes[config.attr_ids['generation']].text)
        #
        # # modification
        # modification = xmlWriter.Elem('Modification', parent_elem=ad)
        # modification.set_content(gidrachDB.gen_dict.get(product.main_category.avito_generation_id))

        dism_product: oc_product.DismantlingProduct
        main_car = product.main_car
        disms_product = main_car.dism_product
        for dism_product in disms_product:
            elem = xmlWriter.Elem(dism_product.dism.dismantling_param.tag, parent_elem=ad)
            elem.set_content(dism_product.dism.name)

        # # type_id
        # type_id = xmlWriter.Elem("TypeId", parent_elem=ad)
        # if product.attribute and product.attribute.attribute_description:
        #     type_id.set_content(get_type_product(product.attribute.attribute_description.name + "|" +
        #                                          product.attribute.text))

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Запчасти')

        # SparePartType
        spare_part_type = xmlWriter.Elem('SparePartType', parent_elem=ad)
        for i in product.attributes.values():
            if i.attribute_description.name in config.spare_part_type:
                spare_part_type.set_content(config.spare_part_type.get(i.attribute_description.name))

                # Spare Type tag
                spare_type_tag = xmlWriter.Elem(config.tags.get(i.attribute_description.name)[0],
                                                parent_elem=ad)
                spare_type_tag.set_content(config.tags.get(i.attribute_description.name)[1]
                                           .get(i.text))
                break

        # manager_name
        manager_name = xmlWriter.Elem('ManagerName', parent_elem=ad)
        manager_name.set_content(config.manager_name)

        # title
        title = xmlWriter.Elem('Title', parent_elem=ad)
        title.set_content(product.description.name)

        # condition
        condition = xmlWriter.Elem('Condition', parent_elem=ad)
        condition.set_content('Б/у')

        # address
        address = xmlWriter.Elem('Address', parent_elem=ad)
        address.set_content(config.address)

        # phone
        phone = xmlWriter.Elem('ContactPhone', parent_elem=ad)
        phone.set_content(config.phone)

        # category
        category = xmlWriter.Elem('Category', parent_elem=ad)
        category.set_content('Запчасти и аксессуары')

        # ad_status
        ad_status = xmlWriter.Elem('AdStatus', parent_elem=ad)
        ad_status.set_content('Free')

        # cost
        cost = xmlWriter.Elem('Price', parent_elem=ad)
        cost.set_content(product.price)

        # oem_number
        oem_number = xmlWriter.Elem('OEM', parent_elem=ad)
        oem_number.set_content(product.mpn)

        # brand
        brand = xmlWriter.Elem('Brand', parent_elem=ad)
        brand.set_content(product.manufacturer.name)

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Для автомобилей')

        avito_document.add_elem(ad)
        print(f'gen 1 product at {time.time() - timestart_one}')

    avito_document.close_document()
    print(f'generate full avito file at {time.time() - timestart}')


if __name__ == '__main__':
    gidrachDB.init()
    avito_xml(gidrachDB.products)
