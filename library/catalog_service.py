import json
import requests
from django.core.cache import cache


class CatalogService:

    def response_error503(self):
        return json.dumps({
            "error": "external_service_unavailable",
            "message": "El catálogo externo no está disponible. Inténtalo más tarde."
        })

    def response_error502(self):
        return json.dumps({
            "error": "external_service_error",
            "message": "Error al consultar el catálogo externo. Inténtalo más tarde."
        })
    
    def response_error500(self):
        return json.dumps({
            "error": "external_service_error",
            "message": "Error inesperado al consultar el catálogo externo. Inténtalo más tarde."
        })

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

        if response.status_code == 503:
            return CatalogService().response_error503()
        if response.status_code == 502:
            return CatalogService().response_error502()
        if response.status_code != 200:
            return CatalogService().response_error500()

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
            return CatalogService().response_error500()
        
    @staticmethod
    def resolve_games(external_game_ids):

        if not external_game_ids:
            return []

        resolved_games = []

        for game_id in external_game_ids:

            cache_key = f"game_{game_id}"
            cached_game = cache.get(cache_key)

            if cached_game:
                resolved_games.append(cached_game)
                continue

            try:
                response = requests.get(
                    "https://www.cheapshark.com/api/1.0/games",
                    params={"id": game_id},
                    timeout=10
                )

                if response.status_code == 503:
                    return CatalogService().response_error503()
                if response.status_code == 502:
                    return CatalogService().response_error502()
                if response.status_code != 200:
                    return CatalogService().response_error500()

                game_data = response.json()
                data = game_data.get("info", {})
                steam_app_id = data.get("steamAppID")

                game = {
                    "external_game_id": steam_app_id,
                    "title": data.get("title"),
                    "thumb": f"https://store.steampowered.com/app/{steam_app_id}" if steam_app_id else None,
                }

                cache.set(cache_key, game, timeout=3600)
                resolved_games.append(game)

            except requests.RequestException:
                return CatalogService().response_error500()

        return resolved_games