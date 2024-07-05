from django.shortcuts import redirect


class ProfileRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "profile"):
            return redirect("profiles:profile_new")
        return super().dispatch(request, *args, **kwargs)
