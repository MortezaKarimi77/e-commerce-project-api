# brands app cache keys


def all_brands() -> str:
    return "brands:all"


def single_brand(brand) -> str:
    return f"brands:{brand}"


# categories app cache keys


def all_categories() -> str:
    return "categories:all"


def single_category(category) -> str:
    return f"categories:{category}"
