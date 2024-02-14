import re

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, VARCHAR, DECIMAL, ForeignKeyConstraint, PrimaryKeyConstraint, Boolean, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column, attribute_mapped_collection, validates, Mapped
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

from config import type_dict

Base = declarative_base()


class ProductBase(Base):
    __tablename__ = 'oc_product'
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    image: Mapped[str] = mapped_column(VARCHAR)
    video_youtube: Mapped[str] = mapped_column(VARCHAR)
    product_images = relationship('ProductImage', back_populates='product')


class Product(ProductBase):
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price = mapped_column(DECIMAL(15, 4), nullable=False, default=0.0000)
    model: Mapped[str] = mapped_column(VARCHAR, nullable=False)

    mpn: Mapped[str] = mapped_column(VARCHAR)

    main_car_sku: Mapped[str] = mapped_column("main_car_sku", VARCHAR, ForeignKey('oc_product.sku'))
    main_car = relationship('ProductCar', remote_side=ProductBase.sku, lazy='selectin', join_depth=0)
    location = mapped_column(VARCHAR)

    # categories = relationship('ProductCategory', back_populates='product', lazy='joined')

    manufacturer_id = mapped_column(VARCHAR, ForeignKey('oc_manufacturer.manufacturer_id'))
    manufacturer = relationship("Manufacturer", lazy='joined')

    # selectin 0.39 2300mb
    # joined 0.41 2500mb
    # subquery 0.48 2250mb

    description = relationship('ProductDescription', back_populates='product', uselist=False, lazy='selectin')
    attributes = relationship('ProductAttribute', back_populates='product',
                              collection_class=attribute_mapped_collection('attribute_id'), lazy='selectin')

    # @hybrid_property
    # def main_category(self):
    #     for category in self.categories:
    #         if category.main_category:
    #             return category.category


class Manufacturer(Base):
    __tablename__ = 'oc_manufacturer'
    manufacturer_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=False)


class ProductCar(ProductBase):
    dism_product = relationship('DismantlingProduct', back_populates='product', lazy='joined')


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
    attribute_id = Column(Integer, nullable=False, primary_key=True)
    text = Column(VARCHAR)

    attribute_description = relationship('AttributeDescription', uselist=False, lazy='selectin')

    product = relationship('Product', back_populates='attributes')


class ProductImage(Base):
    __tablename__ = 'oc_product_image'
    product_image_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('oc_product.product_id'), nullable=False)
    image = Column(VARCHAR)

    product = relationship('Product', back_populates='product_images')


class AttributeDescription(Base):
    __tablename__ = 'oc_attribute_description'
    attribute_id = Column(Integer, ForeignKey('oc_product_attribute.attribute_id'), primary_key=True)
    name = Column(VARCHAR, nullable=False)


class InformationDescription(Base):
    __tablename__ = 'oc_information_description'
    information_id = Column(Integer, primary_key=True)
    title = Column(VARCHAR)
    description = Column(VARCHAR)


# class Category(Base):
#     __tablename__ = 'oc_category'
#     category_id = Column(Integer, primary_key=True)
#     avito_generation_id = Column(Integer)
#
#
# class ProductCategory(Base):
#     __tablename__ = 'oc_product_to_category'
#     product_id = Column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
#     category_id = Column(Integer, ForeignKey('oc_category.category_id'), primary_key=True)
#     main_category = Column(Boolean)
#
#     category = relationship('Category', lazy='joined')
#     product = relationship('Product', back_populates='categories')


class Dismantling(Base):
    __tablename__ = 'oc_dismantling'
    dism_id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('oc_dismantling_param.type_id'))
    avito_id = Column(Integer)
    name = Column(VARCHAR)

    dismantling_param = relationship('DismantlingParam')


class DismantlingParam(Base):
    __tablename__ = 'oc_dismantling_param'
    param_id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    tag = Column(VARCHAR)
    name = Column(VARCHAR)


class DismantlingProduct(Base):
    __tablename__ = 'oc_product_dismantling'
    product_id = Column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    dism_id = Column(Integer, ForeignKey('oc_dismantling.dism_id'), primary_key=True)

    product = relationship('ProductCar', back_populates='dism_product')
    dism = relationship('Dismantling', lazy='selectin')
