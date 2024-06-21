from pydantic import BaseModel
from src.utils.Utils import Utils
from pydantic import Field
from datetime import datetime


class CellBaseModel(BaseModel):
    created_at: datetime = Field(default_factory=Utils.current_utc_time)
    updated_at: datetime = Field(default_factory=Utils.current_utc_time)
