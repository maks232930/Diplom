from django import forms

from .models import Message, Review


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = 'first_name', 'email', 'subject', 'message'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тема'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Сообщение', 'cols': '30', 'rows': '7'}),
        }


# class RecordingForm(forms.ModelForm):
# class Meta:
#     model = Recording
#     fields = ('')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'email', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'cols': '30', 'rows': '7'}),
        }
