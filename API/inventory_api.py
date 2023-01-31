import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from API.database import SessionLocal, engine
import API.models as models
import API.schemas as schemas
import API.crud as crud
from sqlalchemy.orm import Session
from typing import List, Optional

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Inventory API")

# Locations
@app.get("/locations/", response_model=List[schemas.LocationsSchema], tags=["Locations"])
async def get_locations(db: Session = Depends(get_db)):
    locations = crud.get_locations(db)
    return locations


@app.get("/locations/name/{location_name}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def get_location_by_name(location_name: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location_name)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@app.get("/locations/id/{location_id}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_id(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@app.post("/locations/", response_model=schemas.LocationsSchema, tags=["Locations"], status_code=201)
async def create_location(location: schemas.LocationsSchema, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location.name)
    if db_location:
        raise HTTPException(status_code=400, detail="Location already exists")
    return crud.create_location(db=db, location=location)


@app.put("/locations/name/{location_name}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def update_location_by_name(location_name: str, location: schemas.LocationsSchema, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location_name)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    n_location = db.query(models.Locations).filter(models.Locations.name == location.name).first()
    if n_location is not None and db_location.name != n_location.name:
        raise HTTPException(status_code=400, detail="Location already exists")
    return crud.update_location_by_name(db=db, name=location_name, location=location)


@app.put("/locations/id/{location_id}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def update_location_by_id(location_id: int, location: schemas.LocationsSchema, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_id(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    n_location = db.query(models.Locations).filter(models.Locations.name == location.name).first()
    if n_location is not None and db_location.name != n_location.name:
        raise HTTPException(status_code=400, detail="Location already exists")
    return crud.update_location_by_id(db=db, location_id=location_id, location=location)


@app.delete("/locations/name/{location_name}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def delete_location_by_name(location_name: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location_name)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db_location_devices = db.query(models.Devices).join(models.Locations).filter(models.Locations.name == location_name).all()
    if len(db_location_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The location assigned to the device cannot be deleted")
    return crud.delete_location_by_name(db=db, name=location_name)


@app.delete("/locations/id/{location_id}", response_model=schemas.LocationsSchema, tags=["Locations"])
async def delete_location_by_id(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_id(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db_location_devices = db.query(models.Devices).join(models.Locations).filter(models.Locations.location_id == location_id).all()
    if len(db_location_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The location assigned to the device cannot be deleted")
    return crud.delete_location_by_id(db=db, location_id=location_id)

# Producers
@app.get("/producers/", response_model=List[schemas.ProducersSchema], tags=["Producers"])
async def get_producers(db: Session = Depends(get_db)):
    producers = crud.get_producers(db)
    return producers


@app.get("/producers/name/{producer_name}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def get_producer_by_name(producer_name: str, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_name(db, name=producer_name)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer


@app.get("/producers/id/{producer_id}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def get_producer_by_id(producer_id: int, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_id(db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    return db_producer


@app.post("/producers/", response_model=schemas.ProducersSchema, tags=["Producers"], status_code=201)
async def create_producer(producer: schemas.ProducersSchema, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_name(db, name=producer.name)
    if db_producer:
        raise HTTPException(status_code=400, detail="Producer already exists")
    return crud.create_producer(db=db, producer=producer)


@app.put("/producers/name/{producer_name}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def update_producer_by_name(producer_name: str, producer: schemas.ProducersSchema, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_name(db, name=producer_name)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    n_producer = db.query(models.Producers).filter(models.Producers.name == producer.name).first()
    if n_producer is not None and db_producer.name != n_producer.name:
        raise HTTPException(status_code=400, detail="Producer already exists")
    return crud.update_producer_by_name(db=db, name=producer_name, producer=producer)


@app.put("/producers/id/{producer_id}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def update_producer_by_id(producer_id: int, producer: schemas.ProducersSchema, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_id(db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    n_producer = db.query(models.Producers).filter(models.Producers.name == producer.name).first()
    if n_producer is not None and db_producer.name != n_producer.name:
        raise HTTPException(status_code=400, detail="Producer already exists")
    return crud.update_producer_by_id(db=db, producer_id=producer_id, producer=producer)


@app.delete("/producers/name/{producer_name}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def delete_producer_by_name(producer_name: str, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_name(db, name=producer_name)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    db_producer_ean_devices = db.query(models.EAN_Devices).join(models.Producers).filter(models.Producers.name == producer_name).all()
    if len(db_producer_ean_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The producer assigned to the device cannot be deleted")
    return crud.delete_producer_by_name(db=db, name=producer_name)


@app.delete("/producers/id/{producer_id}", response_model=schemas.ProducersSchema, tags=["Producers"])
async def delete_producer_by_id(producer_id: int, db: Session = Depends(get_db)):
    db_producer = crud.get_producer_by_id(db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=404, detail="Producer not found")
    db_producer_ean_devices = db.query(models.EAN_Devices).join(models.Producers).filter(models.Producers.producer_id == producer_id).all()
    if len(db_producer_ean_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The producer assigned to the device cannot be deleted")
    return crud.delete_producer_by_id(db=db, producer_id=producer_id)

# Categories
@app.get("/categories/", response_model=List[schemas.CategoriesSchema], tags=["Categories"])
async def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


@app.get("/categories/name/{category_name}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def get_category_by_name(category_name: str, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.get("/categories/id/{category_id}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.post("/categories/", response_model=schemas.CategoriesSchema, tags=["Categories"], status_code=201)
async def create_category(category: schemas.CategoriesSchema, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db=db, category=category)


@app.put("/categories/name/{category_name}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def update_category_by_name(category_name: str, category: schemas.CategoriesSchema, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    n_category = db.query(models.Categories).filter(models.Categories.name == category.name).first()
    if n_category is not None and db_category.name != n_category.name:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.update_category_by_name(db=db, name=category_name, category=category)


@app.put("/categories/id/{category_id}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def update_category_by_id(category_id: int, category: schemas.CategoriesSchema, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    n_category = db.query(models.Categories).filter(models.Categories.name == category.name).first()
    if n_category is not None and db_category.name != n_category.name:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.update_category_by_id(db=db, category_id=category_id, category=category)



@app.delete("/categories/name/{category_name}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def delete_category_by_name(category_name: str, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category_name)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category_ean_devices = db.query(models.EAN_Devices).join(models.Categories).filter(models.Categories.name == category_name).all()
    if len(db_category_ean_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The category assigned to the device cannot be deleted")
    return crud.delete_category_by_name(db=db, name=category_name)


@app.delete("/categories/id/{category_id}", response_model=schemas.CategoriesSchema, tags=["Categories"])
async def delete_category_by_id(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category_ean_devices = db.query(models.EAN_Devices).join(models.Categories).filter(models.Categories.category_id == category_id).all()
    if len(db_category_ean_devices) > 0:
        raise HTTPException(status_code=500, detail=f"The category assigned to the device cannot be deleted")
    return crud.delete_category_by_id(db=db, category_id=category_id)

# EAN Devices
@app.get("/ean_devices/", response_model=List[schemas.EANDevicesSchema], tags=["EAN Devices"])
async def get_ean_devices(db: Session = Depends(get_db), category_name: Optional[str] = None, producer_name: Optional[str] = None):
    ean_devices = crud.get_ean_devices(db, category_name, producer_name)
    return ean_devices


@app.get("/ean_devices/model/{ean_device_model}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def get_ean_device_by_model(ean_device_model: str, db: Session = Depends(get_db)):
    db_ean_device = crud.get_ean_device_by_model(db, model=ean_device_model)
    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    return db_ean_device


@app.get("/ean_devices/id/{ean_devices_id}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def get_ean_device_by_id(ean_device_id: int, db: Session = Depends(get_db)):
    db_ean_device = crud.get_ean_device_by_id(db, ean_device_id=ean_device_id)
    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    return db_ean_device


@app.get("/ean_devices/ean/{ean_code}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def get_ean_device_by_ean_code(ean_code: str, db: Session = Depends(get_db)):
    db_ean_device = crud.get_device_by_ean_code(db, ean_code=ean_code)
    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    return db_ean_device


@app.post("/ean_devices/name", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"], status_code=201)
async def create_ean_device_by_name(ean_device: schemas.EANDevicesSchema, db: Session = Depends(get_db)):
    # print(ean_device)
    db_ean_device = crud.get_device_by_ean_code(db, ean_code=ean_device.ean)
    if db_ean_device:
        raise HTTPException(status_code=400, detail="EAN Device already exists")
    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category doesn't exist")
    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    if not producer:
        raise HTTPException(status_code=400, detail="Producer doesn't exist")
    return crud.create_ean_device_by_name(db=db, ean_device=ean_device)


@app.post("/ean_devices/id", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"], status_code=201)
async def create_ean_device_by_id(ean_device: schemas.EANDevicesSchema, db: Session = Depends(get_db)):
    db_ean_device = crud.get_device_by_ean_code(db, ean_code=ean_device.ean)
    if db_ean_device:
        raise HTTPException(status_code=400, detail="EAN Device already exists")
    category = db.query(models.Categories).filter(models.Categories.category_id == ean_device.category.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category doesn't exist")
    producer = db.query(models.Producers).filter(models.Producers.producer_id == ean_device.producer.producer_id).first()
    if not producer:
        raise HTTPException(status_code=400, detail="Producer doesn't exist")
    return crud.create_ean_device_by_id(db=db, ean_device=ean_device)


# @app.put("/ean_devices/name/{ean_code}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
# async def update_ean_device_by_ean(ean_device_code: str, ean_device: schemas.EANDevicesSchema, db: Session = Depends(get_db)):
#     db_ean_device = crud.get_device_by_ean_code(db, ean_code=ean_device_code)
#     if db_ean_device is None:
#         raise HTTPException(status_code=404, detail="EAN Device not found")
#     n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean_device.ean).first()
#     if n_ean_device is not None and n_ean_device.ean != db_ean_device.ean:
#         raise HTTPException(status_code=400, detail="EAN Device already exists")
#     category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
#     if not category:
#         raise HTTPException(status_code=400, detail="Category doesn't exist")
#     producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
#     if not producer:
#         raise HTTPException(status_code=400, detail="Producer doesn't exist")
#
#     n_ean_device = crud.update_ean_device_by_ean(db=db, ean=ean_device_code, ean_device=ean_device)
#
#     return n_ean_device

@app.put("/ean_devices/name/{ean_device_id}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def update_ean_device_by_name(ean_device_id: int, ean_device: schemas.EANDevicesSchema, db: Session = Depends(get_db)):
    print('HALO' + str(ean_device_id))
    print(ean_device)
    db_ean_device = crud.get_ean_device_by_id(db, ean_device_id=ean_device_id)
    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean_device.ean).first()
    if n_ean_device is not None and n_ean_device.ean != db_ean_device.ean:
        raise HTTPException(status_code=400, detail="EAN Device already exists")
    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category doesn't exist")
    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    if not producer:
        raise HTTPException(status_code=400, detail="Producer doesn't exist")

    n_ean_device = crud.update_ean_device_by_id_name(db=db, ean_device_id=ean_device_id, ean_device=ean_device)

    return n_ean_device


@app.put("/ean_devices/id/{ean_device_id}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def update_ean_device_by_id(ean_device_id: int, ean_device: schemas.EANDevicesSchema, db: Session = Depends(get_db)):
    db_ean_device = crud.get_ean_device_by_id(db, ean_device_id=ean_device_id)
    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    n_ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == ean_device.ean).first()
    if n_ean_device is not None and n_ean_device.ean != db_ean_device.ean:
        raise HTTPException(status_code=400, detail="EAN Device already exists")
    category = db.query(models.Categories).filter(models.Categories.name == ean_device.category.name).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category doesn't exist")
    producer = db.query(models.Producers).filter(models.Producers.name == ean_device.producer.name).first()
    if not producer:
        raise HTTPException(status_code=400, detail="Producer doesn't exist")

    n_ean_device = crud.update_ean_device_by_id(db=db, ean_device_id=ean_device_id, ean_device=ean_device)

    return n_ean_device

@app.delete("/ean_devices/name/{ean_device_code}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def delete_ean_device_by_ean(ean_code: str, db: Session = Depends(get_db)):
    db_ean_device = crud.get_device_by_ean_code(db, ean_code=ean_code)

    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    return crud.delete_ean_device_by_ean(db=db, ean=ean_code)


@app.delete("/ean_devices/id/{ean_device_id}", response_model=schemas.EANDevicesSchema, tags=["EAN Devices"])
async def delete_device_by_id(ean_device_id: int, db: Session = Depends(get_db)):
    db_ean_device = crud.get_ean_device_by_id(db, ean_device_id=ean_device_id)

    if db_ean_device is None:
        raise HTTPException(status_code=404, detail="EAN Device not found")
    return crud.delete_ean_device_by_id(db=db, ean_device_id=ean_device_id)


# Devices
@app.get("/devices/", response_model=List[schemas.DevicesSchema], tags=["Devices"])
async def get_devices(db: Session = Depends(get_db), location_name: Optional[str] = None, ean_code: Optional[str] = None):
    devices = crud.get_devices(db, location_name, ean_code)
    return devices

@app.get("/devices/name/{device_name}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def get_device_by_name(device_name: str, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device_name)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@app.get("/devices/id/{device_id}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@app.get("/devices/qr/{qr_code}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def get_device_by_qr_code(qr_code: str, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_qr_code(db, qr_code=qr_code)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@app.post("/devices/name", response_model=schemas.DevicesSchema, tags=["Devices"], status_code=201)
async def create_device_by_name(device: schemas.DevicesSchema, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device.name)
    if db_device:
        raise HTTPException(status_code=400, detail="Device already exists")
    location = db.query(models.Locations).filter(models.Locations.name == device.location.name).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location doesn't exist")
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == device.ean_device.ean).first()
    if not ean_device:
        raise HTTPException(status_code=400, detail="EAN Device doesn't exist")
    return crud.create_device_by_name(db=db, device=device)

@app.post("/devices/id", response_model=schemas.DevicesSchema, tags=["Devices"], status_code=201)
async def create_device_by_id(device: schemas.DevicesSchema, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_id(db, device_id=device.device_id)
    if db_device:
        raise HTTPException(status_code=400, detail="Device already exists")
    location = db.query(models.Locations).filter(models.Locations.location_id == device.location.location_id).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location doesn't exist")
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean_device_id == device.ean_device.ean_device_id).first()
    if not ean_device:
        raise HTTPException(status_code=400, detail="EAN Device doesn't exist")
    # print(device)
    return crud.create_device_by_id(db=db, device=device)

@app.put("/devices/name/{device_name}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def update_device_by_name(device_name: str, device: schemas.DevicesSchema, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device_name)
    old_location_id = db_device.location_id
    old_location_name = db_device.location.name
    old_status = db_device.status
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    n_device = db.query(models.Devices).filter(models.Devices.name == device.name).first()
    if n_device is not None and n_device.name != db_device.name:
        raise HTTPException(status_code=400, detail="Device already exists")
    location = db.query(models.Locations).filter(models.Locations.name == device.location.name).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location doesn't exist")
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == device.ean_device.ean).first()
    if not ean_device:
        raise HTTPException(status_code=400, detail="EAN Device doesn't exist")

    n_device = crud.update_device_by_name(db=db, name=device_name, device=device)

    # TODO
    # if old_location_id != n_device.location_id:
    #     crud.create_device_history(db, event=f'Zmiana lokalizacji urządzenia: {old_location_name} -> {n_device.location.name}', device=n_device, user=current_user)
    #
    # if old_status != n_device.status:
    #     crud.create_device_history(db, event=f'Zmiana statusu urządzenia: {old_status} -> {n_device.status}', device=n_device, user=current_user)

    return n_device

@app.put("/devices/id/{device_id}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def update_device_by_id(device_id: int, device: schemas.DevicesSchema, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_id(db, device_id=device_id)
    old_location_id = db_device.location_id
    old_location_name = db_device.location.name
    old_status = db_device.status
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    n_device = db.query(models.Devices).filter(models.Devices.name == device.name).first()
    if n_device is not None and n_device.name != db_device.name:
        raise HTTPException(status_code=400, detail="Device already exists")
    location = db.query(models.Locations).filter(models.Locations.location_id == device.location.location_id).first()
    if not location:
        raise HTTPException(status_code=400, detail="Location doesn't exist")
    ean_device = db.query(models.EAN_Devices).filter(models.EAN_Devices.ean == device.ean_device.ean).first()
    if not ean_device:
        raise HTTPException(status_code=400, detail="EAN Device doesn't exist")

    n_device = crud.update_device_by_id(db=db, device_id=device_id, device=device)
    # TODO
    # if old_location_id != n_device.location_id:
    #     crud.create_device_history(db,
    #                                event=f'Zmiana lokalizacji urządzenia: {old_location_name} -> {n_device.location.name}',
    #                                device=n_device)
    #
    # if old_status != n_device.status:
    #     crud.create_device_history(db, event=f'Zmiana statusu urządzenia: {old_status} -> {n_device.status}',
    #                                device=n_device)

    return n_device

@app.delete("/devices/name/{device_name}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def delete_device_by_name(device_name: str, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device_name)
    # TODO
    # crud.delete_device_history_by_name(db, name=device_name)
    # crud.delete_verification_device_link(db, device_id=db_device.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.delete_device_by_name(db=db, name=device_name)


@app.delete("/devices/id/{device_id}", response_model=schemas.DevicesSchema, tags=["Devices"])
async def delete_device_by_id(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_id(db, device_id=device_id)
    # TODO
    # crud.delete_device_history_by_name(db, name=db_device.name)
    # crud.delete_verification_device_link(db, device_id=db_device.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud.delete_device_by_id(db=db, device_id=device_id)

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
