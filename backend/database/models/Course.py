from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column('id', Integer, primary_key=True)
    description = Column('text', String)
    tests = relationship('Class')
    teacher_id = Column('teacher_id', ForeignKey('user.id'))
