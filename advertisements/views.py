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
from django_project import settings


def advertisement_list(request):
    f = AdvertisementFilter(
        request.GET, queryset=Advertisement.objects.all().order_by("-last_updated")
    )
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        advertisements = Advertisement.objects.all().order_by("-last_updated")
    else:
        advertisements = f.qs

    paginator = Paginator(advertisements, settings.PAGE_SIZE)
    advertisements_page = paginator.page(1)  # default to 1 when this view is triggered

    context = {
        "form": f.form,
        "ads": advertisements_page,
        "has_filter": has_filter,
    }
    return render(request, "advertisements/advertisement_list.html", context)


def get_advertisements(request):
    import time

    time.sleep(2)

    if not request.headers.get("HX-Request"):
        raise Http404()

    page = request.GET.get(
        "page", 1
    )  # ?page=2, then this will extract 2. If it doesn't, then default to 1

    f = AdvertisementFilter(
        request.GET, queryset=Advertisement.objects.all().order_by("-last_updated")
    )
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        advertisements = Advertisement.objects.all().order_by("-last_updated")
    else:
        advertisements = f.qs

    paginator = Paginator(advertisements, settings.PAGE_SIZE)
    context = {"ads": paginator.page(page)}

    return render(
        request,
        "advertisements/advertisement_list_partial.html#advertisements_list",
        context,
    )


class AdvertisementCreateView(
    LoginRequiredMixin, ProfileRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Advertisement
    form_class = AdvertisementCreateForm
    success_message = "Successfully created ad!"
    template_name = "advertisements/advertisement_form.html"

    def form_valid(self, form):
        # sets the author instance of the Profile to the user creating the profile
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        # Returns the URL to redirect to after the form is successfully submitted
        return reverse(
            "advertisements:advertisement_detail", kwargs={"pk": self.object.pk}
        )


class AdvertisementDetailView(DetailView):
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
        return (
            self.request.user.profile == comment.author
            or self.request.user.is_superuser
        )


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
