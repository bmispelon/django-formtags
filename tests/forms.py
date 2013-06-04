from django import forms


def dummy_validator(value):
    if value == 'invalid':
        raise forms.ValidationError('invalid')
    return value


class TestForm(forms.Form):
    foo = forms.CharField(required=False, validators=[dummy_validator])
    bar = forms.CharField(help_text='help bar', required=False)
    baz = forms.CharField(label='<baz>', help_text='<baz>', required=False)
    qux = forms.CharField(validators=[dummy_validator])
