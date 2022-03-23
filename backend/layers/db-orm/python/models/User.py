from sqlalchemy import Column, Integer, Table, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


take_test = Table('take_test', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('test_id', ForeignKey('tests.id'))
)


take_course = Table('take_course', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('course_id', ForeignKey('courses.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', VARCHAR(1024))
    date_joined = Column('date_joined', DateTime(timezone=True))
    first_name = Column('first_name', VARCHAR(1024))
    last_name = Column('last_name', VARCHAR(1024))
    tests = relationship('Test', secondary=take_test)
    courses = relationship('Course', secondary=take_course)
    course_teach = relationship('Course')