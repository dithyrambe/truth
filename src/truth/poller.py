import asyncio
from collections import deque
from typing import AsyncGenerator, Generator

from loguru import logger

from truth.models import Status
from truth.client import TruthClient


DEFAULT_CACHE_SIZE = 20
DEFAULT_POLLING_INTERVAL_SECONDS = 60


class TruthPoller:
    def __init__(
        self,
        client: TruthClient,
        cache_size: int = DEFAULT_CACHE_SIZE,
    ) -> None:
        self.client = client or TruthClient()
        self.cache_size = cache_size
        self._cache: deque[Status] = deque(maxlen=cache_size)

    async def poll_for_new_statuses(
        self,
        account_id: str,
        polling_interval: int = DEFAULT_POLLING_INTERVAL_SECONDS,
    ) -> Generator[list[Status]]:
        while True:
            statuses = await self.client.fetch_latest_statuses(account_id=account_id)
            async for status in self.yield_new_statuses(statuses):
                logger.info(f"{status.created_at}: {status.content}")
            await asyncio.sleep(polling_interval)

    async def yield_new_statuses(
        self, statuses: list[Status]
    ) -> AsyncGenerator[Status, None]:
        for status in sorted(statuses, key=lambda s: s.created_at, reverse=False):
            if self._cache and status.created_at <= self._cache[-1].created_at:
                logger.debug(
                    f"skipping already known {status.id} created at {status.created_at}"
                )
                continue
            logger.debug(f"caching {status.id} created at {status.created_at}")
            self._cache.append(status)
            yield status
