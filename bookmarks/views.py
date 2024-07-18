from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView
from django.contrib import messages
from .models import Bookmark
from profiles.models import Profile


class CreateBookmarkView(LoginRequiredMixin, View):
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
        return redirect(model.get_absolute_url())


class DeleteBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        bookmark_id = kwargs.get("bookmark_id")
        profile = get_object_or_404(Profile, user=request.user)
        bookmark = get_object_or_404(Bookmark, id=bookmark_id, profile=profile)
        bookmark.delete()
        messages.success(request, "Successfully removed bookmark!")
        return redirect("bookmarks:list")


class ListBookmarksView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = "bookmarks/bookmark_list.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Bookmark.objects.filter(profile=profile).select_related("content_type")
