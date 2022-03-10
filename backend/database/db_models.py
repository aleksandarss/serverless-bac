from sqlalchemy import Column, Integer, String, Table, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'tests'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    total_points = Column('text', Integer)
    assignments = relationship('Assignment')
    course_id = Column('course_id', ForeignKey('course.id'))


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    answer = Column('answer', String)
    points = Column('points', Integer)
    test_id = Column(Integer, ForeignKey('tests.id'))

class Class(Base):
    __tablename__ = 'classes'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    course_id = Column('course_id', ForeignKey('courses.id'))
    assignments = relationship('Assignment')


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', VARCHAR(1024))
    date_joined = Column('date_joined', DateTime(timezone=True))
    first_name = Column('first_name', VARCHAR(1024))
    last_name = Column('last_name', VARCHAR(1024))
    # tests = relationship('Test', secondary=take_test)
    # courses = relationship('Course', secondary=take_course)
    course_teach = relationship('Course')

class Course(Base):
    __tablename__ = 'courses'

    id = Column('id', Integer, primary_key=True)
    description = Column('text', String)
    tests = relationship('Test')
    classes = relationship('Class')
    teacher_id = Column('teacher_id', ForeignKey('users.id'))

take_course = Table('take_course', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('course_id', ForeignKey('courses.id'))
)

take_test = Table('take_test', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('test_id', ForeignKey('tests.id'))
)