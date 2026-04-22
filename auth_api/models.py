from django.contrib.auth.models import AbstractUser # Utilizamos AbstractUser para personalizar el modelo de User
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Podemos agregar campos adicionales si es necesario
    pass