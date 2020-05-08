from pydantic import BaseModel
from datetime import datetime


class LinkBase(BaseModel):
    pass


class LinkCreate(LinkBase):
    full_link: str
    # short_link: str


class Link(LinkBase):
    full_link: str
    short_link: str
    created: datetime

    class Config:
        orm_mode = True
    pass
