from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import ProfileRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView
from django.contrib import messages
from .models import Bookmark
from profiles.models import Profile
from advertisements.models import Advertisement
from openmics.models import OpenMic
from .mixins import BookmarkMixin
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.contrib.messages import get_messages
from django.db.models import OuterRef, Subquery


class CreateDetailBookmarkView(LoginRequiredMixin, ProfileRequiredMixin, View):
    """
    View to handle the creation of a bookmark for a specific object in detail views (e.g. Advertisement Detail, Open Mic Detail).
    Requires the user to be logged in and to have a profile.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create or confirm a bookmark on a specific object.
        Only processes HTMX requests.
        """
        # Check if the request is an HTMX request by looking for the "HX-Request" header.
        # Else, return error 400
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # Retrieve the app label, model name, and object ID from the URL parameters as
        # they are required to create a bookmark using ContentType framework
        app_label = kwargs.get("app_label")
        model_name = kwargs.get("model_name")
        object_id = kwargs.get("object_id")

        # Get the ContentType for the specified app label and model name.
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )

        # Retrieve the specific object (model instance) based on the content type and object ID.
        model = content_type.get_object_for_this_type(id=object_id)

        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=request.user)

        # Attempt to retrieve an existing bookmark or create a new one if it doesn't exist.
        bookmark, created = Bookmark.objects.get_or_create(
            profile=profile, content_type=content_type, object_id=object_id
        )

        # Display a success message if the bookmark was created, otherwise inform the user it already exists.
        if created:
            messages.success(request, "Successfully bookmarked!")
        else:
            messages.info(request, "Already bookmarked.")

        # Prepare the context for rendering the bookmark button.
        context = {
            "is_bookmarked": True,  # Indicates that the item is bookmarked.
            "bookmark": bookmark,  # The bookmark object.
            "object": model,  # The model instance being bookmarked.
            "messages": get_messages(
                request
            ),  # Any messages to be displayed to the user.
        }

        # Render the bookmark button template with the updated context.
        html = render_to_string(
            "bookmarks/bookmark_button_detail.html", context, request=request
        )

        # Return the rendered HTML with a 200 OK status.
        return HttpResponse(html, status=200)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests with a 405 Method Not Allowed response.
        This view is intended for POST requests only.
        """
        return render(request, "405.html", status=405)


class DeleteDetailBookmarkView(LoginRequiredMixin, View):
    """
    View to handle the deletion of a bookmark for a specific object in detail views.
    Requires the user to be logged in.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to delete a bookmark on a specific object.
        Only processes HTMX requests.
        """

        # Check if the request is an HTMX request by looking for the "HX-Request" header.
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # Retrieve the bookmark ID from the URL parameters.
        bookmark_id = kwargs.get("bookmark_id")

        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=request.user)

        try:
            # Attempt to retrieve the bookmark for the current user's profile.
            bookmark = get_object_or_404(Bookmark, id=bookmark_id, profile=profile)

            # Retrieve the model instance associated with the bookmark before deletion.
            model = bookmark.content_object

            # Delete the bookmark.
            bookmark.delete()

            # Add a success message to the context indicating the bookmark was removed.
            messages.success(request, "Successfully removed bookmark!")

            # Prepare the context for rendering the bookmark button after deletion.
            context = {
                "is_bookmarked": False,  # Indicates that the item is no longer bookmarked.
                "object": model,  # The model instance that was bookmarked.
                "messages": get_messages(
                    request
                ),  # Any messages to be displayed to the user.
            }

            # Render the bookmark button template with the updated context.
            html = render_to_string(
                "bookmarks/bookmark_button_detail.html", context, request=request
            )

            # Return the rendered HTML with a 200 OK status.
            return HttpResponse(html, status=200)

        except Http404:
            # If the bookmark is not found, add an error message and return a 404 response.
            messages.error(request, "Bookmark not found.")
            return HttpResponse(status=404)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests with a 405 Method Not Allowed response.
        This view is intended for POST requests only.
        """
        return render(request, "405.html", status=405)


class CreateListBookmarkView(LoginRequiredMixin, ProfileRequiredMixin, View):
    """
    View to handle the creation of a bookmark for a specific object in list views.
    Requires the user to be logged in and to have a profile.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create or confirm a bookmark on a specific object.
        Only processes HTMX requests.
        """
        # Check if the request is an HTMX request by looking for the "HX-Request" header.
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # Retrieve the app label, model name, and object ID from the URL parameters as
        # they are required to create a bookmark using ContentType framework
        app_label = kwargs.get("app_label")
        model_name = kwargs.get("model_name")
        object_id = kwargs.get("object_id")

        # Get the ContentType for the specified app label and model name.
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )

        # Retrieve the specific object (model instance) based on the content type and object ID.
        model = content_type.get_object_for_this_type(id=object_id)

        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=request.user)

        # Attempt to retrieve an existing bookmark or create a new one if it doesn't exist.
        bookmark, created = Bookmark.objects.get_or_create(
            profile=profile, content_type=content_type, object_id=object_id
        )

        # Display a success message if the bookmark was created, otherwise inform the user it already exists.
        if created:
            messages.success(request, "Successfully bookmarked!")
        else:
            messages.info(request, "Already bookmarked.")

        # Update the bookmarked_objects context with the newly created or existing bookmark.
        context = {
            "object": model,  # The model instance being bookmarked.
            "bookmarked_objects": {
                bookmark.object_id: bookmark
            },  # Add the bookmark to the context.
            "messages": get_messages(
                request
            ),  # Any messages to be displayed to the user.
        }

        # Render the bookmark button template for list views with the updated context.
        html = render_to_string(
            "bookmarks/bookmark_button_list.html", context, request=request
        )

        # Return the rendered HTML with a 200 OK status.
        return HttpResponse(html)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests with a 405 Method Not Allowed response.
        This view is intended for POST requests only.
        """
        return render(request, "405.html", status=405)


class DeleteListBookmarkView(LoginRequiredMixin, View):
    """
    View to handle the deletion of a bookmark for a specific object in list views (e.g. Advertisement lists, Open Mics list).
    Requires the user to be logged in.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to delete a bookmark on a specific object.
        Only processes HTMX requests.
        """
        # Check if the request is an HTMX request by looking for the "HX-Request" header,
        # else return error 400
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # Retrieve the bookmark ID from the URL parameters.
        bookmark_id = kwargs.get("bookmark_id")

        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=request.user)

        try:
            # Attempt to retrieve the bookmark for the current user's profile.
            bookmark = get_object_or_404(Bookmark, id=bookmark_id, profile=profile)

            # Retrieve the model instance associated with the bookmark before deletion.
            model = bookmark.content_object

            # Delete the bookmark.
            bookmark.delete()

            # Add a success message to the context indicating the bookmark was removed.
            messages.success(request, "Successfully removed bookmark!")

            # Update the bookmarked_objects context to reflect that the object is no longer bookmarked.
            context = {
                "object": model,  # The model instance that was bookmarked.
                "bookmarked_objects": {},  # Clear the bookmarked_objects context.
                "messages": get_messages(
                    request
                ),  # Any messages to be displayed to the user.
            }

            # Render the bookmark button template for list views with the updated context.
            html = render_to_string(
                "bookmarks/bookmark_button_list.html", context, request=request
            )

            # Return the rendered HTML with a 200 OK status.
            return HttpResponse(html, status=200)

        except Http404:
            # If the bookmark is not found, add an error message and return a 404 response.
            messages.error(request, "Bookmark not found.")
            return HttpResponse(status=404)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests with a 405 Method Not Allowed response.
        This view is intended for POST requests only.
        """
        return render(request, "405.html", status=405)


class BookmarkProfileListView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    """
    View to display a list of profiles that the logged-in user has bookmarked.
    Requires the user to be logged in and to have a profile.
    """

    # The model that this view will operate on.
    model = Profile

    # The template used to render the bookmarked profiles list page.
    template_name = "bookmarks/bookmark_profile_list.html"

    # The name of the context variable that will contain the list of profiles in the template.
    context_object_name = "profiles"

    def get_queryset(self):
        """
        Retrieves the queryset of profiles that the current user has bookmarked.
        The queryset is annotated with the created date of the bookmark and ordered by it.
        """
        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=self.request.user)
        # Get the ContentType for the Profile model.
        profile_content_type = ContentType.objects.get_for_model(Profile)

        # Subquery to fetch the created date of the bookmark associated with each profile.
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile, content_type=profile_content_type, object_id=OuterRef("pk")
        ).values("created")[:1]

        # Annotate the Profile queryset with the bookmark created date and order by it
        return (
            Profile.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=profile_content_type
                ).values(
                    "object_id"
                )  # Filter profiles based on the bookmarked object IDs.
            )
            .annotate(
                bookmark_created=Subquery(bookmark_subquery)
            )  # Annotate with the bookmark created date.
            .order_by(
                "-bookmark_created"
            )  # Order by the bookmark created date, descending.
        )

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including the count of bookmarked profiles.
        """
        context = super().get_context_data(**kwargs)

        # Add the count of bookmarked profiles to the context.
        context["profiles_count"] = self.get_queryset().count()
        return context


class BookmarkAdvertisementListView(
    LoginRequiredMixin, ProfileRequiredMixin, BookmarkMixin, ListView
):
    """
    View to display a list of advertisements that the logged-in user has bookmarked.
    Requires the user to be logged in and to have a profile.
    Inherits from BookmarkMixin to provide additional bookmark-related context to display Bookmark buttons.
    """

    # The model that this view will operate on.
    model = Advertisement

    # The template used to render the bookmarked advertisements list page.
    template_name = "bookmarks/bookmark_advertisement_list.html"

    # The name of the context variable that will contain the list of advertisements in the template.
    context_object_name = "ads"

    def get_queryset(self):
        """
        Retrieves the queryset of advertisements that the current user has bookmarked.
        The queryset is annotated with the created date of the bookmark and ordered by it.
        """
        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=self.request.user)

        # Get the ContentType for the Advertisement model.
        advertisement_content_type = ContentType.objects.get_for_model(Advertisement)

        # Subquery to fetch the created date of the bookmark associated with each advertisement.
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile,
            content_type=advertisement_content_type,
            object_id=OuterRef("pk"),
        ).values("created")[:1]

        # Annotate the Advertisement queryset with the bookmark created date and order by it.
        return (
            Advertisement.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=advertisement_content_type
                ).values(
                    "object_id"
                )  # Filter advertisements based on the bookmarked object IDs.
            )
            .annotate(
                bookmark_created=Subquery(bookmark_subquery)
            )  # Annotate with the bookmark created date.
            .order_by(
                "-bookmark_created"
            )  # Order by the bookmark created date, descending.
        )

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including the count of bookmarked advertisements.
        Also adds bookmark-related context for the list of advertisements.
        """
        # Get the base context from the superclass.
        context = super().get_context_data(**kwargs)

        # Retrieve the queryset of bookmarked advertisements.
        queryset = self.get_queryset()

        # Add the count of bookmarked advertisements to the context.
        context["ads_count"] = queryset.count()

        # Add bookmark context for the advertisements (list of objects).
        # Returns a group of bookmarked advertisements to mark which advertisements have been bookmarked,
        # required for displaying the Bookmark buttons
        ads_bookmark_context = self.get_bookmark_context(self.request.user, queryset)
        context.update(ads_bookmark_context)

        return context


class BookmarkOpenMicListView(
    LoginRequiredMixin, ProfileRequiredMixin, BookmarkMixin, ListView
):
    """
    View to display a list of OpenMic events that the logged-in user has bookmarked.
    Requires the user to be logged in and to have a profile.
    Inherits from BookmarkMixin to provide additional bookmark-related context to display Bookmark buttons.
    """

    # The model that this view will operate on.
    model = OpenMic

    # The template used to render the bookmarked OpenMic events list page.
    template_name = "bookmarks/bookmark_openmic_list.html"

    # The name of the context variable that will contain the list of OpenMic events in the template.
    context_object_name = "openmics"

    def get_queryset(self):
        """
        Retrieves the queryset of OpenMic events that the current user has bookmarked.
        The queryset is annotated with the created date of the bookmark and ordered by it.
        """
        # Get the current user's profile.
        profile = get_object_or_404(Profile, user=self.request.user)

        # Get the ContentType for the OpenMic model.
        openmic_content_type = ContentType.objects.get_for_model(OpenMic)

        # Subquery to fetch the created date of the bookmark associated with each OpenMic.
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile,
            content_type=openmic_content_type,
            object_id=OuterRef("pk"),
        ).values("created")[:1]

        # Annotate the OpenMic queryset with the bookmark created date and order by it.
        return (
            OpenMic.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=openmic_content_type
                ).values(
                    "object_id"
                )  # Filter OpenMics based on the bookmarked object IDs.
            )
            .annotate(
                bookmark_created=Subquery(bookmark_subquery)
            )  # Annotate with the bookmark created date.
            .order_by(
                "-bookmark_created"
            )  # Order by the bookmark created date, descending.
        )

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including the count of bookmarked OpenMic events.
        Also adds bookmark-related context for the list of OpenMic events.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the queryset of bookmarked OpenMic events.
        queryset = self.get_queryset()

        # Add the count of bookmarked OpenMic events to the context.
        context["openmics_count"] = queryset.count()

        # Add bookmark context for the open mics (list of objects).
        # Returns a group of bookmarked open mics to mark which open mics have been bookmarked,
        # required for displaying the Bookmark buttons
        ads_bookmark_context = self.get_bookmark_context(self.request.user, queryset)
        context.update(ads_bookmark_context)

        return context
