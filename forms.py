from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Forclosure, Employer, Engagement, Generalcase
from django.forms import ClearableFileInput


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class ForclosureForm(forms.ModelForm):
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Forclosure
        fields = ['id','nssf_no','reason','remark','reviewer', 'attachments']

    def clean_nssf_no(self):
        nssf_no = self.cleaned_data.get('nssf_no')
        employer = Employer.objects.filter(nssf_no=nssf_no).first()
        if not employer:
            raise forms.ValidationError('Invalid NSSF number')
        return nssf_no

    def save(self, commit=True):
        instance = super().save(commit=False)
        employer = Employer.objects.get(nssf_no=self.cleaned_data['nssf_no'])
        instance.employer_name = employer.employer_name
        if commit:
            instance.save()
        return instance


class EngagementForm(forms.ModelForm):
    action_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Engagement
        fields = ['nssf_no', 'employer_name', 'activity_done','monthly_contributions','members', 'comment', 'action_date', 'reviewer','engaged_person','engaged_mobile','engaged_email']

    activity_done = forms.MultipleChoiceField(choices=Engagement.ACTIVITY_CHOICES, widget=forms.SelectMultiple)
    comment = forms.CharField(widget=forms.Textarea)
    

class EngagementSearchForm(forms.Form):
    nssf_no = forms.CharField(label='NSSF No', max_length=130)


class GeneralcaseForm(forms.ModelForm):
    action_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    class Meta:
        model = Generalcase
        fields = ['subject', 'any_other_info', 'comment', 'action_date', 'reviewer']

    comment = forms.CharField(widget=forms.Textarea)

class EmployerSearchForm(forms.Form):
    employer_name = forms.CharField(label='NAME', max_length=130)

class SearchEmployerForm(forms.Form):
    q = forms.CharField(label='Search by employer name', max_length=100)