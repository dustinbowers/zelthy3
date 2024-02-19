from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from zelthy.core.storage_utils import ZFileField
from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.dynamic_models.models import DynamicModelBase


AGE_CHOICES = [
    ('12-17', '12-17'),
    ('18-59', '18-59'),
    ('>=60', '>=60'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

CONTACT_PERSON_CHOICES = [
    ('self', 'Self'),
    ('spouse', 'Spouse'),
    ('daughter', 'Daughter'),
    ('daughter-in-law', 'Daughter-in-law'),
    ('son', 'Son'),
    ('son-in-law', 'Son-in-law'),
    ('nephew', 'Nephew'),
    ('niece', 'Niece'),
    ('granddaughter', 'Granddaughter'),
    ('grandson', 'Grandson'),
    ('others', 'Others'),
]

YEARS_SINCE_DIAGNOSIS_CHOICES = [
    ('<=1 year', '<=1 year'),
    ('2-5 years', '2-5 years'),
    ('6-10 years', '6-10 years'),
    ('>10 years', '>10 years'),
]

DISCONTINUATION_REASON_CHOICES = [
    ('dr_decision', "Dr's decision to end treatment"),
    ('patient_decision', "Patient's decision to end treatment"),
    ('deceased', 'Deceased'),
    ('change_medication', 'Change of medication'),
    ('change_therapy', 'Change of therapy'),
    ('medication_side_effect', 'Medication side effect'),
    ('no_response', 'No response to medication'),
    ('financial_problems', 'Patient financial problems'),
    ('disease_progression', 'Disease progression'),
    ('uncontactable', 'Uncontactable'),
    ('ineligibility_location', 'Program ineligibility (Location)'),
    ('ineligibility_age', 'Program ineligibility (Age)'),
    ('ineligibility_employment', 'Program ineligibility (Employment)'),
    ('ineligibility_citizenship', 'Program ineligibility (Citizenship)'),
    ('poor_service', 'Poor service/quality of program'),
    ('opt_out', 'Opt-out from PSP'),
]


class AbstractPatient(DynamicModelBase):
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    dob = models.DateField('Date of Birth', null=True, blank=True)
    age = models.CharField('Age', max_length=10, choices=AGE_CHOICES, null=True, blank=True)
    gender = models.CharField('Gender', max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    contact_number = PhoneNumberField('Primary Phone', null=True, blank=True)
    consent = models.BooleanField('Consent', default=False)
    user = ZForeignKey(AppUserModel, related_name='patient', on_delete=models.CASCADE, null=True)

    class Meta(DynamicModelBase.Meta):
        abstract = True

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ({self.id+10000})'


class AbstractPatientProgram(DynamicModelBase):
    '''
    Any FK relation has to be established in the app model.
    for example, Relation between Patient and Patient Program.
    '''
    consent = models.BooleanField('Consent', default=False)
    consent_date = models.DateField('Consent Date', null=True, blank=True)
    consent_file =  ZFileField(upload_to='attachments/', null=True, blank=True)
    contact_person = models.CharField('Contact Person', max_length=20, choices=CONTACT_PERSON_CHOICES)
    contact_person_text = models.CharField('Contact Person Text', null=True, blank=True)
    years_since_diagnosis = models.CharField('Years of Diagnosis', max_length=20, choices=YEARS_SINCE_DIAGNOSIS_CHOICES)
    hospital_text = models.CharField('Hospital Text', null=True, blank=True)
    training_date = models.DateField('Training Date', null=True, blank=True)
    training_type = models.CharField('Training Type', null=True, blank=True)
    discontinuation_date = models.DateField('Discontinuation Date', null=True, blank=True)
    discontinuation_reason = models.CharField('Discontinuation Reason', max_length=20, choices=DISCONTINUATION_REASON_CHOICES, null=True, blank=True)

    class Meta(DynamicModelBase.Meta):
        abstract = True

    def __str__(self):
        return f'Patient Program ID: {self.id + 10000}'