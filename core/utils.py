def brand_directory_path(brand, filename) -> str:
    brand_name = brand.url.replace("-", " ").strip()
    return f"brands/{brand_name}/{filename}"


def product_directory_path(product, filename):
    category_name = product.category.media_folder_name
    product_name = product.url.replace("-", " ").strip()
    return f"products/{category_name}/{product_name}/{filename}"
