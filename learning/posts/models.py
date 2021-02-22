"""Posts models"""
from django.db import models as m


# Create your models here.
class User(m.Model):
    """User Model"""
    email = m.EmailField(unique=True)  # unique = True, el valor no puede repetirse
    password = m.CharField(max_length=100)

    first_name = m.CharField(max_length=25)
    last_name = m.CharField(max_length=25)

    is_admin = m.BooleanField(default=False)  # Valor por defecto

    bio = m.TextField(blank=True)  # Que pueda  estar vacia

    birthdate = m.DateField(blank=True, null=True)  # blank, permite valores vacios; null, permite valores nulos

    

    created = m.DateTimeField(auto_now_add=True)  # Que se agregue automaticamente al momento de crearse la instancia
    modified = m.DateTimeField(auto_now=True)  # Guardar la fecha de la última vez que se editó

    def __str__(self):
        return self.email
