from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Review(Base):
    __tablename__ = 'Review'

    user_id = Column("User ID", String, primary_key=True)
    asin = Column("ASIN", String, primary_key=True)
    rating = Column("Rating", String)
    product_title = Column("Product Title", String)