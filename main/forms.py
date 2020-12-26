from django import forms

class Addform(forms.Form):
    verh = forms.CharField(label='Zagolovok', max_length=100)
    content=forms.CharField(label='Soderzimoe', max_length=300)
