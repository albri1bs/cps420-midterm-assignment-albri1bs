from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class Category(str, enum.Enum):
    electronics  = "electronics"
    clothing     = "clothing"
    accessories  = "accessories"
    books        = "books"
    keys         = "keys"
    wallet       = "wallet"
    other        = "other"

class Status(str, enum.Enum):
    lost         = "lost"
    found        = "found"
    claimed      = "claimed"

class Item(Base):
    __tablename__ = "items"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(200), nullable=False)
    description  = Column(String(1000), default="")
    category     = Column(Enum(Category), default=Category.other)
    location     = Column(String(200), nullable=False)
    status       = Column(Enum(Status), default=Status.lost)
    resolved     = Column(Boolean, default=False)
    date_lost    = Column(DateTime(timezone=True), nullable=False)
    created      = Column(DateTime(timezone=True), server_default=func.now())
    claims       = relationship("Claim", back_populates="item",
                                cascade="all, delete-orphan")

class Claim(Base):
    __tablename__ = "claims"

    id             = Column(Integer, primary_key=True, index=True)
    item_id        = Column(Integer, ForeignKey("items.id"), nullable=False)
    claimant_name  = Column(String(100), nullable=False)
    claimant_email = Column(String(150), nullable=False)
    description    = Column(String(1000), nullable=False)
    approved       = Column(Boolean, default=False)
    created        = Column(DateTime(timezone=True), server_default=func.now())
    item           = relationship("Item", back_populates="claims")