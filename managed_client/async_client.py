import aiohttp


class AsyncManagedAPIClient:
    """Asynchronous context-managed API client using aiohttp."""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_item(self, data) -> dict:
        """Send POST request to /items with provided data."""
        async with self.session.post(f"{self.base_url}/items", json=data) as resp:
            if resp.status < 200 or resp.status >= 300:
                raise Exception(resp.status, await resp.text())
            return await resp.json()

    async def delete_item(self, item_id: int) -> None:
        """Send DELETE request to /items/{item_id}."""
        async with self.session.delete(f"{self.base_url}/items/{item_id}") as resp:
            if resp.status < 200 or resp.status >= 300:
                raise Exception(resp.status, await resp.text())
