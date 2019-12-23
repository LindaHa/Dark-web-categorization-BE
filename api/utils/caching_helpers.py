from typing import Any, Dict, List
from api.models import Page, Group
import redis
import pickle


def redis_cache_complex_object(redis_key: str, complex_object: object) -> None:
    r = redis.Redis()
    pickled_obj = pickle.dumps(complex_object)
    r.set(redis_key, pickled_obj)


def redis_get_complex_object(redis_key: str) -> Any:
    r = redis.Redis()
    from_redis = r.get(redis_key)
    if from_redis:
        return pickle.loads(from_redis)
    return None


# The json with pages and additional info of the response
def cache_json_pages(json: str) -> None:
    r = redis.Redis()
    r.append('json_pages', json)


def get_cached_json_pages() -> str:
    r = redis.Redis()
    json_pages = r.get('json_pages')

    return json_pages


# Returns all pages as individuals
def get_cached_all_pages() -> Dict[str, Page]:
    return redis_get_complex_object('all_pages')


def cache_all_pages(pages: Dict[str, Page]) -> None:
    redis_cache_complex_object('all_pages', pages)


# Content for a specific page
def get_cached_specific_content(url: str) -> str:
    return redis_get_complex_object('specific_content_' + url)


def cache_specific_content(url: str, content: str) -> None:
    redis_cache_complex_object('specific_content_' + url, content)


# Groups representing communities or sub-communities of communities of pages
def get_cached_all_groups() -> List[Group]:
    return redis_get_complex_object('all_groups')


def cache_all_groups(groups: List[Group]) -> None:
    redis_cache_complex_object('all_groups', groups)


def get_cached_group_subgroups(group_id: str) -> Group:
    return redis_get_complex_object('groups_' + group_id)


def cache_groups_subgroups(parent_group_id: str, groups: List[Group]) -> None:
    redis_cache_complex_object('groups_' + parent_group_id, groups)


# Groups created by dividing pages according to their category, the sub-groups are divided into communities
def cache_all_groups_by_category(groups: List[Group]) -> None:
    redis_cache_complex_object('all_groups_by_category', groups)


def get_cached_all_groups_by_category() -> List[Group]:
    return redis_get_complex_object('all_groups_by_category')
