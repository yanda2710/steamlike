from django.test import TestCase

import json

from auth_api.views import register, login

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
    
    # TODO: REVISAR, NO IDENTIFICA EL USUARIO AUTENTICADO, DA 400 EN LUGAR DE 200, POSIBLE PROBLEMA CON LA AUTENTICACIÓN EN LOS TESTS

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


    # --- Tests POST /api/library/entries (user) ---
