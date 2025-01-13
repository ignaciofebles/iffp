from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class EditUserForm(UserChangeForm):
    password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Dejar igual si no deseas cambiar la contraseña."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'password')


    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:  # Si se ha ingresado una nueva contraseña
            user.set_password(password)
        if commit:
            user.save()
        return user
