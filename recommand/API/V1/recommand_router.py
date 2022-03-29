from typing import List
from django.shortcuts import redirect
from ninja import Router
from django.http import HttpRequest, JsonResponse
from recommand.models import Repositories
from recommand.API.V1.schemas import (
    Create_Request,
    Create_Response,
    CrawlingRequest,
    CrawlingResponse,
    SearchReqeust,
    SearchResponse
)
from recommand.services import Recommand_Repository, SEARCH, SEARCH_KEYWORD, DB_TO_CSV
import re 

router = Router(tags=["recommand"])

@router.post('/create', response={201:List[Create_Response]})
def Create_Recommand(request: HttpRequest, create_request: Create_Request) -> List[Repositories]:
    recommands = Recommand_Repository(create_request.REPO_ID, 'repo.csv')
    recommands_list = [repository for repository in recommands.repositories.keys()]
    repositories = list(Repositories.objects.all())
    repos = [0 for i in range(len(recommands_list))]
    for repository in repositories:
        if repository.repo_id in recommands_list:
            index = recommands_list.index(repository.repo_id)
            repos[index] = repository
    return repos

@router.post("/crawling_data/", response=CrawlingResponse)
def Crawling_Repo(request: HttpRequest, Crawling_repo_request: CrawlingRequest) -> dict:
    keyword = re.sub('[^a-zA-Z0-9가-힣]','',Crawling_repo_request.KEYWORD)
    SEARCH(keyword)
    return redirect('/api/v1/recommand/update_csv')

@router.get("/update_csv", response=str)
def create_csv(request: HttpRequest):
    DB_TO_CSV()
    return JsonResponse({'message':"success"})

@router.get("/searchkeyword/{keyword}", response=SearchResponse)
def search_keyword(request: HttpRequest, keyword: str) -> dict:
    keyword = re.sub('[^a-zA-Z0-9가-힣]','',keyword)
    keyword_page =  SEARCH_KEYWORD(keyword)
    return JsonResponse({"message" : keyword_page})
