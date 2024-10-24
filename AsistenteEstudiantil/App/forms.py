from django import forms
from .models import UserProfile, Icon
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    # Agregar campos adicionales si es necesario
    icon = forms.ModelChoiceField(
        queryset=Icon.objects.all(),
        empty_label="Selecciona un icono",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Agregar 'password1' y 'password2'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar las etiquetas de los campos si es necesario
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Repita la Contraseña'

        # Deshabilitar la restricción de longitud mínima de contraseña
        self.fields['password1'].min_length = 6
        self.fields['password2'].min_length = 6
        

        # Eliminar validadores de complejidad de contraseña
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []