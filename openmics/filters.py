import django_filters
from django.forms import CheckboxSelectMultiple, CheckboxInput
from .models import OpenMic
from profiles.models import Genre
from dal import autocomplete
from cities_light.models import City


def get_genre_choices():
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


class OpenMicFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    location = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url="profiles:location_autocomplete"),
    )

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

    SORT_CHOICES = (("event_date", "Event Date (soonest first)"),)

    order_by = django_filters.ChoiceFilter(
        label="Sort by", choices=SORT_CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        expression = "-last_updated" if value == "" else "event_date"
        return queryset.order_by(expression)

    class Meta:
        model = OpenMic
        fields = [
            "title",
            "location",
            "genres",
            "free",
            "order_by",
        ]
