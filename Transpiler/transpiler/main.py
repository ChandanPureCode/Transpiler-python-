from typing import Union, Dict, Any
import importlib
import sys

from fastapi import FastAPI, Body, HTTPException

import uvicorn
import os

from Dsl import Dsl

from PC.decoder.decode import decode
from PC.dsl import DSL

from visitors import Visitor

app = FastAPI()


@app.get("/")
def health_check():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "System is up and running"


@app.post(
    "/transpile",
)
async def dsl_transpile(body: Dict = Body(...)):
    # try:
    dsl_instance: DSL = decode(body["dsl"])
    visiter = Visitor(dsl_instance)

    print(visiter.walk())

    return {"response": "dsl_instance"}

    # except Exception as exc:

    #     print(exc)
    #     raise HTTPException(status_code=400, detail="Error creating item")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
