from django.db import models
from django.utils.timezone import now 
from django.core.validators import MinValueValidator

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Rutina(models.Model):
    nombre = models.CharField(max_length=150)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.fecha.strftime('%d-%m-%Y')})"

class Serie(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='series')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)  # Permitir valores nulos
    numero_serie = models.IntegerField(validators=[MinValueValidator(0)])
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    repeticiones = models.PositiveIntegerField()
    nota = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.ejercicio.nombre} - Serie {self.numero_serie}"
