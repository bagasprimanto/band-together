import django_filters
from django.forms import CheckboxSelectMultiple
from .models import Advertisement, AdType
from profiles.models import Genre, Skill
from dal import autocomplete
from cities_light.models import City


def get_ad_type_choices():
    return [(ad_type.id, ad_type.name) for ad_type in AdType.objects.all()]


def get_genre_choices():
    return [(genre.id, genre.name) for genre in Genre.objects.all()]


def get_skill_choices():
    return [(skill.id, skill.name) for skill in Skill.objects.all()]


class AdvertisementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    ad_type = django_filters.MultipleChoiceFilter(
        field_name="ad_type",
        choices=get_ad_type_choices(),
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

    class Meta:
        model = Advertisement
        fields = [
            "title",
            "ad_type",
            "location",
            "genres",
            "skills",
        ]
