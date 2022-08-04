from django import forms
from .models import *
from .views import *



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rate']
        