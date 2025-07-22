# /backend/tests/conftest.py
import pytest
from app import create_app
from config import TestingConfig
from models import db, User, Incident

@pytest.fixture(scope='module')
def test_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        # Create a regular user and an admin user for testing
        user = User(username='testuser', email='test@example.com', is_admin=False)
        user.set_password('password123')
        
        admin = User(username='adminuser', email='admin@example.com', is_admin=True)
        admin.set_password('password123')

        db.session.add(user)
        db.session.add(admin)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()