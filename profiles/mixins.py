from django.shortcuts import redirect
from django.contrib import messages


class ProfileRequiredMixin:
    """
    Mixin to ensure that the user has a profile before allowing access to the view.
    If the user does not have a profile, they are redirected to the profile creation page.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method to check if the user has a profile.
        If not, display an error message and redirect them to the profile creation page.
        """

        # Check if the user has a 'profile' attribute (i.e., if a profile is associated with the user)
        if not hasattr(request.user, "profile"):

            # If no profile exists, display an error message to the user
            messages.error(
                request, "You must create a profile first to access this feature!"
            )

            # Redirect the user to the profile creation page
            return redirect("profiles:profile_new")

        # If the user has a profile, proceed with the normal dispatch process
        return super().dispatch(request, *args, **kwargs)
