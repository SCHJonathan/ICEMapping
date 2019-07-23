from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

GENDER = (
    ('', 'Choose...'),
    ('Female', 'Female'),
    ('Male', 'Male'),
    ('NA', 'Prefer not to answer')
)


RACE = (
    ('', 'Choose...'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Asian', 'Asian'),
    ('NA', 'Prefer not to answer')
)

Age = (
    ('', 'Choose...'),
    ('Young', 'Young'),
    ('Middle', 'Middle'),
    ('Old', 'Old'),
    ('NA', 'Prefer not to answer')
)


class UserInfoForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    geoid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'GeoID'}))
    age = forms.ChoiceField(choices=Age)
    race = forms.ChoiceField(choices=RACE)
    gender = forms.ChoiceField(choices=GENDER)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'geoid',
            Row(
                Column('age', css_class='form-group col-md-6 mb-0'),
                Column('race', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )
