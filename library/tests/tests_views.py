from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

import json

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

class AuthenticationTests(TestCase):
    def test_register(self):
        # Precondiciones

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={
            "username": "testuser",
            "password": "testpassword"
        }, content_type="application/json")

        # Comprobaciones
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Usuario registrado exitosamente")

    def test_register_invalid(self): # JSON vacío
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={}, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("username", response.json()["details"])
        self.assertIn("password", response.json()["details"])
        self.assertEqual(response.json()["details"]["username"], "Cannot be empty")
        self.assertEqual(response.json()["details"]["password"], "Cannot be empty")

    def test_register_invalid_username(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={
            "username": "",
            "password": "testpassword"
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("username", response.json()["details"])
        self.assertEqual(response.json()["details"]["username"], "Cannot be empty")

    def test_register_invalid_password(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={
            "username": "testuser",
            "password": ""
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("password", response.json()["details"])
        self.assertEqual(response.json()["details"]["password"], "Cannot be empty")

    def test_register_empty(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={}, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("username", response.json()["details"])
        self.assertIn("password", response.json()["details"])
        self.assertEqual(response.json()["details"]["username"], "Cannot be empty")
        self.assertEqual(response.json()["details"]["password"], "Cannot be empty")

    def test_register_duplicate(self):
        # Precondiciones
        User.objects.create_user(username="testuser", password="testpassword")

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/register/", data={
            "username": "testuser",
            "password": "testpassword"
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("username", response.json()["details"])
        self.assertEqual(response.json()["details"]["username"], "Username already exists")

    