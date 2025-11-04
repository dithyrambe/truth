import asyncio
from truth.client import TruthClient
from truth.poller import TruthPoller
from typer import Option, Typer


TRUMP_ID = "107780257626128497"
cli = Typer(add_completion=False)


async def _poll(
    account_id: str,
    polling_interval: int = 5,
):
    client = TruthClient()
    poller = TruthPoller(client=client)
    await poller.poll_for_new_statuses(
        account_id=account_id,
        polling_interval=polling_interval,
    )


@cli.command()
def poll(
    account_id: str = Option(
        TRUMP_ID, "-a", "--account-id", help="Account to poll status from"
    ),
    polling_interval: int = Option(
        60, "-i", "--polling-interval", help="Polling interval"
    ),
):
    asyncio.run(
        _poll(
            account_id=account_id,
            polling_interval=polling_interval,
        )
    )
