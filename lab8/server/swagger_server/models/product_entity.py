from ..database import db
from sqlalchemy.orm import Mapped, mapped_column

class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(db.String(300), unique=False, nullable=True)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    sku: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=True)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    created_at: Mapped[int]
    updated_at: Mapped[int]
    
    # def __repr__(self):
    #     return f'{self.name}'
    def __str__(self):
        return f'<Product name={self.name}, price={self.price}, quantity={self.quantity}>'
