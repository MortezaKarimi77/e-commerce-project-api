def brand_directory_path(brand, filename) -> str:
    brand_name = brand.url.replace("-", " ").strip()
    return f"brands/{brand_name}/{filename}"
