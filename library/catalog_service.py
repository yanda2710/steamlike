import json, requests

from django.core.cache import cache

class CatalogService:
    @staticmethod
    def search_catalog(query):
        cache_key = f"search_{query}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return cached_response

        # Simulate a search in the catalog (replace with actual logic)
        response = requests.get(f"https://api.example.com/catalog/search?q={query}")
        
        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
            return data
        else:
            return {"error": "Failed to fetch catalog data"}