import os

from datetime import datetime
from django.contrib.gis.geos import LineString

from comptages.datamodel import models


def test_data_path(file_path):
    """Return the path of file in the directory with the test data."""
    path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_data/',
        file_path
    )

    return path


def create_test_count(
        installation_name="00208495",
        class_="SWISS10",
        start=datetime(2020, 1, 1),
        end=datetime(2020, 12, 31),
        lanes=2):
    """Create a count object with related tables in the DB."""
    installation = models.Installation.objects.create(
        permanent=True,
        name=installation_name,
        active=True,
    )

    class_ = models.Class.objects.create(
        name=class_,
    )

    sensor_type = models.SensorType.objects.create(
        name="test sensor type",
    )

    brand = models.Brand.objects.create(
        name="test brand",
    )

    model = models.Model.objects.create(
        name="test model",
        id_brand=brand,
    )

    device = models.Device.objects.create(
        name="test device",
        id_model=model,
    )

    count = models.Count.objects.create(
        start_service_date=start,
        end_service_date=end,
        start_process_date=start,
        end_process_date=end,
        start_put_date=start,
        end_put_date=end,
        id_model=model,
        id_device=device,
        id_sensor_type=sensor_type,
        id_class=class_,
        id_installation=installation,
    )

    section = models.Section.objects.create(
        id=installation_name,
        name=installation_name,
        geometry=LineString((0, 0), (1, 1)),
    )

    for i in range(lanes):
        models.Lane.objects.create(
            number=i+1,
            direction=1 if i % 2 == 0 else 0,
            id_installation=installation,
            id_section=section,
        )

    return count
