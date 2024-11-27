from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _

class UserProfileForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Name')}),
        label=""
    )

    lastName = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Last Name')}),
        label=""
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'email'}),
        label=""
    )
    
    password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Password')}),
        label=""
    )

    confirm_password = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Confirm your password')}),
        label=""
    )
    
    class Meta:
        model = User
        fields = ['name','lastName', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class EditAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','lastName']

    def __init__(self, *args, **kwargs):
        super(EditAccount,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})