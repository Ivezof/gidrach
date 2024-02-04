import re

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, VARCHAR, DECIMAL, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from config import type_dict

Base = declarative_base()


class Product(Base):
    __tablename__ = 'oc_product'
    product_id = Column(Integer, primary_key=True)
    sku = Column(VARCHAR, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(DECIMAL(15, 4), nullable=False, default=0.0000)
    model = Column(VARCHAR, nullable=False)
    image = Column(VARCHAR)
    mpn = Column(VARCHAR)
    video_youtube = Column(VARCHAR)
    main_car_sku = Column(VARCHAR)
    location = Column(VARCHAR)

    manufacturer_id = Column(VARCHAR, ForeignKey('oc_manufacturer.manufacturer_id'))
    manufacturer = relationship("Manufacturer")

    description = relationship('ProductDescription', back_populates='product', uselist=False)
    attribute = relationship('ProductAttribute', back_populates='product', uselist=False)


class Manufacturer(Base):
    __tablename__ = 'oc_manufacturer'
    manufacturer_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)


class ProductDescription(Base):
    __tablename__ = 'oc_product_description'
    product_id = Column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    name = Column(VARCHAR, nullable=False)
    meta_h1 = Column(VARCHAR)
    description = Column(VARCHAR, nullable=False)

    product = relationship('Product', back_populates='description')


class ProductAttribute(Base):
    __tablename__ = 'oc_product_attribute'
    product_id = Column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    attribute_id = Column(Integer, ForeignKey('oc_attribute_description.attribute_id'), nullable=False)
    text = Column(VARCHAR)

    attribute_description = relationship('AttributeDescription')

    product = relationship('Product', back_populates='attribute')


class AttributeDescription(Base):
    __tablename__ = 'oc_attribute_description'
    attribute_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)
