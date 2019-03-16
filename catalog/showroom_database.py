import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
            }


class Showroom(Base):
    __tablename__ = 'showroom'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


@property
def serialize(self):
    return {'name': self. name, 'id': self. id}


class Bike(Base):
    __tablename__ = 'bike'
    bike_name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    about = Column(String(250))
    millage = Column(String(10))
    engine_capacity = Column(String(20))
    max_power = Column(String(1000))
    Transmission = Column(Integer)
    kerb_weight = Column(String(100))
    price = Column(String(100))
    bike_id = Column(Integer, ForeignKey('showroom.id'))
    showroom = relationship(Showroom)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'bike_name': self. bike_name,
            'id': self. id,
            'about': self. about,
            'millage': self. millage,
            'engine_capacity': self. engine_capacity,
            'max_power': self. max_power,
            'Transmission': self. Transmission,
            'kerb_weight': self. kerb_weight,
            'price': self. price,
            'bike_id': self. bike_id
            }
engine = create_engine('sqlite:///bikewala.db')
Base.metadata.create_all(engine)

