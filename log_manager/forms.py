from django import forms
from .models import Employee

class EmployeeIDForm(forms.Form):
    unique_id = forms.CharField(
        label="Employee ID",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 123456',
            'autofocus': 'autofocus'
        })
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Enter Password'}))




class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['picture', 'name', 'phone', 'email', 'department', 'type']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. Collins Effah'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 08012345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. mail@example.com'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'picture': 'Picture',
            'name': 'Name',
            'phone': 'Contact Number',
            'email': 'Email',
            'department': 'Department',
            'type':'Type'
        }
