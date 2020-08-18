from django.db import models
from requestpage.enums import RequestType, Status, State
from phonenumber_field.modelfields import PhoneNumberField

class Request(models.Model):

    Request_Choice = [(i.value, i.value) for i in RequestType]
    Status_Choice = [(i.value, i.value) for i in Status]
    State_Choice = [(i.value, i.value) for i in State]

    request_type = models.CharField(max_length=255, choices=Request_Choice)
    request_desc = models.CharField(max_length=100)
    request_date =  models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=Status_Choice )
    state = models.CharField(max_length=255, choices=State_Choice)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_number = PhoneNumberField(unique=True)
