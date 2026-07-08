import random

import factory
from main.app import db
from main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyFunction(
        lambda: "1234" if random.choice([True, False]) else None
    )
    car_number = factory.Faker("bothify", text="???###")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=5, max=100)

    @factory.lazy_attribute
    def count_available_places(self):
        return self.count_places
