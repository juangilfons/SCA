from django.db import models
from django.core.exceptions import ValidationError
import re

def validar_rotulo(valor):
    # This regular expression checks for the format XXX_XXX with exactly 3 uppercase letters on each side of the underscore
    if not re.match(r'^[A-Z]{3}_[A-Z]{3}$', valor):
        raise ValidationError('Identificador debe tener el siguiente formato: XXX_XXX (letras mayúsculas).')
class AreaDecision(models.Model):
    rotulo = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()


