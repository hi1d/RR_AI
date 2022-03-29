from typing import List, Optional
from ninja import Schema

class Create_Response(Schema):
    id: int
    keyword: str
    repo_id: int 
    repo_name: str
    full_name: str
    description: Optional[str]
    created: str
    language: Optional[str]
    stars: int
    forks: int
    topics: List