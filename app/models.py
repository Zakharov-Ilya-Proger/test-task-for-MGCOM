from typing import Dict
from pydantic import BaseModel


class FormData(BaseModel):
    fields: Dict[str, str]
