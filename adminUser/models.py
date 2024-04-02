from django.db import models

# Create your models here.
class UserCredentials(models.Model):
    application_idU = models.CharField(primary_key = True, max_length = 20)
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    middle_name = models.CharField(max_length=50, null = True, blank = True)
    course_applied = models.CharField(max_length=50, null = True, blank = True)
    password = models.CharField(max_length=50, null = True, blank = True)
    
class AddResult(models.Model):
    application_idR = models.CharField(max_length = 20, null = True, blank = True)
    verbal_Comprehension = models.CharField(max_length = 50, null = True, blank = True)
    verbal_Reasoning = models.CharField(max_length = 50, null = True, blank = True)
    figural_Reasoning = models.CharField(max_length = 50, null = True, blank = True)
    qualitative_Reasoning = models.CharField(max_length = 50, null = True, blank = True)
    status = models.CharField(max_length = 50, null = True, blank = True)
    