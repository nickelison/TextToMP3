from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import User, Mp3File

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    # Add form-control class to all fields.
    # See: https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ConfirmDeleteAccountForm(ModelForm):
    class Meta:
        model = User
        fields = []

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Please upload a JPEG or PNG image.')

class ProfilePictureForm(forms.ModelForm):
    profile_picture = forms.ImageField(validators=[validate_file_extension])

    class Meta:
        model = User
        fields = ['profile_picture']

class CreateMp3Form(forms.Form):
    title = forms.CharField(
        label='File Name (do not include .mp3 file extension)',
        validators=[
            RegexValidator(r'^[\w-]+$', message="Only alphanumeric characters, hyphens, and underscores are allowed in the filename."),
        ],
        max_length=128,
        error_messages={'max_length': "More more than 128 characters are allowed in the filename."},
        widget=forms.TextInput(attrs={
            'placeholder': 'audio.mp3',
            'class': 'form-control'})
    )
    text = forms.CharField(
        label='Text (maximum of 3000 characters)',
        max_length=3000,
        error_messages={'max_length': "More more than 3000 characters are allowed in the filename."},
        widget=forms.Textarea(attrs={
            'class': 'form-control'})
    )
    voice = forms.ChoiceField(
        label='Voice',
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    use_neural_engine = forms.BooleanField(
        label='Use neural engine',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class DeleteMp3Form(forms.Form):
    mp3_id = forms.IntegerField()