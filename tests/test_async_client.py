import pytest
from managed_client.async_client import AsyncManagedAPIClient


class MockResponse:
    """Helper mock response that works as an async context manager."""

    def __init__(self, status: int, json_data=None, text_data=None):
        self.status = status
        self._json_data = json_data
        self._text_data = text_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False

    async def json(self):
        return self._json_data

    async def text(self):
        return self._text_data


class MockSession:
    """Fake aiohttp.ClientSession with async close()."""

    def __init__(self, response: MockResponse):
        self._response = response

    def post(self, *args, **kwargs):
        return self._response

    def delete(self, *args, **kwargs):
        return self._response

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_async_create_item_success():
    response = MockResponse(
        status=200,
        json_data={"id": 1, "name": "test"},
    )
    mock_session = MockSession(response)

    async with AsyncManagedAPIClient("http://fakeapi") as client:
        client.session = mock_session
        result = await client.create_item({"name": "test"})
        print(result)
        assert result["id"] == 1
        assert result["name"] == "test"


@pytest.mark.asyncio
async def test_async_create_item_error():
    response = MockResponse(
        status=400,
        text_data="Bad Request",
    )
    mock_session = MockSession(response)

    async with AsyncManagedAPIClient("http://fakeapi") as client:
        client.session = mock_session
        with pytest.raises(Exception) as exc:
            await client.create_item({"name": "fail"})