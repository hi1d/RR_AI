import json
from config.conf.github_token import token
from recommand.models import Repositories
import requests, asyncio
from time import time
from asgiref.sync import sync_to_async
from django.db.transaction import atomic

@atomic
def db_create(repo_dict: dict, keyword: str):
    if repo_dict['topics'] == []:
        return 
    Repositories.objects.create(
        keyword = keyword,
        repo_id = repo_dict['id'],
        repo_name = repo_dict['name'],
        full_name = repo_dict['full_name'],
        description = repo_dict['description'],
        created = (repo_dict['created_at'].replace("T"," ").replace("Z","")),
        language = repo_dict['language'],
        stars = repo_dict['stargazers_count'],
        forks = repo_dict['forks'],
        topics = repo_dict['topics']
        ) 


async def REPO_INFO(repo: dict, keyword: str) -> None:
    
    await sync_to_async(db_create)(repo, keyword)

async def async_run(keyword):
    headers = {'Authorization': f'token {token}'}
    repo_list = requests.get(f'https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=100', headers=headers).json()
    futures = [asyncio.ensure_future(REPO_INFO(repo, keyword)) for repo in repo_list['items']]
    await asyncio.gather(*futures)

def search_loop_start(keyword):
    loop.run_until_complete(async_run(keyword))        

def SEARCH(keyword: str):
    start = time()
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    search_loop_start(keyword)
    loop.close()
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - start))
    return 'success'
