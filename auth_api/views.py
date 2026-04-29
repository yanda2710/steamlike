import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

# Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, get_user_model
User = get_user_model()

from library.views import error_response

# POST /api/auth/register/
    # Register a new user
    # json body: { "username": "str", "password": "str" }

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    # Get all data from request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST # Si no es JSON, intentamos obtener los datos del formulario tradicional
        
        # return JsonResponse({
            # "error": "Invalid JSON data"
            # }, status=400)

    username = data.get("username")
    password = data.get("password")

    # Diccionary to store all errors, it's JSON
    errors = {}

    # Check username format
    if username == "" or username is None: # Check if it's empty
        errors["username"] = "Cannot be empty"
    elif not isinstance(username, str): # Check if it's a string
        errors["username"] = "Must be a string"
    elif User.objects.filter(username=username).exists(): # Check if it already exists
        errors["username"] = "Username already exists"

    # Check password format
    if password == "" or password is None: # Check if it's empty
        errors["password"] = "Cannot be empty"
    elif not isinstance(password, str): # Check if it's a string
        errors["password"] = "Must be a string"
    elif len(password) < 8: # Check if it's at least 8 characters long
        errors["password"] = "Must be at least 8 characters long"

    # If there are errors, return them
    if errors:
        return error_response(errors)

    # Create the user
    user = User.objects.create_user(
        username=username,
        password=password
    )

    return JsonResponse({
        "message": "Usuario registrado exitosamente",
        "user": {
            # "id": user.id, # No funciona, no sé por qué, así que lo dejo comentado por si acaso
            "username": user.username
        }
    }, status=201)

# POST /api/auth/login/
    # Login a user, change its behavior in the future to return a token or something like that
    # json body: { "username": "str", "password": "str" }

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # Get all data from request
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST # Si no es JSON, intentamos obtener los datos del formulario tradicional

        # return JsonResponse({
            # "error": "Invalid JSON data"
            # }, status=400)
    
    # Check if username and password are in the request body
    username = data.get("username")
    password = data.get("password")

    # Diccionary to store all errors, it's JSON
    errors = {}

    # Check username format
    if username == "" or username is None: # Check if it's empty
        errors["username"] = "Cannot be empty"
    elif not isinstance(username, str): # Check if it's a string
        errors["username"] = "Must be a string"
    
    # Check password format
    if password == "" or password is None: # Check if it's empty
        errors["password"] = "Cannot be empty"
    elif not isinstance(password, str): # Check if it's a string
        errors["password"] = "Must be a string"

    # If there are format errors, return them
    if errors:
        return error_response(errors)
    
    # Check if the user exists and the password is correct
    user = authenticate(request, username=username, password=password) # authenticate() returns the user if the credentials are correct, otherwise it returns None

    # If the user is None, it means that the credentials are incorrect
    if user is None:
        return JsonResponse({
            "message": "Credenciales incorrectas"
            }, status=401)
    
    # Login the user
    login(request, user) # Sirve para recordar que el usuario ha iniciado sesión
        
    return JsonResponse({
        "message": "Usuario autenticado exitosamente",
        "user": {
            "username": user.username
        }
    }, status=200)

# GET /api/users/me/
    # Check if the user is authenticated

@require_GET
def check_login(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "Unauthorized",
            "message": "No autenticado"
            }, status=401)
    
    return JsonResponse({
        "id": request.user.id, # No sé si lo llamará correctamente
        "username": request.user.username
    }, status=200)