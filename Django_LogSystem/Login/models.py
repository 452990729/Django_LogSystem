from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LoginUser(User):
    info_right = models.CharField(max_length=32,default='nobody')
