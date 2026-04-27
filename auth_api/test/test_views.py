from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

class AuthenticationTests(TestCase):

    # --- Tests para registro de usuarios ---

    def test_register(self): # Registro válido
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

    # --- Tests para login de usuarios ---

    def test_login(self): # Login válido
        # Precondiciones
        User.objects.create_user(username="testuser", password="testpassword")

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={
            "username": "testuser",
            "password": "testpassword"
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Usuario autenticado exitosamente")

    def test_login_invalid(self): # JSON vacío
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={}, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "validation_error")
        self.assertIn("details", response.json())
        self.assertIn("username", response.json()["details"])
        self.assertIn("password", response.json()["details"])
        self.assertEqual(response.json()["details"]["username"], "Cannot be empty")
        self.assertEqual(response.json()["details"]["password"], "Cannot be empty")

    def test_login_invalid_username(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={
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

    def test_login_invalid_password(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={
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

    def test_login_wrong_credentials(self):
        # Precondiciones
        User.objects.create_user(username="testuser", password="testpassword")

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={
            "username": "testuser",
            "password": "wrongpassword"
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Credenciales incorrectas")

    def test_login_nonexistent_user(self):
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/auth/login/", data={
            "username": "nonexistentuser",
            "password": "testpassword"
        }, content_type="application/json")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Credenciales incorrectas")

    # --- Tests para check_login ---

    def test_check_login_authenticated(self): # Usuario autenticado
        # Precondiciones
        User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/users/me/")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())
        self.assertEqual(response.json()["username"], "testuser")

    def test_check_login_unauthenticated(self): # Usuario no autenticado
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/users/me/")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Unauthorized")
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "No autenticado")

    def test_check_login_after_logout(self): # Usuario que se ha autenticado pero luego ha cerrado sesión
        # Precondiciones
        User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.client.logout()

        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.get("/api/users/me/")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Unauthorized")
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "No autenticado")

    def test_check_login_invalid_method(self): # Método no permitido
        # Precondiciones
        # Llamada (usando self.client y la ruta de la vista que queremos probar)
        response = self.client.post("/api/users/me/")
        
        # Comprobaciones
        self.assertEqual(response.status_code, 405)

    #