from pydantic import BaseModel


class WikiBase(BaseModel):
    name: str
    description: str
    photo_url: str


class WikiIn(WikiBase):
    author_id: str


class WikiOut(WikiIn):
    id: str


class WikiInDB(WikiOut):
    deleted: bool = False

