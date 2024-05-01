import asyncio
from datetime import datetime
from uuid import UUID

import motor.motor_asyncio  # type: ignore
from faker import Faker
from pydantic import BaseModel, Field
from uuid_extensions.uuid7 import uuid7


class Rating(BaseModel):
    """Describes one rating"""

    id: UUID = Field(
        ...,
        alias="_id",
        description="The id of the rating",
        example=UUID("123e4567-e89b-12d3-a456-426655440000"),
    )
    rating: float = Field(..., description="Ratings for coffee")
    coffee_id: UUID = Field(
        ...,
        description="The id of the coffee",
        example=UUID("123e4567-e89b-12d3-a456-426655440001"),
    )


class Coffee(BaseModel):
    """Describes a Coffee"""

    id: UUID = Field(
        ...,
        alias="_id",
        description="The id of the coffee",
        example=UUID("123e4567-e89b-12d3-a456-426655440000"),
    )
    name: str = Field(..., description="Name of coffee")
    owner_id: UUID = Field(
        ...,
        description="The id of the owner of the coffee",
        example=UUID("123e4567-e89b-12d3-a456-426655440000"),
    )
    owner_name: str = Field(..., description="Name of the owner of the coffee")


client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://root:example@localhost:27017",
    serverSelectionTimeoutMS=5000,
    uuidRepresentation="standard",
)


async def aggregate_normalized_ratings_and_coffees():
    """Aggregate the ratings and count of each coffee."""

    db = client["coffee_backend"]

    starttime = datetime.now()

    coffees = db["coffee"].aggregate(
        [
            {
                "$lookup": {
                    "from": "rating",
                    "localField": "_id",
                    "foreignField": "coffee_id",
                    "as": "rating",
                }
            },
            {
                "$addFields": {
                    "count": {"$size": "$rating"},
                    "avgRating": {"$avg": "$rating.rating"},
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "owner_id": 1,
                    "count": 1,
                    "avgRating": 1,
                }
            },
            {"$limit": 150},
            {"$skip": 100},
        ]
    )

    coffees = [coffee async for coffee in coffees]

    print(len(coffees))
    endtime = datetime.now()
    formatted_start_time = (
        starttime.strftime("%Y-%m-%d %H:%M:%S")
        + f".{starttime.microsecond // 1000:03d}"
    )
    formatted_end_time = (
        endtime.strftime("%Y-%m-%d %H:%M:%S") + f".{endtime.microsecond // 1000:03d}"
    )
    print(formatted_start_time)
    print(formatted_end_time)

    # print(coffees)


async def list_ratings():
    """List all ratings."""

    starttime = datetime.now()

    db = client["coffee_backend"]

    ratings = db["rating"].find().limit(100)

    ratings = [rating async for rating in ratings]

    print(len(ratings))

    endtime = datetime.now()
    formatted_start_time = (
        starttime.strftime("%Y-%m-%d %H:%M:%S")
        + f".{starttime.microsecond // 1000:03d}"
    )
    formatted_end_time = (
        endtime.strftime("%Y-%m-%d %H:%M:%S") + f".{endtime.microsecond // 1000:03d}"
    )
    print(formatted_start_time)
    print(formatted_end_time)


asyncio.run(aggregate_normalized_ratings_and_coffees())
# asyncio.run(list_ratings())
