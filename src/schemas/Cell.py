from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from src.contrib.schemas import BaseSchemaMixin, OutMixin
from src.utils.Utils import Utils


class CellSchemaBase(BaseModel):
    value: float = Field(..., description="Cell value")
    type: str = Field(..., description="Cell type")


class CellIn(CellSchemaBase, BaseSchemaMixin):
    worksheet_name: str = Field(description="Cell worksheet name")
    column_name: str = Field(description="Cell column name")
    row: int = Field(description="Cell row")
    col: int = Field(description="Cell column")


class CellOut(CellSchemaBase, OutMixin):
    pass


class CellUpdateIn(CellIn, BaseSchemaMixin):
    row: Optional[int] = Field(None, description="Cell row")
    col: Optional[int] = Field(None, description="Cell column")
    value: Optional[float] = Field(None, description="Cell value")
    type: Optional[str] = Field(None, description="Cell type")

    updated_at: datetime = Field(
        default_factory=Utils.current_utc_time, description="Updated cell time"
    )


class CellUpdateOut(CellOut):
    pass
