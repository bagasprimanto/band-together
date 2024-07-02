from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Create a CustomUser if there is a need to expand the data included in User
    """

    pass
