from typing import List

from pydantic import BaseModel


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class ChatInput(BaseRequest):
    message: str


class ModeInput(BaseModel):
    mode: str


class idInput(BaseModel):
    id_: str


class SimilaritySearchInput(BaseRequest):
    query: str


class MetaData(BaseRequest):
    page: str


class StoreChunksInput(BaseRequest):
    text: List
    metadata: List[MetaData]
