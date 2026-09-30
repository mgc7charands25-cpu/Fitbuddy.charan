import pytest
from app import app, build_fallback_plan


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page_renders(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'FitBuddy AI' in response.data


def test_fallback_plan_contains_key_sections():
    profile = {
        'goal': 'Fat loss',
        'experience': 'Beginner',
        'days': 4,
        'training_type': 'Balanced',
    }
    plan = build_fallback_plan(profile)
    assert 'AI Fitness Plan for Fat loss' in plan
    assert 'Recovery guidance:' in plan
    assert 'Nutrition note:' in plan
