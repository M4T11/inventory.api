from sqlalchemy import Date, Column, ForeignKey, Integer, String, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import relationship
from .database import Base


class Locations(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    devices = relationship('Devices', back_populates="location")

class Producers(Base):
    __tablename__ = "producers"
    producer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ean_device = relationship('EAN_Devices', back_populates="producer")

class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ean_device = relationship('EAN_Devices', back_populates="category")

class EAN_Devices(Base):
    __tablename__ = "ean_devices"
    ean_device_id = Column(Integer, primary_key=True, index=True)
    ean = Column(String)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    producer_id = Column(Integer, ForeignKey('producers.producer_id'))
    model = Column(String)

    producer = relationship('Producers', back_populates='ean_device', lazy='subquery')
    category = relationship('Categories', back_populates='ean_device', lazy='subquery')

    devices = relationship('Devices', back_populates="ean_device")

class Devices(Base):
    __tablename__ = "devices"
    device_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    serial_number = Column(String)
    description = Column(String)

    ean_device_id = Column(Integer, ForeignKey('ean_devices.ean_device_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    status = Column(String)
    date_added = Column(Date)
    qr_code = Column(String)

    location = relationship('Locations', back_populates='devices', lazy='subquery')
    ean_device = relationship('EAN_Devices', back_populates='devices', lazy='subquery')
    history = relationship('Device_histories', back_populates='device')


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)

    devices_history = relationship('Device_histories', back_populates="user")


class Device_histories(Base):
    __tablename__ = "device_histories"
    history_id = Column(Integer, primary_key=True, index=True)
    event = Column(String)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    date = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship('Users', back_populates='devices_history', lazy='subquery')
    device = relationship('Devices', back_populates='history', lazy='subquery')