import re
import time

import xmlWriter
import config
import gidrachDB
from config import type_dict

avito_document = xmlWriter.Document(config.xml_path, config.avito_xml_name, 'Ads',
                                    {'formatVersion': '3', 'target': "Avito.ru"})


def get_type_product(product_attr):
    if product_attr in type_dict:
        return type_dict.get(product_attr)
    for k, v in type_dict.items():
        if re.search(k.replace('*', '\\w*').replace('|', '\\|'), product_attr):
            return v


def avito_xml(products):
    timestart = time.time()
    for product in products:
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

        # type_id
        type_id = xmlWriter.Elem("TypeId", parent_elem=ad)
        if product.attribute and product.attribute.attribute_description:
            type_id.set_content(get_type_product(product.attribute.attribute_description.name + "|" +
                                                 product.attribute.text))

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

        avito_document.add_elem(ad)
        print(f'gen 1 product at {time.time() - timestart_one}')

    avito_document.close_document()
    print(f'generate full avito file at {time.time() - timestart}')


if __name__ == '__main__':
    gidrachDB.init()
    avito_xml(gidrachDB.products)
