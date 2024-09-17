import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'non-standard password'
        ),
            code='invalid'
    )

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={
        'placeholder': 'Ex.: John'
    }),
    error_messages={'required': 'Write your first name'},
    label='First Name'
    )
    last_name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
        'placeholder': 'Ex.: Doe'
    }),
    label='Last Name'
    )
    username = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={
        'placeholder': 'Your username'
    }),
    label='Username'
    )
    email = forms.EmailField(
        required=True,
        widget = forms.TextInput(attrs={
        'placeholder': 'Your e-mail'    
    }),
    label='E-mail'
    )
    password = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    ) 
    password2 = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs={
            'placeholder': 'enter your password again'
        }),
    label='Repeate your password'
    ) 
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
                raise ValidationError('User e-mail is already in use', code='invalid',)
                
        return email