from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'tests'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    total_points = Column('text', Integer)
    assignments = relationship('Assignment')