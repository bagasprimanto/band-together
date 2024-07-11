from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
)
from .models import Advertisement, Comment
from .forms import AdvertisementCreateForm, AdvertisementEditForm, CommentCreateForm
from .filters import AdvertisementFilter
from profiles.mixins import ProfileRequiredMixin
from django.http import HttpResponseRedirect


class AdvertisementListView(ListView):
    model = Advertisement
    context_object_name = "ads"
    template_name = "advertisements/advertisement_list.html"


def advertisement_list(request):
    f = AdvertisementFilter(request.GET, queryset=Advertisement.objects.all())
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        advertisements = Advertisement.objects.all().order_by("-last_updated")
    else:
        advertisements = f.qs

    context = {
        "form": f.form,
        "ads": advertisements,
        "has_filter": has_filter,
    }
    return render(request, "advertisements/advertisement_list.html", context)


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
        context["form"] = CommentCreateForm()
        context["comments"] = Comment.objects.filter(
            parent_advertisement=advertisement
        ).order_by("-created")
        return context


class CommentFormView(LoginRequiredMixin, ProfileRequiredMixin, FormView):
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

    def form_invalid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        comments = (
            advertisement.comment_set.all()
        )  # Assuming a reverse relation named `comment_set`
        context = {"ad": advertisement, "form": form, "comments": comments}
        return render(self.request, "post_detail.html", context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        context["ad"] = advertisement
        context["comments"] = Comment.objects.filter(
            parent_advertisement=advertisement
        ).order_by("-created")
        return context


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
