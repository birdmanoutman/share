import httpx


class NotionAPI:
    def __init__(self, token):
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13"
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def create_page(self, database_id, properties):
        url = f"{self.base_url}/pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        response = await self.client.post(url, json=data)
        response.raise_for_status()
        return response.json()

    async def retrieve_database_pages(self, database_id, filter=None, sorts=None):
        url = f"{self.base_url}/databases/{database_id}/query"
        data = {}
        if filter:
            data['filter'] = filter
        if sorts:
            data['sorts'] = sorts
        response = await self.client.post(url, json=data)
        response.raise_for_status()
        return response.json().get('results', [])

    async def update_page_properties(self, page_id, properties):
        url = f"{self.base_url}/pages/{page_id}"
        data = {"properties": properties}
        response = await self.client.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    async def archive_page(self, page_id, archive_property_name):
        properties = {
            archive_property_name: {
                "checkbox": True
            }
        }
        return await self.update_page_properties(page_id, properties)

    async def close(self):
        await self.client.aclose()
