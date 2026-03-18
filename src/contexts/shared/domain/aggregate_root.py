from pydantic import BaseModel


class AggregateRoot(BaseModel):
    model_config = {"populate_by_name": True}
