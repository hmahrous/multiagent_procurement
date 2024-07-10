from typing import List

from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ChatOutput(BaseResponse):
    response: str


class StoreChunksOutput(BaseResponse):
    UUIDS: List[str]
