# timezone_choices.py
import zoneinfo

# Generate the fixed list of timezone choices
TIMEZONES_CHOICES = [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]
