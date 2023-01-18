from typing import Union, Dict, Any
from fastapi import FastAPI, Body, HTTPException
import uvicorn

from Dsl import Dsl
from PC.decoder.decode import decode
from PC.dsl import DSL
from visitors import Visitor

app = FastAPI()


@app.get("/")
def health_check():
    """
    Health check endpoint
    """
    return "System is up and running"


@app.post("/transpile", response_model=Dict[str, Union[str, Dict[str, str]]])
async def dsl_transpile(body: Dict = Body(...)):
    try:
        dsl_instance: DSL = decode(body["dsl"])
        visiter = Visitor(dsl_instance)
        response = visiter.walk()
        return {"response": response}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
