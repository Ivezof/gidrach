from sqlalchemy import VARCHAR, Integer, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class ProductBase(Base):
    __tablename__ = 'oc_product'
    image: Mapped[str] = mapped_column(VARCHAR, index=True)
    video_youtube: Mapped[str] = mapped_column(VARCHAR, index=True)
    product_images: Mapped[list] = relationship('ProductImage', back_populates='product', lazy='joined')
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(VARCHAR, nullable=False)

    @hybrid_property
    def all_images(self):
        images = [self.image]
        if not self.product_images:
            return images
        if type(self.product_images) is list:
            for img in self.product_images:
                images.append(img.image)
        else:
            images.append(self.product_images.image)
        return images


class Product(ProductBase):

    price: Mapped[int] = mapped_column(Integer)
    mpn: Mapped[str] = mapped_column(VARCHAR)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    description = relationship('ProductDescription', back_populates='product', uselist=False, lazy='joined')
    main_car_sku: Mapped[str] = mapped_column("main_car_sku", VARCHAR, ForeignKey('oc_product.sku'), index=True)
    main_car = relationship('ProductCar', remote_side=ProductBase.sku, join_depth=0, lazy='selectin')

    categories = relationship('ProductCategory', back_populates='product', lazy='joined')


class ProductCar(ProductBase):
    pass


class ProductDescription(Base):
    __tablename__ = 'oc_product_description'
    product_id = mapped_column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    name = mapped_column(VARCHAR, nullable=False)
    description = mapped_column(VARCHAR, nullable=False)
    product = relationship('Product', back_populates='description')


class ProductImage(Base):
    __tablename__ = 'oc_product_image'
    product_image_id = mapped_column(Integer, primary_key=True)
    product_id = mapped_column(Integer, ForeignKey('oc_product.product_id'), nullable=False)
    image = mapped_column(VARCHAR)

    product = relationship('Product', back_populates='product_images')


class Category(Base):
    __tablename__ = 'oc_category'
    category_id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey('oc_category.category_id'))
    avito_generation_id = mapped_column(Integer)
    parent = relationship('Category', remote_side=[category_id])


class ProductCategory(Base):
    __tablename__ = 'oc_product_to_category'
    product_id = mapped_column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    category_id = mapped_column(Integer, ForeignKey('oc_category.category_id'), primary_key=True)
    main_category = mapped_column(Boolean)

    category = relationship('Category')
    product = relationship('Product', back_populates='categories')
