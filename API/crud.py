from sqlalchemy.orm import Session
import API.models as models
import API.schemas as schemas
from datetime import date, datetime
import uuid

# Locations
def get_locations(db: Session):
    return db.query(models.Locations).all()


def get_location_by_name(db: Session, name: str):
    return db.query(models.Locations).filter(models.Locations.name == name).first()


def get_location_by_id(db: Session, location_id: int):
    return db.query(models.Locations).filter(models.Locations.location_id == location_id).first()


def create_location(db: Session, location: schemas.LocationsSchema):
    db_location = models.Locations(name=location.name)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


def update_location_by_name(db: Session, name: str, location: schemas.LocationsSchema):
    n_location = db.query(models.Locations).filter(models.Locations.name == name).first()
    n_location.name = location.name
    db.commit()
    db.refresh(n_location)
    return n_location


def update_location_by_id(db: Session, location_id: int, location: schemas.LocationsSchema):
    n_location = db.query(models.Locations).filter(models.Locations.location_id == location_id).first()
    n_location.name = location.name
    db.commit()
    db.refresh(n_location)
    return n_location


def delete_location_by_name(db: Session, name: str):
    db_location = db.query(models.Locations).filter(models.Locations.name == name).first()
    db.delete(db_location)
    db.commit()
    return db_location


def delete_location_by_id(db: Session, location_id: int):
    db_location = db.query(models.Locations).filter(models.Locations.location_id == location_id).first()
    db.delete(db_location)
    db.commit()
    return db_location

# Producers
def get_producers(db: Session):
    return db.query(models.Producers).all()


def get_producer_by_name(db: Session, name: str):
    return db.query(models.Producers).filter(models.Producers.name == name).first()


def get_producer_by_id(db: Session, producer_id: int):
    return db.query(models.Producers).filter(models.Producers.producer_id == producer_id).first()


def create_producer(db: Session, producer: schemas.ProducersSchema):
    db_producer = models.Producers(name=producer.name)
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)
    return db_producer


def update_producer_by_name(db: Session, name: str, producer: schemas.ProducersSchema):
    n_producer = db.query(models.Producers).filter(models.Producers.name == name).first()
    n_producer.name = producer.name
    db.commit()
    db.refresh(n_producer)
    return n_producer


def update_producer_by_id(db: Session, producer_id: int, producer: schemas.ProducersSchema):
    n_producer = db.query(models.Producers).filter(models.Producers.producer_id == producer_id).first()
    n_producer.name = producer.name
    db.commit()
    db.refresh(n_producer)
    return n_producer


def delete_producer_by_name(db: Session, name: str):
    db_producer = db.query(models.Producers).filter(models.Producers.name == name).first()
    db.delete(db_producer)
    db.commit()
    return db_producer


def delete_producer_by_id(db: Session, producer_id: int):
    db_producer = db.query(models.Producers).filter(models.Producers.producer_id == producer_id).first()
    db.delete(db_producer)
    db.commit()
    return db_producer

# Categories
def get_categories(db: Session):
    return db.query(models.Categories).all()


def get_category_by_name(db: Session, name: str):
    return db.query(models.Categories).filter(models.Categories.name == name).first()


def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Categories).filter(models.Categories.category_id == category_id).first()


def create_category(db: Session, category: schemas.CategoriesSchema):
    db_category = models.Categories(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category_by_name(db: Session, name: str, category: schemas.CategoriesSchema):
    n_category = db.query(models.Categories).filter(models.Categories.name == name).first()
    n_category.name = category.name
    db.commit()
    db.refresh(n_category)
    return n_category


def update_category_by_id(db: Session, category_id: int, category: schemas.CategoriesSchema):
    n_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    n_category.name = category.name
    db.commit()
    db.refresh(n_category)
    return n_category


def delete_category_by_name(db: Session, name: str):
    db_category = db.query(models.Categories).filter(models.Categories.name == name).first()
    db.delete(db_category)
    db.commit()
    return db_category


def delete_category_by_id(db: Session, category_id: int):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    db.delete(db_category)
    db.commit()
    return db_category

# EAN Devices

def get_ean_devices(db: Session, category_name=None, producer_name=None):
    if category_name is not None:
        return db.query(models.EAN_Devices).join(models.Categories).filter(models.Categories.name == category_name).all()
    if producer_name is not None:
        return db.query(models.EAN_Devices).join(models.Producers).filter(models.Producers.name == producer_name).all()
    return db.query(models.EAN_Devices).all()

def get_ean_device_by_model(db: Session, model: str):
    return db.query(models.EAN_Devices).filter(models.EAN_Devices.model == model).first()

def get_ean_device_by_id(db: Session, ean_device_id: int):
    return db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == ean_device_id).first()

def get_device_by_ean_code(db: Session, ean_code: str):
    return db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean_code).first()

def create_ean_device_by_name(db: Session, ean_device: schemas.EANDevicesSchema):
    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    db_ean_device = models.EAN_Devices(ean=ean_device.ean, category=category, producer=producer,
                               model=ean_device.model)
    db.add(db_ean_device)
    db.commit()
    db.refresh(db_ean_device)
    return db_ean_device

def create_ean_device_by_id(db: Session, ean_device: schemas.EANDevicesSchema):
    category = db.query(models.Categories).filter(models.Categories.category_id == ean_device.category.category_id).first()
    producer = db.query(models.Producers).filter(models.Producers.producer_id == ean_device.producer.producer_id).first()
    db_ean_device = models.EAN_Devices(ean=ean_device.ean, category=category, producer=producer,
                               model=ean_device.model)
    db.add(db_ean_device)
    db.commit()
    db.refresh(db_ean_device)
    return db_ean_device

def update_ean_device_by_ean(db: Session, ean: str, ean_device: schemas.EANDevicesSchema):
    n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean).first()
    n_ean_device.ean = ean_device.ean

    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    n_ean_device.category = category

    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    n_ean_device.producer = producer
    n_ean_device.model = ean_device.model

    db.commit()
    db.refresh(n_ean_device)
    return n_ean_device


def update_ean_device_by_id(db: Session, ean_device_id: int, ean_device: schemas.EANDevicesSchema):
    n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == ean_device_id).first()
    n_ean_device.ean = ean_device.ean

    category = db.query(models.Categories).filter(models.Categories.category_id == ean_device.category.category_id).first()
    n_ean_device.category = category

    producer = db.query(models.Producers).filter(models.Producers.producer_id == ean_device.producer.producer_id).first()
    n_ean_device.producer = producer
    n_ean_device.model = ean_device.model

    db.commit()
    db.refresh(n_ean_device)
    return n_ean_device

def update_ean_device_by_id_name(db: Session, ean_device_id: int, ean_device: schemas.EANDevicesSchema):
    n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == ean_device_id).first()
    n_ean_device.ean = ean_device.ean

    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    n_ean_device.category = category

    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    n_ean_device.producer = producer
    n_ean_device.model = ean_device.model

    db.commit()
    db.refresh(n_ean_device)
    return n_ean_device

def delete_ean_device_by_ean(db: Session, ean: str):
    db_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean).first()
    db.delete(db_ean_device)
    db.commit()
    return db_ean_device


def delete_ean_device_by_id(db: Session, ean_device_id: int):
    db_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == ean_device_id).first()
    db.delete(db_ean_device)
    db.commit()
    return db_ean_device

# Devices

def get_devices(db: Session, location_name=None, ean_code=None):
    if location_name is not None:
        return db.query(models.Devices).join(models.Locations).filter(models.Locations.name == location_name).all()
    if ean_code is not None:
        return db.query(models.Devices).join(models.EAN_Devices).filter(models.EAN_Devices.ean == ean_code).all()
    return db.query(models.Devices).all()

def get_device_by_name(db: Session, name: str):
    return db.query(models.Devices).filter(models.Devices.name == name).first()

def get_device_by_id(db: Session, device_id: int):
    return db.query(models.Devices).filter(models.Devices.device_id == device_id).first()

def get_device_by_qr_code(db: Session, qr_code: str):
    return db.query(models.Devices).filter(models.Devices.qr_code == qr_code).first()

def create_device_by_name(db: Session, device: schemas.DevicesSchema):
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == device.ean_device.ean).first()
    location = db.query(models.Locations).filter(models.Locations.name == device.location.name).first()
    db_device = models.Devices(name=device.name, serial_number=device.serial_number,
                               description=device.description, ean_device=ean_device,
                               location=location, quantity=device.quantity, condition=device.condition, status=device.status, date_added=date.today(),
                               qr_code=str(uuid.uuid4()))
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def create_device_by_id(db: Session, device: schemas.DevicesSchema):
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == device.ean_device.ean_device_id).first()
    location = db.query(models.Locations).filter(models.Locations.location_id == device.location.location_id).first()
    db_device = models.Devices(name=device.name, serial_number=device.serial_number,
                               description=device.description, ean_device=ean_device,
                               location=location, quantity=device.quantity, condition=device.condition, status=device.status, date_added=date.today(),
                               qr_code=str(uuid.uuid4()))
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device_by_name(db: Session, name: str, device: schemas.DevicesSchema):
    n_device = db.query(models.Devices).filter(models.Devices.name == name).first()
    n_device.name = device.name
    n_device.serial_number = device.serial_number
    n_device.description = device.description

    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == device.ean_device.ean).first()
    n_device.ean_device = ean_device
    location = db.query(models.Locations).filter(models.Locations.name == device.location.name).first()
    n_device.location = location

    n_device.quantity = device.quantity
    n_device.condition = device.condition
    n_device.status = device.status
    n_device.date_added = n_device.date_added
    n_device.qr_code = n_device.qr_code
    db.commit()
    db.refresh(n_device)
    return n_device

def update_device_by_id(db: Session, device_id: int, device: schemas.DevicesSchema):
    n_device = db.query(models.Devices).filter(models.Devices.device_id == device_id).first()
    n_device.name = device.name
    n_device.serial_number = device.serial_number
    n_device.description = device.description

    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == device.ean_device.ean_device_id).first()
    n_device.ean_device = ean_device
    location = db.query(models.Locations).filter(models.Locations.location_id == device.location.location_id).first()
    n_device.location = location

    n_device.quantity = device.quantity
    n_device.condition = device.condition
    n_device.status = device.status
    n_device.date_added = n_device.date_added
    n_device.qr_code = n_device.qr_code
    db.commit()
    db.refresh(n_device)
    return n_device


def delete_device_by_name(db: Session, name: str):
    db_device = db.query(models.Devices).filter(models.Devices.name == name).first()
    db.delete(db_device)
    db.commit()
    return db_device


def delete_device_by_id(db: Session, device_id: int):
    db_device = db.query(models.Devices).filter(models.Devices.device_id == device_id).first()
    db.delete(db_device)
    db.commit()
    return db_device

# # DeviceHistories
# def get_devices_histories(db: Session):
#     return db.query(models.Device_histories).all()
#
# def get_device_histories_by_name(db: Session, name: str):
#     return db.query(models.Device_histories).join(models.Devices).filter(models.Devices.name == name).all()
#
# def get_device_histories_by_id(db: Session, device_id: int):
#     return db.query(models.Device_histories).join(models.Devices).filter(models.Devices.device_id == device_id).all()
#
# def create_device_history(db: Session, event, device, user):
#     db_device_history = models.Device_histories(event=event, device=device, date=datetime.now(), user=user)
#     db.add(db_device_history)
#     db.commit()
#     db.refresh(db_device_history)
#     return db_device_history
#
# def delete_device_history_by_name(db: Session, name: str):
#     db_device_history = db.query(models.Device_histories).join(models.Devices).filter(models.Devices.name == name).all()
#     for d in db_device_history:
#         db.delete(d)
#         db.commit()
#     return db_device_history

# # UserAuthentication
# def get_users(db: Session):
#     return db.query(models.Users).all()
#
# def get_user_by_username(db: Session, username: str):
#     return db.query(models.Users).filter(models.Users.username == username).first()
#
# def create_user(db: Session, user: schemas.UsersSchema):
#     db_user = models.Users(username=user.username, password= auth.get_password_hash(user.password), email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def update_username(db: Session, username: str, user: schemas.UsersSchema):
#     n_user = db.query(models.Users).filter(models.Users.username == username).first()
#     n_user.username = user.username
#     n_user.password = auth.get_password_hash(user.password)
#     n_user.email = user.email
#     db.commit()
#     db.refresh(n_user)
#     return n_user

