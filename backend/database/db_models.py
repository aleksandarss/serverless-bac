from sqlalchemy import Column, Integer, String, Table, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String)
    answer = Column('answer', String)
    points = Column('points', Integer)
    test_id = Column(Integer, ForeignKey('tests.id'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Test(Base):
    __tablename__ = 'tests'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    text = Column('text', String)
    total_points = Column('total_points', Integer)
    assignments = relationship(Assignment)
    course_id = Column('course_id', ForeignKey('courses.id'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Class(Base):
    __tablename__ = 'classes'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    text = Column('text', String)
    course_id = Column('course_id', ForeignKey('courses.id'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TakeCourse(Base):
    __tablename__ = 'take_course'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    course_id = Column('course_id', ForeignKey('courses.id'))
    progress = Column('progress', Integer, nullable=True)
    user = relationship('User', backref=backref("course_assoc"))
    course = relationship('Course', backref=backref("user_assoc"))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TakeTest(Base):
    __tablename__ = 'take_test'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    points = Column('points', Integer)
    user_id = Column('user_id', ForeignKey('users.id')),
    test_id = Column('test_id', ForeignKey('tests.id'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Course(Base):
    __tablename__ = 'courses'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', String)
    tests = relationship(Test)
    classes = relationship(Class)
    teacher_id = Column('teacher_id', ForeignKey('users.id'))
    students = relationship('User', secondary='take_course')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', VARCHAR(1024))
    date_joined = Column('date_joined', DateTime(timezone=True))
    first_name = Column('first_name', VARCHAR(1024))
    last_name = Column('last_name', VARCHAR(1024))
    role = Column('role', String)
    # tests = relationship(TakeTest)
    courses = relationship(Course, secondary='take_course')
    course_teach = relationship(Course)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
