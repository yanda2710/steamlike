import json
import requests

from django.http import JsonResponse

from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

from .models import LibraryEntry

from django.contrib.auth import get_user_model
User = get_user_model()

@require_GET
def health(request):
    return JsonResponse({"status": "ok"})

# Helper function to return a JSON response with error details
def error_response(errors):
    return JsonResponse({
        "error": "validation_error",
        "message": "Datos de entrada inválidos",
        "details": errors
    }, status=400)

def duplicate_entry_response():
    return JsonResponse({
        "error": "duplicate_entry",
        "message": "El juego ya existe en la biblioteca",
        "details": {"external_game_id": "duplicate"}
    }, status=400)

# url /library/entries

# GET
    # Get all library entries in the DB
    # Función definida más abajo para mantener el código organizado, y porque es un GET, no un POST

# POST
    # Add a game to the DB
    # json body: { "external_game_id": "str", "status": "str", "hours_played": integer }

@csrf_exempt
def games(request):
    if request.method == "GET":
        return get_entries(request)

    elif request.method == "POST":
        return add_game(request)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# GET /api/library/entries
    # Get all library entries in the DB by user
    # Only return the entries that belong to the authenticated user (user field of the entry is equal to the authenticated user)

@require_GET
def get_entries(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized",
            "message": "No autenticado"
        }, status=401)
    
    entries = LibraryEntry.objects.filter(user=request.user) # Solo obtenemos las entradas que pertenecen al usuario autenticado
    
    entries_data = []
    for entry in entries:
        entries_data.append({
            # "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        })
    return JsonResponse({"Entries": entries_data}, status=200)

# POST /api/library/entries
@csrf_exempt
def add_game(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized",
            "message": "No autenticado"
        }, status=401)

    # Get all data from request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON data"
            }, status=400)
        
    # User data from the request body
    external_game_id = data.get("external_game_id") # str
    status = data.get("status") # str wishlist, playing, completed, dropped
    hours_played = data.get("hours_played") # integer >= 0

    # Diccionary to store all errors, it's JSON
    errors = {}

    # Check external_game_id format
    if external_game_id == "" or external_game_id is None: # Check if it's empty
        errors["external_game_id"] = "Cannot be empty"
    elif not isinstance(external_game_id, str): # Check if it's a string
        errors["external_game_id"] = "Must be a string"
    elif LibraryEntry.objects.filter(external_game_id=external_game_id).exists(): # Check if it already exists
        return duplicate_entry_response()

    # Check status format
    if status == "" or status is None: # Check if it's empty
        errors["status"] = "Cannot be empty"
    elif not isinstance(status, str): # Check if it's a string
        errors["status"] = "Must be a string"
    elif status not in LibraryEntry.ALLOWED_STATUSES: # Check if it's one of the allowed statuses
        errors["status"] = "Invalid status value or format (must be lowercase)"

    # Check hours_played format
    if hours_played == "" or hours_played is None: # Check if it's empty
        errors["hours_played"] = "Cannot be empty"
    elif not isinstance(hours_played, int): # Check if it's an integer
        errors["hours_played"] = "Must be a integer"
    elif hours_played < 0: # Check if it's greater than or equal to 0
        errors["hours_played"] = "Must be greater than 0, or 0"

    # If there are any errors, return a JSON response with the error details
    if errors:
        return error_response(errors)

    # If all the data is valid, create a new LibraryEntry and save it to the DB in the same line
    # No need for entry.save() because create() already saves the object to the DB
    entry = LibraryEntry.objects.create(
        external_game_id=external_game_id,
        status=status,
        hours_played=hours_played,
        user=request.user if request.user.is_authenticated else None # Asignamos el usuario autenticado, o None si no hay ninguno (aunque en producción debería ser obligatorio estar autenticado para agregar juegos)
    )

    return JsonResponse({
        "message": "Game added successfully",
        "entry": {
            "id": entry.pk, # No sé si es necesario, pero lo dejo por si acaso
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        }
    }, status=201)

# url /library/entries/{external_game_id}

# GET
    # Get the library entry with the specified external_game_id

# PATCH
    # Update the library entry with the specified external_game_id
    # json body: { "status": "str", "hours_played": integer }

@csrf_exempt
def game_detailed(request, external_game_id):
    if request.method == "GET":
        return get_entry(request, external_game_id)

    elif request.method == "PATCH":
        return update_entry(request, external_game_id)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# GET /api/library/entries/{external_game_id}/
@require_GET
def get_entry(request, external_game_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized",
            "message": "No autenticado"
            }, status=401)
    
    try:
        entry = LibraryEntry.objects.get(user=request.user, external_game_id=external_game_id) # Solo obtenemos la entrada que pertenece al usuario autenticado y tiene el external_game_id especificado
    except LibraryEntry.DoesNotExist:
        return JsonResponse({
            "error": "not_found",
            "message": "La entrada solicitada no existe"
            }, status=404)
    
    return JsonResponse({
        "external_game_id": entry.external_game_id,
        "status": entry.status,
        "hours_played": entry.hours_played
        }, status=200)

# PATCH /api/library/entries/{external_game_id}/
@csrf_exempt
def update_entry(request, external_game_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "unauthorized",
            "message": "No autenticado"
            }, status=401)
    
    try:
        entry = LibraryEntry.objects.get(user=request.user, external_game_id=external_game_id) # Solo obtenemos la entrada que pertenece al usuario autenticado y tiene el external_game_id especificado
    except LibraryEntry.DoesNotExist:
        return JsonResponse({
            "error": "not_found",
            "message": "La entrada solicitada no existe"
            }, status=404)

    # Get all data from request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON data"
            }, status=400)

    # Check if there's any data to update
    if not data:
        return JsonResponse({
            "error": "validation_error",
            "message": "No data provided for update",
        }, status=400)

    # User data from the request body
    status = data.get("status") # str wishlist, playing, completed, dropped
    hours_played = data.get("hours_played") # integer >= 0

    # Check if not empty, and if it's valid, then update the entry
    if status is not None:
        if status == "" or not isinstance(status, str) or status not in LibraryEntry.ALLOWED_STATUSES:
            return error_response({"status": "Invalid status value or format (must be lowercase)"})
        entry.status = status

    if hours_played is not None:
        if hours_played == "" or not isinstance(hours_played, int) or hours_played < 0:
            return error_response({"hours_played": "Must be a integer greater than or equal to 0"})
        entry.hours_played = hours_played

    # Save the updated entry to the DB
    entry.save()

    # Return the updated entry data in the response
    return JsonResponse({
        "message": "Game updated successfully",
        "entry": {
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        }
    }, status=200)

# url /api/catalog/search/

# GET
    # Search for games in the catalog by name
    # Query parameter: ?q=game_name

@require_GET
def search_catalog(request):
    # Get parameter q from query params
    query = request.GET.get("q", "")

    # Validate that the query parameter is not empty, if it is, return an error response
    if query == "":
        return JsonResponse({
            "error": "validation_error",
            "message": "Query parameter 'q' is required and cannot be empty"
        }, status=400)

    # Call to API
    response = requests.get("https://www.cheapshark.com/api/1.0/games", params={"title": query, "limit": 10})

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
        
        return JsonResponse({"results": results}, status=200)
    
    except requests.RequestException as e:
        return JsonResponse({
            "error": "api_error",
            "message": "Error fetching data from API"
        }, status=500)

# url /api/catalog/resolve/

    # POST
        # Resolve a bunch of external_game_id's to get their details from the API
        # json body: { "external_game_ids": ["str", "str", ...] } Obligatorio y no vacío

@csrf_exempt
def resolve_games(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # Get all data from request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON data"
            }, status=400)

    external_game_ids = data.get("external_game_ids")

    # Validate that external_game_ids is provided and is a non-empty list of strings
    if not external_game_ids or not isinstance(external_game_ids, list) or not all(isinstance(id, str) for id in external_game_ids):
        return JsonResponse({
            "error": "validation_error",
            "message": "Field 'external_game_ids' is required and must be a non-empty list of strings"
        }, status=400)

    resolved_games = []

    for game_id in external_game_ids:
        try:
            response = requests.get(
                "https://www.cheapshark.com/api/1.0/games",
                params={"id": game_id}
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

    return JsonResponse({"resolved_games": resolved_games}, status=200)



