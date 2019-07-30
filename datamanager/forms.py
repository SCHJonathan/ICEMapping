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
    ('OtherRace', 'Other Race'),
    ('NA', 'Prefer not to answer')
)

Age = (
    ('', 'Choose...'),
    ('Young', 'Young'),
    ('Middle', 'Middle'),
    ('Old', 'Old'),
    ('NA', 'Prefer not to answer')
)

Dept = (
    ('', 'Choose...'),
    ('North','North'),
    ('South','South'),
    ('Main','Main' )
)

RATE = (
    ('', 'Choose...'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

Area = (
    ('', 'Choose...'),
    ('south', 'South Quad'),
    ('main', 'Main Quad'),
    ('engin', 'North Quad'),
)

Preference = (
    ('', 'Choose...'),
    ('-1', 'Dislike'),
    ('-0.5', 'Not good'),
    ('0', 'No prefer'),
    ('0.5', 'Good'),
    ('1', 'Prefer'),
)

#   Forms for user to filled out. I use the 'crispy_forms' API to beautify the form.
#   You can google this API to see how it works and use their documentation as reference.
class UserInfoForm(forms.Form):
    geoid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'GeoID'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Your age'}))
    race = forms.ChoiceField(choices=RACE)
    gender = forms.ChoiceField(choices=GENDER)
    dept = forms.ChoiceField(choices=Dept)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('geoid', css_class='form-group col-md-6 mb-0'),
                Column('age', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('dept', css_class='form-group col-md-4 mb-0'),
                Column('race', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )

class CommentForm(forms.Form):
    rate = forms.ChoiceField(choices=RATE)
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Leave your comment: '}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rate',
            'comment',
            Submit('submit', 'Submit')
        )

# input_data = [Pop, White, Black, Asian, OtherRace, Male, Female, Young, Middle, Old, Sdist, Ndist, Mdist]
class recommandationForm(forms.Form):
    young = forms.ChoiceField(choices=Preference)
    old = forms.ChoiceField(choices=Preference)
    middle = forms.ChoiceField(choices=Preference)
    white = forms.ChoiceField(choices=Preference)
    black = forms.ChoiceField(choices=Preference)
    asian = forms.ChoiceField(choices=Preference)
    otherrace = forms.ChoiceField(choices=Preference)
    population = forms.ChoiceField(choices=Preference)
    male = forms.ChoiceField(choices=Preference)
    female = forms.ChoiceField(choices=Preference)
    south = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Acceptable distance away from south quad'}))
    main = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Acceptable distance away from main quad'}))
    north = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Acceptable distance away from north quad'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('young', css_class='form-group col-md-4 mb-0'),
                Column('middle', css_class='form-group col-md-4 mb-0'),
                Column('old', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('black', css_class='form-group col-md-3 mb-0'),
                Column('white', css_class='form-group col-md-3 mb-0'),
                Column('asian', css_class='form-group col-md-3 mb-0'),
                Column('otherrace', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('population', css_class='form-group col-md-4 mb-0'),
                Column('male', css_class='form-group col-md-4 mb-0'),
                Column('female', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('south', css_class='form-group col-md-4 mb-0'),
                Column('main', css_class='form-group col-md-4 mb-0'),
                Column('north', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )
