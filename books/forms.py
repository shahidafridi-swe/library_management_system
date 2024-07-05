from django import forms

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment',]
    
        widgets = {
                'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write Your Review Here...'})
            }        