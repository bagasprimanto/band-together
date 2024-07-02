from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    Override the UserCreationForm to point to the CustomUserModel
    """

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    """
    Override the UserChangeForm to point to the CustomUserModel
    """

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )
