from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from config.index import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(250))
    password = Column(String(250))
    company_id = Column(Integer,ForeignKey("companies.id"))
    company = relationship("Company", back_populates="users")
