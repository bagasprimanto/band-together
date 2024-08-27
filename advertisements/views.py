from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Advertisement, Comment
from .forms import AdvertisementCreateForm, AdvertisementEditForm, CommentCreateForm
from inbox.forms import InboxCreateMessageForm
from .filters import AdvertisementFilter
from profiles.mixins import ProfileRequiredMixin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import Http404
from django.conf import settings
from bookmarks.mixins import BookmarkMixin, BookmarkSingleObjectMixin
from reports.forms import ReportForm


def advertisement_list(request):
    """
    Gets the first page of the list of advertisements
    """

    # Part of Django filters,
    # initialize the advertisement filter with the GET parameters and the queryset of all advertisements,
    # ordered by the last updated date (descending).
    f = AdvertisementFilter(
        request.GET, queryset=Advertisement.objects.all().order_by("-last_updated")
    )

    # Check if any filter fields are present in the GET parameters.
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    # If no filters are applied, retrieve all advertisements ordered by the last updated date.
    if not has_filter:
        advertisements = Advertisement.objects.all().order_by("-last_updated")
    else:
        # If filters are applied, get the filtered queryset.
        advertisements = f.qs

    # Paginate the advertisements with the number of items per page defined in settings.PAGE_SIZE.
    # This defaults to the first page when this view is triggered.
    paginator = Paginator(advertisements, settings.PAGE_SIZE)
    advertisements_page = paginator.page(1)  # default to 1 when this view is triggered

    context = {
        "form": f.form,  # The form object associated with the filter.
        "ads": advertisements_page,
        "ads_count": advertisements.count,  # The total count of advertisements.
        "has_filter": has_filter,
    }

    # Add bookmark context to the context dictionary.
    bookmark_context = BookmarkMixin().get_bookmark_context(
        request.user, advertisements
    )
    context.update(bookmark_context)  # Update the context with bookmark information.

    # Render the advertisement list template with the provided context.
    return render(request, "advertisements/advertisement_list.html", context)


def get_advertisements(request):
    """
    Handles HTMX requests to get advertisements for pages beyond the first page.
    """

    # Check if the request is an HTMX request. If not, raise a 404 error.
    if not request.headers.get("HX-Request"):
        raise Http404()

    # Get the page number from the GET parameters. If not provided, default to page 1.
    page = request.GET.get(
        "page", 1  # ?page=2 will extract 2; defaults to 1 if not present.
    )

    # Initialize the advertisement filter with the GET parameters and the queryset of all advertisements,
    # ordered by the last updated date (descending).
    f = AdvertisementFilter(
        request.GET, queryset=Advertisement.objects.all().order_by("-last_updated")
    )

    # Check if any filter fields are present in the GET parameters.
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    # If no filters are applied, retrieve all advertisements ordered by the last updated date.
    # If filters are applied, get the filtered queryset.
    if not has_filter:
        advertisements = Advertisement.objects.all().order_by("-last_updated")
    else:
        advertisements = f.qs

    # Paginate the advertisements with the number of items per page defined in settings.PAGE_SIZE.
    paginator = Paginator(advertisements, settings.PAGE_SIZE)
    context = {"ads": paginator.page(page)}

    # Add bookmark context to the context dictionary.
    # Gets bookmarks for advertisements pertaining to the current user.
    bookmark_context = BookmarkMixin().get_bookmark_context(
        request.user, advertisements
    )
    context.update(bookmark_context)

    return render(
        request,
        "advertisements/advertisement_list_partial.html#advertisements_list",
        context,
    )


class AdvertisementCreateView(
    LoginRequiredMixin, ProfileRequiredMixin, SuccessMessageMixin, CreateView
):
    """
    View for creating new Advertisements
    """

    # The model that this view will operate on.
    model = Advertisement

    # The form class that will be used to create a new advertisement.
    form_class = AdvertisementCreateForm

    # The success message to display when an advertisement is successfully created.
    success_message = "Successfully created ad!"

    # The template used to render the form.
    template_name = "advertisements/advertisement_form.html"

    def form_valid(self, form):
        # This method is called when the submitted form is valid.
        # Set the author of the advertisement to the current user's profile.
        form.instance.author = self.request.user.profile

        # Call the superclass's form_valid method to save the form and handle the redirection.
        return super().form_valid(form)

    def get_success_url(self):
        # This method returns the URL to redirect to after the advertisement is successfully created.
        # The URL will point to the detail view of the newly created advertisement.
        return reverse(
            "advertisements:advertisement_detail", kwargs={"pk": self.object.pk}
        )


class AdvertisementDetailView(BookmarkSingleObjectMixin, DetailView):
    model = Advertisement
    template_name = "advertisements/advertisement_detail.html"
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        context["comment_form"] = CommentCreateForm()
        context["createmessage_form"] = InboxCreateMessageForm()
        context["comments"] = Comment.objects.filter(
            parent_advertisement=advertisement
        ).order_by("-created")

        # Get bookmark context for Advertisement
        bookmark_context = self.get_single_bookmark_context(
            self.request.user, self.get_object()
        )
        context.update(bookmark_context)

        # Pass context for report button
        advertisement = self.get_object()
        context["report_form"] = ReportForm()
        context["app_label"] = advertisement._meta.app_label
        context["model_name"] = advertisement._meta.model_name

        return context


class CommentCreateView(LoginRequiredMixin, ProfileRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "advertisements/advertisement_detail.html"

    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        comment = form.save(commit=False)
        comment.author = (
            self.request.user.profile
        )  # Assuming the user has a profile attribute
        comment.parent_advertisement = advertisement
        comment.save()
        return HttpResponseRedirect(
            reverse(
                "advertisements:advertisement_detail", kwargs={"pk": advertisement.pk}
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        context["ad"] = advertisement
        context["comments"] = Comment.objects.filter(
            parent_advertisement=advertisement
        ).order_by("-created")
        context["comment_form"] = self.form_class
        return context

    def form_invalid(self, form):
        # Get the context data for rendering the form with errors
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        ad_pk = (
            self.object.parent_advertisement.pk
        )  # Assuming `ad` is the related name for the advertisement
        return reverse("advertisements:advertisement_detail", kwargs={"pk": ad_pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user.profile == comment.author


class AdvertisementEditView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):

    model = Advertisement
    success_message = "Successfully edited ad!"
    form_class = AdvertisementEditForm
    template_name = "advertisements/advertisement_edit.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user.profile == advertisement.author


class AdvertisementDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Advertisement
    success_message = "Successfully deleted ad!"
    context_object_name = "ad"
    success_url = reverse_lazy("advertisements:advertisement_list")

    def test_func(self):
        advertisement = self.get_object()
        return self.request.user.profile == advertisement.author
