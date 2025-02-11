from django import forms
from .models import Rutina, Serie, Ejercicio, Usuario

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la rutina'
            })
        }

class SerieForm(forms.ModelForm):
    ejercicio = forms.ModelChoiceField(
        queryset=Ejercicio.objects.all(),
        empty_label="Selecciona un ejercicio",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Selecciona un usuario",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    numero_serie = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'N° de serie'
        })
    )
    peso = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Peso (kg)'
        })
    )
    repeticiones = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeticiones'
        })
    )
    nota = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Nota (opcional)',
            'rows': 3
        })
    )

    class Meta:
        model = Serie
        fields = ['ejercicio', 'usuario', 'numero_serie', 'peso', 'repeticiones', 'nota']
