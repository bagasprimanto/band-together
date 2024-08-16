import zoneinfo

from django.utils import timezone

from .models import Profile


class TimezoneMiddleware:
    """
    Middleware to set the time zone based on the authenticated user's profile.

    If the user is authenticated, it attempts to set the time zone to the user's
    preferred time zone stored in their profile.

    If the user is not authenticated
    or if the profile does not exist, it deactivates the time zone, which means
    Django will use the default time zone.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the provided get_response function.
        This function is called later to pass the request to the next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        The main logic of the middleware is executed here. It handles each request.

        1. If the user is authenticated, it attempts to retrieve the user's profile.
        2. If the profile exists, the middleware activates the time zone specified in the profile.
        3. If the profile does not exist, or if the user is not authenticated, the middleware deactivates time zone handling.
        4. Finally, it passes the request to the next middleware or view.

        :param request: The HTTP request object.
        :return: The response after passing through the middleware.
        """

        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Attempt to get the user's profile
                profile = request.user.profile
            except Profile.DoesNotExist:
                # If the profile does not exist, deactivate the time zone
                timezone.deactivate()
            else:
                # Activate the time zone specified in the user's profile
                timezone.activate(zoneinfo.ZoneInfo(profile.timezone))
        else:
            # If the user is not authenticated, deactivate the time zone
            timezone.deactivate()

        # Pass the request to the next middleware or view
        return self.get_response(request)
