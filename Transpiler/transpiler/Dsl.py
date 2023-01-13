from pydantic import BaseModel
from PC.dsl import DSL

class Dsl(BaseModel):
    dsl : str