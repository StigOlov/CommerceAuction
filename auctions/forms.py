from django import forms
from .models import Category

class CreateListingForm(forms.Form):
    item_name = forms.CharField(max_length=100)
    item_price = forms.DecimalField(max_digits=10, decimal_places=2)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    closing_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(choices=Category.CATEGORY_CHOICES)
    image = forms.ImageField(required=False)

    