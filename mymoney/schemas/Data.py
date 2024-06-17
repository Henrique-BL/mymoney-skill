from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from mymoney.contrib.schemas import BaseSchemaMixin, OutMixin
from mymoney.utils.Utils import Utils


class DataBase(BaseModel):
    value: float = Field(..., description="Data value")
    type: str = Field(..., description="Data type")


class DataIn(DataBase, BaseSchemaMixin):
    row: int = Field(description="Data cell row")
    col: int = Field(description="Data cell column")


class DataOut(DataBase, OutMixin):
    pass


class DataUpdate(BaseSchemaMixin):
    value: Optional[float] = Field(None, description="Data value")
    type: Optional[str] = Field(None, description="Data type")
    updated_at: datetime = Field(
        default_factory=Utils.current_utc_time, description="Updated data time"
    )


class DataUpdateOut(DataOut):
    pass
