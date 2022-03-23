from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    answer = Column('answer', String)
    points = Column('points', Integer)
    test_id = Column(Integer, ForeignKey('tests.id'))