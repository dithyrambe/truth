from httpx import AsyncClient
from httpx_retries import Retry, RetryTransport

from truth.models import Status

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0"
)


class TruthClient:
    def __init__(
        self,
        base_url: str = "https://truthsocial.com",
        headers: dict[str, str] | None = None,
        client: AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url
        self.headers = headers or {}
        self.client = client or AsyncClient(
            transport=RetryTransport(
                retry=Retry(
                    status_forcelist={429},
                    respect_retry_after_header=True,
                ),
            ),
        )

    async def fetch_latest_statuses(self, account_id: str) -> list[Status]:
        response = await self.client.get(
            url=f"{self.base_url}/api/v1/accounts/{account_id}/statuses",
            params={
                "exclude_replies": "true",
                "only_replies": "false",
                "with_muted": "true",
            },
            headers={
                "User-Agent": DEFAULT_USER_AGENT,
            }
            | self.headers,
        )
        response.raise_for_status()
        return sorted(
            [Status.model_validate(status) for status in response.json()],
            key=lambda s: s.created_at,
            reverse=True,
        )
