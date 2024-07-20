from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
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
    def post(self, request, *args, **kwargs):
        app_label = kwargs.get("app_label")
        model_name = kwargs.get("model_name")
        object_id = kwargs.get("object_id")
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        model = content_type.get_object_for_this_type(id=object_id)
        profile = get_object_or_404(Profile, user=request.user)
        bookmark, created = Bookmark.objects.get_or_create(
            profile=profile, content_type=content_type, object_id=object_id
        )

        if created:
            messages.success(request, "Successfully bookmarked!")
        else:
            messages.info(request, "Already bookmarked.")

        if request.headers.get("HX-Request"):
            context = {
                "is_bookmarked": True,
                "bookmark": bookmark,
                "object": model,
                "messages": get_messages(request),
            }
            html = render_to_string(
                "bookmarks/bookmark_button_detail.html", context, request=request
            )

            return HttpResponse(html)

        return redirect(model.get_absolute_url())


class DeleteDetailBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        bookmark_id = kwargs.get("bookmark_id")
        profile = get_object_or_404(Profile, user=request.user)

        try:
            bookmark = get_object_or_404(Bookmark, id=bookmark_id, profile=profile)
            model = bookmark.content_object
            bookmark.delete()
            messages.success(request, "Successfully removed bookmark!")

            if request.headers.get("HX-Request"):
                context = {
                    "is_bookmarked": False,
                    "object": model,
                    "messages": get_messages(request),
                }
                html = render_to_string(
                    "bookmarks/bookmark_button_detail.html", context, request=request
                )

                return HttpResponse(html)

        except Http404:
            messages.error(request, "Bookmark not found.")

            if request.headers.get("HX-Request"):
                context = {
                    "is_bookmarked": False,
                    "object": None,
                    "messages": get_messages(request),
                }
                html = render_to_string(
                    "bookmarks/bookmark_button_detail.html", context, request=request
                )
                return HttpResponse(html)

        return redirect(model.get_absolute_url())


class CreateListBookmarkView(LoginRequiredMixin, ProfileRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        app_label = kwargs.get("app_label")
        model_name = kwargs.get("model_name")
        object_id = kwargs.get("object_id")
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        model = content_type.get_object_for_this_type(id=object_id)
        profile = get_object_or_404(Profile, user=request.user)
        bookmark, created = Bookmark.objects.get_or_create(
            profile=profile, content_type=content_type, object_id=object_id
        )

        if created:
            messages.success(request, "Successfully bookmarked!")
        else:
            messages.info(request, "Already bookmarked.")

        if request.headers.get("HX-Request"):
            # Update the bookmarked_objects context
            context = {
                "object": model,
                "bookmarked_objects": {bookmark.object_id: bookmark},
                "messages": get_messages(request),
            }

            html = render_to_string(
                "bookmarks/bookmark_button_list.html", context, request=request
            )
            return HttpResponse(html)

        return redirect(model.get_absolute_url())


class DeleteListBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        bookmark_id = kwargs.get("bookmark_id")
        profile = get_object_or_404(Profile, user=request.user)

        try:
            bookmark = get_object_or_404(Bookmark, id=bookmark_id, profile=profile)
            model = bookmark.content_object
            bookmark.delete()
            messages.success(request, "Successfully removed bookmark!")

            if request.headers.get("HX-Request"):
                # Update the bookmarked_objects context
                context = {
                    "object": model,
                    "bookmarked_objects": {},
                    "messages": get_messages(request),
                }
                html = render_to_string(
                    "bookmarks/bookmark_button_list.html", context, request=request
                )
                return HttpResponse(html)

        except Http404:
            messages.error(request, "Bookmark not found.")

            if request.headers.get("HX-Request"):
                context = {
                    "object": None,
                    "bookmarked_objects": {},
                    "messages": get_messages(request),
                }
                html = render_to_string(
                    "bookmarks/bookmark_button_list.html", context, request=request
                )
                return HttpResponse(html)

        return redirect(model.get_absolute_url())


class BookmarkProfileListView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Profile
    template_name = "bookmarks/bookmark_profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        profile_content_type = ContentType.objects.get_for_model(Profile)

        # Subquery to fetch the created date of the bookmark
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile, content_type=profile_content_type, object_id=OuterRef("pk")
        ).values("created")[:1]

        # Annotate the Profile queryset with the bookmark created date and order by it
        return (
            Profile.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=profile_content_type
                ).values("object_id")
            )
            .annotate(bookmark_created=Subquery(bookmark_subquery))
            .order_by("-bookmark_created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles_count"] = self.get_queryset().count()
        return context


class BookmarkAdvertisementListView(
    LoginRequiredMixin, ProfileRequiredMixin, BookmarkMixin, ListView
):
    model = Advertisement
    template_name = "bookmarks/bookmark_advertisement_list.html"
    context_object_name = "ads"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        advertisement_content_type = ContentType.objects.get_for_model(Advertisement)

        # Subquery to fetch the created date of the bookmark
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile,
            content_type=advertisement_content_type,
            object_id=OuterRef("pk"),
        ).values("created")[:1]

        # Annotate the Advertisement queryset with the bookmark created date and order by it
        return (
            Advertisement.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=advertisement_content_type
                ).values("object_id")
            )
            .annotate(bookmark_created=Subquery(bookmark_subquery))
            .order_by("-bookmark_created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["ads_count"] = queryset.count()

        # Add bookmark context for the ads (list of objects)
        ads_bookmark_context = self.get_bookmark_context(self.request.user, queryset)
        context.update(ads_bookmark_context)

        return context


class BookmarkOpenMicListView(
    LoginRequiredMixin, ProfileRequiredMixin, BookmarkMixin, ListView
):
    model = OpenMic
    template_name = "bookmarks/bookmark_openmic_list.html"
    context_object_name = "openmics"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        openmic_content_type = ContentType.objects.get_for_model(OpenMic)

        # Subquery to fetch the created date of the bookmark
        bookmark_subquery = Bookmark.objects.filter(
            profile=profile,
            content_type=openmic_content_type,
            object_id=OuterRef("pk"),
        ).values("created")[:1]

        # Annotate the Advertisement queryset with the bookmark created date and order by it
        return (
            OpenMic.objects.filter(
                id__in=Bookmark.objects.filter(
                    profile=profile, content_type=openmic_content_type
                ).values("object_id")
            )
            .annotate(bookmark_created=Subquery(bookmark_subquery))
            .order_by("-bookmark_created")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["openmics_count"] = queryset.count()

        # Add bookmark context for the ads (list of objects)
        ads_bookmark_context = self.get_bookmark_context(self.request.user, queryset)
        context.update(ads_bookmark_context)

        return context
