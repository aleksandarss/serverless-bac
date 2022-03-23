from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Class(Base):
    __tablename__ = 'classes'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    class_id = Column('Integer', ForeignKey('classes.id'))
    assignments = relationship('Assignment')