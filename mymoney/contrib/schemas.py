from pydantic import BaseModel, Field


class BaseSchemaMixin(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class OutMixin(BaseModel):
    row: int = Field()
    col: int = Field()
