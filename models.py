from django.db import models
from django_fsm import transition, FSMIntegerField, FSMField, transition
from django_fsm_log.decorators import fsm_log_by, fsm_log_description
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import pandas as pd
from django.contrib.contenttypes.models import ContentType
from multiselectfield import MultiSelectField

# Create your models here.

def get_default_attachment():
    # Provide the path to the default attachment
    return 'attachments/default_file.pdf'


User = get_user_model()

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    #forclosure = models.ForeignKey('Forclosure', on_delete=models.CASCADE, related_name='attachments')
    forclosure = models.ForeignKey('Forclosure', on_delete=models.CASCADE, related_name='attachments',blank=True, null=True)
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE, related_name='attachments',blank=True, null=True)
    generalcase = models.ForeignKey('Generalcase', on_delete=models.CASCADE, related_name='attachments',blank=True, null=True)
    #generalquery = models.ForeignKey('Generalquery', on_delete=models.CASCADE, related_name='attachments',blank=True, null=True)


class Forclosure(models.Model):
    STATE_CHOICES = (
        ('initiated', 'Initiated'),
        ('cancelled', 'Cancelled'),
        ('first_reviewed', 'First_reviewed'),
        ('resubmited', 'Resubmited'),
        ('assigned', 'Assigned'),
        ('rejected', 'Rejected'),
        ('reversed', 'Reversed'),
        ('approved', 'Approved'),
        ('authorise', 'Authorised'),        
    )

    REASON_CHOICES = (
        ('nira', 'Employer closed in URSB'),
        ('others', 'Others'),
       
    )

    state = FSMField(default='initiated', choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
   


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forclosures')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_forclosures', limit_choices_to={'groups__name': 'Supervisors'})
    next_action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='next_action_forclosures', blank=True, null=True, limit_choices_to={'groups__name': 'Assessors'})
    employer_name = models.CharField(max_length=130)
    nssf_no = models.CharField(max_length=130)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    #attachment = models.FileField(upload_to='attachments/', blank=False, null=False)
    #attachment = models.FileField(upload_to='attachments/', default=get_default_attachment)
    remark = models.TextField(blank=True)
    review_comment = models.TextField(blank=True)



    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source=['initiated','reversed','resubmited'], target='cancelled')
    def cancel(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='cancel', review_comment=review_comment)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source=['initiated','resubmited'], target='first_reviewed')
    def first_review(self,user,review_comment):        
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='first_review', review_comment=review_comment)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source=['assigned','first_reviewed'], target= 'approved')
    def approve(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='approve', review_comment=review_comment)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source=['initiated', 'assigned','resubmited','first_reviewed'], target='reversed')
    def reverse(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='reverse', review_comment=review_comment)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='reversed', target='resubmited')
    def resubmit(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='resubmit', review_comment=review_comment)
        #pass



    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source=['initiated', 'assigned','approved','first_reviewed'], target='rejected')
    def reject(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='reject', review_comment=review_comment)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='first_reviewed', target='assigned')
    def assign(self, user, next_action_user, review_comment):
        self.next_action_user = next_action_user
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='assign', review_comment=review_comment)
        #pass


    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='approved', target='authorised')
    def authorise(self,user,review_comment):
        self.review_comment = review_comment
        self.save()
        ForclosureLog.objects.create(model=self, user=user, action='authorise', review_comment=review_comment)
        #pass


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new instance (not yet saved to the database)
            self.updated_at = self.created_at
        super(Forclosure, self).save(*args, **kwargs)


class ForclosureLog(models.Model):
    # Define your model fields here
    model = models.ForeignKey(Forclosure, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forclosure_logs')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='forclosure_logs')
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')    
    review_comment = models.TextField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
  

class Employer(models.Model):
    party_role_id = models.IntegerField()
    nssf_no = models.CharField(max_length=255)
    employer_name = models.CharField(max_length=255)
    registry_dt = models.DateField(null=True, blank=True)
    party_role_type_descr = models.CharField(max_length=255)
    # Add other fields as needed

    def save(self, *args, **kwargs):
        if pd.isnull(self.registry_dt):
            self.registry_dt = None  # Set None instead of "NaT"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'employers'


class Engagement(models.Model):
    ACTIVITY_CHOICES = (
         ('account4noncompliance','Account for non-compliance'),
        ('member_reg', 'Member registration'),
        ('assessment', 'Assessment'),
        ('fl', 'Financial Literacy'),

        ('roadshow', 'Roadshow'),
        ('audit', 'Compliance Audit'),
        ('inspection', 'Inspection'),
        #('senstisation', 'Senstisation'),
        ('support', 'Support'),
        ('recovery', 'Collections recovery'),
        ('emp_reg', 'Employer registration'),
        #('mapping', 'Mapping'),
        ('suspe', 'Suspence clearence'),
        #('closure', 'Employer closure'),
        ('records', 'Update records'),
        ('paye_nssf', 'PAYE vs NSSF Reconciliation'),
        #('visit', 'Physical visit'),
        ('benefits', 'Benefits Verification'),
        ('zero_audit', 'Zero value audit'),
        ('legal', 'Sent to legal'),
        ('legacy', 'Legacy audit file closure'),
        ('no_deed', 'Full no deed recovery'),
        ('name_change', 'Employer name change'),
        
    )

    STATE_CHOICES = (
        ('recorded', 'Recorded'),
        ('forwarded', 'forwarded'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),        
    )


    state = FSMField(default='recorded', choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagements')
    employer_name = models.CharField(max_length=130)
    nssf_no = models.CharField(max_length=130)
    activity_done = MultiSelectField(choices=ACTIVITY_CHOICES, max_choices=11)
    action_date = models.DateField(null=True, blank=True)
    monthly_contributions = models.FloatField(null=True, blank=True)
    members = models.IntegerField(null=True, blank=True)

    engaged_person = models.CharField(max_length=130,blank=True, null=True)
    engaged_mobile = models.CharField(max_length=20, blank=True, null=True)  # New field for engaged mobile
    engaged_email = models.EmailField(blank=True, null=True)  # New field for engaged email


    #attachment = models.FileField(upload_to='attachments/', blank=False, null=False)
    #attachment = models.FileField(upload_to='attachments/', default=get_default_attachment)
    comment = models.TextField(blank=True)
    remark = models.TextField(blank=True)
    #next_action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='next_action_engagements', blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_engagements',blank=True, null=True)#, limit_choices_to={'groups__name': 'Supervisors'})
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_engagements')


    REASON_CHOICES = (
        ('inconsistent_funding', 'Inconsistent funding from government/donors'),
        ('covid19_effects', 'Covid-19 effects'),
        ('economic_strain', 'Economic strain and cash flow challenges'),
        ('employer_not_started', 'Employer was registered but hasn’t started operating'),
        ('unable_to_locate_employer', 'Inability to locate employer/briefcase company'),
        ('hard_to_reach_employer', 'Hard to reach employer (very far)'),
        ('high_employer_to_rm_ratio', 'High employer to RM ratio'),
        ('ignorance_of_nssf_law', 'Ignorance of the NSSF law'),
        ('informal_employer_closure', 'Informal employer closure'),
        ('informal_employments', 'Informal employments (casual laborers)'),
        ('lack_of_trust_in_nssf', 'Lack of trust in the NSSF brand'),
        ('non_payment_during_school_holidays', 'Non-payment during school holidays'),
        ('system_breakdown', 'Painful system experiences and breakdown/internet connectivity issues'),
        ('political_instability', 'Political instability'),
        ('political_interference', 'Political interference and restricted access to employer premises'),
        ('stubborn_employer', 'Stubborn and adamant employer'),
        ('unfavorable_registration_requirements', 'Unfavorable registration requirements for new members and employers'),
        ('occasional_delays', 'Occasional delays in remitting NSSF contributions'),
    )

    reason_for_non_compliance = models.CharField(max_length=50, choices=REASON_CHOICES, blank=True, null=True)

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='recorded', target='forwarded')
    def forward(self,user, reviewer):
        #self.remark = remark
        self.reviewer = reviewer
        self.save()
        EngagementLog.objects.create(model=self, user=user, action='forward')
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='recorded', target='cancelled')
    def cancel(self,user):
        #self.remark = remark
        self.save()
        EngagementLog.objects.create(model=self, user=user, action='cancel')
        #pass


    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='forwarded', target='rejected')
    def reject(self,user,remark):
        self.remark = remark
        self.save()
        EngagementLog.objects.create(model=self, user=user, action='reject', remark=remark)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='forwarded', target= 'approved')
    def approve(self,user,remark):
        self.remark = remark
        self.save()
        EngagementLog.objects.create(model=self, user=user, action='approve', remark=remark)
        #pass




class EngagementLog(models.Model):
    # Define your model fields here
    model = models.ForeignKey(Engagement, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagement_logs')  
    remark = models.TextField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    
   

class Generalcase(models.Model):

    STATE_CHOICES = (
        ('recorded', 'Recorded'),
        ('forwarded', 'forwarded'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),        
    )

    state = FSMField(default='recorded', choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generalcases')
    subject = models.CharField(max_length=130)
    action_date = models.DateTimeField()
    any_other_info = models.CharField(max_length=130)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_generalcases',blank=True, null=True)#, limit_choices_to={'groups__name': 'Supervisors'})
    #next_action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='next_action_generalcases', blank=True, null=True, limit_choices_to={'groups__name': 'Assessors'})    
    remark = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='recorded', target='forwarded')
    def forward(self,user, reviewer):
        #self.remark = remark
        self.reviewer = reviewer
        self.save()
        GeneralcaseLog.objects.create(model=self, user=user, action='forward')
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='recorded', target='cancelled')
    def cancel(self,user):
        #self.remark = remark
        self.save()
        GeneralcaseLog.objects.create(model=self, user=user, action='cancel')
        #pass


    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='forwarded', target='rejected')
    def reject(self,user,remark):
        self.remark = remark
        self.save()
        GeneralcaseLog.objects.create(model=self, user=user, action='reject', remark=remark)
        #pass

    @fsm_log_by
    @fsm_log_description
    @transition(field=state, source='forwarded', target= 'approved')
    def approve(self,user,remark):
        self.remark = remark
        self.save()
        GeneralcaseLog.objects.create(model=self, user=user, action='approve', remark=remark)
        #pass

class GeneralcaseLog(models.Model):
    # Define your model fields here
    model = models.ForeignKey(Generalcase, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generalcase_logs')  
    remark = models.TextField()
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True)