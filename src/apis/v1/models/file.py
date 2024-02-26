from pydantic import BaseModel


class FileRequest(BaseModel):
    files: list[str]
    scopes: list[str]


class ImageRequest(BaseModel):
    image: object


class ImageRespone(BaseModel):
    name: str
    path: str


class FileFilter(BaseModel):
    offset: int
    limit: int
    filter: list[str]
