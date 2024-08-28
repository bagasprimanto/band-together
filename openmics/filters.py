import django_filters
from django.forms import CheckboxSelectMultiple, CheckboxInput
from .models import OpenMic
from profiles.models import Genre
from dal import autocomplete
from cities_light.models import City
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django_filters import DateFromToRangeFilter
from django_filters.widgets import DateRangeWidget
from django_filters import DateFromToRangeFilter
from django_filters.widgets import DateRangeWidget


def get_genre_choices():
    """
    Returns a list of tuples containing the id and name of each Genre for use in filter choices
    """
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


class OpenMicFilter(django_filters.FilterSet):
    """
    Filter class for Open Mic model
    """

    # CharFilter for filtering advertisements by title, using case-insensitive containment matching
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    # A ModelChoiceFilter for filtering by location (City)
    # Uses an autocomplete widget for enhanced user experience
    location = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url="profiles:location_autocomplete"),
    )

    # A DateFromToRangeFilter for filtering events by a date range.
    # The filter widget allows users to select a start and end date.
    event_date = DateFromToRangeFilter(
        field_name="event_date",
        widget=DateRangeWidget(attrs={"type": "date"}),
    )

    # A ModelMultipleChoiceFilter for filtering open mic events by genres.
    # Displayed as checkboxes with a responsive layout.
    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        widget=CheckboxSelectMultiple(attrs={"class": "d-flex flex-wrap row-cols-4"}),
    )

    # A BooleanFilter for filtering events based on whether they have a free entry fee.
    # Uses a custom method (`filter_free_events`) to filter events where the entry fee is zero.
    free = django_filters.BooleanFilter(
        field_name="free",
        label="Free Entry Fee",
        method="filter_free_events",
        widget=CheckboxInput,
    )

    def filter_free_events(self, queryset, name, value):
        """
        Custom method to filter events where the entry fee is free (i.e., entry_fee is 0).
        This method is used by the `free` filter above.
        """

        if value:
            return queryset.filter(entry_fee=0)
        return queryset

    def filter_by_order(self, queryset, name, value):
        """
        Custom method to order the filtered queryset.
        Orders by `event_date` if a value is provided, otherwise orders by `last_updated`.
        """

        expression = "-last_updated" if value == "" else "event_date"
        return queryset.order_by(expression)

    class Meta:
        model = OpenMic
        fields = [
            "title",
            "location",
            "event_date",
            "genres",
            "free",
        ]
