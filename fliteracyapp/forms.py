from django import forms
from .models import Fl_event, Fl_attendants


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

class Fl_eventForm(forms.ModelForm):
    #attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    attachments = MultipleFileField(required=False)
    class Meta:
        model = Fl_event
        fields = ['id','event_name', 'event_date', 'employer', 'employer_number','fl_advisors_involved', 'contact_person', 'designation',
       'contact_phone', 'contact_email', 'program', 'delivery_mode','on_spot_feedback']



class FlAttendantsForm(forms.ModelForm):
    class Meta:
        model = Fl_attendants
        fields = ['event_name', 'event_date']



class SearchMemberForm(forms.Form):
    q = forms.CharField(label='Search by name', max_length=100)

class RegisterAttendantForm(forms.Form):
    name = forms.CharField(max_length=100)
    #nssf_number = forms.CharField(max_length=20)
    # Add other fields as needed