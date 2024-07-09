from django.shortcuts import redirect
from django.contrib import messages


class ProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "profile"):
            messages.error(
                request, "You must create a profile first to access this feature!"
            )
            return redirect("profiles:profile_new")
        return super().dispatch(request, *args, **kwargs)
