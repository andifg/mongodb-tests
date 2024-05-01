import asyncio
import random
import time
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


faker = Faker()

db = client["coffee_backend"]

db.drop_collection("coffee")
db.drop_collection("rating")

client.get_io_loop = asyncio.get_running_loop


async def insert_many():

    coffees = []

    owner_id = uuid7()

    for i in range(3000):
        coffee = Coffee(
            _id=uuid7(),
            name=faker.name(),
            owner_id=owner_id,
            owner_name="Test Owner",
        )
        coffees.append(coffee.dict(by_alias=True))

    for key, coffee in enumerate(coffees):
        print("Inserting coffee " + str(key))

        await db["coffee"].insert_one(coffee)

        number_ratings = random.randint(150, 250)

        for _ in range(number_ratings):
            rating = Rating(
                _id=uuid7(),
                rating=random.uniform(0, 5),
                coffee_id=coffee["_id"],
            )

            await db["rating"].insert_one(rating.dict(by_alias=True))

    print("Done inserting coffees and ratings.")

    coffee_count = await db["coffee"].count_documents({})
    rating_count = await db["rating"].count_documents({})

    print(f"Inserted {coffee_count} coffees and {rating_count} ratings.")


asyncio.run(insert_many())
