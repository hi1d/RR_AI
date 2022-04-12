from recommand.models import Repositories

def SEARCH_KEYWORD(keyword: str) -> str:
    result = Repositories.objects.filter(keyword=keyword).exists()
    if not result:
        return "none"
    return "already"