from django import forms
from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabets allowed.')

class WordleForm(forms.Form):
    guess = forms.CharField(
        max_length=5, 
        min_length=5,
        validators=[alpha],
        widget = forms.HiddenInput (
            attrs = ({
                'x-ref':'guess',
                'x-model':'guess_xmodel',
            })
        )
    )


    attempts_left = forms.IntegerField(initial=6, required=False, widget = forms.HiddenInput())

    attempt_number = forms.IntegerField(initial=1, required=False, widget=forms.HiddenInput())

    target_word = forms.CharField(required=False, widget = forms.HiddenInput())

class GuessForm(forms.Form):
    guess = forms.CharField(required=False, widget=forms.HiddenInput())
    l1_color = forms.CharField(initial='bg-secondary bg-opacity-25 text-light',widget=forms.HiddenInput())
    l2_color = forms.CharField(initial='bg-secondary bg-opacity-25 text-light',widget=forms.HiddenInput())
    l3_color = forms.CharField(initial='bg-secondary bg-opacity-25 text-light',widget=forms.HiddenInput())
    l4_color = forms.CharField(initial='bg-secondary bg-opacity-25 text-light',widget=forms.HiddenInput())
    l5_color = forms.CharField(initial='bg-secondary bg-opacity-25 text-light',widget=forms.HiddenInput())


class AlphabetForm(forms.Form):
    l_color = forms.CharField(required=False, initial='bg-secondary bg-opacity-25 text-light', widget=forms.HiddenInput())