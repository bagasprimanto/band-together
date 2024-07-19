from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import ProfileRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView
from django.contrib import messages
from .models import Bookmark
from profiles.models import Profile
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.messages import get_messages


class CreateBookmarkView(LoginRequiredMixin, ProfileRequiredMixin, View):
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
                "bookmarks/bookmark_button.html", context, request=request
            )

            return HttpResponse(html)

        return redirect(model.get_absolute_url())


class DeleteBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        bookmark_id = kwargs.get("bookmark_id")
        profile = get_object_or_404(Profile, user=request.user)
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
                "bookmarks/bookmark_button.html", context, request=request
            )

            return HttpResponse(html)

        return redirect(model.get_absolute_url())


class ListBookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = "bookmarks/bookmark_list.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Bookmark.objects.filter(profile=profile).select_related("content_type")
