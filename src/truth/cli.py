import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from truth.agent import INSTRUCTIONS, SCHEMA_GUARD, SEP, USER_TEMPLATE, SentimentResult
from truth.client import TruthClient
from truth.poller import TruthPoller
from typer import Option, Typer
import typer


TRUMP_ID = "107780257626128497"
cli = Typer(add_completion=False)


@cli.command()
def poll(
    account_id: str = Option(
        TRUMP_ID, "-a", "--account-id", help="Account to poll status from"
    ),
    polling_interval: int = Option(
        60, "-i", "--polling-interval", help="Polling interval"
    ),
):
    async def _poll(
        account_id: str,
        polling_interval: int,
    ):
        client = TruthClient()
        poller = TruthPoller(client=client)
        async for status in poller.poll(
            account_id=account_id,
            polling_interval=polling_interval,
        ):
            typer.echo(f"{status.created_at}: {status.content}")

    asyncio.run(
        _poll(
            account_id=account_id,
            polling_interval=polling_interval,
        )
    )


@cli.command()
def handle_truth(
    model: str = Option(
        "eu.anthropic.claude-3-haiku-20240307-v1:0",
        envvar="BEDROCK_MODEL",
        help="Bedrock model name / arn to use",
    ),
    account_id: str = Option(
        TRUMP_ID, "-a", "--account-id", help="Account to poll status from"
    ),
    polling_interval: int = Option(
        60, "-i", "--polling-interval", help="Polling interval"
    ),
):
    async def _handle_truth(
        model_name: str,
        account_id: str,
        polling_interval: int,
    ):
        model = BedrockConverseModel(model_name=model_name)
        agent = Agent(
            model=model,
            instructions=SEP.join([INSTRUCTIONS, SCHEMA_GUARD]),
            output_type=SentimentResult,
        )

        client = TruthClient()
        poller = TruthPoller(client=client)
        async for status in poller.poll(
            account_id=account_id,
            polling_interval=polling_interval,
        ):
            tweet_content = status.content
            rendered_prompt = USER_TEMPLATE.render(tweet_content=tweet_content)
            result = await agent.run(rendered_prompt)
            typer.echo(f"{status.created_at}: {status.content}")
            typer.echo(result.output.model_dump_json(indent=2))

    asyncio.run(
        _handle_truth(
            model_name=model,
            account_id=account_id,
            polling_interval=polling_interval,
        )
    )
