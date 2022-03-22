from config.conf.github_token import token
from recommand.models import Repositories
from bs4 import BeautifulSoup
import requests, asyncio
from time import sleep, time
from asgiref.sync import sync_to_async
from functools import partial

def db_create(repo_dict: dict, keyword: str):
    if repo_dict['topics'] == []:
        print("topics is Empty")
        return 
    if Repositories.objects.filter(repo_id=repo_dict['id']).exists():
        print("DB Already Data")
        return 
    Repositories.objects.create(
        keyword = keyword,
        repo_id = repo_dict['id'],
        repo_name = repo_dict['repo_name'],
        full_name = repo_dict['full_name'],
        description = repo_dict['description'],
        created = repo_dict['created'],
        language = repo_dict['language'],
        stars = repo_dict['stars'],
        forks = repo_dict['forks'],
        subscribers = repo_dict['subscribers'],
        topics = repo_dict['topics']
    ) 

    print("DB Create Success")

async def REPO_INFO(repo: str, keyword: str, keyword_page: int) -> None:
    url = 'https://api.github.com/repos/'+repo
    if keyword == 1:
        request = partial(requests.get, url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',  'referer' : 'https://github.com/search?q=django&type=Repositories', 'Authorization': f'token {token}'})
    else:
        request = partial(requests.get, url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',  'referer' : f'https://github.com/search?p={keyword_page}&q={keyword}&type=Repositories', 'Authorization': f'token {token}'})
    repo_info = await loop.run_in_executor(None, request)
    repo_info = repo_info.json()
    try:
        repo_dict = {
        'id' : int(repo_info['id']),
        'repo_name' : str(repo_info['name']),
        'full_name' : str(repo_info['full_name']),
        'description' : str(repo_info['description']),
        'created' : str(repo_info['created_at'].replace("T"," ").replace("Z","")),
        'language' : str(repo_info['language']),
        'stars' : int(repo_info['stargazers_count']),
        'forks' : int(repo_info['forks']),
        'subscribers' : int(repo_info['subscribers_count']),
        'topics' : repo_info['topics']
        }
    except KeyError:
        status == "limit"
        return
    await sync_to_async(db_create)(repo_dict, keyword)

async def async_run(pages, keyword, keyword_page):
    futures = [asyncio.ensure_future(REPO_INFO(page.text, keyword, keyword_page)) if status != "limit" else 0 for page in pages]
    await asyncio.gather(*futures)

def REPO_INFO_CREATE(keyword:str, keyword_page: int, count =[]) -> None:
    print(f"{keyword_page} start")
    if len(count) >= 10:
        status = "limit"
        return 
    url = f"https://github.com/search?o=desc&p={keyword_page}&q={keyword}&s=stars&type=Repositories"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Authorization': f'token {token}'})
    if 'Whoa there!' in response.text:
        print("retry...")
        count.append(0)
        sleep(5)
        REPO_INFO_CREATE(keyword, keyword_page)
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.select('#js-pjax-container > div > div.col-12.col-md-9.float-left.px-2.pt-3.pt-md-0.codesearch-results > div > ul > li > div.mt-n1.flex-auto > div.d-flex > div:nth-child(1) > a')
    
    loop.run_until_complete(async_run(pages, keyword, keyword_page))        
    count.clear()

def SEARCH(keyword: str):
    start = time()
    global loop
    global status
    status = "True"
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
    for page in range(1,31):
        REPO_INFO_CREATE(keyword, page)
        if status == 'limit':
            return 'limit'
    loop.close()
    end = time()
    print('실행 시간: {0:.3f}초'.format(end - start))
    return 'success'
