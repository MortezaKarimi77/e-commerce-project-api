from django.core.cache import cache


def get_cached_queryset(queryset, cache_key, timeout=None):
    cached_queryset = cache.get_or_set(key=cache_key, default=queryset, timeout=timeout)
    return cached_queryset


def get_cached_object(get_object_function, cache_key, timeout=None):
    cached_object = cache.get(key=cache_key)
    if cached_object is None:
        object = get_object_function()
        cached_object = cache.get_or_set(key=cache_key, default=object, timeout=timeout)
    return cached_object


def brand_directory_path(brand, filename) -> str:
    brand_name = brand.url.replace("-", " ").strip()
    return f"brands/{brand_name}/{filename}"


def product_directory_path(product, filename):
    category_name = product.category.media_folder_name
    product_name = product.url.replace("-", " ").strip()
    return f"products/{category_name}/{product_name}/{filename}"
