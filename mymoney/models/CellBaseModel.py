from pydantic import BaseModel
from mymoney.utils.Utils import Utils
from pydantic import Field, UUID4
from datetime import datetime
import uuid


class CellBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=Utils.current_utc_time)
    updated_at: datetime = Field(default_factory=Utils.current_utc_time)
