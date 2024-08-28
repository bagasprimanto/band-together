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
    """
    View for displaying the details of a specific conversation in the inbox.
    Requires the user to be logged in and to have a profile.
    """

    # The model that this view will operate on.
    model = Conversation

    # The template used to render the conversation detail page.
    template_name = "inbox/inbox.html"

    # The name of the context variable that will contain the conversation object in the template.
    context_object_name = "conversation"

    # The name of the URL keyword argument that will be used to retrieve the conversation by its primary key.
    pk_url_kwarg = "conversation_pk"

    def get_object(self):
        """
        Retrieves the specific conversation object that the current user is a part of.
        Ensures that the user only accesses conversations they are a participant in.
        """
        # Filter conversations to include only those where the current user's profile is a participant.
        my_conversations = Conversation.objects.filter(
            participants=self.request.user.profile
        )

        # Retrieve the specific conversation based on the primary key from the URL, ensuring the user is a participant.
        conversation = get_object_or_404(
            my_conversations, id=self.kwargs.get(self.pk_url_kwarg)
        )

        # Return the conversation object.
        return conversation

    def get_context_data(self, **kwargs):
        """
        Adds extra context to the template beyond the default context provided by DetailView.
        Marks the conversation as seen if the latest message is from another participant and hasn't been seen.
        """
        # Initialize the base context provided by the superclass.
        context = super().get_context_data(**kwargs)

        # Retrieve the conversation object for the current view.
        conversation = self.get_object()

        # Get the latest message in the conversation.
        latest_message = conversation.messages.first()

        # Mark conversation as seen if it hasn't been seen and the latest message is not from the current user
        if (
            not conversation.is_seen
            and latest_message.sender != self.request.user.profile
        ):
            conversation.is_seen = True
            conversation.save()

        # Add the user's conversations to the context.
        context["my_conversations"] = Conversation.objects.filter(
            participants=self.request.user.profile
        )

        # Return the updated context to be used in the template.
        return context


class SearchProfilesView(ListView):
    """
    Search profiles view for displaying list of profiles when creating a new message.
    No need to login or profile required since an anonymous user can also access the Profiles List page anyway.
    """

    # The model that this view will operate on.
    model = Profile

    # The template used to render the list of profiles.
    template_name = "inbox/searchprofiles_list.html"

    # The name of the context variable that will contain the list of profiles in the template.
    context_object_name = "profiles"

    def get_queryset(self):
        """
        Overrides the default queryset to filter profiles based on the search term provided by the user.
        Excludes the profile of the current user from the search results.
        """
        # Get the search term from the GET parameters.
        letters = self.request.GET.get("search_profile", "")

        # If the search term is provided, filter profiles by display name, excluding the current user's profile.
        if len(letters) > 0:
            return Profile.objects.filter(display_name__icontains=letters).exclude(
                display_name=self.request.user.profile.display_name
            )[
                :5
            ]  # Limit results to the first 5 profiles.

        # If no search term is provided, return an empty queryset.
        else:
            return Profile.objects.none()

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides the dispatch method to ensure that the view only accepts HTMX requests.
        If the request is not an HTMX request, return a 400 Bad Request response.
        """
        # Check if the request is an HTMX request by looking for the "HX-Request" header.
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # If it's an HTMX request, proceed with the normal dispatch process.
        return super().dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Overrides the response rendering to handle cases where no profiles are found.
        If no profiles match the search criteria, return an empty response.
        """
        # If the context does not contain any profiles, return an empty HTTP response.
        if not context[self.context_object_name].exists():
            return HttpResponse("")
        # Otherwise, proceed with the normal rendering process.
        return super().render_to_response(context, **response_kwargs)


class CreateMessageView(LoginRequiredMixin, ProfileRequiredMixin, View):
    """
    View to handle the creation of a new message to a specific recipient.
    Requires the user to be logged in and to have a profile.
    """

    # The form class used to create a new message.
    form_class = InboxCreateMessageForm

    # The template used to render the message creation form.
    template_name = "inbox/createmessage_form.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides the dispatch method to retrieve the recipient's profile based on the slug in the URL.
        Ensures that the recipient exists before processing the request.
        """

        # Retrieve the recipient's profile using the slug from the URL.
        self.recipient = get_object_or_404(Profile, slug=self.kwargs["profile_slug"])

        # Continue with the normal dispatch process.
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to display the message creation form.
        Ensures that the view only accepts HTMX requests.
        """

        # Check if the request is an HTMX request by looking for the "HX-Request" header.
        if not request.headers.get("HX-Request"):
            return HttpResponse("This endpoint only accepts HTMX requests.", status=400)

        # Initialize an empty form.
        form = self.form_class()

        # Prepare the context with the recipient's profile and the form.
        context = {
            "recipient": self.recipient,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to process the form submission and create a new message.
        """

        # Populate the form with the POST data.
        form = self.form_class(request.POST)

        # Check if the form is valid.
        if form.is_valid():
            # Create a message instance without saving it to the database yet.
            message = form.save(commit=False)
            # Assign the sender of the message to the current user's profile.
            message.sender = request.user.profile

            # Retrieve all conversations involving the current user.
            my_conversations = request.user.profile.conversations.all()

            # Check if there is an existing conversation with the recipient.
            for c in my_conversations:
                if self.recipient in c.participants.all():
                    # If a conversation exists, assign the message to this conversation.
                    message.conversation = c
                    message.save()

                    # Update the conversation's metadata.
                    c.lastmessage_created = timezone.now()
                    c.is_seen = False  # Set the conversation is_seen = false since only the sender will see the message first, not the recipient
                    c.save()

                    # Redirect to the conversation detail page.
                    return redirect("inbox:inbox_detail", conversation_pk=c.pk)

            # If no conversation exists, create a new one.
            new_conversation = Conversation.objects.create()

            # Add both the current user and the recipient to the conversation.
            new_conversation.participants.add(request.user.profile, self.recipient)
            new_conversation.save()

            # Assign the message to the new conversation.
            message.conversation = new_conversation
            message.save()

            # Redirect to the new conversation's detail page.
            return redirect("inbox:inbox_detail", conversation_pk=new_conversation.pk)

        # If the form is invalid, prepare the context and re-render the form with errors.
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
