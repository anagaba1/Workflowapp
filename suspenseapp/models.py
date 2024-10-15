from django.db import models

# Create your models here.

class Suspense(models.Model):
    member_id = models.CharField(max_length=255, null=True, blank=True)
    member_name = models.CharField(max_length=255, null=True, blank=True)
    member_identificat_val = models.CharField(max_length=255, null=True, blank=True)
    submitted_file_name = models.CharField(max_length=255, null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    init_member_suspense_contr = models.FloatField(null=True, blank=True)
    ident_member_suspense_contr = models.FloatField(null=True, blank=True)
    cur_member_suspense_contr = models.FloatField(null=True, blank=True)
    init_interest_suspense_amount = models.FloatField(null=True, blank=True)
    cur_interest_suspense_amount = models.FloatField(null=True, blank=True)
    ident_interest_suspense = models.FloatField(null=True, blank=True)
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    employer_identificat_val = models.CharField(max_length=255, null=True, blank=True)
    trn = models.CharField(max_length=255, null=True, blank=True)
    receipt_number = models.CharField(max_length=255, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    statutory_ins_detail_id = models.FloatField(null=True, blank=True)
    employerno = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.member_name