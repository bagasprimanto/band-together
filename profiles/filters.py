import django_filters
from django.forms import CheckboxSelectMultiple, CheckboxInput
from django.db.models import Q
from django.utils.timezone import now, timedelta
from .models import Profile, Genre, Skill, ProfileType
from dal import autocomplete
from cities_light.models import City


def get_profile_type_choices():
    """
    Function for getting profile type from Profile Type model
    """

    return [
        (profile_type.id, profile_type.name)
        for profile_type in ProfileType.objects.all()
    ]


def get_genre_choices():
    """
    Function for getting genres from Genre model
    """
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


def get_skill_choices():
    """
    Function for getting skills from Skill model
    """
    return [(skill.id, skill.name) for skill in Skill.objects.all()]


class ProfileFilter(django_filters.FilterSet):
    """
    FilterSet for filtering Profile objects based on various criteria.
    """

    display_name = django_filters.CharFilter(
        field_name="display_name", lookup_expr="icontains"
    )

    profile_type = django_filters.MultipleChoiceFilter(
        field_name="profile_type",
        choices=get_profile_type_choices(),
        widget=CheckboxSelectMultiple,
    )

    location = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url="profiles:location_autocomplete"),
    )

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "d-flex flex-wrap row-cols-4"}),
    )

    skills = django_filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "d-flex flex-wrap row-cols-4"}),
    )

    # Boolean filter for checking if the profile has a YouTube video link
    has_youtube_video = django_filters.BooleanFilter(
        field_name="has_youtube_video",
        method="filter_has_youtube_video",
        label="Has YouTube Video",
        widget=CheckboxInput,
    )

    # Boolean filter for checking if the profile has a profile picture
    has_profile_picture = django_filters.BooleanFilter(
        field_name="has_profile_picture",
        label="Has Profile Picture",
        method="filter_has_profile_picture",
        widget=CheckboxInput,
    )

    # Method to filter profiles that have at least one YouTube video link
    def filter_has_youtube_video(self, queryset, name, value):
        if value:

            # Return distinct profiles that match the filter criteria
            return (
                queryset.filter(youtube_link_1__isnull=False)
                | queryset.filter(youtube_link_2__isnull=False)
                | queryset.filter(youtube_link_3__isnull=False)
                | queryset.filter(youtube_link_4__isnull=False)
                | queryset.filter(youtube_link_5__isnull=False)
                | queryset.filter(youtube_link_6__isnull=False)
            ).distinct()

        # If not filtering, return the original queryset
        return queryset

    # Method to filter profiles that have a non-empty profile picture
    def filter_has_profile_picture(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(profile_picture__isnull=False) & ~Q(profile_picture="")
            )
        return queryset

    # Choices for the last login date range filter
    LAST_LOGIN_CHOICES = (
        (1, "Last 1 week"),
        (2, "Last 2 weeks"),
        (3, "Last 3 weeks"),
        (4, "Last 4 weeks"),
        (5, "Last 5 weeks"),
        (6, "Last 6 weeks"),
    )

    last_login_range = django_filters.ChoiceFilter(
        label="Last Logged in Within...",
        choices=LAST_LOGIN_CHOICES,
        method="filter_by_last_login_range",
    )

    # Filter for selecting profiles based on last login within a specific time range
    def filter_by_last_login_range(self, queryset, name, value):
        value = int(value)
        cutoff_date = now() - timedelta(weeks=value)
        return queryset.filter(user__last_login__gte=cutoff_date)

    SORT_CHOICES = (
        ("last_updated", "Last Profile Updated Date"),
        ("last_login", "Last Login Date"),
    )

    # Filter for sorting profiles by a selected field
    order_by = django_filters.ChoiceFilter(
        label="Sort by", choices=SORT_CHOICES, method="filter_by_order"
    )

    # Method to sort profiles based on the selected order criterion
    def filter_by_order(self, queryset, name, value):
        expression = "-last_updated" if value == "last_updated" else "-user__last_login"
        return queryset.order_by(expression)

    class Meta:
        model = Profile
        fields = [
            "display_name",
            "profile_type",
            "location",
            "genres",
            "skills",
            "has_youtube_video",
            "has_profile_picture",
            "last_login_range",
            "order_by",
        ]
