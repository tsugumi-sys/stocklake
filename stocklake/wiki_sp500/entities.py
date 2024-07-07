from typing import Optional

from pydantic import BaseModel, ConfigDict


class WikiSP500DataBase(BaseModel):
    symbol: str
    company: str
    sector: Optional[str]
    industry: Optional[str]
    headquarters: Optional[str]


class RawWikiSP500Data(WikiSP500DataBase):
    pass


class PreprocessedWikiSp500Data(WikiSP500DataBase):
    pass


class WikiSP500DataCreate(WikiSP500DataBase):
    pass


class WikiSP500Data(WikiSP500DataBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: str
    updated_at: str
