import pytest
from unittest.mock import MagicMock
from managed_client.client import ManagedAPIClient


def test_create_item_success(monkeypatch):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.json.return_value = {"id": 1, "name": "test"}
    mock_session.post.return_value = mock_response

    with ManagedAPIClient("http://fakeapi") as client:
        client.session = mock_session
        result = client.create_item({"name": "test"})
        assert result["id"] == 1


def test_create_item_error(monkeypatch):
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_session.post.return_value = mock_response

    with ManagedAPIClient("http://fakeapi") as client:
        client.session = mock_session
        with pytest.raises(Exception):
            client.create_item({"name": "fail"})
