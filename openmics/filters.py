import django_filters
from django.forms import CheckboxSelectMultiple
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

    class Meta:
        model = OpenMic
        fields = [
            "title",
            "location",
            "genres",
        ]
