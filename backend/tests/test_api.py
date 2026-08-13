import os

os.environ.setdefault('DATABASE_URL', 'sqlite:////tmp/nominahub-test.db')
os.environ.setdefault('JWT_SECRET_KEY', 'test-secret')
os.environ.setdefault('CORS_ORIGINS', 'http://localhost:4200')

from app import create_app


def test_health_endpoint():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.get('/api/health')

    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok', 'service': 'NominaHub API'}


def test_demo_user_can_login():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.post('/api/auth/login', json={
        'email': 'admin@nominahub.local',
        'password': 'Admin123!',
    })

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['accessToken']
    assert payload['user']['role'] == 'admin'
