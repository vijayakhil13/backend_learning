from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Float
Base= declarative_base()
class Products(Base):
        __tablename__="apii"
        id= Column(Integer, primary_key=True, index=True)
        name= Column(String)
        des= Column(String)
        quantity= Column(Integer)