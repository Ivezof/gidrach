import re
import time
from xml.sax.saxutils import escape

import config
import gidrachDB
import tezariusDB
import xmlWriter
from config import type_dict
from gidrachDB import info_msg_uns_1, info_msg_uns_2, info_msg_1, info_msg_2
from models import oc_product

avito_document = xmlWriter.Document(config.xml_path, config.avito_xml_name, 'Ads',
                                    {'formatVersion': '3', 'target': "Avito.ru"})

avito_sep_document = xmlWriter.Document(config.xml_path, config.avito_sep_xml_name, 'Ads',
                                        {'formatVersion': '3', 'target': "Avito.ru"})

drom_document = xmlWriter.Document(config.xml_path, config.drom_xml_name, 'offers')

p = re.compile("&lt(.*?)&gt;")
msg_drom_1 = p.sub("", info_msg_1.description.replace("&lt;b&gt;", "\n").replace("&amp;nbsp;", " ")).replace("&quot;",
                                                                                                             "")
msg_drom_2 = p.sub("", info_msg_2.description.replace("&lt;br&gt;", "\n").replace("&amp;nbsp;", " ")).replace("&quot;",
                                                                                                              "")


def desc_formatted(new_name, text):
    new_text_split = text.split("\n")
    new_text_split[0] = "&lt;br /&gt;" + new_name
    new_desc = "\n".join(new_text_split)
    return new_desc


def get_type_product(product_attr):
    if product_attr in type_dict:
        return type_dict.get(product_attr)
    for k, v in type_dict.items():
        if re.search(k.replace('*', '\\w*').replace('|', '\\|'), product_attr):
            return v


def update_product_on_site(products: dict):
    tz_products = tezariusDB.Products()
    for tz_product_page in tz_products:
        for tz_product in tz_product_page:
            sku: str = str(tz_product['code'])
            price: int = 0 if tz_product['cost_retail'] is None else int(float(tz_product['cost_retail']))
            qty: int = 0 if tz_product['qty'] is None else int(float(tz_product['qty']))
            name: str = str(tz_product['name'])
            storage_place: str = str(tz_product['StoragePlaces'])

            if sku in products:
                product = products[sku]
                if qty is None:
                    qty = 0
                if price is None or name is None or price == 0:
                    continue
                # request = update(oc_site_product.Product).where(oc_site_product.Product.sku == sku)
                product.price = price
                product.quantity = qty
                product.description.name = name
                product.location = storage_place
                gidrachDB.session.add(product)
                gidrachDB.session.flush()
    gidrachDB.session.commit()


# def validate_products_xml(products: list[gidrachDB.Product]):
#     valid_products = {'default': []}
#     for product in products:
#         time_start = time.time()
#         if not product.main_car or product.main_car == '' or config.attr_ids['make'] not in product.main_car.attributes:
#             continue
#         elif not product.main_car.dism_product:
#             continue
#
#         valid_products['default'].append(product)
#         print(f'1 prods as {time.time() - time_start}')
#     return valid_products


def avito_default_elems(product: gidrachDB.Product, ad: xmlWriter.Elem):
    # id товара
    id_ad = xmlWriter.Elem('Id', parent_elem=ad)
    id_ad.set_content(product.sku)

    # номер телефона
    phone = xmlWriter.Elem('ContactPhone', parent_elem=ad)
    phone.set_content('+79876543210')

    # avitoId
    xmlWriter.Elem("AvitoId", parent_elem=ad)

    # ad type
    ad_type = xmlWriter.Elem('AdType', parent_elem=ad)
    ad_type.set_content('Товар приобретен на продажу')

    # description
    description = xmlWriter.Elem('Description', parent_elem=ad)
    description.set_content(info_msg_uns_1
                            + "\n\n"
                            + gidrachDB.unescape_text(product.description.description)
                            + "\n\n"
                            + info_msg_uns_2, cdata=True)

    # manager_name
    manager_name = xmlWriter.Elem('ManagerName', parent_elem=ad)
    manager_name.set_content(config.manager_name)

    # title
    title = xmlWriter.Elem('Title', parent_elem=ad)
    title.set_content(escape(product.description.name))

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


def avito_rim_default_elems(product: gidrachDB.Product, ad: xmlWriter.Elem):
    # Характеристики шины
    for attr_id, attr_obj in product.attributes.items():
        if attr_id in config.buss_disk_caps_attr_id:
            attr_tag = xmlWriter.Elem(config.buss_disk_caps_attr_id.get(attr_id), parent_elem=ad)
            attr_tag.set_content(attr_obj.text)

    # images
    product_imgs = product.all_images

    images = xmlWriter.Elem('Images', parent_elem=ad)

    for img in product_imgs[:4]:
        xmlWriter.Elem('Image', attr={'url': img}, parent_elem=images)


def avito_xml_accessories(products: list[gidrachDB.Product], document: xmlWriter.Document):
    for product in products:
        ad = xmlWriter.Elem('Ad')
        avito_default_elems(product, ad)

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Для салона')

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Аксессуары')

        # images
        product_imgs = product.all_images

        images = xmlWriter.Elem('Images', parent_elem=ad)

        for img in product_imgs[:4]:
            xmlWriter.Elem('Image', attr={'url': img}, parent_elem=images)

        main_car_imgs = product.main_car.all_images
        for img in main_car_imgs[:6]:
            xmlWriter.Elem('Image', attr={'url': img}, parent_elem=images)

        document.add_elem(ad)


@profile
def avito_xml_auto(products: list[gidrachDB.Product], document: xmlWriter.Document):
    timestart = time.time()

    for product in products:
        print(product.product_id)
        ad = xmlWriter.Elem('Ad')

        avito_default_elems(product, ad)

        dism_product: oc_product.DismantlingProduct
        main_car = product.main_car
        disms_product = main_car.dism_product
        for dism_product in disms_product:
            elem = xmlWriter.Elem(dism_product.dism.dismantling_param.tag, parent_elem=ad)
            elem.set_content(dism_product.dism.name)

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Запчасти')

        # SparePartType
        spare_part_type = xmlWriter.Elem('SparePartType', parent_elem=ad)
        for i in product.attributes.values():
            if i.attribute_description.name in config.spare_part_type:
                spare_part_type.set_content(config.spare_part_type.get(i.attribute_description.name))
                if i.attribute_description.name in config.tags:
                    # Spare Type tag
                    spare_type_tag = xmlWriter.Elem(config.tags.get(i.attribute_description.name)[0],
                                                    parent_elem=ad)
                    spare_type_tag.set_content(config.tags.get(i.attribute_description.name)[1]
                                               .get(i.text))
                break

        # oem_number
        oem_number = xmlWriter.Elem('OEM', parent_elem=ad)
        oem_number.set_content(product.mpn)

        # brand
        brand = xmlWriter.Elem('Brand', parent_elem=ad)
        brand.set_content(product.manufacturer.name)

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Для автомобилей')

        # images
        product_imgs = product.all_images

        images = xmlWriter.Elem('Images', parent_elem=ad)

        for img in product_imgs[:4]:
            xmlWriter.Elem('Image', attr={'url': img}, parent_elem=images)

        main_car_imgs = product.main_car.all_images
        for img in main_car_imgs[:6]:
            xmlWriter.Elem('Image', attr={'url': img}, parent_elem=images)

        document.add_elem(ad)

    print(f'generate full avito file at {time.time() - timestart}')


def avito_xml_buses(products: list[gidrachDB.Product], document: xmlWriter.Document):
    for product in products:
        ad = xmlWriter.Elem('Ad')

        avito_default_elems(product, ad)

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Шины, диски и колёса')

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Легковые шины')

        # add default rim attr
        avito_rim_default_elems(product, ad)

        document.add_elem(ad)


def avito_xml_caps(products: list[gidrachDB.Product], document: xmlWriter.Document):
    for product in products:
        ad = xmlWriter.Elem('Ad')

        avito_default_elems(product, ad)

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Шины, диски и колёса')

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Колпаки')

        # add default rim attr
        avito_rim_default_elems(product, ad)

        document.add_elem(ad)


def avito_xml_disks(products: list[gidrachDB.Product], document: xmlWriter.Document):
    for product in products:
        ad = xmlWriter.Elem('Ad')

        avito_default_elems(product, ad)

        # GoodsType
        goods_type = xmlWriter.Elem('GoodsType', parent_elem=ad)
        goods_type.set_content('Шины, диски и колёса')

        # ProductType
        product_type = xmlWriter.Elem('ProductType', parent_elem=ad)
        product_type.set_content('Диски')

        # add default rim attr
        avito_rim_default_elems(product, ad)

        document.add_elem(ad)


def drom_xml(products: list[gidrachDB.Product], document: xmlWriter.Document):
    for product in products:
        offer = xmlWriter.Elem('offer')

        # название товара
        name = xmlWriter.Elem('name', parent_elem=offer)
        name.set_content(product)

        # condition
        condition = xmlWriter.Elem('condition', parent_elem=offer)
        condition.set_content('Б/у')

        # cost
        cost = xmlWriter.Elem('cost', parent_elem=offer)
        cost.set_content(product.price)

        # oem_number
        oem_number = xmlWriter.Elem('oem_number', parent_elem=offer)
        oem_number.set_content(product.mpn)

        # description
        normal_desc = product.description.description.replace("&lt;br /&gt;", "\n")
        normal_desc = p.sub("", normal_desc)
        description = xmlWriter.Elem('description', parent_elem=offer)
        description.set_content(msg_drom_1 + '\n\n' + normal_desc + '\n\n' + msg_drom_2)

        # photos && video
        media = xmlWriter.Elem('media', parent_elem=offer)
        photos = xmlWriter.Elem('photos', parent_elem=media)

        for img in product.all_images:
            photo = xmlWriter.Elem('photo', parent_elem=photos)
            photo.set_content(img)

        for img in product.main_car.all_images:
            photo = xmlWriter.Elem('photo', parent_elem=photos)
            photo.set_content(img)

        video = xmlWriter.Elem('video', parent_elem=media)
        video.set_content(product.main_car.video_youtube)


def start_xml_generation():
    # avito_xml_accessories(gidrachDB.get_accessories(), avito_document)
    avito_xml_auto(gidrachDB.get_products(), avito_document)

    # avito_xml_accessories(gidrachDB.get_accessories(separator=True), avito_sep_document)
    avito_xml_auto(gidrachDB.get_products(separator=True), avito_sep_document)
    avito_document.close_document()
    avito_sep_document.close_document()


if __name__ == '__main__':
    # update_product_on_site(gidrachDB.get_all_products())
    start_xml_generation()
