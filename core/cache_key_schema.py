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


# products app cache keys


def all_products() -> str:
    return "products:all"


def visible_products() -> str:
    return "products:visible"


def single_product(product) -> str:
    return f"products:{product}"


def category_all_products(category) -> str:
    return f"categories:{category}:products:all"


def category_visible_products(category) -> str:
    return f"categories:{category}:products:visible"


def brand_all_products(brand) -> str:
    return f"brands:{brand}:products:all"


def brand_visible_products(brand) -> str:
    return f"brands:{brand}:products:visible"


def all_product_items() -> str:
    return "product-items:all"


def single_product_item(product_item) -> str:
    return f"product-items:{product_item}"
