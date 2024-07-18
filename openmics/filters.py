import django_filters
from django.forms import CheckboxSelectMultiple, CheckboxInput
from .models import OpenMic
from profiles.models import Genre


def get_genre_choices():
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


class OpenMicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "d-flex flex-wrap row-cols-4"}),
    )

    free = django_filters.BooleanFilter(
        field_name="free",
        label="Free Entry Fee",
        method="filter_free_events",
        widget=CheckboxInput,
    )

    def filter_free_events(self, queryset, name, value):
        if value:
            return queryset.filter(entry_fee=0)
        return queryset

    class Meta:
        model = OpenMic
        fields = [
            "title",
            "location",
            "genres",
            "free",
        ]
