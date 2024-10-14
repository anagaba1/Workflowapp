from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Forclosure, Employer, Engagement, Generalcase, Rating, Getfeedback, Feedback3,Outbound, Deeds, Branch,TeamLeader
from django.forms import ClearableFileInput

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
        
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
    attachments = MultipleFileField(required=True)

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
    #attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    attachments = MultipleFileField(required=False)

    class Meta:
        model = Engagement
        fields = ['nssf_no', 'employer_name', 'main_activity','activity_done', 'reason_for_non_compliance','comment', 'action_date', 'reviewer']

    activity_done = forms.MultipleChoiceField(choices=Engagement.ACTIVITY_CHOICES, widget=forms.SelectMultiple)
    comment = forms.CharField(widget=forms.Textarea)
    

class EngagementSearchForm(forms.Form):
    nssf_no = forms.CharField(label='NSSF No', max_length=130)


class GeneralcaseForm(forms.ModelForm):
    action_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    #attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    attachments = MultipleFileField(required=False)
    class Meta:
        model = Generalcase
        fields = ['subject', 'any_other_info', 'comment', 'action_date', 'reviewer']

    comment = forms.CharField(widget=forms.Textarea)



class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']


class GetfeedbackForm(forms.ModelForm):
    class Meta:
        model = Getfeedback
        fields = [
            'fcr_resolved',
            'nps_rating',
            'ces_easy',
            'overall_satisfaction',
            'additional_comments',
        ]

    fcr_resolved = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    nps_rating = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 10}),
    )
    ces_easy = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    overall_satisfaction = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    additional_comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))



class FeedbackForm3(forms.ModelForm):
    class Meta:
        model = Feedback3
        fields = ['rating']

class DeedsForm(forms.ModelForm):
    
    class Meta:
        model = Deeds
        #fields = '__all__'
        fields = [  # List all fields except `user`
            'nssf_no',
            'employer_name',
            'From_Date',
            'To_Date',
            'First_Installment_Date',
            'Second_Installment_Date',
            'Branch',
            'Deed_source',
            'Legacy_status',
            'Signed_Deed',
            'team_leader',
        # other fields
        ]
        widgets = {
            'Deed_source': forms.Select(choices=Deeds.Source),
            'From_Date': forms.DateInput(format='%Y-%m-%d'),
            'To_Date': forms.DateInput(format='%Y-%m-%d'),
            'First_Installment_Date': forms.DateInput(format='%Y-%m-%d'),
            'Second_Installment_Date': forms.DateInput(format='%Y-%m-%d'),
        }
        Branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        empty_label="Select Branch",
        widget=forms.Select(attrs={'id':'branch_id','class': 'form-control'})
    ),
      
        team_leader = forms.ModelChoiceField(
        queryset=TeamLeader.objects.all(),
        empty_label="Select Team Leader",
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        

class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = '__all__'
        widgets = {
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'nssf_number': forms.TextInput(attrs={'class': 'form-control'}),
            'served_by': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select', 'readonly': True}),
            'nps': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'fcr_resolved': forms.Select(attrs={'class': 'form-select'}),
            'ces_easy': forms.Select(attrs={'class': 'form-select'}),
            'overall_satisfaction': forms.Select(attrs={'class': 'form-select'}),
            'additional_comments': forms.Textarea(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'reason_for_visit': forms.Select(attrs={'class': 'form-select'}),
            'verbatim_rating': forms.Textarea(attrs={'class': 'form-control'}),
            'front_office_reasons': forms.Select(attrs={'class': 'form-select'}),
            'back_office_reasons': forms.Select(attrs={'class': 'form-select'}),
            'greeting_and_enthusiasm': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20'}),
            'emotional_connection': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '25'}),
            'resolution_and_professionalism': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '35'}),
            'hold_procedure': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '20'}),
            'call_closure': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'zero_rated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OutboundForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].disabled = True

    