import json
from django.http import JsonResponse
from .models import LibraryEntry
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})

# POST /library/add_game, json body: { 'external_game_id': 'str', 'status': 'str', 'hours_played': integer }
# Add a game to the DB
@csrf_exempt
def add_game(request):
    if request.method == 'POST':

        # Get all data from user
        data = json.loads(request.body)
        
        # User data from the request body
        external_game_id = data.get('external_game_id') # str
        status = data.get('status') # str wishlist, playing, completed, dropped
        hours_played = data.get('hours_played') # integer >= 0

        # Check the format for each one
        error = None

        # Check external_game_id format
        try:
            if external_game_id == '': # Check if it's empty
                raise ValueError('Cannot be empty')
            if not isinstance(external_game_id, str): # Check if it's a string
                raise TypeError('Must be a string')
            if LibraryEntry.objects.filter(external_game_id=external_game_id).exists(): # Check if it already exists
                raise ValueError('Already exists')

        except (TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Check status format
        try:
            if status == '': # Check if it's empty
                raise ValueError('Cannot be empty')
            if not isinstance(status, str): # Check if it's a string
                raise TypeError('Must be a string')
            if status not in LibraryEntry.ALLOWED_STATUSES: # Check if it's one of the allowed statuses
                raise ValueError('Invalid status value or format (must be lowercase)')
            
        except (TypeError, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        

        # Check hours_played format
        try:
            if hours_played == '': # Check if it's empty
                raise ValueError('Cannot be empty')
            if not isinstance(hours_played, int): # Check if it's an integer
                raise TypeError('Must be a integer')
            if hours_played < 0: # Check if it's greater than or equal to 0
                raise ValueError('Must be greater than 0 or 0')

        except (ValueError, TypeError):
            return JsonResponse({'error': str(e)}, status=400)

        # If all the data is valid, create a new LibraryEntry and save it to the DB, same line
        entry = LibraryEntry.objects.create(
            external_game_id=external_game_id,
            status=status,
            hours_played=hours_played
        )

        return JsonResponse({
            'message': 'Game added successfully',
            'entry': {
                'id': entry.id,
                'external_game_id': entry.external_game_id,
                'status': entry.status,
                'hours_played': entry.hours_played
            }
        }, status=201)
    
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

    # hay algun error por ahí, me dice q tengo q hacerlo, despues lo hago