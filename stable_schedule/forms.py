from django import forms
from django.core.exceptions import ValidationError

from stable_schedule.models import Horse, TrainingSchedule, Feeding, Health, Competition

def check_amount(value):
    if value > 50:
        raise ValidationError("Unfortunately, horses don`t live that long...")
    elif value < 0:
        raise ValidationError("Your horse hasn't been born yet'")
class AddHorseForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'form-control'}),
                                validators=[check_amount]
    )
    pedigree = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

class ModifyHorseForm(forms.ModelForm):
    class Meta:
        model=Horse
        fields=['name', 'age', 'pedigree']

class AddFeedingForm(forms.Form):
    ingredients = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    time_of_day = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ModifyFeedingForm(forms.ModelForm):
    class Meta:
        model=Feeding
        fields=['ingredients', 'time_of_day']


class AddHealthForm(forms.Form):
    care = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

class ModifyHealthForm(forms.ModelForm):
    class Meta:
        model=Health
        fields=['care']

class ModifyTrainingForm(forms.ModelForm):
    class Meta:
        model=TrainingSchedule
        fields=['place']

class AddCompetitionForm(forms.Form):
    place = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

class AddTrainingForm(forms.Form):
    place = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )

class AddHorseToCompetitionForm(forms.Form):
    horse = forms.ChoiceField()
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'form-control'}),
    )