from app.repositories.abstract import UrlRepository
from app.services.dto.dto import ResponseUrlDto

data_urls: list[ResponseUrlDto] = []


class MockUrlRepository(UrlRepository):
    async def get_all_user_urls(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[ResponseUrlDto] | None:
        urls = [i for i in data_urls if i.user_id == user_id]
        res = urls[offset : offset + limit]
        if not res:
            return None
        return res

    async def get_url_by_short_url(self, short_url: str):
        url = [i for i in data_urls if i.short_url == short_url]
        if not url:
            return None
        return url[0]

    async def get_url_by_userid_and_url(self, user_id: int, url: str):
        urlind = [i for i in data_urls if i.user_id == user_id and i.url == url]
        if not urlind:
            return None
        return urlind[0]

    async def get_url_by_url_id(self, url_id: int):
        url = [i for i in data_urls if i.urlid == url_id]
        if not url:
            return None
        return url[0]

    async def insert_url(self, url: str, short_url: str, user_id: int):
        urlid_in_db = max([i.urlid for i in data_urls]) + 1
        urlindb = ResponseUrlDto(
            urlid=urlid_in_db, url=url, short_url=short_url, clics=0, user_id=user_id
        )
        data_urls.append(urlindb)
        if not urlindb:
            return None
        return urlindb

    async def change_url(self, url_id: int, short_url: str):
        url = [i for i in data_urls if i.urlid == url_id]
        if not url:
            return None
        url[0].short_url = short_url
        return url[0]

    async def update_url_clicks(self, url_id: int):
        url = [i for i in data_urls if i.urlid == url_id]
        if not url:
            return None
        url[0].clics += 1
        return url[0]

    async def delete_url(self, url_id: int):
        url = [i for i in data_urls if i.urlid == url_id]
        if not url:
            return None
        data_urls.remove(url[0])
        return url[0]
