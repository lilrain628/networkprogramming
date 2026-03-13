from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


@strawberry.type
@dataclass
class Booking:
    id: strawberry.ID
    name: str
    date: str


@strawberry.input
class BookingInput:
    name: str
    date: str


_BOOKINGS: List[Booking] = []
_NEXT_ID = 1


@strawberry.type
class Query:
    @strawberry.field
    def bookings(self) -> List[Booking]:
        return _BOOKINGS

    @strawberry.field
    def booking(self, id: strawberry.ID) -> Optional[Booking]:
        for booking in _BOOKINGS:
            if str(booking.id) == str(id):
                return booking
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_booking(self, input: BookingInput) -> Booking:
        global _NEXT_ID
        booking = Booking(id=str(_NEXT_ID), name=input.name, date=input.date)
        _NEXT_ID += 1
        _BOOKINGS.append(booking)
        return booking


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
