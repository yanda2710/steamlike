from urllib import response

from django.test import TestCase

import json

from auth_api.views import User, register, login
from library.models import LibraryEntry

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_health(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/health/")

        # Comprobaciones
        # Comprobar el código HTTP que devuelve una vista
        self.assertEqual(response.status_code, 200)
        # Comprobar el contenido de la respuesta
        self.assertEqual(response.json(), {"status": "ok"})
        # Verifica que una clave existe dentro del JSON de la respuesta.
        self.assertIn("status", response.json())
        # Comprueba el valor concreto devuelto por la vista.
        self.assertEqual(response.json()["status"], "ok")
        # Asegura que la respuesta no contiene información que no debería aparecer.
        self.assertNotIn("paco", response.json())

class LibraryEntryViewTests(TestCase):
    
    # --- Tests GET /api/library/entries (user) ---

    def test_get_entries_unauthenticated(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/library/entries/")

        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "error": "unauthorized",
            "message": "No autenticado"
        })
    
    def test_get_entries_authenticated_no_entries(self):
        # Precondiciones
        # Crear un usuario y autenticarse con él
        self.client.post("/api/auth/register/", {
            "username": "testuser",
            "password": "testpassword"
        })

        login_response = self.client.post("/api/auth/login/", {
            "username": "testuser",
            "password": "testpassword"
        })

        self.assertEqual(login_response.status_code, 200)

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/library/entries/")

        # Comprobaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Entries": []})

    def test_get_entries_authenticated_with_entries(self):
        # Precondiciones
        # Crear un usuario y autenticarse con él
        self.client.post("/api/auth/register/", {
            "username": "testuser",
            "password": "testpassword"
        })

        login_response = self.client.post("/api/auth/login/", {
            "username": "testuser",
            "password": "testpassword"
        })

        self.assertEqual(login_response.status_code, 200)

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/library/entries/")

        # Comprobaciones
        self.assertEqual(response.status_code, 200)

    def test_get_entries_authenticated_with_entries_other_user(self):
        # Precondiciones
        # Crear un usuario y autenticarse con él
        self.client.post("/api/auth/register/", {
            "username": "testuser1",
            "password": "testpassword1"
        })

        login_response = self.client.post("/api/auth/login/", {
            "username": "testuser1",
            "password": "testpassword1"
        })

        self.assertEqual(login_response.status_code, 200)

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/library/entries/")

        # Comprobaciones
        self.assertEqual(response.status_code, 200)

    # --- Tests POST /api/library/entries (user) ---

    def test_add_game_unauthenticated(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/library/entries/", {
            "external_game_id": "game123",
            "status": "playing",
            "hours_played": 10
        })

        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "error": "unauthorized",
            "message": "No autenticado"
        })

    def test_add_game_authenticated(self):
        # Precondiciones
        # Crear un usuario y autenticarse con él
        self.client.post("/api/auth/register/", json.dumps({
            "username": "testuser",
            "password": "testpassword"
        }), content_type="application/json")

        login_response = self.client.post("/api/auth/login/", json.dumps({
            "username": "testuser",
            "password": "testpassword"
        }), content_type="application/json")

        self.assertEqual(login_response.status_code, 200)

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/library/entries/", json.dumps({
            "external_game_id": "game123",
            "status": "playing",
            "hours_played": 10
        }), content_type="application/json")

        # Comprobaciones
        self.assertEqual(response.status_code, 201)

    # --- Tests GET /api/library/entries/{external_game_id} (user) ---
    def test_get_entry_unauthenticated(self):
        response = self.client.get("/api/library/entries/game123/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "error": "unauthorized",
            "message": "No autenticado"
        })
