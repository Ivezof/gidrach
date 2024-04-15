"""

INSERT INTO `oc_order` (`order_id`, `invoice_no`, `invoice_prefix`, `store_id`, `store_name`, `store_url`, `customer_id`, `customer_group_id`, `firstname`, `lastname`, `email`, `telephone`, `fax`, `custom_field`, `payment_firstname`, `payment_lastname`, `payment_company`, `payment_address_1`, `payment_address_2`, `payment_city`, `payment_postcode`, `payment_country`, `payment_country_id`, `payment_zone`, `payment_zone_id`, `payment_address_format`, `payment_custom_field`, `payment_method`, `payment_code`, `shipping_firstname`, `shipping_lastname`, `shipping_company`, `shipping_address_1`, `shipping_address_2`, `shipping_city`, `shipping_postcode`, `shipping_country`, `shipping_country_id`, `shipping_zone`, `shipping_zone_id`, `shipping_address_format`, `shipping_custom_field`, `shipping_method`, `shipping_code`, `comment`, `total`, `order_status_id`, `affiliate_id`, `commission`, `marketing_id`, `tracking`, `language_id`, `currency_id`, `currency_code`, `currency_value`, `ip`, `forwarded_ip`, `user_agent`, `accept_language`, `date_added`, `date_modified`, `payment_company_id`, `payment_tax_id`, `order_note_date`, `comment_manager`, `calculated_summ`, `delivery_price`, `build_price`, `build_price_yes_no`, `build_price_prefix`, `rise_product_price`, `rise_product_yes_no`, `rise_product_price_prefix`, `manager_process_orders`, `text_ttn`) VALUES
(NULL, '0', 'INV-2013-00', '0', 'ГИДРАЧ.РФ', 'https://xn--80afdp5b4b.xn--p1ai/', '0', '0', 'Антон', '', '', '', '', '', 'Антон', '', '', '', '', '', '', '', '176', '', '0', '', '', '', '', 'Антон', '', '', '', '', '', '', '', '176', '', '2793', '', '', '', '', '', '1200.0000', '0', '0', '0', '0', '', '1', '1', 'RUB', '1.00000000', '', '', '', '', '2024-03-18 22:11:40', '2024-03-18 22:11:40', '', '', NULL, '', '0.0000', '0.0000', '0.0000', 'N', '+', '0.0000', 'N', '+', '', '');

"""
import datetime

from sqlalchemy import VARCHAR, Integer, ForeignKey, Boolean, Text, DATETIME
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from ..oc_product import Product

Base = declarative_base()


class Order(Base):
    __tablename__ = 'oc_order'
    order_id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, nullable=False)
    invoice_no: Mapped[int] = mapped_column(Integer, index=True, default=0, nullable=False)
    invoice_prefix: Mapped[str] = mapped_column(VARCHAR, default='INV-2013-00', nullable=False)
    store_id: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    store_name: Mapped[str] = mapped_column(VARCHAR, default='ГИДРАЧ.РФ', nullable=False)
    store_url: Mapped[str] = mapped_column(VARCHAR, default='https://xn--80afdp5b4b.xn--p1ai/', nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    customer_group_id: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    firstname: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    lastname: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    email: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    telephone: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    fax: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    custom_field: Mapped[str] = mapped_column(Text, nullable=False, default='')
    payment_firstname: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    payment_lastname: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_company: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_address_1: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_address_2: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_city: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_postcode: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_country: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_country_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_zone: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_zone_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    payment_address_format: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_custom_field: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_method: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_code: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_firstname: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    shipping_lastname: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_company: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_address_1: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_address_2: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_city: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_postcode: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_country: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_country_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shipping_zone: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_zone_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shipping_address_format: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_custom_field: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_method: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    shipping_code: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    comment: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    order_status_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    affiliate_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    commission: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    marketing_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tracking: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    language_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    currency_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    currency_code: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='RUB')
    currency_value: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    ip: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    forwarded_ip: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    user_agent: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    accept_language: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    date_added: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=False, default='')
    date_modified: Mapped[datetime.datetime] = mapped_column(DATETIME, nullable=False, default='')
    payment_company_id: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    payment_tax_id: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    comment_manager: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    manager_process_orders: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    text_ttn: Mapped[str] = mapped_column(VARCHAR, nullable=False, default='')
    tezarius_id: Mapped[str] = mapped_column(VARCHAR, nullable=True, default=None)
    order_product = relationship('OrderProduct', back_populates='order', uselist=True)


class OrderProduct(Base):
    __tablename__ = 'oc_order_product'
    order_product_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('oc_order.order_id'))
    order = relationship('Order', back_populates='order_product', uselist=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey(Product.product_id))
    product: Mapped[Product] = relationship(Product, uselist=False)
    name: Mapped[str] = mapped_column(VARCHAR)
    model: Mapped[str] = mapped_column(VARCHAR)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    tax: Mapped[int] = mapped_column(Integer, default=0)
    reward: Mapped[int] = mapped_column(Integer, default=0)


class OrderStatus(Base):
    __tablename__ = 'oc_order_status'
    order_status_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(VARCHAR)



'''

dt = datetime.strptime(fsale.get('doc_date'), '%Y-%m-%d')
custom_order_product.name = pr.description.name
custom_order_product.product_id = 244231
custom_order_product.total = fsale.get('total')
custom_order_product.price = pr.price
custom_order_product.quantity = fsale.get('qty')
custom_order.total = fsale.get('total')
custom_order.payment_firstname = fsale.get('CounterpartsName')
custom_order.shipping_firstname = fsale.get('CounterpartsName')
custom_order.firstname = fsale.get('CounterpartsName')
custom_order.order_status_id = 5 if int(fsale.get('isCanceled')) == 0 else 8
custom_order.store_name = fsale.get('FirmName')
custom_order.date_added = fsale.get('doc_date')

'''
