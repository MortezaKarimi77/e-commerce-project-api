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


# comments app cache keys


def all_comments() -> str:
    return "comments:all"


def single_comment(comment) -> str:
    return f"comments:{comment}"


# users app cache keys


def all_users() -> str:
    return "users:all"


def single_user(user) -> str:
    return f"users:{user}"
