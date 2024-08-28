from django import template

register = template.Library()


@register.filter
def app_label(value):
    """
    Custom template filter that returns the app label of a given model instance.

    Args:
        value: A model instance whose app label is to be retrieved.

    Returns:
        The app label of the model instance as a string.
    """
    return value._meta.app_label


@register.filter
def model_name(value):
    """
    Custom template filter that returns the model name of a given model instance.

    Args:
        value: A model instance whose model name is to be retrieved.

    Returns:
        The model name of the model instance as a string.
    """
    return value._meta.model_name


@register.filter
def get_item(dictionary, key):
    """
    Custom template filter that retrieves a value from a dictionary using a given key.

    Args:
        dictionary: The dictionary from which to retrieve the value.
        key: The key to look up in the dictionary.

    Returns:
        The value associated with the given key in the dictionary, or None if the key is not found.
    """
    return dictionary.get(key)
