import pytest
from v2.app import create_app
from v2.models import db, Task


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    with app.app_context():
        task1 = Task(task='Test Task 1')
        task2 = Task(task='Test Task 2')
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()


def test_get_all_tasks(client, init_database):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) == 2


def test_add_task(client):
    response = client.post('/tasks', json={'task': 'New Task'})
    assert response.status_code == 201
    assert response.json['task'] == 'New Task'


def test_delete_task(client, init_database):
    task_id = Task.query.first().id
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert Task.query.get(task_id) is None


def test_get_task_by_id(client, init_database):
    task_id = Task.query.first().id
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['id'] == task_id


def test_get_task_by_id_not_found(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404
