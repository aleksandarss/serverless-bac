from sqlalchemy import Column, Integer, String, Table, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', VARCHAR(1024))
    date_joined = Column('date_joined', DateTime(timezone=True))
    full_name = Column('full_name', VARCHAR(1024))
    role = Column('role', String)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


post_tags = Table('post_tags', Base.metadata,
    Column('post_id', ForeignKey('posts.id')),
    Column('tag_id', ForeignKey('tags.id'))
)


class Post(Base):
    __tablename__ = 'posts'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    text = Column('text', String)
    author_id = Column('author_id', ForeignKey('users.id'))
    tags = relationship('Tag', secondary=post_tags)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', VARCHAR(1024))


class Comment(Base):
    __tablename__ = 'comments'
    



