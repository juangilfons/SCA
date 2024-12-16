from django.db import models
from django.core.exceptions import ValidationError
import re

def validar_rotulo(valor):
    if not re.match(r'^[A-Z]{3}_[A-Z]{3}$', valor):
        raise ValidationError('Identificador debe tener el siguiente formato: XXX_XXX (letras mayúsculas).')

class AreaDecision(models.Model):
    rotulo = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    related_areas = models.ManyToManyField('self', blank=True, symmetrical=True)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class OpcionDecision(models.Model):
    description = models.CharField(max_length=100)
    area_decision = models.ForeignKey(AreaDecision, on_delete=models.CASCADE, related_name="opciondecision_set")

    def __str__(self):
        return self.description

class DecisionAlternative(models.Model):
    hexa = models.CharField(max_length=7, unique=True)
    options = models.ManyToManyField(OpcionDecision, related_name="alternatives")

    def __str__(self):
        return "Alternative: " + self.hexa

    def is_valid(self):
        decision_areas = {option.area_decision for option in self.options.all()}
        return len(decision_areas) == AreaDecision.objects.count()


class AreaComparacion(models.Model):
    rotulo = models.CharField(max_length=7, unique=True)
    title = models.CharField(max_length=100)
    peso = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    symbol = models.CharField(max_length=1, default="*")

    def __str__(self):
        return self.title

class OpcionComparacion(models.Model):
    option = models.ForeignKey(OpcionDecision, on_delete=models.CASCADE)
    area_comparacion = models.ForeignKey(AreaComparacion, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(6)], default=0)

    class Meta:
        unique_together = ('option', 'area_comparacion')

    def __str__(self):
        return f"{self.option} - {self.area_comparacion}: {self.value}"

