from django import forms

class BillForm(forms.Form):
    item = forms.CharField(max_length=100)
    itemCategory = forms.CharField()
    quantity = forms.IntegerField()
    price = forms.IntegerField()