# tests/conftest.py

import pytest
from flask import Flask
from app.controllers.customers_route import customers_blueprint
from app.utils.supabase_client import get_supabase_client


@pytest.fixture
def app():
    # Membuat instance aplikasi Flask untuk pengujian
    app = Flask(__name__)
    app.register_blueprint(customers_blueprint)

    yield app


@pytest.fixture
def client(app):
    # Menggunakan aplikasi untuk membuat client testing
    return app.test_client()
