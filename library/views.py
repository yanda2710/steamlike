import json
from django.http import JsonResponse
from .models import LibraryEntry
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
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
@require_GET
def get_entries(request):
    entries = LibraryEntry.objects.all()
    entries_data = []
    for entry in entries:
        entries_data.append({
            # "id": entry.id,
            "external_game_id": entry.external_game_id,
            "status": entry.status,
            "hours_played": entry.hours_played
        })
    return JsonResponse({"All entries": entries_data}, status=200)

# POST /api/library/entries
@csrf_exempt
def add_game(request):
    # Get all data from user
    data = json.loads(request.body)
        
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
    # No need for entruy.save() because create() already saves the object to the DB
    entry = LibraryEntry.objects.create(
        external_game_id=external_game_id,
        status=status,
        hours_played=hours_played
    )

    return JsonResponse({
        "message": "Game added successfully",
        "entry": {
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
    if not LibraryEntry.objects.filter(external_game_id=external_game_id).exists():
        return JsonResponse({
            "error": "not_found",
            "message": "La entrada solicitada no existe"
            }, status=404)
    
    entry = LibraryEntry.objects.get(external_game_id=external_game_id)

    return JsonResponse({
        "external_game_id": entry.external_game_id,
        "status": entry.status,
        "hours_played": entry.hours_played
        }, status=200)

# PATCH /api/library/entries/{external_game_id}/
@csrf_exempt
def update_entry(request, external_game_id):
    if not LibraryEntry.objects.filter(external_game_id=external_game_id).exists():
        return JsonResponse({
            "error": "not_found",
            "message": "La entrada solicitada no existe"
            }, status=404)
    
    # Get the entry to update
    entry = LibraryEntry.objects.get(external_game_id=external_game_id)

    # Get all data from user
    data = json.loads(request.body)

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

