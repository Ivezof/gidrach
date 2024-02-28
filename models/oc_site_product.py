from sqlalchemy import VARCHAR, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = 'oc_product'
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(VARCHAR)
    description = relationship('ProductDescription', back_populates='product', uselist=False, lazy='joined')


class ProductDescription(Base):
    __tablename__ = 'oc_product_description'
    product_id = mapped_column(Integer, ForeignKey('oc_product.product_id'), primary_key=True)
    name = mapped_column(VARCHAR, nullable=False)
    description = mapped_column(VARCHAR, nullable=False)

    product = relationship('Product', back_populates='description')
