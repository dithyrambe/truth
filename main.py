import asyncio

from truth.client import TruthClient
from truth.poller import TruthPoller


async def main():
    trump_id = "107780257626128497"
    client = TruthClient()
    poller = TruthPoller(client=client)
    await poller.poll_for_new_statuses(account_id=trump_id, polling_interval=5)


if __name__ == "__main__":
    asyncio.run(main())
