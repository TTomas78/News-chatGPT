from pydantic import BaseModel
from enum import Enum

class GetAllNewsResponse(BaseModel):
    class NewsData(BaseModel):
        summary: str
        link: str
        title: str

    news: list[NewsData]

class AllowedSource(Enum):
    INFOBAE="infobae"
    NEWSAPI="newsapi"	


class GetOneNewsRequest(BaseModel):
    source: AllowedSource
    link: str
    words_number: int #validate this
    language: str #validate this
    soft_limit: bool

class GetAllNewsRequest(BaseModel):
    

    words_number: int #validate this
    language: str #valdiate this
    source: AllowedSource
    soft_limit: bool
