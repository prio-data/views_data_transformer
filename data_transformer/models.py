
from typing import List, Optional
from pydantic import BaseModel

class Transform(BaseModel):
    level_of_analysis: str
    name: str
    namespace: str

    def path(self):
        return self.level_of_analysis + "/" + self.namespace + "." + self.name

class Argument(BaseModel):
    name: str
    type: Optional[str]

class TransformDetail(Transform):
    arguments: List[Argument]
    docstring: Optional[str]
