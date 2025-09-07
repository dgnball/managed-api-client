import requests


class ManagedAPIClient:
    """Context-managed API client using requests."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = None

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def create_item(self, data: dict) -> dict:
        """Send POST request to items with provided dats."""
        resp = self.session.post(f"{self.base_url}/items", json=data)
        if not resp.ok:
            raise Exception(resp.status_code, resp.text)
        return resp.json()

    def delete_item(self, item_id) -> None:
        """Send DELETE request to /items/{itemid}."""
        resp = self.session.delete(f"{self.base_url}/items/{item_id}")
        if not resp.ok:
            raise Exception(resp.status_code, resp.text)
