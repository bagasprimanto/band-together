import re


def extract_lat_lng_from_url(url):
    # Define the regular expression pattern to match latitude and longitude in the URL
    pattern = r"@(-?\d+\.\d+),(-?\d+\.\d+)"
    match = re.search(pattern, url)

    if match:
        lat, lng = match.groups()
        return float(lat), float(lng)
    return None, None
