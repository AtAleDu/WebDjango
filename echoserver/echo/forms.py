from .models import Book
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True)  # Без ограничений символов
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Используем password1
        if commit:
            user.save()
class LoginForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'description', 'published_date']