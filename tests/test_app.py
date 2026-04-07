from unittest.mock import MagicMock, patch


def test_healthz_returns_ok(client):
    response = client.get('/healthz')

    assert response.status_code == 200
    body = response.get_json()
    assert body['status'] == 'ok'
    assert 'version' in body


def test_index_returns_expected_payload(client):
    response = client.get('/')

    assert response.status_code == 200
    body = response.get_json()
    assert body['message'] == 'cicd-lab'
    assert 'version' in body


@patch('app.app.get_db_pool')
def test_dbcheck_returns_db_1(mock_get_db_pool, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_db_pool.return_value.getconn.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)

    response = client.get('/dbcheck')

    assert response.status_code == 200
    body = response.get_json()
    assert body['status'] == 'ok'
    assert body['db'] == 1
    assert 'version' in body


@patch('app.app.get_db_pool', side_effect=RuntimeError('db down'))
def test_dbcheck_returns_503_when_database_unavailable(_mock_get_db_pool, client):
    response = client.get('/dbcheck')

    assert response.status_code == 503
    body = response.get_json()
    assert body['status'] == 'error'
    assert body['error'] == 'database_unavailable'
