from typing import List

from api.models import Page, Category


def create_categories_for_nodes(nodes: List[Page]) -> List[Category]:
    group_categories = {}
    for node in nodes:
        for node_cat in node.categories:
            if node_cat.name in group_categories:
                group_categories[node_cat.name] += node_cat.occurrence
            else:
                group_categories[node_cat.name] = node_cat.occurrence

    categories = []
    for g_cat in group_categories:
        category = Category(
            name=g_cat,
            occurrence=group_categories[g_cat]
        )
        categories.append(category)

    return categories
