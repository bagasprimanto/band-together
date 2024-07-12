from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, InboxMessage
from profiles.models import Profile
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import ProfileRequiredMixin
from django.http import HttpResponse, Http404
from .forms import InboxCreateMessageForm
from django.utils import timezone


class InboxView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Conversation
    template_name = "inbox/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )
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
        return context


def search_profiles(request):
    letters = request.GET.get("search_profile")
    if request.headers.get("HX-Request"):
        if len(letters) > 0:
            profiles = Profile.objects.filter(display_name__icontains=letters).exclude(
                display_name=request.user.profile.display_name
            )[:5]

            return render(
                request, "inbox/searchprofiles_list.html", {"profiles": profiles}
            )
        else:
            return HttpResponse("")
    else:
        raise Http404()


def create_message(request, slug):
    recipient = get_object_or_404(Profile, slug=slug)
    create_message_form = InboxCreateMessageForm()

    if request.method == "POST":
        form = InboxCreateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile

            my_conversations = request.user.profile.conversations.all()
            for c in my_conversations:
                if recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.lastmessage_created = timezone.now()
                    c.save()
                    return redirect("inbox:inbox_detail", pk=c.pk)
            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user.profile, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect("inbox:inbox_detail", pk=c.pk)

    context = {
        "recipient": recipient,
        "form": create_message_form,
    }
    return render(request, "inbox/createmessage_form.html", context)
