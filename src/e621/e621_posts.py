from typing import Any

import aiohttp

from .config_repository import ConfigRepository


class E621Posts:
    def __init__(self, config: ConfigRepository):
        self._config = config
        self._session: aiohttp.ClientSession | None = None

    async def get_good_post(self) -> dict | None:
        tags = self._config.get_tags()
        limit = self._config.get_limit()
        posts = await self.fetch_posts(tags, limit)

        # Excluding already sent posts
        sent = self._config.get_sent_posts_id()
        posts = list(filter(lambda post: post["id"] not in sent, posts))

        if posts and len(posts) > 0:
            post = posts[0]

            return post

    def get_link(self, post: dict[str, Any]) -> str:
        return "https://e621.net/posts/" + str(post["id"])

    def mark_post_as_sent(self, post_id: int) -> None:
        self._config.mark_post_as_sent(post_id)

    async def fetch_posts(self, tags: str, limit: int) -> list[dict[str, Any]]:
        params = {"tags": tags, "limit": limit}
        return await self._request(params=params)

    async def _request(self, params: dict[str, Any]) -> list[dict[str, Any]]:
        session = await self._get_session()
        async with session.get("https://e621.net/posts.json", params=params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data["posts"]

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self._config.get_headers())
        return self._session

    async def aclose(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
