from django import forms


class TestForm(forms.Form):
    foo = forms.CharField()
    bar = forms.CharField(help_text='help bar')
    baz = forms.CharField(label='<baz>', help_text='<baz>')
