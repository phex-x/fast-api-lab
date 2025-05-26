from pydantic import BaseModel


class ToEncode(BaseModel):
    text: str
    key: str


class Result(BaseModel):
    encoded_data: str
    key: str
    huffman_codes: dict
    padding: int
