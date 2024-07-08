import django_filters
from django.forms import CheckboxSelectMultiple, CheckboxInput
from django.db.models import Q
from .models import Profile, Genre, Skill, ProfileType


def get_profile_type_choices():
    return [
        (profile_type.id, profile_type.name)
        for profile_type in ProfileType.objects.all()
    ]


def get_profile_type_choices():
    return [(pt.id, pt.name) for pt in ProfileType.objects.all()]


def get_genre_choices():
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


def get_skill_choices():
    return [(skill.id, skill.name) for skill in Skill.objects.all()]


class ProfileFilter(django_filters.FilterSet):
    display_name = django_filters.CharFilter(
        field_name="display_name", lookup_expr="icontains"
    )

    profile_type = django_filters.MultipleChoiceFilter(
        field_name="profile_type",
        choices=get_profile_type_choices(),
        widget=CheckboxSelectMultiple,
    )

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    skills = django_filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    has_youtube_video = django_filters.BooleanFilter(
        field_name="has_youtube_video",
        method="filter_has_youtube_video",
        label="Has YouTube Video",
        widget=CheckboxInput,
    )

    has_profile_picture = django_filters.BooleanFilter(
        field_name="has_profile_picture",
        label="Has Profile Picture",
        method="filter_has_profile_picture",
        widget=CheckboxInput,
    )

    def filter_has_youtube_video(self, queryset, name, value):
        if value:
            return (
                queryset.filter(youtube_link_1__isnull=False)
                | queryset.filter(youtube_link_2__isnull=False)
                | queryset.filter(youtube_link_3__isnull=False)
                | queryset.filter(youtube_link_4__isnull=False)
                | queryset.filter(youtube_link_5__isnull=False)
                | queryset.filter(youtube_link_6__isnull=False)
            ).distinct()
        return queryset

    def filter_has_profile_picture(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(profile_picture__isnull=False) & ~Q(profile_picture="")
            )
        return queryset

    SORT_CHOICES = (
        ("created", "Created Date"),
        ("last_login", "Last Login Date"),
    )

    order_by = django_filters.ChoiceFilter(
        label="Sort by", choices=SORT_CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        expression = "-created" if value == "created" else "-user__last_login"
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
            "order_by",
        ]
