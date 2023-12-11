from datetime import datetime
from typing import Optional
from comptages.datamodel import models
import pytz


def yearly_count_for(
    year: int,
    installation: models.Installation,
    class_: Optional[models.Class] = None,
    model: Optional[models.Model] = None,
    device: Optional[models.Device] = None,
    sensor_type: Optional[models.SensorType] = None,
) -> models.Count:
    tz = pytz.timezone("Europe/Zurich")
    model = model or models.Model.objects.all()[0]
    device = device or models.Device.objects.all()[0]
    sensor_type = sensor_type or models.SensorType.objects.all()[0]
    class_ = class_ or models.Class.objects.get(name="SWISS10")
    return models.Count.objects.create(
        start_put_date=tz.localize(datetime(year, 1, 1)),
        start_service_date=tz.localize(datetime(year, 1, 8)),
        start_process_date=tz.localize(datetime(year, 1, 15)),
        end_process_date=tz.localize(datetime(year, 12, 17)),
        end_service_date=tz.localize(datetime(year, 12, 24)),
        end_put_date=tz.localize(datetime(year, 12, 31)),
        id_model=model,
        id_device=device,
        id_sensor_type=sensor_type,
        id_class=class_,
        id_installation=installation,
    )
