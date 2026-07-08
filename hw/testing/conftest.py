
import pytest
from main.app import create_app
from main.app import db as _db
from main.models import Client, Parking


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        _db.create_all()

        client = Client(name="Ivan", surname="Ivanov", credit_card="1234")
        parking = Parking(address="Test", opened=True, count_places=10, count_available_places=10)

        _db.session.add_all([client, parking])
        _db.session.commit()

        yield app

        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db
