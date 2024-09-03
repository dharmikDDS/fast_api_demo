from fastapi import FastAPI, Query
from typing import Annotated
from enum import Enum
from pydantic import BaseModel


def common_positive_resp(message: str, to_send: dict = None) -> dict[str, any]:
    map_to_return = {
        "status": True,
        "message": message,
    }

    if to_send != None:
        map_to_return.update({"data": to_send})

    return map_to_return


def common_negetive_resp(message: str):
    return {
        "status": False,
        "message": message,
    }


class UserModel(BaseModel):
    name: str
    age: int
    profession: str | None = None
    isMarried: bool | None = None


class Paths(str, Enum):
    banana = 0
    mango = 1
    papaya = 2


app = FastAPI()


@app.get("/")
async def root():
    return common_positive_resp("Hello, world!")


@app.get("/user")
async def retriveUser():
    return common_positive_resp(
        "User fetched successfully.",
        {"name": "Johm crisensky", "age": 20, "profession": "Actror"},
    )


# Patrh parameters
@app.get("/items/banana")
async def read_item():
    return common_positive_resp(
        "Item fetched successfully.",
        {"item_id": "banana"},
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return common_positive_resp(
        "Item fetched successfully.",
        {"item_id": item_id},
    )


@app.get("/enumdValue/{path}")
async def get_enumed_value(path: Paths):
    if path is Paths.banana:
        return common_positive_resp(
            "Item fetched successfully.",
            {"item": Paths.banana},
        )

    if path.value == 1:
        return common_positive_resp(
            "Item fetched successfully.",
            {"item": Paths.mango},
        )

    if path is Paths.papaya:
        return common_positive_resp(
            "Item fetched successfully.",
            {"item": Paths.papaya},
        )

    return common_negetive_resp("Item not found.")


## Query Parameters


# with manually handling null values for required
@app.get("/addUser")
async def add_user(
    name: str | None = None,
    profession: str | None = None,
    age: int | None = None,
):
    if name == None:
        return common_negetive_resp("Name is required.")

    if profession == None:
        return common_negetive_resp("Profession is required.")

    return common_positive_resp(
        "User added successfully.",
        {"name": name, "profession": profession, "age": age},
    )


# with automatic handling null values for required
@app.get("/addUser1")
async def add_user1(name: str, profession: str, age: int | None = None):
    return common_positive_resp(
        "User added successfully.",
        {"name": name, "profession": profession, "age": age},
    )


### Request body


# body
@app.post("/updateUser")
async def adD_user_post(user: UserModel):

    return common_positive_resp(
        "User added succesfully.",
        user.model_dump(),
    )


# body + path
@app.post("/updateUser/{user_id}")
async def adD_user_post(user: UserModel, user_id: int):
    print(f"given userId: {user_id}")

    return common_positive_resp(
        "User added succesfully.",
        {
            "user_id": user_id,
            **user.model_dump(),
        },
    )


# body + path + query
@app.post("/updateUser1/{userId}")
async def updateUser1(user: UserModel, userId: int, isMarried: bool | None = None):
    return common_positive_resp(
        "User added succesfully.",
        {"user_id": userId, "is_married_query": isMarried, "user": user.model_dump()},
    )


### Data - validation with query parameters
@app.get("/query-validation")
async def validateQuery(query: Annotated[str | None, Query(max_length=50)] = None):
    return common_positive_resp({"query": query})
