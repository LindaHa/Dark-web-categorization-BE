from typing import List, Callable, Dict

from api.models import Group, Page, Link, Category, MetaGroup, DetailsOptions, PageDetails

oneUrl = 'urlOne'
twoUrl = 'urlTwo'
parentUrl = 'parentUrl'


def make_page(url: str) -> Page:
    return make_custom_page(
        url=url,
        links=[url + 'aaa', url + 'bbb'],
    )


def make_custom_page(url: str, links: List[str] = [], category: str = 'Social', content: str = 'Social page content') -> Page:
    return Page(
        url=url,
        categories=[Category(name=category, occurrence=1)],
        content=content,
        links=[Link(link=lin, occurrences=1) for lin in links]
    )


def make_group(group_id: str) -> Group:
    return Group(
        id=group_id,
        links=[Link(link='0.3', occurrences=2)],
        members={
            oneUrl: make_page(oneUrl),
            twoUrl: make_page(twoUrl)
        },
        categories=[Category(name='Social', occurrence=2)]
    )


def make_custom_group(group_id: str, pages: Dict[str, Page], links: List[Link], categories: List[Category]) -> Group:
    return Group(
        id=group_id,
        links=links,
        members=pages,
        categories=categories
    )


def make_meta_group(group_id: str) -> MetaGroup:
    return MetaGroup(
        id=group_id,
        links=[Link(link='0.3', occurrences=2)],
        first_members=[make_page(oneUrl), make_page(twoUrl)],
        categories=[Category(name='Social', occurrence=2)],
        members_count=2,
        domains_count=2,
    )


def make_multiple_models(number_times: int, model_id: str, func: Callable) -> List:
    groups = []
    while number_times > 0:
        groups.append(func(str(number_times) + model_id))
        number_times -= 1

    return groups


def make_details_options() -> DetailsOptions:
    return DetailsOptions(
        category=True,
        content=False,
        title=True,
        links=True
    )


def make_page_details(page: Page) -> PageDetails:
    return PageDetails(
        url=page.url,
        title=page.title,
        links=[link.link for link in page.links],
        category=page.categories[0].name
    )
