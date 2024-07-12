from django.shortcuts import render, get_object_or_404
from .models import Conversation, InboxMessage
from profiles.models import Profile
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import ProfileRequiredMixin
from .forms import SearchProfileForm
from django.http import HttpResponse


class InboxView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Conversation
    template_name = "inbox/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )
        context["form"] = SearchProfileForm()
        return context


class InboxDetailView(LoginRequiredMixin, ProfileRequiredMixin, DetailView):
    model = Conversation
    template_name = "inbox/inbox.html"
    context_object_name = "conversation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )
        context["form"] = SearchProfileForm()
        return context


def search_profiles(request):
    letters = request.GET.get("search_profile")
    if len(letters) > 0:
        profiles = Profile.objects.filter(display_name__startswith=letters).exclude(
            display_name=request.user.profile.display_name
        )

        return render(request, "inbox/searchprofiles_list.html", {"profiles": profiles})
    else:
        return HttpResponse("")
