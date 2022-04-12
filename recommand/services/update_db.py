from recommand.models import Repositories

def UPDATE_TOPICS() -> None:
    repos = list(Repositories.objects.all())
    for repo in repos:
        if repo.language:
            topics = repo.topics
            language = repo.language
            keyword = repo.keyword
            topics_list = list(map(lambda x: x.lower(),topics))
            if language.lower() not in topics_list:
                topics.append(language)
            else:
                continue
            if keyword.lower() not in topics_list:
                topics.append(keyword)
            repo.save()
        else:
            continue
