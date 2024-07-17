from urllib.parse import urlparse, parse_qs  # Use urllib.parse for Python 3
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@stringfilter
def youthumbnail(value, args):
    """returns youtube thumb url
    args s, l (small, large)"""
    qs = value.split("?")
    video_id = parse_qs(qs[1])["v"][0]

    if args == "s":
        return "http://img.youtube.com/vi/%s/2.jpg" % video_id
    elif args == "l":
        return "http://img.youtube.com/vi/%s/0.jpg" % video_id
    else:
        return None


register.filter("youthumbnail", youthumbnail)


def youtube_embed(value):
    """Returns the embed URL for a YouTube video."""
    parsed_url = urlparse(value)
    video_id = parse_qs(parsed_url.query).get("v")
    if video_id:
        return f"https://www.youtube.com/embed/{video_id[0]}"
    return value


register.filter("youtube_embed", youtube_embed)
