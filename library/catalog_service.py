import json
import requests
from django.core.cache import cache


class CatalogService:
    @staticmethod
    def search_catalog(query):

        cache_key = f"search_{query}"
        cached_response = cache.get(cache_key)

        if cached_response:
            return cached_response

        response = requests.get(
            "https://www.cheapshark.com/api/1.0/games",
            params={
                "title": query,
                "limit": 10
            }
        )

        if response.status_code != 200:
            return {"error": "api_error"}

        try:
            data = response.json()

            results = []

            for game in data:
                results.append({
                    "external_game_id": game.get("gameID"),
                    "title": game.get("external"),
                    "cheapest_price": game.get("cheapest"),
                    "thumb": f"https://store.steampowered.com/app/{game.get('steamAppID')}" if game.get("steamAppID") else None,
                    "steam_link": f"https://store.steampowered.com/app/{game.get('steamAppID')}" if game.get("steamAppID") else None
                })

            cache.set(cache_key, results, timeout=3600)

            return results

        except Exception:
            return {"error": "api_error"}
        
    @staticmethod
    def resolve_games(external_game_ids):

        resolved_games = []

        for game_id in external_game_ids:
            try:
                response = requests.get(
                    "https://www.cheapshark.com/api/1.0/games",
                    params={"id": game_id},
                    timeout=5
                )

                if response.status_code != 200:
                    continue

                game_data = response.json()

                data = game_data.get("info", {})
                steam_app_id = data.get("steamAppID")

                resolved_games.append({
                    "external_game_id": steam_app_id,
                    "title": data.get("title"),
                    "thumb": f"https://store.steampowered.com/app/{steam_app_id}" if steam_app_id else None,
                })

            except requests.RequestException:
                continue

        return resolved_games