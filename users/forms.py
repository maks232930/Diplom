from django import forms

from barbershop.models import Master


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email', 'style': 'width: 50%'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль', 'style': 'width: 50%'}))


class GenerateFreeTimesForm(forms.Form):
    master = forms.ModelChoiceField(queryset=Master.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    start_day = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    end_day = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    interval = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
