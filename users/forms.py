from django import forms

from barbershop.models import Master


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите email', 'style': 'max-width: 380px'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль', 'style': 'max-width: 380px'}))


class GenerateFreeTimesForm(forms.Form):
    master = forms.ModelChoiceField(queryset=Master.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    start_day = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], widget=forms.DateTimeInput(
        attrs={'class': 'form-control', 'type': 'datetime-local'}))
    end_day = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],
                                  widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))
    interval = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class RecordingByDateForm(forms.Form):
    date = forms.DateField(input_formats=['%d.%m.%Y'], widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date',
               'style': 'max-width: 220px; margin-bottom: 10px; margin-right: 10px; font-size: 29px;'}))


class GenerateReportPdfForm(forms.Form):
    master = forms.ModelChoiceField(queryset=Master.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    start_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(input_formats=['%Y-%m-%d'],
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
