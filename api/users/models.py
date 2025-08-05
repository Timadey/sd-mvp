from django.db import models
from django.contrib.auth.models import AbstractUser

from api.core.choices import ROLE_CHOICES
from api.core.validators import PhoneNumberValidator
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)

class CandidateProfile(models.Model):
    phone_validator = PhoneNumberValidator()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_image_url = models.ImageField(upload_to="profile_image", null=True, blank=True)
    phone_number = models.CharField("phone number", max_length=12, null=True, blank=True, validators=[phone_validator])
    organisation = models.CharField("organisation", max_length=100, null=True, blank=True)

