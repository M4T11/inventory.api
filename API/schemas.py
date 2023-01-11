from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class LocationsSchema(BaseModel):
    location_id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True


class ProducersSchema(BaseModel):
    producer_id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True

class CategoriesSchema(BaseModel):
    category_id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True

class EANDevicesSchema(BaseModel):
    ean_device_id: Optional[int] = None
    ean: str
    category: CategoriesSchema
    producer: ProducersSchema
    model: str

    class Config:
        orm_mode = True



class DevicesSchema(BaseModel):
    device_id: Optional[int] = None
    name: str
    serial_number: str
    description: str
    ean_device: EANDevicesSchema
    location: LocationsSchema
    status: str
    date_added: date
    qr_code: str

    class Config:
        orm_mode = True


class UsersSchema(BaseModel):
    user_id: Optional[int] = None
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class DeviceHistoriesSchema(BaseModel):
    history_id: Optional[int] = None
    event: str
    device: DevicesSchema
    date: datetime
    user: UsersSchema

    class Config:
        orm_mode = True
