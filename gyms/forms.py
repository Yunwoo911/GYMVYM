from django import forms
from .models import PersonalInfo

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'height', 'weight', 'medical_conditions', 'medications', 'frequency', 'types', 'intensity', 'goals',
            'diet_habits', 'sleep_pattern', 'stress_level', 'smoking', 'smoking_amount', 'drinking', 'drinking_amount',
            'body_fat_percentage', 'muscle_mass', 'basal_metabolic_rate', 'bmi', 'short_term_goals', 'long_term_goals',
            'preferred_exercise_types', 'available_times'
        ]
        widgets = {
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.TextInput(attrs={'class': 'form-control'}),
            'medications': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'types': forms.Select(attrs={'class': 'form-control'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}),
            'goals': forms.TextInput(attrs={'class': 'form-control'}),
            'diet_habits': forms.Select(attrs={'class': 'form-control'}),
            'sleep_pattern': forms.Select(attrs={'class': 'form-control'}),
            'stress_level': forms.Select(attrs={'class': 'form-control'}),
            'smoking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smoking_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'drinking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'drinking_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'body_fat_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'muscle_mass': forms.NumberInput(attrs={'class': 'form-control'}),
            'basal_metabolic_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control'}),
            'short_term_goals': forms.TextInput(attrs={'class': 'form-control'}),
            'long_term_goals': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_exercise_types': forms.Select(attrs={'class': 'form-control'}),
            'available_times': forms.Select(attrs={'class': 'form-control'}),
        }
