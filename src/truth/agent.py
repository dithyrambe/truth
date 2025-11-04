from enum import Enum
from pydantic import BaseModel, Field
from jinja2 import Template


class Sentiment(str, Enum):
    very_negative = "very_negative"
    negative = "negative"
    neutral = "neutral"
    positive = "positive"
    very_positive = "very_positive"


class Topic(str, Enum):
    crypto = "crypto"
    stocks = "stocks"
    economy = "economy"
    politics = "politics"
    foreign_affairs = "foreign_affairs"
    misc = "misc"


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class SentimentResult(BaseModel):
    sentiment: Sentiment = Field(description="Main sentiment carried by the tweet post")
    sentiment_score: float = Field(
        description=(
            "Sentiment score associated "
            "(the lower the more negative, the higher the more positive sentiment)"
        ),
        ge=-1.0,
        le=1.0,
    )
    topic: Topic = Field(description="Main topic targeted by the tweet post")
    market_relevance: float = Field(
        description="Relevancy score against the main topic",
        ge=0.0,
        le=1.0,
    )
    signal: Signal = Field(description="Whether to buy hold or sell")


SEP = "\n\n"

INSTRUCTIONS = """
You are a financial sentiment parser.
Given a tweet post from Donald Trump (current president of the USA),
analyze it for potential market impact, especially on crypto and stocks.
Respond ONLY in strict JSON that validates against the provided schema.
"""

USER_TEMPLATE = Template(
    """
Tweet:
{{ tweet_content }}

""".strip()
)

SCHEMA_GUARD = f"""
Output MUST be valid JSON for the schema you've been given. Do not include backticks or prose.
Validate your JSON against this JSON Schema (do not print it back):

{SentimentResult.model_json_schema()}
""".strip()
