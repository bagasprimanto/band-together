from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, InboxMessage
from profiles.models import Profile
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import ProfileRequiredMixin
from django.http import HttpResponse
from .forms import InboxCreateMessageForm
from django.utils import timezone


class InboxView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    """
    View for displaying the inbox, which lists the conversations that the logged-in user is a part of.
    Requires the user to be logged in and to have a profile.
    """

    # The model that this view will operate on.
    model = Conversation

    # The template used to render the inbox page.
    template_name = "inbox/inbox.html"

    def get_context_data(self, **kwargs):
        """
        Adds extra context to the template beyond the default context provided by ListView.
        Specifically, it adds the user's conversations to the context.
        """

        context = super().get_context_data(**kwargs)

        # Retrieve the conversations where the current user's profile is a participant.
        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )
        return context


class InboxDetailView(LoginRequiredMixin, ProfileRequiredMixin, DetailView):
    model = Conversation
    template_name = "inbox/inbox.html"
    context_object_name = "conversation"
    pk_url_kwarg = "conversation_pk"

    def get_object(self):
        my_conversations = Conversation.objects.filter(
            participants=self.request.user.profile
        )
        conversation = get_object_or_404(
            my_conversations, id=self.kwargs.get(self.pk_url_kwarg)
        )
        return conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()

        # Mark conversation as seen if it hasn't been seen and the latest message is not from the current user
        latest_message = conversation.messages.first()
        if (
            not conversation.is_seen
            and latest_message.sender != self.request.user.profile
        ):
            conversation.is_seen = True
            conversation.save()

        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )
        return context


class SearchProfilesView(ListView):
    """
    Search profiles view for displaying list of profiles when creating a new message.
    No need to login or profile required since an anonymous user can also access the Profiles List page anyway.
    """

    model = Profile
    template_name = "inbox/searchprofiles_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        letters = self.request.GET.get("search_profile", "")
        if len(letters) > 0:
            return Profile.objects.filter(display_name__icontains=letters).exclude(
                display_name=self.request.user.profile.display_name
            )[:5]
        else:
            return Profile.objects.none()

    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if not context[self.context_object_name].exists():
            return HttpResponse("")
        return super().render_to_response(context, **response_kwargs)


class CreateMessageView(LoginRequiredMixin, ProfileRequiredMixin, View):
    form_class = InboxCreateMessageForm
    template_name = "inbox/createmessage_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.recipient = get_object_or_404(Profile, slug=self.kwargs["profile_slug"])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)
        form = self.form_class()
        context = {
            "recipient": self.recipient,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile

            my_conversations = request.user.profile.conversations.all()
            for c in my_conversations:
                if self.recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.lastmessage_created = timezone.now()
                    c.is_seen = False  # Set the conversation is_seen = false since only the sender will see the message first, not the recipient
                    c.save()
                    return redirect("inbox:inbox_detail", conversation_pk=c.pk)
            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user.profile, self.recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect("inbox:inbox_detail", conversation_pk=new_conversation.pk)

        context = {
            "recipient": self.recipient,
            "form": form,
        }
        return render(request, self.template_name, context)


class CreateReplyView(LoginRequiredMixin, ProfileRequiredMixin, View):
    form_class = InboxCreateMessageForm
    template_name = "inbox/createreply_form.html"

    def get_conversation(self, request):
        # Get all conversations for the logged-in user
        my_conversations = Conversation.objects.filter(
            participants=request.user.profile
        )
        # Get the specific conversation based on conversation_pk
        conversation = get_object_or_404(
            my_conversations, id=self.kwargs["conversation_pk"]
        )
        return conversation

    def get(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)
        conversation = self.get_conversation(request)
        form = self.form_class()
        context = {
            "form": form,
            "conversation": conversation,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        conversation = self.get_conversation(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user.profile
            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.is_seen = False  # Set the conversation is_seen = false since only the sender will see the message first, not the recipient
            conversation.save()
            return redirect("inbox:inbox_detail", conversation_pk=conversation.pk)

        context = {
            "form": form,
            "conversation": self.conversation,
        }
        return render(request, self.template_name, context)


class NotifyNewMessageView(LoginRequiredMixin, ProfileRequiredMixin, View):

    def get(self, request, conversation_pk):
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)
        conversation = get_object_or_404(Conversation, id=conversation_pk)
        latest_message = conversation.messages.first()
        if (
            conversation.is_seen == False
            and latest_message.sender != request.user.profile
        ):
            return render(request, "inbox/notify_icon.html")
        else:
            return HttpResponse("")


class NotifyInboxView(LoginRequiredMixin, ProfileRequiredMixin, View):

    def get(self, request):
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)
        my_conversations = Conversation.objects.filter(
            participants=request.user.profile, is_seen=False
        )
        for c in my_conversations:
            latest_message = c.messages.first()
            if latest_message.sender != request.user.profile:
                return render(request, "inbox/notify_icon.html")
        return HttpResponse("")
